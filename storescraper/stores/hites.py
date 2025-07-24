import json
import logging
import re

from curl_cffi import requests
from bs4 import BeautifulSoup
from decimal import Decimal
from storescraper.categories import (
    SPLIT_AIR_CONDITIONER,
    ALL_IN_ONE,
    CELL,
    DISH_WASHER,
    EXTERNAL_STORAGE_DRIVE,
    GAMING_CHAIR,
    HEADPHONES,
    MONITOR,
    MOUSE,
    NOTEBOOK,
    OVEN,
    PRINTER,
    PROJECTOR,
    REFRIGERATOR,
    SPACE_HEATER,
    STEREO_SYSTEM,
    STOVE,
    TABLET,
    TELEVISION,
    USB_FLASH_DRIVE,
    VIDEO_GAME_CONSOLE,
    WASHING_MACHINE,
    WEARABLE,
    WATER_HEATER,
    ACCESORIES,
    PRINTER_SUPPLY,
    IRON,
    HAIR_CARE,
)

from storescraper.flixmedia import flixmedia_video_urls
from storescraper.product import Product
from storescraper.store import Store
from storescraper import banner_sections as bs
from storescraper.utils import html_to_markdown


class Hites(Store):
    category_paths = [
        [
            "electro-hogar/refrigeracion",
            REFRIGERATOR,
            "Inicio > Electro Hogar > Refrigeración",
        ],
        [
            "electro-hogar/refrigeracion/refrigeradores",
            REFRIGERATOR,
            "Inicio > Electro Hogar > Refrigeración > Refrigeradores",
        ],
        [
            "electro-hogar/refrigeracion/side-by-side",
            REFRIGERATOR,
            "Inicio > Electro Hogar > Refrigeración > Side by Side",
        ],
        [
            "electro-hogar/refrigeracion/freezer-y-frigobar",
            REFRIGERATOR,
            "Inicio > Electro Hogar > Refrigeración > Freezer y Frigobar",
        ],
        [
            "electro-hogar/lavado-y-secado",
            WASHING_MACHINE,
            "Inicio > Electro Hogar > Lavado y Secado",
        ],
        [
            "electro-hogar/lavado-y-secado/lavadoras",
            WASHING_MACHINE,
            "Inicio > Electro Hogar > Lavado y Secado > Lavadoras",
        ],
        [
            "electro-hogar/lavado-y-secado/secadoras/",
            WASHING_MACHINE,
            "Inicio > Electro Hogar > Lavado y Secado > Secadoras",
        ],
        [
            "electro-hogar/lavado-y-secado/lavadoras-secadoras",
            WASHING_MACHINE,
            "Inicio > Electro Hogar > Lavado y Secado > Lavadoras-Secadoras",
        ],
        [
            "electro-hogar/lavado-y-secado/carga-frontal",
            WASHING_MACHINE,
            "Inicio > Electro Hogar > Lavado y Secado > Carga Frontal",
        ],
        [
            "electro-hogar/lavado-y-secado/carga-superior",
            WASHING_MACHINE,
            "Inicio > Electro Hogar > Lavado y Secado > Carga Superior",
        ],
        ["electro-hogar/cocina", OVEN, "Inicio > Electro Hogar > Cocina"],
        [
            "electro-hogar/cocina/cocina-a-gas",
            STOVE,
            "Inicio > Electro Hogar > Cocina > Cocina a gas",
        ],
        [
            "electro-hogar/lavado-y-secado/lavavajillas",
            DISH_WASHER,
            "Inicio > Electro Hogar > Cocina > Lavavajillas",
        ],
        [
            "electro-hogar/cocina/encimeras",
            STOVE,
            "Inicio > Electro Hogar > Cocina > Encimeras",
        ],
        [
            "electro-hogar/cocina/hornos-empotrados",
            OVEN,
            "Inicio > Electro Hogar > Cocina > Hornos Empotrados",
        ],
        [
            "electro-hogar/electrodomesticos-cocina/microondas",
            OVEN,
            "Inicio > Electro Hogar > Electrodomesticos Cocina > Microondas",
        ],
        [
            "electro-hogar/electrodomesticos-cocina/hornos-electricos",
            OVEN,
            "Inicio > Electro Hogar > Electrodomesticos Cocina > Hornos Eléctricos",
        ],
        [
            "electro-hogar/calefaccion",
            SPACE_HEATER,
            "Inicio > Electro Hogar > Calefacción",
        ],
        [
            "electro-hogar/calefaccion/estufas-a-gas",
            SPACE_HEATER,
            "Inicio > Electro Hogar > Calefacción > Estufas a Gas",
        ],
        [
            "electro-hogar/calefaccion/f/estufa-a-lena",
            SPACE_HEATER,
            "Inicio > Electro Hogar > Calefacción > Estufa a Leña",
        ],
        [
            "electro-hogar/calefaccion/estufas-electricas",
            SPACE_HEATER,
            "Inicio > Electro Hogar > Calefacción > Estufas Eléctricas",
        ],
        [
            "electro-hogar/climatizacion",
            SPLIT_AIR_CONDITIONER,
            "Inicio > Electro Hogar > Climatización",
        ],
        [
            "electro-hogar/climatizacion/f/aire-acondicionado",
            SPLIT_AIR_CONDITIONER,
            "Inicio > Electro Hogar > Climatizacioń >  " "Aire Acondicionado",
        ],
        ["tecnologia/tv-video", TELEVISION, "Inicio > Tecnología > TV Video"],
        [
            "tecnologia/tv-video/televisores-smart-tv",
            TELEVISION,
            "Inicio > Tecnología > Tv Video > Smart TV",
        ],
        [
            "tecnologia/tv-video/smart-tv-premium",
            TELEVISION,
            "Inicio > Tecnología > Tv Video > Smart TV Premium",
        ],
        # ['tecnologia/tv-video/smart-tv-hasta-49', Television',
        #  'Inicio > Tecnología > Tv Video > Smart TV Hasta 49'],
        # ['tecnologia/tv-video/smart-tv-entre-50-y-55', 'Television',
        #  'Inicio > Tecnología > Tv Video > Smart TV Entre 50 y 55'],
        # ['tecnologia/tv-video/smart-tv-desde-58', 'Television',
        #  'Inicio > Tecnología > Tv Video > Smart TV Desde 58'],
        [
            "tecnologia/tv-video/smart-tv-samsung",
            TELEVISION,
            "Inicio > Tecnología > Tv Video > Smart Tv Samsung",
        ],
        [
            "tecnologia/tv-video/smart-tv-lg",
            TELEVISION,
            "Inicio > Tecnología > Tv Video > Smart Tv LG",
        ],
        [
            "tecnologia/tv-video/smart-tv-hisense",
            TELEVISION,
            "Inicio > Tecnología > Tv Video > Smart Tv Hisense",
        ],
        [
            "tecnologia/tv-video/f/soundbar",
            STEREO_SYSTEM,
            "Inicio > Tecnología > TV Video > Soundbar",
        ],
        [
            "tecnologia/tv-video/proyectores",
            PROJECTOR,
            "Inicio > Tecnología > TV Video > Proyectores",
        ],
        ["tecnologia/computacion", NOTEBOOK, "Inicio > Tecnología > Computación"],
        [
            "tecnologia/computacion/notebook",
            NOTEBOOK,
            "Inicio > Tecnología > Computación > Notebook",
        ],
        [
            "tecnologia/computacion/tablets",
            TABLET,
            "Inicio > Tecnología > Computación > Tablets",
        ],
        [
            "tecnologia/computacion/computadores-y-all-in-one",
            ALL_IN_ONE,
            "Inicio > Tecnología > Computacioń > All in One",
        ],
        [
            "tecnologia/computacion/monitores",
            MONITOR,
            "Inicio > Tecnología > Computación > Monitores y Proyectores",
        ],
        [
            "tecnologia/computacion/impresoras-y-multifuncionales",
            PRINTER,
            "Inicio > Tecnología > Computación > " "Impresoras y Multifuncionales",
        ],
        [
            "tecnologia/videojuegos/consolas",
            VIDEO_GAME_CONSOLE,
            "Inicio > Tecnología > Video Juego > Consolas",
        ],
        [
            "tecnologia/accesorios-y-otros/mouse-y-teclados",
            MOUSE,
            "Inicio > Tecnología > Accesorios y Otros > Mouse y Teclados",
        ],
        [
            "tecnologia/accesorios-y-otros/pendrives-y-tarjetas-de-memoria",
            USB_FLASH_DRIVE,
            "Inicio > Tecnología > Accesorios y Otros > Pendrives y Tarjetas de Memoria",
        ],
        [
            "tecnologia/accesorios-y-otros/discos-duros-y-pendrives",
            EXTERNAL_STORAGE_DRIVE,
            "Inicio > Tecnología > Accesorios y Otros > Discos Duros y Pendrives",
        ],
        ["tecnologia/audio", HEADPHONES, "Inicio > Tecnología > Audio"],
        [
            "tecnologia/audio/parlantes-bluetooth",
            STEREO_SYSTEM,
            "Inicio > Tecnología > Audio > Parlantes Bluetooth",
        ],
        [
            "tecnologia/audio/karaokes",
            STEREO_SYSTEM,
            "Inicio > Tecnología > Audio > Karaokes",
        ],
        [
            "tecnologia/audio/minicomponentes",
            STEREO_SYSTEM,
            "Inicio > Tecnología > Audio > Minicomponentes",
        ],
        [
            "celulares/audio/audifonos",
            HEADPHONES,
            "Inicio > Celulares > Accesorios para celulares > Audífonos",
        ],
        [
            "celulares/audio/audifonos-inalambrico",
            HEADPHONES,
            "Inicio > Celulares > Accesorios para celulares > Audífonos Inalámbrico",
        ],
        [
            "tecnologia/mundo-gamer/notebook-gamer",
            NOTEBOOK,
            "Tecnología > Mundo Gamer > Notebook Gamer",
        ],
        [
            "tecnologia/mundo-gamer/monitores-gamer",
            MONITOR,
            "Tecnología > Mundo Gamer > Monitores Gamer",
        ],
        [
            "tecnologia/mundo-gamer/sillas-gamer",
            GAMING_CHAIR,
            "Tecnología > Mundo Gamer > Sillas Gamer",
        ],
        [
            "tecnologia/mundo-gamer/audifonos-gamer",
            HEADPHONES,
            "Tecnología > Mundo Gamer > Audífonos Gamer",
        ],
        [
            "tecnologia/mundo-gamer/mouse-y-teclados-gamer",
            MOUSE,
            "Tecnología > Mundo Gamer > Mouse y Teclados Gamer",
        ],
        ["celulares/smartphones", CELL, "Inicio > Celulares > Smartphones"],
        [
            "celulares/smartphones/smartphone",
            CELL,
            "Inicio > Celulares > Smartphones > Smartphones",
        ],
        [
            "celulares/smartphones/celulares-liberados",
            CELL,
            "Inicio > Celulares > Smartphones > Celulares Liberados",
        ],
        [
            "celulares/smartphones/smartphones-reacondicionados",
            CELL,
            "Inicio > Celulares > Smartphones > Celulares Reacondicionados",
        ],
        [
            "celulares/smartphones/celulares-basicos",
            CELL,
            "Inicio > Celulares > Smartphone > Celulares Basicos",
        ],
        [
            "celulares/wearables/smartwatch",
            WEARABLE,
            "Inicio > Celulares > Accesorios para celulares > Smartwatch",
        ],
        [
            "celulares/accesorios-para-celulares/audifonos",
            HEADPHONES,
            "Inicio > Celulares > Accesorios para celulares > Audífonos",
        ],
        [
            "electro-hogar/calefaccion/calefont-y-termos",
            WATER_HEATER,
            "Inicio > Electro Hogar > Calefacción > Calefont y Termos",
        ],
        [
            "electro-hogar/electrodomesticos-cocina",
            ACCESORIES,
            "Inicio > Electro Hogar > Electrodomésticos Cocina",
        ],
        [
            "tecnologia/accesorios-y-otros/tintas-y-toner",
            PRINTER_SUPPLY,
            "Inicio > Tecnología > Accesorios y Otros > Tintas y Toner",
        ],
        [
            "electro-hogar/electrodomesticos-hogar/planchas",
            IRON,
            "Electro Hogar > Electrodomesticos Hogar > Planchas",
        ],
        [
            "belleza/cuidado-personal/secadores-de-pelo",
            HAIR_CARE,
            "Belleza > Cuidado Personal > Secadores De Pelo",
        ],
        [
            "belleza/cuidado-personal/onduladores",
            HAIR_CARE,
            "Belleza > Cuidado Personal > Onduladores",
        ],
        [
            "belleza/cuidado-personal/alisadores",
            HAIR_CARE,
            "Belleza > Cuidado Personal > Alisadores",
        ],
        [
            "electro-hogar/cuidado-personal/secadores-de-pelo",
            HAIR_CARE,
            "Electro Hogar > Cuidado Personal > Secadores de Pelo",
        ],
        [
            "electro-hogar/cuidado-personal/onduladores",
            HAIR_CARE,
            "Electro Hogar > Cuidado Personal > Onduladores",
        ],
        [
            "electro-hogar/cuidado-personal/alisadores",
            HAIR_CARE,
            "Electro Hogar > Cuidado Personal > Alisadores",
        ],
    ]

    @classmethod
    def categories(cls):
        return list({local_category for _, local_category, _ in cls.category_paths})

    @classmethod
    def discover_urls_for_category(cls, category, extra_args=None):
        seen_urls = set()

        for category_path, local_category, _ in cls.category_paths:
            if category != local_category:
                continue

            for product_url in cls._get_product_urls(
                category_path, exclude_marketplace=True
            ):
                if product_url not in seen_urls:
                    seen_urls.add(product_url)
                    yield product_url

    @classmethod
    def discover_urls_for_keyword(cls, keyword, threshold, extra_args=None):
        session = cls.get_session()
        product_urls = []
        page = 1

        while True:
            if page > 40:
                raise Exception("Page overflow")

            search_url = f"https://www.hites.com/search/{keyword}?page={page}"
            print(search_url)

            response = session.get(search_url, timeout=60)

            if response.status_code in [404, 500]:
                return []

            soup = BeautifulSoup(response.text, "lxml")
            json_data = json.loads(soup.find("script", {"id": "hy-data"}).text)
            product_data = json_data["result"]["products"]

            if not product_data:
                break

            for product_entry in product_data:
                slug = product_entry["productString"]
                product_url = f"https://www.hites.com/{slug}"
                product_urls.append(product_url)

                if len(product_urls) == threshold:
                    return product_urls

            page += 1

        return product_urls

    @classmethod
    def products_for_url(cls, url, category=None, extra_args=None):
        print(url)
        session = cls.get_session()
        response = session.get(url, timeout=60)
        soup = BeautifulSoup(response.text, "lxml")

        name = soup.find("h1", "product-name").text
        sku = soup.find("span", "product-id").text

        prices = soup.find("div", "prices")
        normal_price_container = prices.find("span", "sales") or prices.find(
            "span", "list"
        )
        normal_price = Decimal(normal_price_container.find("span", "value")["content"])
        offer_price_container = prices.find("h5", "hites-price")
        offer_price = (
            Decimal(offer_price_container.text.split("$")[1].replace(".", "").strip())
            if offer_price_container
            else normal_price
        )

        has_virtual_assistant = "cdn.livechatinc.com/tracking.js" in response.text
        flixmedia_container = soup.find(
            "script", {"src": "//media.flixfacts.com/js/loader.js"}
        )
        flixmedia_id = None
        video_urls = None

        if flixmedia_container:
            mpn = flixmedia_container["data-flix-mpn"]
            video_urls = flixmedia_video_urls(mpn)

            if video_urls is not None:
                flixmedia_id = mpn

        condition = (
            "https://schema.org/RefurbishedCondition"
            if "reacondicionado" in name.lower()
            else "https://schema.org/NewCondition"
        )

        images = soup.find("div", "primary-images").findAll("div", "carousel-item")
        picture_urls = [
            i.find("img")["src"].replace(" ", "%20")
            for i in images
            if i.find("img") is not None
        ]

        seller_text = soup.find("b", "seller").text.strip()
        seller = None if seller_text == "Hites" else seller_text
        availability_match = re.search(r'"availability":"(.+)"}', response.text)
        availability_text = availability_match.groups()[0]
        stock = (
            0 if seller or availability_text == "http://schema.org/OutOfStock" else -1
        )

        review_count_tag = soup.find("span", "top-stars-rating-details")
        review_count = (
            int(review_count_tag.text.replace("(", "").replace(")", ""))
            if review_count_tag
            else 0
        )

        if review_count:
            review_score_tag = soup.find("div", "yotpo-score-average")
            review_avg_score = float(review_score_tag.find("span").text)
        else:
            review_avg_score = None

        description = html_to_markdown(
            str(soup.find("div", {"id": "descriptionAndDetails"}))
        )

        product = Product(
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
            condition=condition,
            picture_urls=picture_urls,
            video_urls=video_urls,
            has_virtual_assistant=has_virtual_assistant,
            flixmedia_id=flixmedia_id,
            seller=seller,
            review_count=review_count,
            review_avg_score=review_avg_score,
            description=description,
        )

        yield product

    @classmethod
    def banners(cls, extra_args=None):
        session = cls.get_session()
        banners = []
        url = "https://www.hites.com"
        response = session.get(url)
        soup = BeautifulSoup(response.text, "lxml")
        banners_container = soup.findAll("div", "clp-hero-banner")

        for index, banner in enumerate(banners_container):
            destination_urls = [a["href"] for a in banner.findAll("a")]
            destination_urls = list(set(destination_urls))
            picture_container = banner.find("picture")
            picture_url = picture_container.findAll("source")[1]["srcset"]
            banners.append(
                {
                    "url": url,
                    "picture_url": picture_url,
                    "destination_urls": destination_urls,
                    "key": picture_url,
                    "position": index + 1,
                    "section": bs.HOME,
                    "subsection": bs.HOME,
                    "type": bs.SUBSECTION_TYPE_HOME,
                }
            )

        return banners

    @classmethod
    def get_session(cls, extra_args=None):
        return requests.Session(impersonate="chrome120")

    @classmethod
    def sections(cls):
        return [section for _, _, section in cls.category_paths]

    @classmethod
    def section_positions(cls, section, extra_args=None):
        for category_path, _, section_path in cls.category_paths:
            if section != section_path:
                continue

            for idx, product_url in enumerate(
                cls._get_product_urls(category_path, exclude_marketplace=False)
            ):
                if idx >= 300:
                    break

                yield {
                    "field": "discovery_url",
                    "value": product_url,
                    "position": idx + 1,
                    "section": section,
                    "is_sponsored": False,
                }

    @classmethod
    def _get_product_urls(cls, category_path, exclude_marketplace):
        session = cls.get_session()
        start = 0
        step = 48

        while True:
            category_url = f"https://www.hites.com/{category_path}/?sz={step}&start={start}&srule=best-matches"

            if exclude_marketplace:
                category_url += "&prefn1=productoMKP&prefv1=Hites.com"

            print(category_url)

            if start >= step * 100:
                raise Exception(f"Page overflow: {category_url}")

            response = session.get(category_url, timeout=60)

            if response.url != category_url:
                raise Exception(
                    f"Page mismatch. Expecting {category_url} Got {response.url}"
                )

            if response.status_code in [404, 500]:
                break

            soup = BeautifulSoup(response.text, "lxml")
            products = soup.findAll("div", "product-tile")

            if not products:
                break

            for product_entry in products:
                a_tag = product_entry.find("a")

                if not a_tag:
                    continue

                path = a_tag["href"].split("?")[0]
                product_url = (
                    path if "hites.com" in path else f"https://www.hites.com{path}"
                )

                if product_url == "https://www.hites.com/":
                    logging.warning(f"Invalid URL: {category_url}")
                    continue

                yield product_url

            start += step
