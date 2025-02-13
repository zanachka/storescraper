import re
from decimal import Decimal


from storescraper.categories import (
    SOLID_STATE_DRIVE,
    HEADPHONES,
    MOTHERBOARD,
    PROCESSOR,
    VIDEO_CARD,
    POWER_SUPPLY,
    CPU_COOLER,
    RAM,
)
from storescraper.product import Product
from storescraper.store_with_url_extensions import StoreWithUrlExtensions
from storescraper.utils import session_with_proxy


class Campcom(StoreWithUrlExtensions):
    url_extensions = [
        ("PROCESADORES", PROCESSOR),
        ("PLACAS MADRE", MOTHERBOARD),
        ("TARJETAS DE VIDEO", VIDEO_CARD),
        ("REFRIGERACIÓN", CPU_COOLER),
        ("FUENTES DE PODER", POWER_SUPPLY),
        ("OTROS", HEADPHONES),
        ("RAM", RAM),
        ("SSD", SOLID_STATE_DRIVE),
    ]

    @classmethod
    def discover_urls_for_url_extension(cls, url_extension, extra_args=None):
        product_urls = []
        for entry in extra_args["products"]:

            if entry["prd_categoria"] != url_extension:
                continue
            slug = entry["prd_title"].lower().replace(" ", "-")
            product_url = f"https://campcom.cl/producto/{slug}"
            product_urls.append(product_url)

        return product_urls

    @classmethod
    def products_for_url(cls, url, category=None, extra_args=None):
        print(url)
        session = session_with_proxy(extra_args)
        match = re.search(r"https://campcom.cl/producto/(.+)", url)
        slug = match.groups()[0]
        print(slug)
        # hardcoded for now
        title = "Procesador Intel Core Ultra 5-245K"

        for entry in extra_args["products"]:
            if entry["prd_title"] == title:
                matching_entry = entry
                break
        else:
            raise Exception("No matching product found")

        endpoint = f"https://campcom.cl/api/v2/products/{matching_entry['prd_id']}"
        product_data = session.get(endpoint).json()
        name = product_data["prd_title"]
        key = str(product_data["prd_id"])
        stock = product_data["prd_quantity"]
        offer_price = Decimal(product_data["prd_price"])
        normal_price = (offer_price * Decimal("1.04")).quantize(0)
        sku = product_data["prd_sku"]
        picture_urls = [
            f"https://campcom.cl/api/files/productos/{product_data['prd_image']}"
        ]
        description = product_data["prd_description"]

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
        )

        return [p]

    @classmethod
    def preflight(cls, extra_args=None):
        session = session_with_proxy(extra_args)
        products_json = session.get("https://campcom.cl/api/v2/products").json()["list"]
        return {"products": products_json}
