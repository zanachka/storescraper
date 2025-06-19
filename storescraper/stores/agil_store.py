from decimal import Decimal
import logging
from bs4 import BeautifulSoup
from storescraper.categories import (
    MONITOR,
    MOUSE,
    NOTEBOOK,
    POWER_SUPPLY,
    PROCESSOR,
    STORAGE_DRIVE,
    TABLET,
    PRINTER,
    ALL_IN_ONE,
    KEYBOARD_MOUSE_COMBO,
    EXTERNAL_STORAGE_DRIVE,
    PRINTER_SUPPLY,
    HEADPHONES,
    KEYBOARD,
    MOTHERBOARD,
    VIDEO_CARD,
)
from storescraper.product import Product
from storescraper.store_with_url_extensions import StoreWithUrlExtensions
from storescraper.utils import remove_words, html_to_markdown


class AgilStore(StoreWithUrlExtensions):
    url_extensions = [
        ["5507", PRINTER],  # Impresoras
        ["5553", NOTEBOOK],  # Laptop
        ["5554", ALL_IN_ONE],  # All in One
        ["5558", TABLET],  # Tablet
        ["5570", KEYBOARD_MOUSE_COMBO],  # Kit Mouse y Teclado
        ["5572", MOUSE],  # Mouse
        ["5593", MONITOR],  # Monitor
        ["5663", PROCESSOR],  # Procesador
        ["5601", STORAGE_DRIVE],  # Disco Duro Interno
        ["5602", EXTERNAL_STORAGE_DRIVE],  # Disco Duro Externo
        ["5606", POWER_SUPPLY],  # Fuente Poder
        ["5530", PRINTER_SUPPLY],  # Toner
        ["5531", PRINTER_SUPPLY],  # Cartuchos de Tinta
        ["6146", HEADPHONES],  # Audífonos
        ["5573", KEYBOARD],  # Teclados
        ["5581", MOTHERBOARD],  # Placas madre
        ["5609", VIDEO_CARD],  # Tarjetas de video
    ]

    @classmethod
    def discover_urls_for_url_extension(cls, url_extension, extra_args=None):
        session = cls.get_session(extra_args)
        seen_product_urls = set()
        url_webpage = (
            "https://www.agilstore.cl/productos.php?ver=productos&id={}".format(
                url_extension
            )
        )
        print(url_webpage)
        response = session.get(url_webpage, verify=False)
        soup = BeautifulSoup(response.text, "lxml")
        product_containers = soup.findAll("div", "product")

        if not product_containers:
            logging.warning("empty category: " + url_extension)

        for container in product_containers:
            product_url = "https://www.agilstore.cl/" + container.find("a")["href"]
            if product_url not in seen_product_urls:
                seen_product_urls.add(product_url)
                yield product_url

    @classmethod
    def products_for_url(cls, url, category=None, extra_args=None):
        print(url)
        session = cls.get_session(extra_args)
        response = session.get(url, verify=False)
        soup = BeautifulSoup(response.text, "lxml")
        name = soup.find("h2", "product-name").text.strip()
        key = soup.find("input", {"name": "id_producto"})["value"]
        stock = -1
        price = Decimal(remove_words(soup.find("h3", "product-price").contents[-1]))
        sku_label = soup.find("strong", text="Código")
        sku = sku_label.next.next[2:]
        pn_label = soup.find("strong", text="Part Number Fabricante")
        part_number = pn_label.next.next[2:]
        img_tag = soup.find("div", {"id": "product-main-img"}).find("img")
        picture_urls = [img_tag["src"]] if img_tag else None
        description = html_to_markdown(str(soup.find("div", "product-details")))

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
        yield p
