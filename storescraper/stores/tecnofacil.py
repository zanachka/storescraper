import json
import time
from bs4 import BeautifulSoup
from decimal import Decimal

from storescraper.categories import TELEVISION
from storescraper.product import Product
from storescraper.store import Store
from storescraper.utils import (
    session_with_proxy,
    html_to_markdown,
)


class Tecnofacil(Store):
    preferred_products_for_url_concurrency = 1

    @classmethod
    def categories(cls):
        return [
            TELEVISION,
        ]

    @classmethod
    def discover_urls_for_category(cls, category, extra_args=None):
        url_extensions = [TELEVISION]

        session = session_with_proxy(extra_args)
        headers = {
            "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36",
            "x-api-key": "ROGi1LWB3saRqFw4Xdqc4Z9jGWVxYLl9ZEZjbJu9",
            "channel": "2",
        }
        session.headers = headers
        product_urls = []

        for local_category in url_extensions:
            if local_category != category:
                continue
            page = 1

            while True:
                if page >= 25:
                    raise Exception("Page overflow")

                url = f"https://apigt.tienda.max.com.gt/v2/products?sort=DESC&sortBy=relevance&categories=5909&page={page}&pageSize=12"
                print(url)

                response = session.get(url)
                products = response.json()["products"]

                if not products:
                    break

                for product in products:
                    product_urls.append(
                        f"https://www.tecnofacil.com.gt/{product['slug']}"
                    )

                page += 1

        return product_urls

    @classmethod
    def products_for_url(cls, url, category=None, extra_args=None):
        print(url)
        session = session_with_proxy(extra_args)
        session.headers["User-Agent"] = "curl/7.68.0"
        tries = 0

        while tries < 5:
            response = session.get(url)

            if response.status_code == 200:
                break

            time.sleep(20)
            tries += 1

        if response.status_code != 200:
            return []

        soup = BeautifulSoup(response.text, "lxml")
        product_data = json.loads(
            soup.find("script", {"type": "application/ld+json"}).text
        )
        sku = product_data["sku"]
        name = product_data["name"]
        price = Decimal(product_data["offers"][0]["price"])
        stock = (
            -1
            if soup.find(
                "div", {"id": "product-detail-page-add-to-cart-button-section-desktop"}
            )
            else 0
        )
        picture_urls = product_data["image"]
        description = html_to_markdown(product_data["description"])

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
            "GTQ",
            sku=sku,
            part_number=sku,
            picture_urls=picture_urls,
            description=description,
        )

        return [p]
