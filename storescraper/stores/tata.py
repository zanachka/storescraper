import json
from bs4 import BeautifulSoup
from decimal import Decimal, ROUND_DOWN
from storescraper.categories import TELEVISION

from storescraper.product import Product
from storescraper.store import Store
from storescraper.utils import html_to_markdown, session_with_proxy


class Tata(Store):
    @classmethod
    def categories(cls):
        return [TELEVISION]

    @classmethod
    def discover_urls_for_category(cls, category, extra_args=None):
        if category != TELEVISION:
            return []

        product_urls = []
        session = session_with_proxy(extra_args)
        offset = 0

        while True:
            print(offset)
            payload = {
                "first": 18,
                "after": str(offset),
                "sort": "score_desc",
                "term": "",
                "selectedFacets": [
                    {"key": "brand", "value": "lg"},
                ],
            }

            endpoint = f"https://www.tata.com.uy/api/graphql?operationName=ProductsQuery&variables={json.dumps(payload)}"
            response = session.get(endpoint).json()
            product_entries = response["data"]["search"]["products"]

            if product_entries["edges"] == []:
                break

            for edge in product_entries["edges"]:
                product_urls.append(f"https://www.tata.com.uy/{edge['node']['slug']}/p")

            offset += 18

        return product_urls

    @classmethod
    def products_for_url(cls, url, category=None, extra_args=None):
        print(url)
        session = session_with_proxy(extra_args)
        response = session.get(url)
        soup = BeautifulSoup(response.text, "lxml")
        product_data = json.loads(
            soup.findAll("script", {"type": "application/ld+json"})[1].text
        )

        name = product_data["name"]
        sku = product_data["sku"]
        picture_urls = product_data["image"]
        description = product_data["description"]
        offers = product_data["offers"]["offers"]
        offer = None

        for offer_option in offers:
            if (
                offer_option["seller"]["identifier"] == "1"
                and offer_option["price"] > 0
            ):
                offer = offer_option
                break

        if not offer:
            return []

        price = Decimal(offer["price"]).quantize(Decimal("1.00"))
        stock = -1 if offer["availability"] == "https://schema.org/InStock" else 0

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
            "UYU",
            sku=sku,
            picture_urls=picture_urls,
            description=description,
        )

        return [p]
