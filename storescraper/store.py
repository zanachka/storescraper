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
    def discover_urls_for_category_with_custom_exception(
        cls, category, extra_args=None
    ):
        try:
            yield from cls.discover_urls_for_category(category, extra_args=extra_args)
        except Exception as e:
            raise StoreScrapError(f"Error discovering URLs for {category} : {e}") from e

    @classmethod
    def products_for_url_with_custom_exception(
        cls, url, category=None, extra_args=None
    ):
        try:
            yield from cls.products_for_url(
                url, category=category, extra_args=extra_args
            )
        except Exception as e:
            raise StoreScrapError("Error retrieving products") from e

    @classmethod
    def section_positions_with_custom_exception(cls, section, extra_args=None):
        try:
            yield from cls.section_positions(section, extra_args=extra_args)
        except Exception as e:
            raise StoreScrapError("Error obtaining section positions") from e

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
        raw_products = store.products_for_url_with_custom_exception(
            url, category, extra_args
        )
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
        for url in store.discover_urls_for_category_with_custom_exception(
            category, extra_args
        ):
            if url not in discovered_urls:
                logger.info(url)
                discovered_urls.append(url)

        return discovered_urls

    @staticmethod
    @shared_task(autoretry_for=(StoreScrapError,), max_retries=5, default_retry_delay=5)
    def section_positions_task(store_class_name, section, extra_args=None):
        store = get_store_class_by_name(store_class_name)
        logger.info("Obtaining section positions")
        logger.info("Store: " + store.__name__)
        logger.info("Section: " + section)
        section_positions = []
        for url in store.section_positions_with_custom_exception(section, extra_args):
            logger.info(url)
            section_positions.append(url)

        return section_positions

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
    def sections(cls):
        raise NotImplementedError(
            "This method must be implemented by subclasses of Store that implement section positioning"
        )

    @classmethod
    def section_positions(cls, section, extra_args=None):
        raise NotImplementedError(
            "This method must be implemented by subclasses of Store that implement section positioning"
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
    def extra_args_with_preflight(cls, extra_args=None):
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
