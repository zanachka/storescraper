import json

from bs4 import BeautifulSoup
from decimal import Decimal

from storescraper.categories import CELL
from storescraper.product import Product
from storescraper.store import Store


class TiendaEntel(Store):
    @classmethod
    def categories(cls):
        return [
            CELL,
        ]

    @classmethod
    def discover_urls_for_category(cls, category, extra_args=None):
        from .entel import Entel

        if category != CELL:
            return []

        yield from Entel.discover_urls_for_category(category, extra_args)

    @classmethod
    def products_for_url(cls, url, category=None, extra_args=None):
        return cls._products_for_url(url, extra_args)

    @classmethod
    def _products_for_url(cls, url, extra_args=None, retries=5):
        print(url)
        session = cls.get_session(extra_args)

        products = []

        soup = BeautifulSoup(session.get(url).text, "lxml")
        product_detail_container = soup.find("div", {"id": "productDetail"})

        if not product_detail_container:
            # For the case of https://miportal.entel.cl/personas/producto/
            # prod1410051 that displays a blank page
            return []

        raw_json = product_detail_container.find("script").string

        if not raw_json:
            if retries:
                return cls._products_for_url(url, extra_args, retries=retries - 1)
            else:
                raise Exception("JSON error")

        try:
            json_data = json.loads(raw_json)
        except json.decoder.JSONDecodeError:
            return []

        base_name = json_data["renderVOBean"]["productName"]

        description = {}

        for spec in json_data["specifications"]:
            if "groupValue" in spec:
                for attribute in spec["groupValue"]:
                    description[attribute["attributeKey"]] = attribute["attributeValue"]

        description = json.dumps(description)

        for sku in json_data["renderSkusBean"]["skus"]:
            # if not sku["available"]:
            #     continue
            price_container = sku["skuPrice"]
            if not price_container:
                continue

            sku_id = sku["skuId"]

            normal_price = Decimal(price_container).quantize(0)

            offer_price_endpoint = (
                "https://miportal.entel.cl/restpp/equipments/prices/" + sku_id
            )
            offer_price_response = session.get(offer_price_endpoint).json()
            offer_price_text = min(
                [x["priceIVA"] for x in offer_price_response["response"]["Prices"]]
            )
            offer_price = Decimal(offer_price_text).quantize(0)

            pictures_container = []
            stock = 0

            for view in json_data["skuViews"]:
                if view["skuId"] == sku_id:
                    if view["visibilityButtonPdp"] != 0:
                        stock = view["stockDelivery"] + view["stockPickup"]
                    pictures_container = view["images"]
                    break

            picture_urls = []

            for container in pictures_container:
                picture_url = "https://miportal.entel.cl" + container["heroImage"]
                picture_urls.append(picture_url.replace(" ", "%20"))

            if "semi" in sku["skuName"].lower() or "semi" in base_name.lower():
                condition = "https://schema.org/RefurbishedCondition"
            else:
                condition = "https://schema.org/NewCondition"

            product = Product(
                sku["skuName"],
                cls.__name__,
                "Cell",
                url,
                url,
                sku_id,
                stock,
                normal_price,
                offer_price,
                "CLP",
                sku=sku_id,
                picture_urls=picture_urls,
                condition=condition,
                description=description,
            )

            products.append(product)

        return products
