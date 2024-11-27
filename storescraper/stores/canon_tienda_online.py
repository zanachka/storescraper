from bs4 import BeautifulSoup
from decimal import Decimal
import json
import re
from storescraper.product import Product
from storescraper.store_with_url_extensions import StoreWithUrlExtensions
from storescraper.utils import session_with_proxy, html_to_markdown, remove_words
from storescraper.categories import PRINTER, PRINTER_SUPPLY


class CanonTiendaOnline(StoreWithUrlExtensions):
    url_extensions = [
        ["146501", PRINTER],  # Impresoras y Multifuncionales Tinta
        ["59581", PRINTER],  # Impresoras Portátiles
        ["59509", PRINTER],  # Impresoras y Multifuncionales Láser
        ["147513", PRINTER],  # Impresoras Formato Ancho
        ["59551", PRINTER_SUPPLY],  # Tinta
        ["59582", PRINTER_SUPPLY],  # Suministros Impresoras Portátiles
        ["59550", PRINTER_SUPPLY],  # Toner
        ["168502", PRINTER_SUPPLY],  # Toner Caja Dañada
    ]

    @classmethod
    def discover_urls_for_url_extension(cls, url_extension, extra_args):
        product_urls = []
        session = session_with_proxy(extra_args)
        index = 0
        page_size = 72

        while True:
            if index > 1000:
                raise Exception("Page overflow")

            body = {"pageSize": page_size, "beginIndex": index, "storeId": 12351}
            url = f"https://www.canontiendaonline.cl/ProductListingView?categoryId={url_extension}"
            print(url, index)

            response = session.post(url, body)
            soup = BeautifulSoup(response.text, "lxml")
            products = soup.find("div", "product_listing_container").findAll(
                "div", "product"
            )

            if not products:
                break

            for product in products:
                product_urls.append(
                    f"https://www.canontiendaonline.cl{product.find('a')['href']}"
                )

            index += page_size

        return product_urls

    @classmethod
    def products_for_url(cls, url, category=None, extra_args=None):
        print(url)
        session = session_with_proxy(extra_args)
        soup = BeautifulSoup(session.get(url).text, "lxml")
        entry_params = soup.find("input", {"id": "catEntryParams"})["value"]

        key = re.search(r"id:\s*'(\d+)'", entry_params).group(1)
        name = soup.find("span", {"itemprop": "name"}).text
        price = Decimal(remove_words(soup.find("span", {"itemprop": "price"}).text))
        description = soup.find("p", {"itemprop": "description"}).text
        stock = (
            -1
            if soup.find("span", {"itemprop": "availability"}).text.strip()
            == "Disponible"
            else 0
        )
        sku = soup.find("span", "sku").text.split("SKU")[1].strip()
        picture_urls = [
            f"https://www.canontiendaonline.cl{a.find('img')['src']}"
            for a in soup.findAll("a", "launch-prod-view")
        ]

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
            description=description,
            picture_urls=picture_urls,
        )

        return [p]
