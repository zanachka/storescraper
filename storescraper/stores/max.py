import json

from decimal import Decimal
from bs4 import BeautifulSoup

from storescraper.product import Product
from storescraper.store import Store
from storescraper.utils import session_with_proxy
from storescraper.categories import TELEVISION


class Max(Store):
    # Only made to get LG products
    api_base_url = "https://apigt.tienda.max.com.gt"
    headers = {"x-api-key": "ROGi1LWB3saRqFw4Xdqc4Z9jGWVxYLl9ZEZjbJu9"}

    @classmethod
    def categories(cls):
        return [TELEVISION]

    @classmethod
    def discover_urls_for_category(cls, category, extra_args=None):
        if category != TELEVISION:
            return []

        session = session_with_proxy(extra_args)
        session.headers["x-api-key"] = "ROGi1LWB3saRqFw4Xdqc4Z9jGWVxYLl9ZEZjbJu9"
        product_urls = []
        page = 1

        while True:
            if page >= 20:
                raise Exception("Page overflow")

            api_endpoint = f"{cls.api_base_url}/v2/products?page={page}&search=lg"
            response = session.get(api_endpoint)
            json_data = response.json()

            if json_data["products"] == []:
                if page == 1:
                    raise Exception("Empty category")
                break

            product_urls.extend(
                [
                    f"https://www.max.com.gt/{product['meta']['url_key']}"
                    for product in json_data["products"]
                ]
            )
            page += 1

        return product_urls

    @classmethod
    def products_for_url(cls, url, category=None, extra_args=None):
        print(url)
        session = session_with_proxy(extra_args)
        response = session.get(url)

        if response.status_code in [404, 410]:
            return []

        soup = BeautifulSoup(response.text, "lxml")
        product = json.loads(soup.find("script", {"id": "__NEXT_DATA__"}).text)[
            "props"
        ]["pageProps"]["product"]

        name = product["title"]
        picture_urls = [img["url"] for img in product["gallery"]]
        sku = product["sku"]

        prices = json.loads(
            session.get(
                f"{cls.api_base_url}/v1/prices/{sku}",
                headers=cls.headers,
            ).text
        )
        normal_price = Decimal(prices["regularPrice"]["value"])
        sales_price = prices["salesPrice"]
        normal_price = Decimal(sales_price["value"]) if sales_price else normal_price

        summary = json.loads(
            session.get(
                f"{cls.api_base_url}/v1/products/{sku}/contentSyndication",
                headers=cls.headers,
            ).text
        )
        description = ""

        if "dimensions" in summary and summary["dimensions"]:
            description += "Dimensiones:\n"

            for dimension in summary["dimensions"]:
                description += f"- {dimension['label']}: {dimension['value']}\n"

            description += "\n"

        description += "Especificaciones:\n"

        if "specs" in summary:
            for spec in summary["specs"]:
                description += f"- {spec['label']}: {spec['value']}\n"

        stock_info = json.loads(
            session.get(
                f"{cls.api_base_url}/v1/products/{sku}/stock",
                headers=cls.headers,
            ).text
        )

        if "status" not in stock_info:
            return []

        stock = (
            0
            if stock_info["status"] == "OUT_OF_STOCK"
            else stock_info["salableQuantity"]
        )

        p = Product(
            name,
            cls.__name__,
            category,
            url,
            url,
            sku,
            stock,
            normal_price,
            normal_price,
            "GTQ",
            sku=sku,
            part_number=sku,
            picture_urls=picture_urls,
            description=description,
        )

        return [p]
