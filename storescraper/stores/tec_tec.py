import logging
from decimal import Decimal
import validators

from bs4 import BeautifulSoup

from storescraper.categories import (
    NOTEBOOK,
    STORAGE_DRIVE,
    SOLID_STATE_DRIVE,
    POWER_SUPPLY,
    RAM,
    MOTHERBOARD,
    PROCESSOR,
    VIDEO_CARD,
    CPU_COOLER,
    KEYBOARD,
    MOUSE,
    HEADPHONES,
    TABLET,
    VIDEO_GAME_CONSOLE,
    MONITOR,
    WEARABLE,
)
from storescraper.product import Product
from storescraper.store_with_url_extensions import StoreWithUrlExtensions
from storescraper.utils import html_to_markdown, session_with_proxy, remove_words


class TecTec(StoreWithUrlExtensions):
    url_extensions = [
        ["notebooks", NOTEBOOK],
        ["componentes-para-pc/discos-duro", STORAGE_DRIVE],
        ["componentes-para-pc/discos-estado-solido", SOLID_STATE_DRIVE],
        ["componentes-para-pc/fuentes-de-poder", POWER_SUPPLY],
        ["componentes-para-pc/memoria-ram", RAM],
        ["componentes-para-pc/placas-madres", MOTHERBOARD],
        ["componentes-para-pc/procesadores", PROCESSOR],
        ["componentes-para-pc/tarjetas-de-video", VIDEO_CARD],
        ["componentes-para-pc/refrigeracion-cpu", CPU_COOLER],
        ["monitores", MONITOR],
        ["perifericos/teclados", KEYBOARD],
        ["perifericos/mouse", MOUSE],
        ["perifericos/headset-audifonos", HEADPHONES],
        ["tablets", TABLET],
        ["telefonos-y-dispositivos-inteligentes", WEARABLE],
        ["consolas-y-juegos", VIDEO_GAME_CONSOLE],
        ["open-box-y-usados", NOTEBOOK],
    ]

    @classmethod
    def get_session(cls, extra_args=None):
        session = session_with_proxy(extra_args)
        session.headers["user-agent"] = "curl/8.5.0"
        return session

    @classmethod
    def discover_urls_for_url_extension(cls, url_extension, extra_args=None):
        session = cls.get_session(extra_args)
        page = 1
        while True:
            if page > 10:
                raise Exception("page overflow: " + url_extension)

            if page > 1:
                url_webpage = "https://tectec.cl/categoria/{}/page" "/{}/".format(
                    url_extension, page
                )
            else:
                url_webpage = "https://tectec.cl/categoria/{}/".format(url_extension)

            print(url_webpage)
            response = session.get(url_webpage, timeout=60)
            soup = BeautifulSoup(response.text, "lxml")
            product_containers = soup.findAll("div", "product-wrapper")

            if not product_containers:
                if page == 1:
                    print(url_webpage)
                    logging.warning("Empty category: " + url_extension)
                break
            for container in product_containers:
                product_url = container.find("a")["href"]
                yield product_url
            page += 1

    @classmethod
    def products_for_url(cls, url, category=None, extra_args=None):
        print(url)
        session = cls.get_session(extra_args)
        response = session.get(url, timeout=60)
        soup = BeautifulSoup(response.text, "lxml")
        name = soup.find("h1", "product_title").text.strip()
        sku = soup.find("link", {"rel": "shortlink"})["href"].split("p=")[1]

        price_tag = soup.find("p", "price")

        if not price_tag.text.strip():
            return []
        if price_tag.find("ins"):
            offer_price = Decimal(remove_words(price_tag.find("ins").text))
        else:
            offer_price = Decimal(remove_words(price_tag.find("bdi").text))

        normal_price = Decimal(offer_price * Decimal("1.04")).quantize(0)

        if soup.find("p", "stock out-of-stock"):
            stock = 0
        else:
            stock_tag = soup.find("input", {"name": "quantity"})
            if not stock_tag:
                stock = 0
            elif "max" in stock_tag:
                stock = int(stock_tag["max"])
            else:
                stock = int(stock_tag["value"])

        picture_urls = [
            tag["src"]
            for tag in soup.find("div", "woocommerce-product-gallery").findAll("img")
            if validators.url(tag["src"])
        ]
        description = html_to_markdown(soup.find("div", {"id": "tab-description"}).text)

        p = Product(
            name,
            cls.__name__,
            category,
            url,
            url,
            sku,
            stock,
            normal_price,
            offer_price,
            "CLP",
            sku=sku,
            picture_urls=picture_urls,
            description=description,
        )

        return [p]
