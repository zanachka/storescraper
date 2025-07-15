import re
from decimal import Decimal
import json
import logging
from bs4 import BeautifulSoup
from storescraper.categories import (
    ALL_IN_ONE,
    MONITOR,
    NOTEBOOK,
    PRINTER,
    RAM,
    SOLID_STATE_DRIVE,
    TABLET,
    TELEVISION,
    MOUSE,
    VIDEO_CARD,
    PROCESSOR,
    MOTHERBOARD,
    POWER_SUPPLY,
    COMPUTER_CASE,
    CPU_COOLER,
    PRINTER_SUPPLY,
    PROJECTOR,
    HEADPHONES,
    UPS,
)
from storescraper.product import Product
from storescraper.store_with_url_extensions import StoreWithUrlExtensions
from storescraper.utils import (
    get_price_from_price_specification,
    session_with_proxy,
    remove_words,
)


class NoeComputacion(StoreWithUrlExtensions):
    preferred_products_for_url_concurrency = 3

    url_extensions = [
        ["256", NOTEBOOK],
        ["147", SOLID_STATE_DRIVE],
        ["223", RAM],
        ["245", PROCESSOR],
        ["246", MOTHERBOARD],
        ["247", VIDEO_CARD],
        ["248", POWER_SUPPLY],
        ["262", COMPUTER_CASE],
        ["264", CPU_COOLER],
        ["61", NOTEBOOK],
        ["238", ALL_IN_ONE],
        ["252", TABLET],
        ["241", PRINTER],
        ["242", PRINTER_SUPPLY],
        ["184", MONITOR],
        ["189", PROJECTOR],
        ["243", MOUSE],
        ["244", HEADPHONES],
        ["274", UPS],
        ["276", TELEVISION],
    ]

    @classmethod
    def discover_urls_for_url_extension(cls, url_extension, extra_args):
        session = session_with_proxy(extra_args)
        session.headers["user-agent"] = (
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
            "(KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36"
        )
        page = 1

        while True:
            if page > 12:
                raise Exception("Page overflow: " + url_extension)

            url_webpage = (
                "https://noecomputacion.com/tienda/page/{}/"
                "?filter_cat={}&_pjax=.site-content".format(page, url_extension)
            )
            print(url_webpage)
            response = session.get(url_webpage)
            soup = BeautifulSoup(response.text, "lxml")

            if response.status_code == 404:
                if page == 1:
                    logging.warning("Empty category: " + url_extension)

                break

            product_containers = soup.findAll("div", "product")

            for container in product_containers:
                product_url = container.find("a")["href"]
                yield product_url

            page += 1

    @classmethod
    def products_for_url(cls, url, category=None, extra_args=None):
        print(url)
        session = session_with_proxy(extra_args)
        session.headers["user-agent"] = (
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
            "(KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36"
        )
        response = session.get(url, timeout=60)
        soup = BeautifulSoup(response.text, "lxml")

        key = soup.find("link", {"rel": "shortlink"})["href"].split("p=")[1]

        json_data = json.loads(
            soup.findAll("script", {"type": "application/ld+json"})[-1].text
        )

        for entry in json_data["@graph"]:
            if entry["@type"] == "Product":
                product_data = entry

                break
        else:
            raise Exception("No JSON product data found")

        name = product_data["name"][:250]
        sku = str(product_data["sku"])
        description = product_data["description"]
        normal_price = get_price_from_price_specification(product_data)

        offer_price_match = re.search(r"\$([\d|.]+)", description)

        if offer_price_match:
            offer_price_text = offer_price_match.groups()[0]
            offer_price = Decimal(remove_words(offer_price_text))
        else:
            offer_price = normal_price

        if offer_price > Decimal(100000000) or normal_price > Decimal(100000000):
            return []

        qty_input = soup.find("input", "input-text qty text")

        if qty_input:
            if qty_input["max"]:
                stock = int(qty_input["max"])
            else:
                stock = -1
        else:
            if soup.find("button", "single_add_to_cart_button"):
                stock = 1
            else:
                stock = 0

        picture_urls = [
            x["data-src"] for x in soup.findAll("img", "attachment-woocommerce_single")
        ]

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
