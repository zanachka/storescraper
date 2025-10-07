from decimal import Decimal
import json
from bs4 import BeautifulSoup
from storescraper.product import Product
from storescraper.store_with_url_extensions import StoreWithUrlExtensions
from storescraper.utils import (
    session_with_proxy,
    html_to_markdown,
)
from storescraper.categories import (
    NOTEBOOK,
    ALL_IN_ONE,
    TABLET,
    USB_FLASH_DRIVE,
    PROCESSOR,
    COMPUTER_CASE,
    POWER_SUPPLY,
    MOTHERBOARD,
    RAM,
    VIDEO_CARD,
    MOUSE,
    PRINTER,
    HEADPHONES,
    MONITOR,
    KEYBOARD_MOUSE_COMBO,
    KEYBOARD,
    GAMING_CHAIR,
    PRINTER_SUPPLY,
    CPU_COOLER,
    PROJECTOR,
    UPS,
    EXTERNAL_STORAGE_DRIVE,
)


class Cintegral(StoreWithUrlExtensions):
    url_extensions = [
        ("all-in-one-pc-y-portatiles", ALL_IN_ONE),
        ("notebook", NOTEBOOK),
        ("tablet-digitalizadoras-smartphone", TABLET),
        ("impresoras", PRINTER),
        ("impresoras-laser", PRINTER),
        ("impresoras-tinta", PRINTER),
        ("multifuncionales", PRINTER),
        ("plotter", PRINTER),
        ("suministros", PRINTER_SUPPLY),
        ("almacenamiento", USB_FLASH_DRIVE),
        ("memorias", RAM),
        ("placa-madre", MOTHERBOARD),
        ("procesadores", PROCESSOR),
        ("tarjetas-de-video", VIDEO_CARD),
        ("ventiladores-y-water-cooling", CPU_COOLER),
        ("gabinetes", COMPUTER_CASE),
        ("fuentes-de-poder", POWER_SUPPLY),
        ("combo-mouse-y-teclados", KEYBOARD_MOUSE_COMBO),
        ("mouse", MOUSE),
        ("teclados", KEYBOARD),
        ("monitores", MONITOR),
        ("proyeccion", PROJECTOR),
        ("ups", UPS),
        ("audio", HEADPHONES),
        ("apple", NOTEBOOK),
        ("almacenamiento-zona-gamer", EXTERNAL_STORAGE_DRIVE),
        ("monitores-zona-gamer", MONITOR),
        ("notebooks", NOTEBOOK),
        ("perifericos-zona-gamer", MOUSE),
        ("procesadores-zona-gamer", PROCESSOR),
        ("ram", RAM),
        ("sillas-zona-gamer", GAMING_CHAIR),
        ("tarjetas-de-video-zona-gamer", VIDEO_CARD),
    ]

    @classmethod
    def discover_urls_for_url_extension(cls, url_extension, extra_args=None):
        product_urls = []
        session = session_with_proxy(extra_args)
        session.headers["Content-Type"] = "application/x-www-form-urlencoded"
        page = 1

        while True:
            if page >= 30:
                raise Exception("Page overflow: " + url_extension)

            url = f"https://cintegral.cl/categoria/{url_extension}/page/{page}/"
            print(url)

            res = session.get(url, verify=False)
            soup = BeautifulSoup(res.text, "lxml")
            product_tags = soup.find_all("div", "product")

            if not product_tags:
                break

            for product_tag in product_tags:
                product_url = product_tag.find("a")["href"]
                product_urls.append(product_url)

            page += 1

        return product_urls

    @classmethod
    def products_for_url(cls, url, category=None, extra_args=None):
        print(url)
        session = session_with_proxy(extra_args)
        response = session.get(url, verify=False)
        soup = BeautifulSoup(response.text, "lxml")
        key_tag = soup.find("link", {"rel": "shortlink"})

        if not key_tag:
            return []

        key = key_tag["href"].split("?p=")[1]
        product_data_tag = soup.find_all("script", {"type": "application/ld+json"})[0]

        if not product_data_tag:
            return []

        product_data_entries = json.loads(product_data_tag.text)["@graph"]

        for entry in product_data_entries:
            if entry["@type"] == "Product":
                product_data = entry

        name = product_data["name"]
        part_number_tag = soup.find("div", "field_682c8d88970c3")
        part_number = (
            part_number_tag.contents[1].strip()
            if part_number_tag
            else product_data["sku"]
        )
        offer = product_data["offers"]
        stock = -1 if offer["availability"] == "https://schema.org/InStock" else 0
        price = Decimal(offer["price"])
        picture_urls = [
            img["src"]
            for img in soup.find("div", "product-image-slider").find_all("img")
        ]
        description_tag = soup.find("div", {"id": "tab-description"})
        description = (
            html_to_markdown(description_tag.text) if description_tag else None
        )

        if ("reacondicionado" in name) or (
            description and "reacondicionado" in description
        ):
            condition = "https://schema.org/RefurbishedCondition"
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
            price,
            price,
            "CLP",
            sku=key,
            part_number=part_number,
            description=description,
            picture_urls=picture_urls,
            condition=condition,
        )

        return [p]
