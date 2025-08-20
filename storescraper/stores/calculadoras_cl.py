import json
import re
from decimal import Decimal

from bs4 import BeautifulSoup

from storescraper.product import Product
from storescraper.store_with_url_extensions import StoreWithUrlExtensions
from storescraper.utils import html_to_markdown, remove_words


from storescraper.categories import (
    CALCULATOR,
)


class CalculadorasCl(StoreWithUrlExtensions):
    url_extensions = [
        ("categoria-grafica", CALCULATOR),
        ("categoria-financieras", CALCULATOR),
        ("categoria-rollo", CALCULATOR),
        ("calculadoras-open-box", CALCULATOR),
        ("categoria-cientificas", CALCULATOR),
        ("categoria-basicas", CALCULATOR),
    ]

    @classmethod
    def discover_urls_for_url_extension(cls, url_extension, extra_args=None):
        session = cls.get_session(extra_args)
        session.headers["RSC"] = "1"
        page = 1

        while True:
            if page >= 15:
                raise Exception("Page overflow")

            url = f"https://calculadoras.cl/{url_extension}?page={page}"
            print(url)
            response = session.get(url)
            raw_data = re.search(r"\n7:(.+)", response.text).groups()[0]
            json_data = json.loads(raw_data)
            json_products = json_data[3]["children"][1][3]["children"][1][3]["products"]

            if not json_products:
                break

            for product in json_products:
                product_url = f"https://calculadoras.cl/producto/{product['slug']}"
                yield product_url

            page += 1

    @classmethod
    def products_for_url(cls, url, category=None, extra_args=None):
        print(url)

        session = cls.get_session(extra_args)
        session.headers["RSC"] = "1"

        response = session.get(url)
        # Manually decode because the server encoding seems messed up
        response_text = response.content.decode("utf-8")
        raw_data = re.search(r"7:\[(.+)", response_text).groups()[0]
        raw_json = json.loads("[" + raw_data)
        product_data = raw_json[3]["children"][0][3]["product"]
        name = product_data["name"]
        key = product_data["id"]
        stock = -1 if product_data["inStock"] else 0
        normal_price = Decimal(product_data["priceCard"])
        offer_price = Decimal(product_data["priceCash"])
        if offer_price > normal_price:
            offer_price = normal_price
        picture_urls = [x["url"] for x in product_data["images"]]

        # Iterate over each chunk of lines, each chunk starts with a hexadecimal value.
        # Find the chunk that contains the text "characteristics", this one has the product description
        current_text = ""
        description_found = False
        for line in response_text.split("\n"):
            if re.match("[0-9a-f]+:", line):
                if description_found:
                    break
                else:
                    current_text = line + "\n"

            current_text += line + "\n"
            if "characteristics" in line:
                description_found = True

        description_soup = BeautifulSoup(current_text, "lxml")
        description = html_to_markdown(str(description_soup))

        if "OPEN BOX" in name:
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
            sku=key,
            picture_urls=picture_urls,
            description=description,
            condition=condition,
        )

        yield p
