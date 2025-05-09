from bs4 import BeautifulSoup
from decimal import Decimal
import json
from storescraper.product import Product
from storescraper.store_with_url_extensions import StoreWithUrlExtensions
from storescraper.utils import html_to_markdown, remove_words, session_with_proxy
from storescraper.categories import (
    GAMING_CHAIR,
    EXTERNAL_STORAGE_DRIVE,
    USB_FLASH_DRIVE,
    VIDEO_CARD,
    ACCESORIES,
    MONITOR,
    NOTEBOOK,
    MOUSE,
    KEYBOARD,
)


class CentralTech(StoreWithUrlExtensions):
    url_extensions = [
        ["mobiliario", GAMING_CHAIR],
        ["componentes/almacenamiento-externo/discos-externos", EXTERNAL_STORAGE_DRIVE],
        ["componentes/almacenamiento-externo/pendrives", USB_FLASH_DRIVE],
        ["componentes/tarjetas-de-video", VIDEO_CARD],
        ["conectividad-y-redes/adaptadores", ACCESORIES],
        ["monitores-y-proyectores/monitores-profesionales", MONITOR],
        ["portatiles-y-all-in-one/accesorios-notebook", ACCESORIES],
        ["portatiles-y-all-in-one/notebooks", NOTEBOOK],
        ["perifericos/mouse", MOUSE],
        ["perifericos/teclados", KEYBOARD],
    ]

    @classmethod
    def discover_urls_for_url_extension(cls, url_extension, extra_args):
        product_urls = []
        session = session_with_proxy(extra_args)
        page = 1

        while True:
            url = f"https://centraltech.cl/{url_extension}/page/{page}"
            print(url)
            response = session.get(url)

            if response.status_code == 404:
                if page == 1:
                    raise Exception("Invalid section: " + url)
                break

            soup = BeautifulSoup(response.text, "lxml")
            products = soup.findAll("div", "product")

            for product in products:
                product_url = product.find("a")["href"]
                product_urls.append(product_url)

            page += 1

        return product_urls

    @classmethod
    def products_for_url(cls, url, category=None, extra_args=None):
        print(url)
        session = session_with_proxy(extra_args)
        soup = BeautifulSoup(session.get(url).text, "lxml")

        prices = BeautifulSoup(
            soup.find("span", "price").find("div", "precio-info-raw").text, "lxml"
        ).find_all("bdi")
        normal_price = Decimal(remove_words(prices[0].text))
        offer_price = Decimal(remove_words(prices[1].text))

        product_data = json.loads(
            soup.find_all("script", {"type": "application/ld+json"})[1].text
        )
        name = product_data["name"]
        sku = product_data["sku"]
        key = soup.find("link", {"rel": "shortlink"})["href"].split("?p=")[-1]

        assert len(product_data["offers"]) == 1

        offer = product_data["offers"][0]
        stock = -1 if offer["availability"] == "http://schema.org/InStock" else 0
        description = html_to_markdown(product_data["description"])
        gallery = soup.find("div", "electron-product-gallery-main-slider")

        picture_urls = (
            [img["data-src"] for img in gallery.find_all("div", "swiper-slide")]
            if gallery
            else [product_data["image"]]
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
            offer_price,
            "CLP",
            sku=sku,
            part_number=sku,
            description=description,
            picture_urls=picture_urls,
        )

        return [p]
