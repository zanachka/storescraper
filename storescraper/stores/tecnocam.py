import json
import logging
from decimal import Decimal

from bs4 import BeautifulSoup

from storescraper.categories import (
    ALL_IN_ONE,
    CASE_FAN,
    CELL,
    CPU_COOLER,
    EXTERNAL_STORAGE_DRIVE,
    GAMING_CHAIR,
    KEYBOARD,
    KEYBOARD_MOUSE_COMBO,
    MEMORY_CARD,
    MOTHERBOARD,
    MOUSE,
    POWER_SUPPLY,
    TABLET,
    TELEVISION,
    VIDEO_CARD,
    SOLID_STATE_DRIVE,
    STORAGE_DRIVE,
    COMPUTER_CASE,
    PROCESSOR,
    RAM,
    MONITOR,
    HEADPHONES,
    NOTEBOOK,
    USB_FLASH_DRIVE,
    STEREO_SYSTEM,
    MICROPHONE,
    VIDEO_GAME_CONSOLE,
    PRINTER,
    PRINTER_SUPPLY,
    ACCESORIES,
    UPS,
)
from storescraper.product import Product
from storescraper.store_with_url_extensions import StoreWithUrlExtensions
from storescraper.utils import html_to_markdown, session_with_proxy


class Tecnocam(StoreWithUrlExtensions):
    url_extensions = [
        ["computacion/notebooks-accesorios/notebooks", NOTEBOOK],
        ["computacion/notebooks-accesorios/accesorios-notebooks", ACCESORIES],
        ["computacion/laptops-accesorios/repuestos", ACCESORIES],
        ["computacion/componentes-pc/tarjetas", VIDEO_CARD],
        [
            "computacion/componentes-pc/discos-accesorios/discos-duros-ssds",
            SOLID_STATE_DRIVE,
        ],
        ["computacion/componentes-pc/discos-accesorios/accesorios", ACCESORIES],
        ["computacion/componentes-pc/memorias-ram", RAM],
        ["computacion/componentes-pc/procesadores", PROCESSOR],
        ["computacion/componentes-pc/fuentes-alimentacion", POWER_SUPPLY],
        ["computacion/componentes-pc/gabinetes-soportes-pc", COMPUTER_CASE],
        ["computacion/componentes-pc/refrigeracion", CPU_COOLER],
        ["computacion/accesorios-pc-gaming/audifonos", HEADPHONES],
        ["computacion/accesorios-pc-gaming/sillas-gamer", GAMING_CHAIR],
        ["computacion/almacenamiento/pen-drives", USB_FLASH_DRIVE],
        ["computacion/estabilizadores-ups", UPS],
        ["computacion/perifericos-accesorios/cables-hubs-usb", ACCESORIES],
        ["computacion/impresion/insumos-impresion", PRINTER_SUPPLY],
        ["computacion/impresion/impresoras", PRINTER],
        ["computacion/impresion/accesorios", ACCESORIES],
        ["computacion/limpieza-cuidado-pcs", ACCESORIES],
        ["pc-escritorio-all-in-one", ALL_IN_ONE],
        ["computacion/monitores-accesorios/monitores", MONITOR],
        ["perifericos-pc-mouses-teclados", KEYBOARD_MOUSE_COMBO],
        ["computacion/tablets-accesorios/accesorios", ACCESORIES],
        ["computacion/tablets-accesorios/tablets", TABLET],
        ["electronica-audio-video/audio/audio-portatil-accesorios", STEREO_SYSTEM],
        ["electronica-audio-video/audio/audifonos", HEADPHONES],
        ["electronica-audio-video/audio/parlantes-subwoofers", STEREO_SYSTEM],
        ["electronica-audio-video/accesorios-audio-video", ACCESORIES],
        ["electronica-audio-video/cables", ACCESORIES],
        ["celulares-telefonia/accesorios-celulares/cargadores", ACCESORIES],
        ["celulares-telefonia/accesorios-celulares/manos-libres", HEADPHONES],
        ["celulares-telefonia/accesorios-celulares/parlantes", STEREO_SYSTEM],
        ["celulares-telefonia/accesorios-celulares/baterias", ACCESORIES],
        ["celulares-telefonia/accesorios-celulares/cables-datos", ACCESORIES],
    ]

    @classmethod
    def discover_urls_for_url_extension(cls, url_extension, extra_args=None):
        session = session_with_proxy(extra_args)
        products_urls = []
        index = 1

        while True:
            if index > 1000:
                raise Exception("page overflow: " + url_extension)

            url_webpage = f"https://www.tecnocam.cl/listado/{url_extension}/_Desde_{index}_NoIndex_True"
            print(url_webpage)
            response = session.get(url_webpage)
            soup = BeautifulSoup(response.text, "lxml")
            product_containers = soup.find_all("li", "ui-search-layout__item")

            if not product_containers:
                if index == 1:
                    logging.warning("Empty category: " + url_extension)
                break

            for container in product_containers:
                products_url = container.find("a")["href"].split("#")[0].split("?")[0]
                products_urls.append(products_url)

            index += 50

        return products_urls

    @classmethod
    def products_for_url(cls, url, category=None, extra_args=None):
        print(url)
        session = session_with_proxy(extra_args)
        response = session.get(url, timeout=60)
        soup = BeautifulSoup(response.text, "lxml")
        product_data = json.loads(
            soup.find("script", {"type": "application/ld+json"}).text
        )

        key = soup.find("input", {"name": "item_id"})["value"]
        name = product_data["name"]

        if "alternativa" in name.lower() or "alternativo" in name.lower():
            return []

        sku = product_data["sku"]
        offers = product_data["offers"]
        price = Decimal(offers["price"])
        stock = -1 if offers["availability"] == "https://schema.org/InStock" else -1
        description_tag = soup.find("div", "ui-pdp-description")
        description = (
            html_to_markdown(description_tag.text) if description_tag else None
        )
        picture_urls = [
            img["data-zoom"]
            for img in soup.find_all("img", "ui-pdp-gallery__figure__image")
        ]
        condition_tag = soup.find("span", "ui-pdp-subtitle")
        condition = (
            "https://schema.org/RefurbishedCondition"
            if condition_tag.text == "Reacondicionado"
            or "reacondicionado" in name.lower()
            else "https://schema.org/NewCondition"
        )

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
            sku=sku,
            part_number=sku,
            picture_urls=picture_urls,
            description=description,
            condition=condition,
        )

        return [p]
