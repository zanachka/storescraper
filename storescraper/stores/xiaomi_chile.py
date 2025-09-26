import json
import logging
import re
from decimal import Decimal

from bs4 import BeautifulSoup

from storescraper.categories import (
    ACCESORIES,
    CELL,
    HEADPHONES,
    MONITOR,
    MOUSE,
    PRINTER,
    PROJECTOR,
    STEREO_SYSTEM,
    TABLET,
    TELEVISION,
    USB_FLASH_DRIVE,
    WEARABLE,
)
from storescraper.product import Product
from storescraper.store_with_url_extensions import StoreWithUrlExtensions
from storescraper.utils import (
    session_with_proxy,
)


class XiaomiChile(StoreWithUrlExtensions):
    url_extensions = [
        ["4242", CELL],
        ["4874", TABLET],
        ["4264", WEARABLE],
        ["4267", HEADPHONES],
        ["4271", TELEVISION],
        ["5393", STEREO_SYSTEM],
        ["4273", PROJECTOR],
        ["5394", STEREO_SYSTEM],
        ["5450", ACCESORIES],
        ["4291", MONITOR],
        ["5102", PRINTER],
        ["5243", MOUSE],
        ["5453", USB_FLASH_DRIVE],
    ]

    @classmethod
    def discover_urls_for_url_extension(cls, url_extension, extra_args=None):
        session = session_with_proxy(extra_args)
        product_urls = []
        page = 0

        while True:
            if page > 10:
                raise Exception("page overflow: " + url_extension)

            endpoint = f"https://sgp-api.buy.mi.com/cl/search/v1/api/index//0/0/0/{page}/{url_extension}/0?version=v4"
            print(endpoint)
            response = session.get(endpoint).json()
            products = response["data"]["dataProvider"]["data"]

            if not products:
                if page == 0:
                    logging.warning(f"Empty category: {url_extension}")
                break

            for product in products:
                product_urls.append(product["product"]["item_link"])

            page += 1

        return product_urls

    @classmethod
    def products_for_url(cls, url, category=None, extra_args=None):
        print(url)
        session = session_with_proxy(extra_args)
        tag = url.split("https://www.mi.com/cl/product/")[1][:-1]
        endpoint = f"https://go.buy.mi.com/cl/v2/item/productdetail?tag={tag}"
        response = session.get(endpoint).json()
        products = response["data"]["item_detail"]["spu_list"]
        specs_response = session.get(f"https://www.mi.com/cl/product/{tag}/specs/")

        soup = BeautifulSoup(specs_response.text, "lxml")
        script_text = None

        for s in soup.find_all("script"):
            text = s.string if s.string is not None else s.get_text()

            if text and "window.__PRELOADED_STATE__" in text:
                script_text = text
                break

        if '"title":"404 - Xiaomi Chile"' in script_text:
            return []

        specs = json.loads(
            re.search(
                r"window\.__PRELOADED_STATE__\s*=\s*({.*?})\s*;?\s*$",
                script_text,
                re.DOTALL,
            ).group(1)
        )["pagedata"]["data"]
        specs = json.loads(specs)
        description_parts = [
            spec["trans"]
            for spec in specs.values()
            if isinstance(spec, dict) and "trans" in spec
        ]
        general_description = " | ".join(description_parts)
        products_list = []

        for product in products:
            for variant in product["item_list"]:
                name = variant["item_name"]
                key = str(variant["item_id"])
                stock = 0 if variant["is_out_of_stock"] else -1
                price = Decimal(variant["price"])
                picture_urls = [
                    (
                        img["src"]
                        if img["src"].startswith("https:")
                        else f"https:{img['src']}"
                    )
                    for img in variant["resource_list"]
                    if img["type"] == "image"
                ]
                description = f"PRODUCTO ACTUAL: {name} - DESCRIPCIÓN GENERAL: {general_description}"
                print(description)
                exit()
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
                    sku=key,
                    picture_urls=picture_urls,
                    description=description,
                )

                products_list.append(p)

        return products_list
