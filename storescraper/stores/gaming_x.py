from decimal import Decimal
import logging
from bs4 import BeautifulSoup
from storescraper.categories import NOTEBOOK
from storescraper.stores.mercado_libre_chile import MercadoLibreChile
from storescraper.utils import session_with_proxy


class GamingX(MercadoLibreChile):
    seller_whitelist = None

    @classmethod
    def categories(cls):
        return [NOTEBOOK]

    @classmethod
    def discover_urls_for_category(cls, category, extra_args=None):
        url_extensions = [
            ["computacion", NOTEBOOK],
        ]

        session = session_with_proxy(extra_args)
        product_urls = []
        for url_extension, local_category in url_extensions:
            if local_category != category:
                continue

            page = 1

            while True:
                if page > 10:
                    raise Exception(f"Page overflow: {url_extension}")

                index = str(50 * (page - 1) + 1)
                url_webpage = f"https://www.gamingx.cl/listado/{url_extension}/_Desde_{index}_NoIndex_True"
                data = session.get(url_webpage).text
                soup = BeautifulSoup(data, "lxml")
                product_containers = soup.findAll("li", "ui-search-layout__item")

                if not product_containers:
                    if page == 1:
                        logging.warning(f"Empty category: {url_extension}")
                    break

                for container in product_containers:
                    product_url = container.find("a", "poly-component__title")["href"]
                    product_urls.append(product_url)
                page += 1

        return product_urls

    @classmethod
    def products_for_url(cls, url, category=None, extra_args=None):
        return cls._products_for_url_with_custom_price(
            url, category=category, extra_args=extra_args
        )
