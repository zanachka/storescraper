import json
import re
from bs4 import BeautifulSoup
from decimal import Decimal
from storescraper.product import Product
from storescraper.store_with_url_extensions import StoreWithUrlExtensions
from storescraper.utils import html_to_markdown, session_with_proxy
from storescraper.categories import ALL_IN_ONE, KEYBOARD_MOUSE_COMBO, NOTEBOOK


class ZTech(StoreWithUrlExtensions):
    url_extensions = [
        ["notebooks-gamers", NOTEBOOK],
        ["notebooks-empresariales", NOTEBOOK],
        ["ultrabooks", NOTEBOOK],
        ["perifericos", KEYBOARD_MOUSE_COMBO],
        ["all-in-one", ALL_IN_ONE],
    ]

    @classmethod
    def discover_urls_for_url_extension(cls, url_extension, extra_args):
        session = session_with_proxy(extra_args)
        page = 1

        while True:
            if page > 10:
                raise Exception("Page overflow")

            url = f"https://ztech.cl/collections/{url_extension}?page={page}"
            print(url)
            response = session.get(url)
            soup = BeautifulSoup(response.text, "lxml")
            products = soup.findAll("div", "product-card-wrapper")

            if not products:
                break

            for product in products:
                product_url = f"https://ztech.cl{product.find('a')['href']}"
                yield product_url

            page += 1

    @classmethod
    def products_for_url(cls, url, category=None, extra_args=None):
        print(url)
        session = session_with_proxy(extra_args)
        soup = BeautifulSoup(session.get(url).text, "lxml")
        raw_data = soup.findAll("script", {"type": "application/ld+json"})[1].text
        product_data = json.loads(raw_data.replace("\n", " "))

        name = product_data["name"]
        part_number = re.search(r"\[([^]]+)](?!.*\[[^]]+])", name)
        part_number = part_number.group(1) if part_number else None
        description = html_to_markdown(product_data["description"])
        picture_urls = [
            f"https:{slide.find('img')['src']}"
            for slide in soup.findAll("div", "product__media media media--transparent")
        ]
        condition = "https://schema.org/RefurbishedCondition"

        if "hasVariant" in product_data:
            products = []

            for variant in product_data["hasVariant"]:
                name = variant["name"]
                offer = variant["offers"]
                key = offer["url"].split("?variant=")[1]
                price = Decimal(offer["price"])
                stock = (
                    -1 if offer["availability"] == "http://schema.org/InStock" else 0
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
                    part_number=part_number,
                    condition=condition,
                    description=description,
                    picture_urls=picture_urls,
                )

                products.append(p)

            return products
        else:
            offer = product_data["offers"]
            key = soup.find("input", {"type": "hidden", "name": "id"})["value"]
            price = Decimal(offer["price"])
            stock = -1 if offer["availability"] == "https://schema.org/InStock" else 0

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
                part_number=part_number,
                condition=condition,
                description=description,
                picture_urls=picture_urls,
            )

            return [p]
