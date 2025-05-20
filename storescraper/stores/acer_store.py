import json

from bs4 import BeautifulSoup
from decimal import Decimal
from storescraper.categories import (
    MONITOR,
    NOTEBOOK,
    MOUSE,
    HEADPHONES,
    TABLET,
)

from storescraper.product import Product
from storescraper.store_with_url_extensions import StoreWithUrlExtensions
from storescraper.utils import (
    html_to_markdown,
    cf_session_with_proxy,
)


class AcerStore(StoreWithUrlExtensions):
    url_extensions = [
        ["monitores", MONITOR],
        ["outlet-seminuevos", NOTEBOOK],
        ["mouse", MOUSE],
        ["headset", HEADPHONES],
        ["notebook", NOTEBOOK],
        ["tablets", TABLET],
    ]

    @classmethod
    def get_session(cls, extra_args=None):
        return cf_session_with_proxy(extra_args)

    @classmethod
    def discover_urls_for_url_extension(cls, url_extension, extra_args=None):
        session = cls.get_session(extra_args)
        page = 1

        while True:
            url = f"https://www.acerstore.cl/collections/{url_extension}?page={page}"
            print(url)

            response = session.get(url)
            soup = BeautifulSoup(response.text, "lxml")
            products = soup.findAll("div", "product-card-wrapper")

            if not products:
                if page == 1:
                    raise Exception(f"Empty category: {url_extension}")
                break

            for product in products:
                product_url = f"https://www.acerstore.cl{product.find("a")["href"]}"
                yield product_url

            page += 1

    @classmethod
    def products_for_url(cls, url, category=None, extra_args=None):
        print(url)

        session = cls.get_session(extra_args)
        response = session.get(url)
        soup = BeautifulSoup(response.text, "lxml")
        product_data = json.loads(
            soup.findAll("script", {"type": "application/ld+json"})[1].text
        )

        name = product_data["name"]
        sku = product_data["sku"]
        part_number = product_data["category"]
        description = html_to_markdown(soup.find("p", "product__text").text)
        description_lower = description.lower()
        name_lower = name.lower()

        if (
            "outlet" in description_lower
            or "outlet" in name_lower
            or "seminuevo" in description_lower
            or "seminuevo" in name_lower
        ):
            if "openbox" in description_lower or "open box" in description_lower:
                condition = "https://schema.org/OpenBoxCondition"
            else:
                condition = "https://schema.org/RefurbishedCondition"
        else:
            condition = "https://schema.org/NewCondition"

        offer = product_data["offers"]
        price = Decimal(offer["price"])
        key = offer["url"].split("?variant=")[1]
        stock = -1 if offer["availability"] == "http://schema.org/InStock" else 0
        pictures_container = soup.find("div", "carousel-main")
        picture_urls = list(
            set(
                f"https:{img['data-lazy'].split('?')[0]}"
                for img in pictures_container.findAll("img")
            )
        )

        p = Product(
            name,
            cls.__name__,
            category,
            url,
            url,
            key,
            stock,
            price,
            price,
            "CLP",
            sku=sku,
            part_number=part_number,
            description=description,
            picture_urls=picture_urls,
            condition=condition,
        )

        yield p

    # Implemented only for testing purposes, please delete afterwards
    @classmethod
    def sections(cls):
        return [x[0] for x in cls.url_extensions]

    @classmethod
    def section_positions(cls, section_name, extra_args=None):
        for idx, discovery_url in enumerate(
            cls.discover_urls_for_url_extension(section_name, extra_args=extra_args)
        ):
            yield {
                "field": "discovery_url",
                "value": discovery_url,
                "position": idx + 1,
                "section": section_name,
            }
