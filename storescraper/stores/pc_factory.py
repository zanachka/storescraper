import logging
import re
from decimal import Decimal


from storescraper.categories import (
    NOTEBOOK,
    VIDEO_CARD,
    PROCESSOR,
    MONITOR,
    TELEVISION,
    MOTHERBOARD,
    RAM,
    STORAGE_DRIVE,
    SOLID_STATE_DRIVE,
    POWER_SUPPLY,
    COMPUTER_CASE,
    CPU_COOLER,
    TABLET,
    PRINTER,
    CELL,
    EXTERNAL_STORAGE_DRIVE,
    USB_FLASH_DRIVE,
    MEMORY_CARD,
    PROJECTOR,
    VIDEO_GAME_CONSOLE,
    STEREO_SYSTEM,
    ALL_IN_ONE,
    MOUSE,
    OPTICAL_DRIVE,
    KEYBOARD,
    KEYBOARD_MOUSE_COMBO,
    WEARABLE,
    UPS,
    SPLIT_AIR_CONDITIONER,
    GAMING_CHAIR,
    CASE_FAN,
    HEADPHONES,
    DISH_WASHER,
    PRINTER_SUPPLY,
    CALCULATOR,
)
from storescraper.product import Product
from storescraper.store_with_url_extensions import StoreWithUrlExtensions
from storescraper.utils import html_to_markdown


class PcFactory(StoreWithUrlExtensions):
    url_extensions = [
        ["999", ALL_IN_ONE],
        ["735", NOTEBOOK],
        ["411", STORAGE_DRIVE],
        ["266", RAM],
        ["994", TABLET],
        ["418", KEYBOARD_MOUSE_COMBO],
        ["1301", KEYBOARD],
        ["1302", MOUSE],
        ["5", CELL],
        ["936", WEARABLE],
        ["1007", GAMING_CHAIR],
        ["438", VIDEO_GAME_CONSOLE],
        ["38", UPS],
        ["995", MONITOR],
        ["46", PROJECTOR],
        ["422", EXTERNAL_STORAGE_DRIVE],
        ["904", EXTERNAL_STORAGE_DRIVE],
        ["218", USB_FLASH_DRIVE],
        ["48", MEMORY_CARD],
        ["340", STORAGE_DRIVE],
        ["585", SOLID_STATE_DRIVE],
        ["421", STORAGE_DRIVE],
        ["932", STORAGE_DRIVE],
        ["262", PRINTER],
        ["789", TELEVISION],
        ["797", STEREO_SYSTEM],
        ["889", STEREO_SYSTEM],
        ["891", STEREO_SYSTEM],
        ["850", HEADPHONES],
        ["1107", DISH_WASHER],
        ["1021", SPLIT_AIR_CONDITIONER],
        ["272", PROCESSOR],
        ["292", MOTHERBOARD],
        ["112", RAM],
        ["100", RAM],
        ["334", VIDEO_CARD],
        ["326", COMPUTER_CASE],
        ["54", POWER_SUPPLY],
        ["647", CASE_FAN],
        ["648", CPU_COOLER],
        ["286", OPTICAL_DRIVE],
        ["12,442,444,725,973", PRINTER_SUPPLY],
        ["823", CALCULATOR],
    ]

    @classmethod
    def discover_urls_for_url_extension(cls, url_extension, extra_args=None):
        session = cls.get_session(extra_args)

        page = 0
        while True:
            if page > 10:
                raise Exception("page overflow: " + url_extension)

            url_webpage = f"https://api.pcfactory.cl/pcfactory-services-catalogo/v1/catalogo/productos/query?page={page}&size=100&categorias={url_extension}"
            print(url_webpage)
            response = session.get(url_webpage)
            json_data = response.json()
            products_data = json_data["content"]["items"]

            if not products_data:
                if page == 0:
                    logging.warning(f"Empty category: {url_extension}")

                break

            for product_entry in products_data:
                product_url = (
                    "https://www.pcfactory.cl/producto/" + product_entry["slug"]
                )
                yield product_url
            page += 1

    @classmethod
    def products_for_url(cls, url, category=None, extra_args=None):
        print(url)
        session = cls.get_session(extra_args)
        product_id_match = re.search(r"/producto/(\d+)", url)
        product_id = product_id_match.groups()[0]
        # Specs
        res = session.get(
            f"https://api.pcfactory.cl/pcfactory-services-catalogo/v1/catalogo/productos/{product_id}"
        )

        if res.status_code == 404:
            return []

        product_data = res.json()
        sku = str(product_data["id"])
        part_number = product_data["partNumber"]

        if part_number:
            part_number = part_number.strip()

        name = product_data["nombre"]
        description = (
            html_to_markdown(product_data["descripcion"])
            if product_data["descripcion"]
            else ""
        )

        for spec_group in product_data["especificaciones"]:
            for entry in spec_group["detalle"]:
                description += f"\n{entry['nombre']}: {entry['valor']}"

        # Precio
        res = session.get(
            f"https://api.pcfactory.cl/pcfactory-services-catalogo/v1/catalogo/productos/{product_id}/precio"
        )
        price_data = res.json()

        normal_price = Decimal(price_data["precio"]["normal"])

        if price_data["precio"].get("bancoEstado", None):
            offer_price = Decimal(price_data["precio"]["bancoEstado"])
        else:
            offer_price = Decimal(price_data["precio"]["efectivo"])

        # Stock
        res = session.get(
            f"https://api.pcfactory.cl/pcfactory-services-catalogo/v1/catalogo/productos/{product_id}/stock"
        )
        stock_data = res.json()
        stock = 0
        for zona in stock_data["disponibilidad"]:
            for sucursal in zona["sucursales"]:
                stock += int(sucursal["aproximado"].replace("+", ""))

        # Pictures
        res = session.get(
            f"https://api.pcfactory.cl/pcfactory-services-catalogo/v1/catalogo/productos/{product_id}/imagenes"
        )
        pictures_data = res.json()
        picture_urls = [x["sizes"]["0"] for x in pictures_data["imagenes"]]

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
            part_number=part_number,
            picture_urls=picture_urls,
            description=description,
        )
        return [p]
