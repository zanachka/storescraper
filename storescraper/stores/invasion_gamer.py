import logging
from bs4 import BeautifulSoup
from decimal import Decimal
from storescraper.categories import (
    COMPUTER_CASE,
    PROCESSOR,
    RAM,
    MOTHERBOARD,
    VIDEO_CARD,
    SOLID_STATE_DRIVE,
    CPU_COOLER,
    POWER_SUPPLY,
    KEYBOARD,
    MOUSE,
    HEADPHONES,
    GAMING_CHAIR,
    NOTEBOOK,
    MONITOR,
    KEYBOARD_MOUSE_COMBO,
    VIDEO_GAME_CONSOLE,
)
from storescraper.product import Product
from storescraper.store_with_url_extensions import StoreWithUrlExtensions
from storescraper.utils import html_to_markdown, session_with_proxy


class InvasionGamer(StoreWithUrlExtensions):
    url_extensions = [
        ["componentes-pc/gabinetes", COMPUTER_CASE],
        ["procesadores", PROCESSOR],
        ["memorias-ram", RAM],
        ["placas-madres", MOTHERBOARD],
        ["componentes-pc/tarjetas-de-video", VIDEO_CARD],
        ["componentes-pc/ssd-y-almacenamiento", SOLID_STATE_DRIVE],
        ["componentes-pc/refrigeracion", CPU_COOLER],
        ["componentes-pc/fuentes-de-poder", POWER_SUPPLY],
        ["teclados", KEYBOARD],
        ["mouse", MOUSE],
        ["audifonos", HEADPHONES],
        ["accesorios-y-perifericos/sillas-y-escritorios", GAMING_CHAIR],
        ["accesorios-y-perifericos/kit-gamers", KEYBOARD_MOUSE_COMBO],
        ["accesorios-y-perifericos/consolas", VIDEO_GAME_CONSOLE],
        ["notebooks-1", NOTEBOOK],
        ["monitores", MONITOR],
    ]

    @classmethod
    def discover_urls_for_url_extension(cls, url_extension, extra_args=None):
        session = session_with_proxy(extra_args)
        page = 1

        while True:
            if page > 10:
                raise Exception(f"page overflow: {url_extension}")

            url_webpage = f"https://invasiongamer.com/{url_extension}?page={page}"
            print(url_webpage)
            response = session.get(url_webpage)
            soup = BeautifulSoup(response.text, "lxml")
            product_containers = soup.findAll("div", "product-block")

            if not product_containers:
                if page == 1:
                    logging.warning(f"Empty category: {url_extension}")
                break

            for container in product_containers:
                product_path = container.find("a")["href"]
                product_url = f"https://invasiongamer.com{product_path}"
                yield product_url

            page += 1

    @classmethod
    def products_for_url(cls, url, category=None, extra_args=None):
        print(url)
        session = session_with_proxy(extra_args)
        response = session.get(url)
        soup = BeautifulSoup(response.text, "lxml")
        name = soup.find("meta", {"property": "og:title"})["content"]
        key = soup.find("meta", {"property": "og:id"})["content"]
        price = Decimal(
            soup.find("meta", {"property": "product:price:amount"})["content"]
        )
        offer_price = (price * Decimal(0.95)).quantize(0)

        condition = (
            "https://schema.org/OpenBoxCondition"
            if "OPEN" in name.upper()
            else "https://schema.org/NewCondition"
        )
        description_tag = soup.find("div", "product-description")
        description = (
            html_to_markdown(description_tag.text) if description_tag else None
        )

        if "PREVENTA" in name.upper():
            stock = 0
        elif description and "ARRIBO" in description.upper():
            stock = 0
        else:
            stock_text = soup.find("meta", {"property": "product:availability"})[
                "content"
            ]
            stock = -1 if stock_text == "instock" else 0

        p = Product(
            name,
            cls.__name__,
            category,
            url,
            url,
            key,
            stock,
            price,
            offer_price,
            "CLP",
            sku=key,
            condition=condition,
            description=description,
        )

        return [p]
