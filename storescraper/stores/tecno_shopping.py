from bs4 import BeautifulSoup
from decimal import Decimal
import json
from storescraper.product import Product
from storescraper.store_with_url_extensions import StoreWithUrlExtensions
from storescraper.utils import (
    html_to_markdown,
    remove_words,
    session_with_proxy,
)
from storescraper.categories import (
    ACCESORIES,
    EXTERNAL_STORAGE_DRIVE,
    ALL_IN_ONE,
    NOTEBOOK,
    TABLET,
    MONITOR,
    PRINTER,
)


class TecnoShopping(StoreWithUrlExtensions):
    url_extensions = [
        ["accesorios", ACCESORIES],
        ["almacenamiento", EXTERNAL_STORAGE_DRIVE],
        ["computacion/todo-en-uno", ALL_IN_ONE],
        ["computacion/notebooks", NOTEBOOK],
        ["computacion/tablets", TABLET],
        ["computacion/monitores", MONITOR],
        ["impresoras", PRINTER],
    ]

    @classmethod
    def discover_urls_for_url_extension(cls, url_extension, extra_args):
        product_urls = []
        session = session_with_proxy(extra_args)
        session.headers["User-Agent"] = (
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36"
        )
        page = 1

        while True:
            url = f"https://www.tecnoshopping.cl/{url_extension}/page/{page}/"
            print(url)
            response = session.get(url)

            if response.status_code == 404:
                if page == 1:
                    raise Exception("Invalid section: " + url)
                break

            soup = BeautifulSoup(response.text, "lxml")
            products = soup.find("div", "content-area").find_all("li", "product")

            for product in products:
                product_urls.append(product.find("a")["href"])

            page += 1

        return product_urls

    @classmethod
    def products_for_url(cls, url, category=None, extra_args=None):
        print(url)
        session = session_with_proxy(extra_args)
        session.headers["User-Agent"] = (
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36"
        )
        soup = BeautifulSoup(session.get(url).text, "lxml")
        data_entries = json.loads(
            soup.find("script", {"type": "application/ld+json"}).text
        )["@graph"]
        product_data = None

        for entry in data_entries:
            if entry["@type"] == "Product":
                product_data = entry

        name = product_data["name"]
        sku = product_data["sku"]
        offer = product_data["offers"]
        prices_container = soup.find("div", "summary entry-summary")
        prices_container.find("div", "shoptimizer-product-prevnext").decompose()
        offer_price = Decimal(
            remove_words(
                prices_container.find("p", "price_transferencia").text.split()[0]
            )
        )
        normal_price = Decimal(
            remove_words(prices_container.find("p", "price_rebajado").text.split()[0])
        )
        key = soup.find("link", {"rel": "shortlink"})["href"].split("?p=")[-1]
        stock = -1 if offer["availability"] == "https://schema.org/InStock" else 0
        description = html_to_markdown(
            soup.find("div", "woocommerce-Tabs-panel--description").text
        )
        picture_urls = [img["url"] for img in product_data["image"]]

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
