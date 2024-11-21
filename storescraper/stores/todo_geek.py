from decimal import Decimal
import json
import logging
import re
from bs4 import BeautifulSoup
from storescraper.categories import (
    VIDEO_CARD,
    VIDEO_GAME_CONSOLE,
    CELL,
)
from storescraper.product import Product
from storescraper.store_with_url_extensions import StoreWithUrlExtensions
from storescraper.utils import html_to_markdown, remove_words, session_with_proxy


class TodoGeek(StoreWithUrlExtensions):
    url_extensions = [
        ["celulares", CELL],
        ["tarjetas-graficas", VIDEO_CARD],
        ["consolas", VIDEO_GAME_CONSOLE],
    ]

    @classmethod
    def discover_urls_for_url_extension(cls, url_extension, extra_args):
        session = session_with_proxy(extra_args)
        product_urls = []
        page = 1
        while True:
            if page > 10:
                raise Exception("Page overflow: " + url_extension)

            url_webpage = (
                f"https://todogeek.cl/collections/{url_extension}/page/{page}/"
            )
            print(url_webpage)

            res = session.get(url_webpage)
            soup = BeautifulSoup(res.text, "lxml")
            product_containers = soup.findAll("div", "product-content")

            if not product_containers:
                if page == 1:
                    logging.warning(f"Empty category: {url_extension}")
                break

            for container in product_containers:
                product_urls.append(container.find("a")["href"])
            page += 1
        return product_urls

    @classmethod
    def products_for_url(cls, url, category=None, extra_args=None):
        print(url)
        session = session_with_proxy(extra_args)
        response = session.get(url)
        soup = BeautifulSoup(response.text, "lxml")
        page_data = json.loads(
            soup.findAll("script", {"type": "application/ld+json"})[1].text
        )["@graph"]
        product_data = None

        for entry in page_data:
            if entry["@type"] == "Product":
                product_data = entry

        assert len(product_data["offers"]) == 1

        name = product_data["name"]
        sku = str(product_data["sku"])
        offer = product_data["offers"][0]
        stock = -1 if offer["availability"] == "http://schema.org/InStock" else 0

        offer_price = Decimal(
            remove_words(soup.find("p", "price-transferencia").find("bdi").text)
        )
        normal_price = Decimal(
            remove_words(soup.find("p", "price-debito-credito").find("bdi").text)
        )
        description = html_to_markdown(product_data["description"])
        key = soup.find("link", {"rel": "shortlink"})["href"].split("?p=")[-1]
        picture_urls = [
            a["href"]
            for a in soup.find("div", "woocommerce-product-gallery__wrapper").findAll(
                "a"
            )
        ]

        categories = [
            category.text.lower()
            for category in soup.find("span", "posted_in").findAll("a")
        ]

        if "seminuevos" in categories or "seminuevo" in name:
            condition = "https://schema.org/RefurbishedCondition"
        elif "open box" in categories or "open box" in name:
            condition = "https://schema.org/OpenBoxCondition"
        else:
            condition = "https://schema.org/NewCondition"

        p = Product(
            name,
            cls.__name__,
            category,
            url,
            url,
            key,
            stock,
            normal_price,
            offer_price,
            "CLP",
            sku=sku,
            picture_urls=picture_urls,
            description=description,
            condition=condition,
        )

        return [p]
