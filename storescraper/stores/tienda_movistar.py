from decimal import Decimal
import requests
import csv
from io import StringIO
from storescraper.categories import (
    HEADPHONES,
    TABLET,
    CELL,
    STEREO_SYSTEM,
    TELEVISION,
)
from storescraper.product import Product
from storescraper.store import Store
from storescraper.utils import remove_words


class TiendaMovistar(Store):
    category_paths = [
        (
            "celulares",
            "Electronica > Comunicacion > Telefonia > Telefonos moviles",
            CELL,
        ),
        ("tablets", "Electronica > Ordenadores > Tablets", TABLET),
        (
            "audifonos",
            "Electrónica > Audio > Equipo de sonido > Auriculares",
            HEADPHONES,
        ),
        ("smarthome", "Electrónica > Video > Televisores", TELEVISION),
        (
            "parlantes-bluetooth",
            "Electrónica > Audio > Equipo de sonido > Altavoces",
            STEREO_SYSTEM,
        ),
    ]

    @classmethod
    def categories(cls):
        return [
            CELL,
            TABLET,
            HEADPHONES,
            TELEVISION,
            STEREO_SYSTEM,
        ]

    @classmethod
    def discover_urls_for_category(cls, category, extra_args=None):
        url = cls.generate_discover_url_for_category(category)
        return [url]

    @classmethod
    def products_for_url(cls, url, category=None, extra_args=None):
        products = []

        for _, category_path, local_category in cls.category_paths:
            if local_category != category:
                continue

            print(category_path)
            url = f"https://docs.google.com/spreadsheets/d/1DCuy426WhXTwFd9hkILoL4eD6VIheqkL-GS7KJ6xLgw/export?format=csv"
            response = requests.get(url)
            response.encoding = "utf-8"
            csv_data = csv.DictReader(StringIO(response.text))
            data = list(csv_data)
            filtered_entries = [
                entry
                for entry in data
                if entry["categoría en google product"] == category_path
            ]

            for entry in filtered_entries:
                price = Decimal(remove_words(entry["precio de oferta"]))
                sku = entry["id"]
                products.append(
                    Product(
                        name=entry["título"],
                        store=cls.__name__,
                        category=category,
                        url=entry["enlace"],
                        discovery_url=cls.generate_discover_url_for_category(category),
                        key=sku,
                        stock=0 if entry["disponibilidad"] == "agotado" else -1,
                        normal_price=price,
                        offer_price=price,
                        currency="CLP",
                        sku=sku,
                        condition=(
                            "https://schema.org/NewCondition"
                            if entry["estado"] == "Nuevo"
                            else "https://schema.org/RefurbishedCondition"
                        ),
                        description=entry["descripción"],
                        picture_urls=[entry["enlace imagen"]],
                    )
                )

        return products

    @classmethod
    def generate_discover_url_for_category(cls, category):
        for url_path, _, local_category in cls.category_paths:
            if local_category == category:
                return f"https://catalogo.movistar.cl/tienda/{url_path}"
