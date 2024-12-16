import logging
import re
import time

from decimal import Decimal
from bs4 import BeautifulSoup

from storescraper.categories import (
    MONITOR,
    STORAGE_DRIVE,
    RAM,
    UPS,
    SOLID_STATE_DRIVE,
    EXTERNAL_STORAGE_DRIVE,
    MEMORY_CARD,
)
from storescraper.product import Product
from storescraper.store_with_url_extensions import StoreWithUrlExtensions
from storescraper.utils import html_to_markdown, remove_words, session_with_proxy


class VideoVision(StoreWithUrlExtensions):
    url_extensions = [
        ["monitores-accesorios-cctv", MONITOR],
        ["discos-duros-accesorios", STORAGE_DRIVE],
        ["discos-duros-ssd-internos", SOLID_STATE_DRIVE],
        ["disco-duro-ssd-externo", EXTERNAL_STORAGE_DRIVE],
        ["disco-duro-videovigilancia", STORAGE_DRIVE],
        ["memorias", RAM],
        ["memorias-notebook", RAM],
        ["memorias-pc", RAM],
        ["micro-sd", MEMORY_CARD],
        ["ups", UPS],
    ]

    @classmethod
    def discover_urls_for_url_extension(cls, url_extension, extra_args=None):
        session = session_with_proxy(extra_args)
        product_urls = []
        page = 1
        while True:
            if page > 10:
                raise Exception("page overflow: " + url_extension)
            url_webpage = (
                "https://videovision.cl/categoria-producto/"
                "{}/page/{}/".format(url_extension, page)
            )
            print(url_webpage)
            response = session.get(url_webpage)
            soup = BeautifulSoup(response.text, "lxml")
            product_containers = soup.findAll("li", "product")

            if not product_containers:
                if page == 1:
                    logging.warning("Empty category: " + url_extension)
                break
            for container in product_containers:
                product_url = container.find("a")["href"]
                product_urls.append(product_url)
            page += 1
        return product_urls

    @classmethod
    def products_for_url(cls, url, category=None, extra_args=None):
        print(url)
        session = session_with_proxy(extra_args)
        response = session.get(url)

        if response.status_code == 404:
            return []

        soup = BeautifulSoup(response.text, "html5lib")
        tries = 0

        while tries < 3:
            key_tag = soup.find("link", {"rel": "shortlink"})

            if key_tag:
                break

            tries += 1
            time.sleep(10)

        if not key_tag:
            return []

        key = key_tag["href"].split("p=")[-1]
        name = soup.find("h2", "product_title").text
        sku = soup.find("span", "sku").text
        part_number = soup.find(
            "div", "description woocommerce-product-details__short-description"
        ).text.strip()
        stock = -1 if soup.find("button", {"name": "add-to-cart"}) else 0
        price = soup.find("div", "product-summary-wrap").find("p", "price").find("bdi")

        if not price:
            return []
        else:
            price = (Decimal(remove_words(price.text)) * Decimal("1.19")).quantize(0)

        picture_urls = []

        for img in soup.find("div", "woocommerce-product-gallery__wrapper").findAll(
            "img"
        ):
            picture = img.get("href")

            if picture:
                picture_urls.append(picture)

        description = html_to_markdown(soup.find("div", {"id": "tab-description"}).text)

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
            part_number=part_number,
            picture_urls=picture_urls,
            description=description,
        )

        return [p]
