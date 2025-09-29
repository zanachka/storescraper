import json
import logging
from decimal import Decimal

from bs4 import BeautifulSoup

from storescraper.categories import (
    CASE_FAN,
    HEADPHONES,
    GAMING_CHAIR,
    KEYBOARD,
    MICROPHONE,
    MONITOR,
    COMPUTER_CASE,
    MOUSE,
    ACCESORIES,
    POWER_SUPPLY,
    CPU_COOLER,
    SOLID_STATE_DRIVE,
)
from storescraper.product import Product
from storescraper.store import Store
from storescraper.utils import html_to_markdown, session_with_proxy


class Valrod(Store):
    @classmethod
    def categories(cls):
        return [
            GAMING_CHAIR,
            COMPUTER_CASE,
            MONITOR,
            POWER_SUPPLY,
            CPU_COOLER,
            CASE_FAN,
            MOUSE,
            KEYBOARD,
            HEADPHONES,
            MICROPHONE,
            ACCESORIES,
        ]

    @classmethod
    def discover_urls_for_category(cls, category, extra_args=None):
        url_extensions = [
            ["sillas-y-sofas", GAMING_CHAIR],
            ["gabinetes", COMPUTER_CASE],
            ["monitores", MONITOR],
            ["hardware/fuentes-de-poder", POWER_SUPPLY],
            ["hardware/disipadores", CPU_COOLER],
            ["hardware/enfriadores-liquidos", CPU_COOLER],
            ["hardware/ventiladores", CASE_FAN],
            ["hardware/discos-ssd", SOLID_STATE_DRIVE],
            ["perifericos-y-accesorios/mouse-y-mousepads", MOUSE],
            ["perifericos-y-accesorios/teclados", KEYBOARD],
            ["perifericos-y-accesorios/audifonos", HEADPHONES],
            ["perifericos-y-accesorios/accesorios", MICROPHONE],
            ["hogar/cocina", ACCESORIES],
        ]
        session = session_with_proxy(extra_args)
        product_urls = []

        for url_extension, local_category in url_extensions:
            if local_category != category:
                continue

            page = 1

            while True:
                if page > 10:
                    raise Exception("page overflow: " + url_extension)

                url_webpage = "https://valrod.cl/{}?page={}".format(url_extension, page)
                print(url_webpage)
                response = session.get(url_webpage)
                soup = BeautifulSoup(response.text, "lxml")
                product_container = soup.findAll("div", "product-block__wrapper")

                if not product_container:
                    if page == 1:
                        logging.warning("Empty category: " + url_extension)
                    break

                for container in product_container:
                    product_url = container.find("a")["href"]
                    product_urls.append("https://valrod.cl" + product_url)

                page += 1

        return product_urls

    @classmethod
    def products_for_url(cls, url, category=None, extra_args=None):
        print(url)
        session = session_with_proxy(extra_args)
        response = session.get(url)
        soup = BeautifulSoup(response.text, "lxml")
        name = soup.find("h1", "product-page__title").text
        key = soup.find("form", {"name": "buy"})["action"].split("/")[-1]
        scripts = json.loads(soup.find("script", {"type": "application/ld+json"}).text)
        product_data = None

        for script in scripts:
            if script["@type"] == "Product":
                product_data = script

        if "sku" in product_data:
            sku = product_data.get("sku")
        else:
            sku = json.loads(soup.find("script", "product-attributes-json").text)[
                "info"
            ]["variant"].get("sku")

        if sku == "":
            sku = None

        offer = product_data["offers"]
        stock = -1 if offer["availability"] == "http://schema.org/InStock" else 0
        price = Decimal(offer["price"])
        picture_urls = list(
            set(
                tag["src"].split("?")[0]
                for tag in soup.find(
                    "swiper-slider", "product-gallery__carousel--main"
                ).find_all(
                    "img", "product-gallery__image product-gallery__image--hidden"
                )
            )
        )
        upper_name = name.upper()

        if "CAJA ABIERTA" in upper_name or "SEGUNDA SELECCION" in upper_name:
            condition = "https://schema.org/RefurbishedCondition"
        else:
            condition = "https://schema.org/NewCondition"

        description_tag = soup.find("div", "product-details product-details--table")
        description = (
            html_to_markdown(description_tag.text) if description_tag else None
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
            condition=condition,
            description=description,
        )

        return [p]
