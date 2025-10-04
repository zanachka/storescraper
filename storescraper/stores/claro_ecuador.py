import json
from decimal import Decimal

from storescraper.categories import TELEVISION
from storescraper.product import Product
from storescraper.store import Store
from storescraper.utils import session_with_proxy


class ClaroEcuador(Store):
    @classmethod
    def categories(cls):
        return [TELEVISION]

    @classmethod
    def discover_urls_for_category(cls, category, extra_args=None):
        if category != TELEVISION:
            return []

        session = session_with_proxy(extra_args)
        session.headers["RSC"] = "1"

        url_webpage = "https://catalogo.claro.com.ec/personas/buscador?q=lg"
        response = session.get(url_webpage)
        content = response.content.decode("utf-8")
        search_results = json.loads(content.split("\n")[-2].split(":", 1)[1])[3]
        for search_result in search_results["state"]["queries"][1]["state"]["data"][
            "content"
        ]:
            if search_result["category"]["slug"] != "equipos":
                continue
            product_url = search_result["url"]
            yield product_url

    @classmethod
    def products_for_url(cls, url, category=None, extra_args=None):
        print(url)
        session = session_with_proxy(extra_args)
        session.headers["RSC"] = "1"
        response = session.get(url)
        content = response.content.decode("utf-8")

        for line in content.splitlines():
            if "idProducto" in line:
                break
        else:
            raise Exception("No product data found")

        product_entry = json.loads(line.split(":", 1)[1])[3]
        product_entry = product_entry["state"]["queries"][0]["state"]["data"]["content"]

        if "producto" not in product_entry:
            return []

        for presentacion in product_entry["producto"]["presentaciones"].values():
            price = Decimal(
                presentacion["financiamiento"]["precioNormalConImpOriginal"]
            ).quantize(Decimal("0.01"))

            for color in presentacion["colores"].values():
                picture_urls = [
                    "https://catalogo.claro.com.ec/" + tag["rutaZoom"]
                    for tag in color["imgs"]
                ]

                for sku in color["skus"].values():
                    name = sku["nombrePro"]
                    key = str(sku["id"])
                    stock = sku["stock"]

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
                        "USD",
                        sku=key,
                        picture_urls=picture_urls,
                    )

                    yield p
