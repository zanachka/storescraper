import traceback
from collections import OrderedDict

from celery import shared_task
from celery.utils.log import get_task_logger


from .utils import (
    get_store_class_by_name,
    session_with_proxy,
)

logger = get_task_logger(__name__)


class StoreScrapError(Exception):
    def __init__(self, message):
        super(StoreScrapError, self).__init__(message)


class Store:
    preferred_discover_urls_concurrency = 3
    preferred_products_for_url_concurrency = 10
    prefer_async = True

    ##########################################################################
    # API methods
    ##########################################################################

    @classmethod
    def products_for_keyword(
        cls,
        keyword,
        threshold,
        extra_args=None,
        products_for_url_concurrency=None,
        use_async=None,
    ):

        sanitized_parameters = cls.sanitize_parameters(
            products_for_url_concurrency=products_for_url_concurrency,
            use_async=use_async,
        )

        products_for_url_concurrency = sanitized_parameters[
            "products_for_url_concurrency"
        ]
        use_async = sanitized_parameters["use_async"]

        extra_args = cls._extra_args_with_preflight(extra_args)

        product_urls = cls.discover_urls_for_keyword(keyword, threshold, extra_args)

        product_entries = OrderedDict()

        for url in product_urls:
            product_entries[url] = {
                "positions": [],
                "category": None,
            }

        if extra_args is None:
            extra_args = {}

        extra_args["source"] = "keyword_search"

        return cls.products_for_urls(
            product_entries,
            extra_args=extra_args,
            products_for_url_concurrency=products_for_url_concurrency,
            use_async=use_async,
        )

    @classmethod
    def discover_urls_for_category_with_preflight(cls, category, extra_args=None):
        extra_args = cls._extra_args_with_preflight(extra_args)
        return cls.discover_urls_for_category(category, extra_args=extra_args)

    @classmethod
    def products_for_url_with_preflight(cls, url, category=None, extra_args=None):
        extra_args = cls._extra_args_with_preflight(extra_args)
        return cls.products_for_url(url, category=category, extra_args=extra_args)

    ##########################################################################
    # Celery tasks wrappers
    ##########################################################################

    @staticmethod
    @shared_task(autoretry_for=(StoreScrapError,), max_retries=5, default_retry_delay=5)
    def products_for_url_task(store_class_name, url, category=None, extra_args=None):
        store = get_store_class_by_name(store_class_name)
        logger.info("Obtaining products for URL")
        logger.info("Store: " + store.__name__)
        logger.info("Category: {}".format(category))
        logger.info("URL: " + url)

        try:
            raw_products = store.products_for_url(url, category, extra_args)
        except Exception:
            error_message = "Error retrieving products from {}: {} - {}" "".format(
                store_class_name, url, traceback.format_exc()
            )
            logger.error(error_message)
            raise StoreScrapError(error_message)

        serialized_products = [p.serialize() for p in raw_products]

        for idx, product in enumerate(serialized_products):
            logger.info("{} - {}".format(idx, product))

        return serialized_products

    @staticmethod
    @shared_task(autoretry_for=(StoreScrapError,), max_retries=5, default_retry_delay=5)
    def discover_urls_for_category_task(store_class_name, category, extra_args=None):
        store = get_store_class_by_name(store_class_name)
        logger.info("Discovering URLs")
        logger.info("Store: " + store.__name__)
        logger.info("Category: " + category)
        discovered_urls = []
        try:
            for url in store.discover_urls_for_category(category, extra_args):
                if url not in discovered_urls:
                    logger.info(url)
                    discovered_urls.append(url)
        except Exception:
            error_message = "Error discovering URLs from {}: {} - {}".format(
                store_class_name, category, traceback.format_exc()
            )
            logger.error(error_message)
            raise StoreScrapError(error_message)

        return discovered_urls

    ##########################################################################
    # Implementation dependant methods
    ##########################################################################

    @classmethod
    def categories(cls):
        raise NotImplementedError(
            "This method must be implemented by subclasses of Store"
        )

    @classmethod
    def discover_urls_for_category(cls, category, extra_args=None):
        raise NotImplementedError(
            "This method must be implemented by subclasses of Store"
        )

    @classmethod
    def products_for_url(cls, url, category=None, extra_args=None):
        raise NotImplementedError(
            "This method must be implemented by subclasses of Store"
        )

    @classmethod
    def discover_urls_for_keyword(cls, keyword, threshold, extra_args=None):
        raise NotImplementedError(
            "This method must be implemented by subclasses of Store"
        )

    @classmethod
    def preflight(cls, extra_args=None):
        # Executes any logic that needs to be done only once per scraping
        # (e.g. obtaining session cookies). Should return a dictionary that
        # is merged with the "extra_args" available in the "discover" methods
        # above or products_for_url.
        return {}

    @classmethod
    def get_session(cls, extra_args=None):
        # Returns the requests session that should be used for the HTTP requests
        # made by the scraper. This is useful for tools outside storescraper that
        # may want to fetch the raw HTTP response for some product or category path
        return session_with_proxy(extra_args)

    ##########################################################################
    # Utility methods
    ##########################################################################

    @classmethod
    def sanitize_parameters(
        cls,
        categories=None,
        discover_urls_concurrency=None,
        products_for_url_concurrency=None,
        use_async=None,
    ):
        if categories is None:
            categories = cls.categories()
        else:
            categories = [
                category for category in cls.categories() if category in categories
            ]

        if discover_urls_concurrency is None:
            discover_urls_concurrency = cls.preferred_discover_urls_concurrency

        if products_for_url_concurrency is None:
            products_for_url_concurrency = cls.preferred_products_for_url_concurrency

        if use_async is None:
            use_async = cls.prefer_async

        return {
            "categories": categories,
            "discover_urls_concurrency": discover_urls_concurrency,
            "products_for_url_concurrency": products_for_url_concurrency,
            "use_async": use_async,
        }

    ######################################################################
    # Private methods
    ######################################################################

    @classmethod
    def _extra_args_with_preflight(cls, extra_args=None):
        # Merges the extra_args with the preflight args and prevents
        # preflight from being called twice unnecesarily

        # If the preflight args have already been calculated, return
        if extra_args is not None and "preflight_done" in extra_args:
            return extra_args

        preflight_args = {"preflight_done": True}
        preflight_args.update(cls.preflight(extra_args))
        if extra_args is not None:
            preflight_args.update(extra_args)

        return preflight_args
