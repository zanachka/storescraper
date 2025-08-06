import logging
import re
import json

from bs4 import BeautifulSoup
from decimal import Decimal

from storescraper.product import Product
from storescraper.store import Store
from storescraper.utils import session_with_proxy, html_to_markdown
from storescraper.categories import WASHING_MACHINE


class Comandato(Store):
    @classmethod
    def categories(cls):
        return [
            WASHING_MACHINE,
        ]

    @classmethod
    def discover_urls_for_category(cls, category, extra_args=None):
        session = session_with_proxy(extra_args)
        product_urls = []

        if category != WASHING_MACHINE:
            return []

        url = "https://www.comandato.com/lg?PS=200"
        soup = BeautifulSoup(session.get(url).text, "lxml")
        products = soup.findAll("div", "vtex-search-result-3-x-galleryItem")

        if not products:
            logging.warning("Empty url {}".format(url))

        for product in products:
            product_url = f"https://www.comandato.com{product.find('a')['href']}"
            product_urls.append(product_url)

        return product_urls

    @classmethod
    def products_for_url(cls, url, category=None, extra_args=None):
        print(url)
        session = session_with_proxy(extra_args)
        response = session.get(url)

        if response.status_code == 404:
            return []

        data = response.text
        soup = BeautifulSoup(data, "lxml")
        product_data = json.loads(
            soup.find("script", {"type": "application/ld+json"}).text
        )
        name = product_data["name"]
        sku = product_data["mpn"]
        offers = product_data["offers"]["offers"]
        assert len(offers) == 1
        offer = offers[0]
        stock = -1 if offer["availability"] == "http://schema.org/InStock" else 0
        price_tag = soup.find("span", "vtex-product-price-1-x-currencyContainer")
        price = Decimal(
            price_tag.text.replace("$", "").replace(".", "").replace(",", ".")
        )

        picture_urls = [
            img["src"].split("?")[0]
            for img in soup.find_all("img", "vtex-store-components-3-x-productImageTag")
        ]

        description = html_to_markdown(
            str(soup.find("div", "vtex-disclosure-layout-1-x-content--product-info"))
        )

        p = Product(
            name,
            cls.__name__,
            category,
            url,
            url,
            sku,
            stock,
            price,
            price,
            "USD",
            sku=sku,
            picture_urls=picture_urls,
            description=description,
        )

        return [p]
