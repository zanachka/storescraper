import json
import time
from decimal import Decimal
from bs4 import BeautifulSoup
from storescraper.categories import GROCERIES
from storescraper.product import Product
from storescraper.store_with_url_extensions import StoreWithUrlExtensions
from storescraper.utils import (
    html_to_markdown,
    remove_words,
    cf_session_with_proxy,
    check_ean13,
)


class TottusSupermercado(StoreWithUrlExtensions):
    url_extensions = [
        # Despensa
        ("CATG27056", GROCERIES),
        ("CATG27060", GROCERIES),
        ("CATG27059", GROCERIES),
        ("CATG27062", GROCERIES),
        ("CATG27063", GROCERIES),
        ("CATG27067", GROCERIES),
        ("CATG27066", GROCERIES),
        ("CATG27064", GROCERIES),
        ("CATG27065", GROCERIES),
        ("CATG27669", GROCERIES),
        # Carnes
        ("CATG27090", GROCERIES),
        ("CATG27092", GROCERIES),
        ("CATG27091", GROCERIES),
        ("CATG27093", GROCERIES),
        ("CATG27094", GROCERIES),
        ("CATG27097", GROCERIES),
        # Frutas y Verduras
        ("CATG27098", GROCERIES),
        ("CATG27099", GROCERIES),
        ("CATG27100", GROCERIES),
        ("CATG27101", GROCERIES),
        ("CATG27102", GROCERIES),
        ("CATG27103", GROCERIES),
        ("CATG27123", GROCERIES),
        ("CATG27124", GROCERIES),
        # Lácteos y Quesos
        ("CATG27180", GROCERIES),
        ("CATG27179", GROCERIES),
        ("CATG27185", GROCERIES),
        ("CATG27182", GROCERIES),
        ("CATG27189", GROCERIES),
        ("CATG27195", GROCERIES),
        ("CATG27192", GROCERIES),
        # Desayunos y Dulces
        ("CATG27113", GROCERIES),
        ("CATG27114", GROCERIES),
        ("CATG27115", GROCERIES),
        ("CATG27116", GROCERIES),
        ("CATG27117", GROCERIES),
        ("CATG27118", GROCERIES),
        ("CATG27119", GROCERIES),
        ("CATG27120", GROCERIES),
        ("CATG27121", GROCERIES),
        ("CATG27122", GROCERIES),
        # Fiambres y Huevos
        ("CATG27203", GROCERIES),
        ("CATG27266", GROCERIES),
        ("CATG27267", GROCERIES),
        ("CATG27268", GROCERIES),
        ("CATG27269", GROCERIES),
        ("CATG27270", GROCERIES),
        ("CATG27271", GROCERIES),
        # Bebidas y Jugos
        ("CATG27215", GROCERIES),
        ("CATG27216", GROCERIES),
        ("CATG27217", GROCERIES),
        ("CATG27218", GROCERIES),
        ("CATG27219", GROCERIES),
        # Platos Preparados
        ("CATG27272", GROCERIES),
        ("CATG27273", GROCERIES),
        ("CATG27274", GROCERIES),
        ("CATG27277", GROCERIES),
        ("CATG27278", GROCERIES),
        # Panadería y Pastelería
        ("CATG27140", GROCERIES),
        ("CATG27144", GROCERIES),
        ("CATG27142", GROCERIES),
        # Congelados
        ("CATG27125", GROCERIES),
        ("CATG27129", GROCERIES),
        ("CATG27126", GROCERIES),
        ("CATG27127", GROCERIES),
        ("CATG27132", GROCERIES),
        ("CATG27130", GROCERIES),
        # Pescados y Mariscos
        ("CATG27421", GROCERIES),
        ("CATG27422", GROCERIES),
        ("CATG27423", GROCERIES),
        ("CATG27425", GROCERIES),
        ("CATG27426", GROCERIES),
    ]

    @classmethod
    def get_session(cls, extra_args=None):
        return cf_session_with_proxy(extra_args)

    @classmethod
    def discover_urls_for_url_extension(cls, url_extension, extra_args=None):
        session = cls.get_session()
        page = 1

        while True:
            if page >= 50:
                raise Exception(f"Page overflow: {url_extension}")

            print(f"{url_extension} page {page}")

            response = session.get(
                f"https://www.falabella.com/s/browse/v1/listing/cl?store=to_com&categoryId={url_extension}&pid=9e635d19-b626-4171-8beb-d92e58c2a417&page={page}"
            )
            json_data = response.json()
            products = json_data["data"]["results"]

            if not products:
                if page == 1:
                    raise Exception(f"Empty section: {url_extension}")
                break

            for product in products:
                product_url = product["url"]
                yield product_url

            page += 1

    @classmethod
    def products_for_url(cls, url, category=None, extra_args=None):
        print(url)
        session = cls.get_session()
        session.headers["User-Agent"] = (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36"
        )
        session.headers["origin"] = "https://www.tottus.cl"

        for _ in range(5):
            response = session.get(url)
            soup = BeautifulSoup(response.text, "lxml")
            next_container = soup.find("script", {"id": "__NEXT_DATA__"})

            if next_container:
                break

            time.sleep(5)
        else:
            return []

        page_props = json.loads(next_container.contents[0])["props"]["pageProps"]
        product_data = page_props["productData"]
        brand = product_data["brandName"]
        name = f"{brand} - {product_data['name']}"
        description = html_to_markdown(product_data["longDescription"])

        assert len(product_data["variants"]) == 1

        for model in product_data["variants"]:
            key = model["id"]
            normal_price = None
            offer_price = None

            for price in model["prices"]:
                if price["type"] == "internetPrice":
                    normal_price = Decimal(remove_words(price["price"][0]))
                if price["type"] == "cmrPrice":
                    offer_price = Decimal(remove_words(price["price"][0]))

            if not offer_price:
                offer_price = normal_price

            picture_urls = [img["url"] for img in model["medias"]]
            raw_ean = model["okayToShopBarcodes"][0]
            ean = raw_ean if check_ean13(raw_ean) else None
            description_response = session.get(
                f"https://api.okto.shop/snippet_v1/?url={url}&ean={raw_ean}"
            )

            if description_response.text:
                description_soup = (
                    BeautifulSoup(description_response.text, "lxml").find("body").text
                )
                description_html = json.loads(description_soup)["html"]
                description += html_to_markdown(description_html)

            specs = [f"- Marca: {brand}"] + [
                f"- {item['name']}: {item['value']}"
                for item in model["attributes"]["specifications"]
            ]
            description += "\n" + "\n".join(specs)
            seller_entry = None

            for offer in model["offerings"]:
                if offer["sellerId"] == "TOTTUS_CHILE":
                    seller_entry = offer
                    break

            sku = seller_entry["sellerSkuId"]

            if seller_entry.get(
                "sellerProductStatus", None
            ) == "ACTIVO" or seller_entry.get("isActive", False):
                stock = -1
            elif not product_data["isOutOfStock"] and model.get(
                "isOnlineSellable", False
            ):
                stock = -1
            else:
                stock = 0

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
                ean=ean,
            )

            yield p
