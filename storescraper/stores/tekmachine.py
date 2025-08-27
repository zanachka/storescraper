from decimal import Decimal
import logging
from bs4 import BeautifulSoup
from storescraper.categories import *
from storescraper.product import Product
from storescraper.store_with_url_extensions import StoreWithUrlExtensions
from storescraper.utils import (
    cf_session_with_proxy,
    html_to_markdown,
    remove_words,
    session_with_proxy,
)


class Tekmachine(StoreWithUrlExtensions):
    preferred_discover_urls_concurrency = 3
    preferred_products_for_url_concurrency = 3

    url_extensions = [
        ["procesadores", PROCESSOR],
        ["placas-madres", MOTHERBOARD],
        ["memorias", RAM],
        ["discos-solidos", SOLID_STATE_DRIVE],
        ["tarjetas-de-video", VIDEO_CARD],
        ["fuentes-de-poder", POWER_SUPPLY],
        ["gabinetes", COMPUTER_CASE],
        ["audifonos", HEADPHONES],
        ["mouse", MOUSE],
        ["teclado", KEYBOARD],
        ["case-fan", CASE_FAN],
        ["cpu-cooling", CPU_COOLER],
        ["monitores", MONITOR],
        ["sistema-de-sonido", STEREO_SYSTEM],
        ["sillas-gamers", GAMING_CHAIR],
    ]

    @classmethod
    def discover_urls_for_url_extension(cls, url_extension, extra_args):
        session = cf_session_with_proxy(extra_args)
        session.headers["User-Agent"] = (
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
            "(KHTML, like Gecko) Chrome/62.0.3202.62 Safari/537.36"
        )
        product_urls = []
        page = 1

        while True:
            if page > 15:
                raise Exception("page overflow: " + url_extension)

            url_webpage = f"https://tekmachine.cl/product-category/{url_extension}/page/{page}/?stock_status=instock,onsale&_pjax=.main-page-wrapper"
            print(url_webpage)
            response = session.get(url_webpage)
            soup = BeautifulSoup(response.text, "lxml")
            product_containers = soup.findAll("div", "product-grid-item")

            if not product_containers:
                if page == 1:
                    logging.warning(f"Empty category: {url_extension}")
                break

            for container in product_containers:
                product_urls.append(container.find("a")["href"])

            page += 1

        return product_urls

    @classmethod
    def products_for_url(cls, url, category=None, extra_args=None):
        print(url)
        session = session_with_proxy(extra_args)
        session.headers["User-Agent"] = (
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
            "(KHTML, like Gecko) Chrome/62.0.3202.62 Safari/537.36"
        )
        response = session.get(url)
        soup = BeautifulSoup(response.text, "lxml")
        name = soup.find("span", "breadcrumb-last").text.strip()
        key = soup.find("link", {"rel": "shortlink"})["href"].split("p=")[1]
        sku_tag = soup.find("span", "sku")
        sku = sku_tag.text.strip()[:45] if sku_tag else None

        stock_tag = soup.find("p", "in-stock")
        if not stock_tag or "backorder" in stock_tag.text.lower():
            stock = 0
        else:
            stock = -1

        prices = soup.find("p", "price").findAll("span", "amount")
        normal_price = Decimal(remove_words(prices[0].text))

        if normal_price == 0:
            return []

        if len(prices) > 1:
            offer_price = Decimal(remove_words(prices[1].text))
        else:
            offer_price = normal_price

        picture_urls = [
            a["href"]
            for a in soup.find(
                "figure", "woocommerce-product-gallery__wrapper"
            ).find_all("a")
            if a["href"] != "#"
        ]
        description_tag = soup.find("div", {"id": "tab-description"})
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
            normal_price,
            offer_price,
            "CLP",
            sku=sku,
            part_number=sku,
            picture_urls=picture_urls,
            description=description,
        )

        return [p]
