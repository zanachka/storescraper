import logging

import validators
from bs4 import BeautifulSoup
from decimal import Decimal

from storescraper.categories import (
    TELEVISION,
    STEREO_SYSTEM,
    HEADPHONES,
    SPACE_HEATER,
    REFRIGERATOR,
    WASHING_MACHINE,
    DISH_WASHER,
    VACUUM_CLEANER,
    OVEN,
    CELL,
    WEARABLE,
    NOTEBOOK,
    TABLET,
    MOUSE,
    GAMING_CHAIR,
    EXTERNAL_STORAGE_DRIVE,
    PRINTER,
    VIDEO_GAME_CONSOLE,
    WATER_HEATER,
    STOVE,
    SPLIT_AIR_CONDITIONER,
    PRINTER_SUPPLY,
    ACCESORIES,
    ELECTRIC_GRILL,
    IRON,
    HAIR_CARE,
)
from storescraper.product import Product
from storescraper.store import Store
from storescraper.utils import html_to_markdown, session_with_proxy
from storescraper import banner_sections as bs


class Abc(Store):
    ajax_resources = [
        ["celulares", CELL, "Tecnología / Celulares"],
        ["smartphones", CELL, "Tecnología / Celulares / Smartphones"],
        ["smartwatch", WEARABLE, "Tecnología / Celulares / Smartwatch"],
        [
            "accesorios-telefonos",
            HEADPHONES,
            "Tecnología / Celulares / Accesorios Teléfonos",
        ],
        ["ver-todo-celulares", CELL, "Tecnología / Celulares / Ver todo Celulares"],
        ["televisores", TELEVISION, "Tecnología / Televisores"],
        ["smart-tv", TELEVISION, "Tecnología / Televisores / Smart TV"],
        ["soundbar", STEREO_SYSTEM, "Tecnología / Televisores / Soundbar"],
        [
            "ver-todo-televisores",
            TELEVISION,
            "Tecnología / Televisores / Ver todo Televisores",
        ],
        ["computadores", NOTEBOOK, "Tecnología / Computadores"],
        ["notebooks", NOTEBOOK, "Tecnología / Computadores / Notebooks"],
        ["tablet", TABLET, "Tecnología / Computadores / Tablet"],
        ["todo-impresoras", PRINTER, "Tecnología / Computadores / Impresoras"],
        [
            "ver-todo-computadores",
            NOTEBOOK,
            "Tecnología / Computadores / Todo Computadores",
        ],
        ["audio", HEADPHONES, "Tecnología / Audio"],
        ["minicomponentes", STEREO_SYSTEM, "Tecnología / Audio / Minicomponentes"],
        [
            "parlantes-portátiles",
            STEREO_SYSTEM,
            "Tecnología / Audio / Parlantes portátiles",
        ],
        ["audifonos", HEADPHONES, "Tecnología / Audio / Audífonos"],
        ["soundbar", STEREO_SYSTEM, "Tecnología / Audio / Soundbar"],
        ["ver-todo-audio", HEADPHONES, "Tecnología / Audio / Ver todo Audio"],
        [
            "discos-duros",
            EXTERNAL_STORAGE_DRIVE,
            "Tecnología / Accesorios Computación / Discos Duros",
        ],
        [
            "mouse-i-teclados",
            MOUSE,
            "Tecnología / Accesorios Computación / Mouse y Teclados",
        ],
        ["notebooks-gamer", NOTEBOOK, "Tecnología / Mundo Gamer / Notebooks Gamer"],
        ["consolas", VIDEO_GAME_CONSOLE, "Tecnología / Mundo Gamer / Consolas"],
        ["audifonos-gamer", HEADPHONES, "Tecnología / Mundo Gamer / Audífonos Gamer"],
        ["sillas-gamer", GAMING_CHAIR, "Tecnología / Mundo Gamer / Sillas Gamer"],
        ["accesorios-gamer", MOUSE, "Tecnología / Mundo Gamer / Accesorios Gamer"],
        ["refrigeradores", REFRIGERATOR, "Línea Blanca / Refrigeradores"],
        ["freezer", REFRIGERATOR, "Línea Blanca / Refrigeradores / Freezer"],
        ["side-by-side", REFRIGERATOR, "Línea Blanca / Refrigeradores / Side by Side"],
        ["no-frost", REFRIGERATOR, "Línea Blanca / Refrigeradores / No Frost"],
        ["frio-directo", REFRIGERATOR, "Línea Blanca / Refrigeradores / Frío Directo"],
        ["frigobar", REFRIGERATOR, "Línea Blanca / Refrigeradores / Frigobar"],
        [
            "ver-todo-refrigeracion",
            REFRIGERATOR,
            "Línea Blanca / Refrigeradores / Ver todo Refrigeración",
        ],
        ["lavado-y-secado", WASHING_MACHINE, "Línea Blanca / Lavado y Secado"],
        ["lavadoras", WASHING_MACHINE, "Línea Blanca / Lavado y Secado / Lavadoras"],
        ["secadoras", WASHING_MACHINE, "Línea Blanca / Lavado y Secado / Secadoras"],
        [
            "lavadoras-secadoras",
            WASHING_MACHINE,
            "Línea Blanca / Lavado y Secado / Lavadoras - Secadoras",
        ],
        [
            "ver-todo-lavado-y-secado",
            WASHING_MACHINE,
            "Línea Blanca / Lavado y Secado / Ver todo Lavado y Secado",
        ],
        [
            "hornos-electricos",
            OVEN,
            "Línea Blanca / Electrodomésticos / Hornos Eléctricos",
        ],
        ["microondas", OVEN, "Línea Blanca / Electrodomésticos / Microondas"],
        ["cocinas-a-gas", STOVE, "Línea Blanca / Cocina / Cocinas a Gas"],
        ["encimeras", STOVE, "Línea Blanca / Cocina / Encimeras"],
        ["hornos-empotrables", OVEN, "Línea Blanca / Cocina / Hornos empotrables"],
        [
            "lavaplatos-y-lavavajillas",
            DISH_WASHER,
            "Línea Blanca / Cocina / Lavaplatos y Lavavajillas",
        ],
        [
            "aires-acondicionados",
            SPLIT_AIR_CONDITIONER,
            "Línea Blanca / Climatización / Aires Acondicionados",
        ],
        [
            "calefont-y-termos",
            WATER_HEATER,
            "Línea Blanca / Climatización / Calefont y Termos",
        ],
        ["estufas", SPACE_HEATER, "Línea Blanca / Climatización / Estufas"],
        ["aspiradoras", VACUUM_CLEANER, "Línea Blanca / Aseo y Limpieza / Aspiradoras"],
        [
            "aspiradoras-robot",
            VACUUM_CLEANER,
            "Línea Blanca / Aseo y Limpieza / Aspiradoras Robot",
        ],
        ["electrodomesticos", ACCESORIES, "Línea Blanca / Electrodomésticos"],
        [
            "parrillas-electricas",
            ELECTRIC_GRILL,
            "Línea Blanca / Cocina / Parrillas Eléctricas",
        ],
        ["tintas", PRINTER_SUPPLY, "Tecnología / Computadores / Tintas"],
        ["planchas", IRON, "Línea Blanca / Aseo y Limpieza / Planchas"],
        [
            "secadores-de-pelo",
            HAIR_CARE,
            "Belleza / Cuidado Personal / Secadores de Pelos",
        ],
        [
            "alisadores-i-onduladores",
            HAIR_CARE,
            "Belleza / Cuidado Personal / Alisadores I Onduladores",
        ],
    ]

    @classmethod
    def categories(cls):
        return list({local_category for _, local_category, _ in cls.ajax_resources})

    @classmethod
    def discover_urls_for_category(cls, category, extra_args=None):
        seen_urls = set()

        for (
            category_id,
            local_categories,
            _,
        ) in cls.ajax_resources:
            if category not in local_categories:
                continue

            for product_url in cls._get_product_urls(category_id, extra_args):
                if product_url not in seen_urls:
                    seen_urls.add(product_url)
                    yield product_url

    @classmethod
    def discover_urls_for_keyword(cls, keyword, threshold, extra_args=None):
        session = session_with_proxy(extra_args)
        product_urls = []

        url = (
            "https://www.abc.cl/on/demandware.store/"
            "Sites-Abc-Site/es_CL/Search-UpdateGrid?"
            "q={}&srule=product-outstanding"
            "&start=0&sz=1000".format(keyword)
        )

        response = session.get(url).text
        soup = BeautifulSoup(response, "lxml")

        products = soup.findAll("div", "lp-product-tile")

        if not products:
            return []

        for container in products:
            product_url = "https://www.abc.cl{}".format(
                container.find("a", "image-link")["href"]
            )
            product_urls.append(product_url)

            if len(product_urls) == threshold:
                return product_urls

        return product_urls

    @classmethod
    def products_for_url(cls, url, category=None, extra_args=None):
        print(url)
        session = session_with_proxy(extra_args)
        response = session.get(url)

        if response.status_code in [410, 404]:
            return []

        soup = BeautifulSoup(response.text, "lxml")
        name = soup.find("h1", {"itemprop": "name"}).text.strip()
        key = soup.find("span", {"itemprop": "sku"})["data-sku"]
        prices_tag = soup.find("div", "prices")
        internet_price_tag = prices_tag.find("p", "internet")

        if internet_price_tag:
            normal_price_tag = internet_price_tag.find("span", "price-value")
        else:
            js_internet_price_tag = prices_tag.find("p", "js-internet-price")

            if not js_internet_price_tag:
                return []

            normal_price_tag = js_internet_price_tag.find("span", "price-value")

        normal_price = Decimal(normal_price_tag["data-value"]).quantize(0)

        offer_price_tag = prices_tag.find("p", "js-tlp-price")

        if offer_price_tag:
            offer_price_text = offer_price_tag.find("span", "price-value")
            offer_price = Decimal(offer_price_text["data-value"]).quantize(0)
        else:
            offer_price = normal_price

        stock = -1
        sku_tag = soup.find("span", "cod")

        if sku_tag:
            sku = soup.find("span", "cod").text.split(":")[1].strip()
        else:
            sku = key

        description = html_to_markdown(str(soup.find("div", "description-and-detail")))
        picture_urls = [
            x.find("img")["src"]
            for x in soup.findAll("div", "primary-image")
            if validators.url(x.find("img")["src"])
        ]

        product = Product(
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
            description=description,
            picture_urls=picture_urls,
        )

        yield product

    @classmethod
    def banners(cls, extra_args=None):
        session = session_with_proxy(extra_args)
        banners = []

        soup = BeautifulSoup(session.get("https://www.abc.cl").text, "lxml")
        slider_tags = soup.find("section", {"id": "carrusel_bps"}).findAll(
            "li", "carrusel-slide"
        )

        for index, slider_tag in enumerate(slider_tags):
            destination_urls = [slider_tag.find("a")["href"]]
            picture_url = slider_tag.find("source")["srcset"]

            banners.append(
                {
                    "url": "https://www.abc.cl",
                    "picture_url": picture_url,
                    "destination_urls": destination_urls,
                    "key": picture_url,
                    "position": index + 1,
                    "section": bs.HOME,
                    "subsection": bs.HOME,
                    "type": bs.SUBSECTION_TYPE_HOME,
                }
            )

        if not banners:
            raise Exception("No banners for Home section: https://www.abc.cl")

        return banners

    @classmethod
    def sections(cls):
        return [section for _, _, section in cls.ajax_resources]

    @classmethod
    def section_positions(cls, section, extra_args=None):
        section_positions = []

        for category_id, _, section_path in cls.ajax_resources:
            if section != section_path:
                continue

            idx = 1

            for product_url in cls._get_product_urls(category_id, extra_args):
                section_positions.append(
                    {
                        "field": "discovery_url",
                        "value": product_url,
                        "position": idx,
                        "section": section,
                    }
                )
                idx += 1

        return section_positions

    @classmethod
    def _get_product_urls(cls, category_id, extra_args):
        session = session_with_proxy(extra_args)
        session.headers["User-Agent"] = (
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
            "(KHTML, like Gecko) Chrome/62.0.3202.62 Safari/537.36"
        )
        url = (
            "https://www.abc.cl/on/demandware.store/Sites-Abc-Site/es_CL/Search-UpdateGrid?cgid={}&"
            "srule=best-matches&sz=1000"
        ).format(category_id)
        print(url)

        res = session.get(url)
        soup = BeautifulSoup(res.text, "lxml")
        product_cells = soup.findAll("div", "product-tile__item")

        if not product_cells:
            logging.warning("Empty category: " + category_id)

        for product_cell in product_cells:
            product_path = product_cell.find("a", "image-link")

            if not product_path:
                continue

            product_url = "https://www.abc.cl" + product_path["href"]
            yield product_url
