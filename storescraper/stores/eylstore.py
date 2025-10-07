import json
import logging
from decimal import Decimal
import re

from bs4 import BeautifulSoup

from storescraper.categories import (
    COMPUTER_CASE,
    CPU_COOLER,
    HEADPHONES,
    KEYBOARD,
    MONITOR,
    MOTHERBOARD,
    MOUSE,
    POWER_SUPPLY,
    PROCESSOR,
    RAM,
    SOLID_STATE_DRIVE,
    VIDEO_CARD,
)
from storescraper.product import Product
from storescraper.store_with_url_extensions import StoreWithUrlExtensions
from storescraper.utils import html_to_markdown, session_with_proxy


class Eylstore(StoreWithUrlExtensions):
    preferred_products_for_url_concurrency = 3

    url_extensions = [
        ["procesadores", PROCESSOR],
        ["gabinetes", COMPUTER_CASE],
        ["placas-madres", MOTHERBOARD],
        ["fuentes-de-poder", POWER_SUPPLY],
        ["tarjetas-de-video", VIDEO_CARD],
        ["tarjetas-de-video", SOLID_STATE_DRIVE],
        ["memorias-ram", RAM],
        ["refrigeracion", CPU_COOLER],
        ["teclados", KEYBOARD],
        ["mouse", MOUSE],
        ["audifonos", HEADPHONES],
        ["monitores", MONITOR],
    ]

    @classmethod
    def discover_urls_for_url_extension(cls, url_extension, extra_args):
        session = session_with_proxy(extra_args)
        session.headers["Content-Type"] = (
            "application/x-www-form-urlencoded; charset=UTF-8"
        )
        product_urls = []
        page = 1

        while True:
            url = f"https://eylstore.cl/categorias/{url_extension}?page={page}"
            print(url)
            response = session.get(url)
            print(response)
            soup = BeautifulSoup(response.text, "lxml")
            product_containers = soup.find_all("div", "grid")
            product_links = []

            for product_container in product_containers:
                for a in product_container.find_all(
                    "a", href=re.compile(r"^/producto/")
                ):
                    product_links.append(a["href"])

            if not product_links:
                if page == 1:
                    logging.warning(f"Empty category: {url_extension}")
                break

            for product_link in product_links:
                product_urls.append(f"https://www.eylstore.cl{product_link}")

            page += 1

        return product_urls

    @classmethod
    def products_for_url(cls, url, category=None, extra_args=None):
        print(url)
        session = session_with_proxy(extra_args)
        response = session.get(url)
        soup = BeautifulSoup(response.text, "lxml")
        scripts = soup.find_all("script")
        pattern = re.compile(r'"product"\s*:\s*\{.*?"id"\s*:\s*"?(\d+)"?', re.DOTALL)

        for script in scripts:
            text = script.string or script.get_text()

            for t in (text, text.replace('\\"', '"').replace("\\n", " ")):
                for m in pattern.finditer(t):
                    key = m.group(1)

        product_data = json.loads(
            soup.find("script", {"type": "application/ld+json"}).text
        )

        name = product_data["name"]
        offer = product_data["offers"]
        offer_price = Decimal(offer["price"])
        normal_price = Decimal(Decimal(1.05) * offer_price).quantize(0)
        sku = product_data.get("sku")
        description = html_to_markdown(product_data["description"])
        picture_urls = product_data["image"]

        stock_endpoint = f"https://www.eylstore.cl/api/productos/{key}/stock"
        stock_response = session.get(stock_endpoint).json()
        stock = 0

        for _, v in stock_response.items():
            stock += v

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
            part_number=sku,
            description=description,
        )

        return [p]
