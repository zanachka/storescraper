from decimal import Decimal
import logging
import json
import re

from bs4 import BeautifulSoup
from storescraper.categories import (
    CASE_FAN,
    COMPUTER_CASE,
    CPU_COOLER,
    GAMING_CHAIR,
    HEADPHONES,
    KEYBOARD,
    MEMORY_CARD,
    MONITOR,
    MOTHERBOARD,
    MOUSE,
    NOTEBOOK,
    POWER_SUPPLY,
    PROCESSOR,
    RAM,
    STEREO_SYSTEM,
    SOLID_STATE_DRIVE,
    VIDEO_CARD,
    VIDEO_GAME_CONSOLE,
)
from storescraper.product import Product
from storescraper.store_with_url_extensions import StoreWithUrlExtensions
from storescraper.utils import (
    get_price_from_price_specification,
    html_to_markdown,
    session_with_proxy,
)


class PowerPlay(StoreWithUrlExtensions):
    url_extensions = [
        ["consolas-de-videojuegos/xbox/consolas", VIDEO_GAME_CONSOLE],
        ["consolas-de-videojuegos/nintendo/consolas", VIDEO_GAME_CONSOLE],
        ["consolas-de-videojuegos/playstation/consolas", VIDEO_GAME_CONSOLE],
        ["hardware/notebook-gamer", NOTEBOOK],
        ["hardware/componentes/gabinetes", COMPUTER_CASE],
        ["hardware/componentes/fuentes-de-poder", POWER_SUPPLY],
        ["hardware/componentes/procesador", PROCESSOR],
        ["hardware/componentes/placa-madre", MOTHERBOARD],
        ["hardware/componentes/memorias-ram", RAM],
        ["hardware/componentes/almacenamiento", SOLID_STATE_DRIVE],
        ["hardware/componentes/memorias-flash", MEMORY_CARD],
        ["hardware/componentes/tarjeta-de-video", VIDEO_CARD],
        [
            "hardware/componentes/refrigeracion-y-ventilacion/refrigeracion-liquida",
            CPU_COOLER,
        ],
        ["hardware/componentes/refrigeracion-y-ventilacion/cooler-cpu", CPU_COOLER],
        [
            "hardware/componentes/refrigeracion-y-ventilacion/ventilador-gabinete",
            CASE_FAN,
        ],
        ["hardware/monitores", MONITOR],
        ["perifericos-gamer/teclados-gamer", KEYBOARD],
        ["perifericos-gamer/mouse-gamer", MOUSE],
        ["perifericos-gamer/audifonos-gamer", HEADPHONES],
        ["sillas-y-mobiliario-gamer/sillas-gamer", GAMING_CHAIR],
        ["auriculares-y-audio/auriculares-bluetooth", HEADPHONES],
        ["auriculares-y-audio/auriculares-con-cable", HEADPHONES],
        ["auriculares-y-audio/parlantes-bluetooth", STEREO_SYSTEM],
        ["auriculares-y-audio/parlantes-pc-hogar", STEREO_SYSTEM],
    ]

    @classmethod
    def discover_urls_for_url_extension(cls, url_extension, extra_args):
        product_urls = []
        session = session_with_proxy(extra_args)
        page = 1

        while True:
            url = f"https://www.power-play.cl/todos-los-productos/{url_extension}?page={page}"
            print(url)

            response = session.get(url)
            soup = BeautifulSoup(response.text, "lxml")
            products = soup.findAll("article", "product-block")

            if not products:
                if page == 1:
                    logging.warning(f"Empty category: {url_extension}")
                break

            for product in products:
                product_url = product.find("a")["href"]
                product_urls.append(f"https://www.power-play.cl{product_url}")

            page += 1

        return product_urls

    @classmethod
    def products_for_url(cls, url, category=None, extra_args=None):
        print(url)
        session = session_with_proxy(extra_args)
        soup = BeautifulSoup(session.get(url).text, "lxml")
        script = soup.find("script", {"type": "application/ld+json"})

        if not script:
            return []

        json_data = json.loads(script.text)

        for item in json_data:
            if item["@type"] == "Product":
                product_data = item
                key = soup.find("script", "product-json")["data-productid"]
                name = product_data["name"]
                sku = str(product_data["sku"]) if "sku" in product_data else None
                normal_price = Decimal(product_data["offers"]["price"])
                gallery = soup.find(
                    "swiper-slider", "product-gallery__carousel--main"
                ).find_all("img", "product-gallery__image product-gallery__image--main")
                picture_urls = [img["src"].split("?")[0] for img in gallery]
                description = html_to_markdown(product_data["description"])
                stock = (
                    -1
                    if product_data["offers"]["availability"]
                    == "https://schema.org/InStock"
                    else 0
                )

                p = Product(
                    name,
                    cls.__name__,
                    category,
                    url,
                    url,
                    key,
                    stock,
                    normal_price,
                    normal_price,
                    "CLP",
                    sku=sku,
                    description=description,
                    picture_urls=picture_urls,
                )

                return [p]

        return []
