import json
import logging
import random
import re
import urllib

import time

from decimal import Decimal

import validators
from bs4 import BeautifulSoup
from html import unescape

from curl_cffi.requests import RequestsError
from dateutil.parser import parse
from curl_cffi import requests
from requests import TooManyRedirects

from storescraper.categories import *
from storescraper.product import Product
from storescraper.store import Store
from storescraper.utils import (
    remove_words,
    html_to_markdown,
    session_with_proxy,
    cf_session_with_proxy,
)
from storescraper import banner_sections as bs


class Falabella(Store):
    preferred_discover_urls_concurrency = 3
    preferred_products_for_url_concurrency = 20
    store_and_subdomain = None
    product_url_template = (
        "https://www.falabella.com/falabella-cl/product/{}/product/{}"
    )
    seller_id = "FALABELLA"
    banners_base_url = "https://www.falabella.com/falabella-cl/{}"
    banners_sections_data = [
        [bs.HOME, "Home", bs.SUBSECTION_TYPE_HOME, ""],
        # # CATEGORY PAGES # #
        [
            bs.REFRIGERATION,
            "Electrohogar-Refrigeradores",
            bs.SUBSECTION_TYPE_CATEGORY_PAGE,
            "category/cat3205/Refrigeradores?isLanding=true",
        ],
        [
            bs.AUDIO,
            "Audio",
            bs.SUBSECTION_TYPE_CATEGORY_PAGE,
            "category/cat2005/Audio?isLanding=true",
        ],
        [
            bs.CELLS,
            "Telefonía-Celulares y Teléfonos",
            bs.SUBSECTION_TYPE_CATEGORY_PAGE,
            "category/cat2018/Celulares-y-Telefonos?isLanding=true",
        ],
        # # MOSAICS ##
        [
            bs.LINEA_BLANCA_FALABELLA,
            "Electro y Tecnología-Línea Blanca",
            bs.SUBSECTION_TYPE_MOSAIC,
            "category/cat7090035/Linea-Blanca?isPLP=1",
        ],
        [
            bs.REFRIGERATION,
            "Refrigeradores-No Frost",
            bs.SUBSECTION_TYPE_MOSAIC,
            "category/cat4074/No-Frost",
        ],
        [
            bs.REFRIGERATION,
            "Refrigeradores-Side by Side",
            bs.SUBSECTION_TYPE_MOSAIC,
            "category/cat4091/Side-by-Side",
        ],
        [
            bs.WASHING_MACHINES,
            "Lavadoras",
            bs.SUBSECTION_TYPE_MOSAIC,
            "category/cat3136/Lavadoras",
        ],
        [
            bs.WASHING_MACHINES,
            "Lavadoras-Lavadoras",
            bs.SUBSECTION_TYPE_MOSAIC,
            "category/cat4060/Lavadoras",
        ],
        [
            bs.WASHING_MACHINES,
            "Lavadoras-Lavadoras-Secadoras",
            bs.SUBSECTION_TYPE_MOSAIC,
            "category/cat1700002/Lavadoras-Secadoras",
        ],
        [
            bs.WASHING_MACHINES,
            "Lavadoras-Secadoras",
            bs.SUBSECTION_TYPE_MOSAIC,
            "category/cat4088/Secadoras",
        ],
        [
            bs.WASHING_MACHINES,
            " Lavadoras-Lavadoras Doble Carga",
            bs.SUBSECTION_TYPE_MOSAIC,
            "category/cat11400002/Lavadoras-Doble-Carga",
        ],
        [
            bs.TELEVISIONS,
            "Tecnología-TV",
            bs.SUBSECTION_TYPE_MOSAIC,
            "category/cat1012/TV?isPLP=1",
        ],
        [
            bs.TELEVISIONS,
            "Televisores LED",
            bs.SUBSECTION_TYPE_MOSAIC,
            "category/cat7190148/Televisores-LED",
        ],
        [
            bs.TELEVISIONS,
            "LEDs menores a 50 pulgadas",
            bs.SUBSECTION_TYPE_MOSAIC,
            "category/cat11161614/LEDs-menores-a-50-pulgadas",
        ],
        [
            bs.TELEVISIONS,
            "LEDs entre 50 - 55 pulgadas",
            bs.SUBSECTION_TYPE_MOSAIC,
            "category/cat11161675/LEDs-entre-50---55-pulgadas",
        ],
        [
            bs.TELEVISIONS,
            "LEDs sobre 55 pulgadas",
            bs.SUBSECTION_TYPE_MOSAIC,
            "category/cat11161679/LEDs-sobre-55-pulgadas",
        ],
        [
            bs.TELEVISIONS,
            "TV-LED",
            bs.SUBSECTION_TYPE_MOSAIC,
            "category/cat2850014/LED",
        ],
        [
            bs.TELEVISIONS,
            "TV-Smart TV",
            bs.SUBSECTION_TYPE_MOSAIC,
            "category/cat3040054/Smart-TV",
        ],
        [
            bs.TELEVISIONS,
            "TV-4K UHD",
            bs.SUBSECTION_TYPE_MOSAIC,
            "category/cat3990038/4K-UHD",
        ],
        [
            bs.TELEVISIONS,
            "TV-Televisores OLED",
            bs.SUBSECTION_TYPE_MOSAIC,
            "category/cat2850016/Televisores-OLED",
        ],
        [
            bs.TELEVISIONS,
            "TV-Pulgadas Altas",
            bs.SUBSECTION_TYPE_MOSAIC,
            'category/cat12910024/Televisores-LED-Desde-65"',
        ],
        [
            bs.AUDIO,
            "Audio-Soundbar y Home Theater",
            bs.SUBSECTION_TYPE_MOSAIC,
            "category/cat2045/Home-Theater",
        ],
        [
            bs.AUDIO,
            "Home Theater",
            bs.SUBSECTION_TYPE_MOSAIC,
            "category/cat3050040/Home-Theater",
        ],
        [
            bs.AUDIO,
            "Soundbar",
            bs.SUBSECTION_TYPE_MOSAIC,
            "category/cat1700004/Soundbar",
        ],
        [
            bs.AUDIO,
            "Minicomponente",
            bs.SUBSECTION_TYPE_MOSAIC,
            "category/cat70018/Minicomponente",
        ],
        [
            bs.AUDIO,
            "Audio-Equipos de Música y Karaokes",
            bs.SUBSECTION_TYPE_MOSAIC,
            "category/cat3091/?mkid=CA_P2_MIO1_024794",
        ],
        [
            bs.AUDIO,
            "Audio-Hi-Fi",
            bs.SUBSECTION_TYPE_MOSAIC,
            "category/cat3203/Hi-Fi",
        ],
        [
            bs.AUDIO,
            "Audio",
            bs.SUBSECTION_TYPE_MOSAIC,
            "category/cat2005/Audio?isPLP=1",
        ],
        [
            bs.CELLS,
            "Smartphones",
            bs.SUBSECTION_TYPE_MOSAIC,
            "category/cat720161/Smartphones",
        ],
        [
            bs.CELLS,
            "Electro y Tecnología-Teléfonos",
            bs.SUBSECTION_TYPE_MOSAIC,
            "category/cat2018/Telefonos?isPLP=1",
        ],
    ]
    section_position_variants = [
        {"id": "FALABELLA", "section_prefix": "FALABELLA", "exclude_marketplace": True},
        {"id": None, "section_prefix": "GRUPO", "exclude_marketplace": False},
    ]

    category_paths = [
        [
            "cat720161",
            CELL,
            "Home > Tecnología-Telefonía > Celulares y Teléfonos > Smartphones",
        ],
        [
            "cat1280018",
            CELL,
            "Home > Tecnología-Telefonía > Celulares y Teléfonos > Celulares Básicos",
        ],
        ["cat1640002", HEADPHONES, "Home > Tecnología-Audio > Audífonos"],
        [
            "cat70037",
            MEMORY_CARD,
            "Home > Tecnología-Telefonía > Accesorios "
            "Celulares > Tarjetas de Memoria",
        ],
        ["cat4290064", WEARABLE, "Home > Tecnología-Wearables > Smartband"],
        ["cat4290063", WEARABLE, "Home > Tecnología-Wearables > SmartWatch"],
        [
            "cat429001",
            WEARABLE,
            "Home > Tecnología-Wearables > SmartWatch Infantil",
        ],
        ["cat1012", TELEVISION, "Home > Tecnología-TV y Video"],
        ["cat7190148", TELEVISION, "Home > Tecnología-TV > Smart TV"],
        [
            "cat7190148",
            TELEVISION,
            'Home > Tecnología-TV > Smart tv entre 50" - 55"',
            {"f.variant.custom.Tama%C3%B1o_de_la_pantalla": "50::55"},
        ],
        [
            "cat7190148",
            TELEVISION,
            'Home > Tecnología-TV > Smart tv sobre 55"',
            {
                "f.derived.product.Tamano_de_la_pantalla": "58::60::65::70::75::77::85::86::98"
            },
        ],
        [
            "cat7190148",
            TELEVISION,
            'Home > Tecnología-TV > Smart tv menores a 50"',
            {
                "f.variant.custom.Tama%C3%B1o_de_la_pantalla": "1::20::24::32::39::40::42::43::48"
            },
        ],
        ["cat2070", PROJECTOR, "Home > Tecnología-TV > Proyectores"],
        ["cat2005", STEREO_SYSTEM, "Home > Tecnología-Audio"],
        [
            "cat3091",
            STEREO_SYSTEM,
            "Home > Tecnología-Audio > Equipos de Música y Karaokes",
        ],
        ["cat3203", STEREO_SYSTEM, "Home > Tecnología-Audio > Hi-Fi"],
        [
            "cat3171",
            STEREO_SYSTEM,
            "Home > Tecnología-Audio > Parlantes Bluetooth",
        ],
        [
            "cat2045",
            STEREO_SYSTEM,
            "Home > Tecnología-Audio > Soundbar y Home Theater",
        ],
        [
            "cat3155",
            MOUSE,
            "Home > Tecnología-Computadores > Accesorios Computación > Mouse",
        ],
        [
            "cat2370002",
            KEYBOARD,
            "Home > Tecnología-Computadores > Accesorios Computación > Teclados",
        ],
        [
            "cat3239",
            STEREO_SYSTEM,
            "Home > Tecnología-Computadores > Accesorios Computación > Parlantes y Subwoofer",
        ],
        ["cat40051", ALL_IN_ONE, "Home > Tecnología-Computadores > All in one"],
        [
            "cat3087",
            EXTERNAL_STORAGE_DRIVE,
            "Home > Tecnología-Computadores > Almacenamiento > Discos duros",
        ],
        [
            "cat3177",
            USB_FLASH_DRIVE,
            "Home > Tecnología-Computación > Almacenamiento > Pendrives",
        ],
        [
            "cat1820006",
            PRINTER,
            "Home > Tecnología-Computadores > Impresoras y Tintas > Impresoras Multifuncionales",
        ],
        [
            "cat1820004",
            PRINTER,
            "Home > Tecnología-Computadores > Impresoras y Tintas > Impresoras",
        ],
        [
            "cat6680042",
            PRINTER,
            "Home > Tecnología-Computadores > Impresoras y Tintas > Impresoras Tradicionales",
        ],
        [
            "cat11970007",
            PRINTER,
            "Home > Tecnología-Computadores > Impresoras y Tintas > Impresoras Láser",
        ],
        ["cat2062", MONITOR, "Home > Tecnología-Computadores > Monitores"],
        ["cat70057", NOTEBOOK, "Home > Tecnología-Computadores > Notebooks"],
        ["cat7230007", TABLET, "Home > Tecnología-Computadores > Tablets"],
        [
            "cat4930009",
            HEADPHONES,
            "Home > Tecnología-Computadores > Accesorios gamer > Audífonos gamer",
        ],
        [
            "CATG19011",
            GAMING_CHAIR,
            "Home > Tecnología-Computadores > Accesorios gamer > Sillas gamer",
        ],
        [
            "CATG19008",
            KEYBOARD,
            "Home > Tecnología-Computadores > Accesorios gamer > Tecaldos gamer",
        ],
        [
            "CATG19007",
            MOUSE,
            "Home > Tecnología-Computadores > Accesorios gamer > Mouse gamer",
        ],
        [
            "cat2023",
            VIDEO_GAME_CONSOLE,
            "Home > Tecnología - Zona Gamer > Videojuegos",
        ],
        [
            "cat3114",
            OVEN,
            "Home > Electrohogar-Electrodomésticos Cocina > Hornos Eléctricos",
        ],
        [
            "cat3151",
            OVEN,
            "Home > Electrohogar-Electrodomésticos Cocina > Microondas",
        ],
        [
            "cat3136",
            WASHING_MACHINE,
            "Home > Electrohogar-Línea blanca > Lavado",
        ],
        [
            "cat4060",
            WASHING_MACHINE,
            "Home > Electrohogar-Línea blanca > Lavado > Lavadoras",
        ],
        [
            "cat1700002",
            WASHING_MACHINE,
            "Home > Electrohogar-Línea blanca > Lavado > Lavadoras-Secadoras",
        ],
        [
            "cat4088",
            WASHING_MACHINE,
            "Home > Electrohogar-Línea blanca > Lavado > Secadoras",
        ],
        [
            "cat4061",
            DISH_WASHER,
            "Home > Electrohogar-Línea blanca > Lavado > Lavavajillas",
        ],
        [
            "cat3205",
            REFRIGERATOR,
            "Home > Electrohogar-Línea Blanca > Refrigeración > Refrigeradores",
        ],
        [
            "cat4091",
            REFRIGERATOR,
            "Home > Electrohogar-Línea Blanca > Refrigeración > Refrigeradores > Side by side",
        ],
        [
            "cat4074",
            REFRIGERATOR,
            "Home > Electrohogar-Línea Blanca > Refrigeración > Refrigeradores > No Frost",
        ],
        [
            "CATG19019",
            REFRIGERATOR,
            "Home > Electrohogar-Línea Blanca > Refrigeración > Refrigeradores > Top Freezer",
        ],
        [
            "CATG19020",
            REFRIGERATOR,
            "Home > Electrohogar-Línea Blanca > Refrigeración > Refrigeradores > Bottom Freezer",
        ],
        [
            "cat4054",
            OVEN,
            "Home > Electrohogar-Línea blanca > Cocina > Hornos Empotrables",
        ],
        [
            "cat2019",
            SPLIT_AIR_CONDITIONER,
            "Home > Electrohogar-Climatización > Aire acondicionado",
        ],
        [
            "CATG34744",
            NOTEBOOK,
            "Home > Especiales-Otras categorias > PC gamer",
        ],
        [
            "cat3025",
            VACUUM_CLEANER,
            "Home > Electrohogar-Aspirado y Limpieza > Aspiradoras",
        ],
        ["cat1130010", STEREO_SYSTEM, "Home > Tecnología-Audio > Tornamesas"],
        [
            "cat9910024",
            SPACE_HEATER,
            "Home > Electrohogar-Calefacción > Calefacción > Estufas Gas",
        ],
        [
            "cat16250010",
            SPACE_HEATER,
            "Home > Electrohogar-Calefacción > Calefacción > Estufas Parafina",
        ],
        [
            "cat9910006",
            SPACE_HEATER,
            "Home > Electrohogar-Calefacción > Calefacción > Estufas Eléctricas",
        ],
        [
            "CATG35044",
            SPACE_HEATER,
            "Home > Electrohogar-Calefacción > Calefacción > Estufas a Leña",
        ],
        [
            "cat9910027",
            SPACE_HEATER,
            "Home > Electrohogar-Calefacción > Calefacción > Estufas a Pellet",
        ],
        [
            "cat2013",
            WATER_HEATER,
            "Home > Cocina y Baño-Baño > Calefont y Termos",
        ],
        [
            "cat70012",
            STOVE,
            "Home > Electrohogar - Línea blanca > Cocina > Cocina a gas",
        ],
        [
            "cat4045",
            STOVE,
            "Home > Electrohogar - Línea blanca > Cocina > Encimeras",
        ],
        [
            "cat2034",
            ACCESORIES,
            "Home > Electrohogar - Electrodomésticos cocina",
        ],
        [
            "cat3246",
            PRINTER_SUPPLY,
            "Home > Tecnología-Computadores > Impresoras y Tintas > Tintas y Toners",
        ],
        [
            "cat2069",
            PERFUME,
            "Home > Belleza y salud > Perfumes",
        ],
        ["cat3182", IRON, "Home > Electrohogar - Línea blanca > Planchas"],
        [
            "cat3223",
            HAIR_CARE,
            "Home > Belleza, higiene y salud > Tecnología para la Belleza > Secadores de pelo",
        ],
        [
            "cat3018",
            HAIR_CARE,
            "Home > Belleza, higiene y salud > Tecnología para la Belleza > Plancha de pelo",
        ],
        [
            "cat3170",
            HAIR_CARE,
            "Home > Belleza, higiene y salud > Tecnología para la Belleza > Onduladores de pelo",
        ],
    ]

    @classmethod
    def categories(cls):
        return list({x[1] for x in cls.category_paths})

    @classmethod
    def discover_urls_for_category(cls, category, extra_args=None):
        session = cf_session_with_proxy(extra_args)

        for e in cls.category_paths:
            category_id, local_category, section_name = e[:3]
            if category != local_category:
                continue

            if len(e) == 4:
                extra_params = e[3]
            else:
                extra_params = {}

            yield from cls._get_product_urls(
                session, category_id, extra_params, cls.seller_id, extra_args["zones"]
            )

    @classmethod
    def discover_urls_for_keyword(cls, keyword, threshold, extra_args=None):
        session = requests.Session(impersonate="chrome120")

        base_url = "https://www.falabella.com/falabella-cl/search?Ntt={}&page={}"

        discovered_urls = []
        page = 1
        while True:
            if page > 150:
                raise Exception("Page overflow " + keyword)

            search_url = base_url.format(urllib.parse.quote(keyword), page)
            res = session.get(search_url, timeout=30)

            if res.status_code == 500:
                break

            soup = BeautifulSoup(res.text, "lxml")

            script = soup.find("script", {"id": "__NEXT_DATA__"})
            json_data = json.loads(script.text)

            if "results" not in json_data["props"]["pageProps"]:
                break

            for product_data in json_data["props"]["pageProps"]["results"]:
                product_url = product_data["url"]
                discovered_urls.append(product_url)

                if len(discovered_urls) == threshold:
                    return discovered_urls

            page += 1

        return discovered_urls

    @classmethod
    def products_for_url(cls, url, category=None, extra_args=None):
        print(url)
        extra_args = extra_args or {}
        use_cf = extra_args.get("use_cf", True)
        if use_cf:
            session = cf_session_with_proxy(extra_args)
        else:
            session = session_with_proxy(extra_args)
            session.headers["User-Agent"] = (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/125.0.0.0 Safari/537.36"
            )

        for i in range(3):
            try:
                response = session.get(url, timeout=30)
            except RequestsError:
                return []
            except UnicodeDecodeError:
                return []
            except TooManyRedirects:
                return []

            if response.status_code in [404, 500]:
                return []

            if "notFound" in response.url:
                return []

            content = response.text.replace("&#10;", "")

            if "NEXT_DATA" in content:
                break
            else:
                return []
        else:
            return []

        soup = BeautifulSoup(content, "html5lib")
        next_container = soup.find("script", {"id": "__NEXT_DATA__"})

        if not next_container:
            return []

        page_props = json.loads(next_container.contents[0])["props"]["pageProps"]

        if "productData" not in page_props:
            return []

        product_data = page_props["productData"]
        long_description = product_data["longDescription"]

        if long_description:
            description_soup = BeautifulSoup(unescape(long_description), "html5lib")
            description = html_to_markdown(str(description_soup))
        else:
            description = ""

        for spec in product_data["attributes"]["specifications"]:
            description += f"\n{spec['name']}: {spec['value']}"

        slug = product_data["slug"]
        publication_id = product_data["id"]
        brand = product_data["brandName"] or "Genérico"
        base_name = "{} {}".format(brand, product_data["name"])
        # Remove weird unicode characters
        # base_name = base_name.encode("ascii", "ignore").decode("ascii")

        products = []

        if "variants" not in product_data:
            return []

        reviews_url = (
            "https://api.bazaarvoice.com/data/display/"
            "0.2alpha/product/summary?PassKey="
            "m8bzx1s49996pkz12xvk6gh2e&productid={}&"
            "contentType=reviews,questions&"
            "reviewDistribution=primaryRating,"
            "recommended&rev=0".format(product_data["id"])
        )

        review_data = json.loads(session.get(reviews_url, timeout=30).text)
        review_count = review_data["reviewSummary"]["numReviews"]
        review_avg_score = review_data["reviewSummary"]["primaryRating"]["average"]

        is_international_shipping = product_data["internationalShipping"]["applicable"]
        base_model_name = f"{product_data['brandName']} {product_data['name']}"

        for model in product_data["variants"]:
            if len(product_data["variants"]) > 1:
                model_name = f"{base_model_name} - {model['name']}"
            else:
                model_name = base_model_name

            sku = model["id"]
            sku_url = (
                "https://www.falabella.com/falabella-cl/product/{}/{}/"
                "{}".format(publication_id, slug, sku)
            )

            prices = {e["type"]: e for e in model["prices"]}

            if not prices:
                continue

            normal_price_keys = ["eventPrice", "internetPrice", "normalPrice"]
            offer_price_keys = ["cmrPrice", "eventPrice"]

            normal_price = None
            offer_price = None

            remove_words_blacklist = (
                extra_args.get("remove_words_blacklist", None) if extra_args else None
            )

            for key in normal_price_keys:
                if key not in prices:
                    continue
                normal_price = Decimal(
                    remove_words(
                        prices[key]["price"][0], blacklist=remove_words_blacklist
                    )
                )
                if normal_price.is_finite():
                    break
                else:
                    normal_price = None

            for key in offer_price_keys:
                if key not in prices:
                    continue
                offer_price = Decimal(
                    remove_words(
                        prices[key]["price"][0], blacklist=remove_words_blacklist
                    )
                )
                if offer_price.is_finite():
                    break
                else:
                    offer_price = None

            if not normal_price and not offer_price:
                # No valid prices found
                continue

            if not offer_price:
                offer_price = normal_price

            if not normal_price:
                normal_price = offer_price

            if normal_price > Decimal("50000000") or offer_price > Decimal("50000000"):
                continue

            seller_entry = None

            if model["offerings"] and "sellerName" in model["offerings"][0]:
                if "falabella" not in model["offerings"][0]["sellerName"].lower():
                    seller_entry = model["offerings"][0]
            elif model["offerings"] and "sellerId" in model["offerings"][0]:
                if "falabella" not in model["offerings"][0]["sellerId"].lower():
                    seller_entry = model["offerings"][0]

            stock = 0
            seller = (
                seller_entry.get("sellerName", seller_entry["sellerId"])
                if seller_entry
                else None
            )

            if is_international_shipping:
                stock = 0
            elif seller_entry and (
                seller_entry.get("sellerProductStatus", None) == "ACTIVO"
                or seller_entry.get("isActive", False)
            ):
                stock = -1
            elif model.get("isPurchaseable", True):
                availabilities = model["availability"]

                for availability in availabilities:
                    if availability["shippingOptionType"] in [
                        "All",
                        "HomeDelivery",
                        "SiteToStore",
                        "PickupInStore",
                    ]:
                        if availability["quantity"]:
                            stock = -1
                            break

            if "reacondicionado" in base_name.lower():
                condition = "https://schema.org/RefurbishedCondition"
            elif "reacondicionado" in description.lower():
                condition = "https://schema.org/RefurbishedCondition"
            else:
                condition = "https://schema.org/NewCondition"

            picture_urls = [
                x["url"] + "?scl=1.0"
                for x in model["medias"]
                if validators.url(x["url"])
            ]
            # model_name = model["name"].encode("ascii", "ignore").decode("ascii")

            p = Product(
                model_name[:200],
                cls.__name__,
                category,
                sku_url,
                url,
                sku,
                stock,
                normal_price,
                offer_price,
                "CLP",
                sku=sku,
                picture_urls=picture_urls,
                review_count=review_count,
                review_avg_score=review_avg_score,
                condition=condition,
                seller=seller,
                description=description,
            )

            products.append(p)

        return products

    @classmethod
    def sections(cls):
        return [x[2] for x in cls.category_paths]

    @classmethod
    def section_positions(cls, section, extra_args=None):
        session = cf_session_with_proxy(extra_args)

        for e in cls.category_paths:
            category_id, local_category, section_name = e[:3]
            if section_name != section:
                continue

            if len(e) == 4:
                extra_params = e[3]
            else:
                extra_params = {}

            for section_variant in cls.section_position_variants:
                category_product_urls = cls._get_product_urls(
                    session,
                    category_id,
                    extra_params,
                    section_variant["id"],
                    extra_args["zones"],
                )

                if section_variant["section_prefix"]:
                    full_section_name = "{} > {}".format(
                        section_variant["section_prefix"], section_name
                    )
                else:
                    full_section_name = section_name

                for idx, url in enumerate(category_product_urls):
                    if idx >= 300:
                        break

                    section_position = {
                        "field": "discovery_url",
                        "value": url,
                        "position": idx + 1,
                        "section": full_section_name,
                    }
                    yield section_position

    @classmethod
    def _get_product_urls(cls, session, category_id, extra_params, seller_id, zones):
        discovered_urls = []
        base_url = f"https://www.falabella.com/s/browse/v1/listing/cl?pid=15c37b0b-a392-41a9-8b3b-978376c700d5&categoryId={category_id}"
        category_details = json.loads(session.get(base_url).text)["data"][
            "categoryParentDetails"
        ]
        category_name = None

        for category in category_details:
            if category_id == category["id"]:
                category_name = category["link"].split("/")[-1]

        base_url = (
            "https://www.falabella.com/s/browse/v1/listing/cl?"
            "&pid=15c37b0b-a392-41a9-8b3b-978376c700d5&categoryName={}&categoryId={}&page={}"
        )

        for key, value in extra_params.items():
            base_url += "&{}={}".format(key, urllib.parse.quote(value))

        base_url += "&zones={}".format(urllib.parse.quote(zones))
        page = 1

        while True:
            if page > 210:
                raise Exception("Page overflow: " + category_id)

            pag_url = base_url.format(category_name, category_id, page)

            if cls.store_and_subdomain:
                pag_url += "&subdomain={}&store={}".format(
                    cls.store_and_subdomain, cls.store_and_subdomain
                )

            if seller_id:
                pag_url += "&f.derived.variant.sellerId={}".format(seller_id)

            print(pag_url)

            res = cls.retrieve_json_page(session, pag_url)

            if "results" not in res or not res["results"]:
                if page == 1:
                    logging.warning(
                        "Empty category: {} - {}".format(category_id, extra_params)
                    )
                break

            for result in res["results"]:
                product_url = cls.product_url_template.format(
                    result["productId"], result["skuId"]
                )

                if product_url not in discovered_urls:
                    discovered_urls.append(product_url)
                    yield product_url

            page += 1

    @classmethod
    def retrieve_json_page(cls, session, url, retries=5):
        if "?" in url:
            separator = "&"
        else:
            separator = "?"

        modified_url = "{}{}v={}".format(url, separator, random.random())

        try:
            res = session.get(modified_url, timeout=30)
            return json.loads(res.content.decode("utf-8"))["data"]
        except Exception:
            if retries > 0:
                time.sleep(3)
                return cls.retrieve_json_page(session, url, retries=retries - 1)
            else:
                raise

    @classmethod
    def banners(cls, extra_args=None):
        banners = []

        for (
            section,
            subsection,
            subsection_type,
            url_suffix,
        ) in cls.banners_sections_data:
            url = cls.banners_base_url.format(url_suffix)
            print(url)

            if subsection_type == bs.SUBSECTION_TYPE_HOME:
                session = requests.Session(impersonate="chrome120")
                soup = BeautifulSoup(session.get(url, timeout=30).text, "lxml")
                next_data = json.loads(
                    soup.find("script", {"id": "__NEXT_DATA__"}).text
                )

                for container in next_data["props"]["pageProps"]["page"]["containers"]:
                    if container["key"] == "showcase":
                        showcase_container = container
                        break
                else:
                    raise Exception("No showcase container found")

                for container in showcase_container["components"]:
                    if "slides" in container["data"]:
                        slides = container["data"]["slides"]
                        break
                else:
                    raise Exception("No slides found")

                for idx, slide in enumerate(slides):
                    if "type" not in slide:
                        continue

                    main_url = slide.get("mainUrl", None)

                    if main_url:
                        destination_urls = [main_url[:500]]
                    elif slide["type"] == "background_image_only":
                        destination_urls = []
                    else:
                        destination_urls = list({slide["urlLeft"], slide["urlRight"]})

                    picture_url = slide["imgBackgroundDesktopUrl"]

                    banners.append(
                        {
                            "url": url,
                            "picture_url": picture_url,
                            "destination_urls": destination_urls,
                            "key": picture_url,
                            "position": idx + 1,
                            "section": section,
                            "subsection": subsection,
                            "type": subsection_type,
                        }
                    )

                if not banners:
                    raise Exception("No banners for Home section: " + url)

            elif subsection_type == bs.SUBSECTION_TYPE_CATEGORY_PAGE:
                session = requests.Session(impersonate="chrome120")
                soup = BeautifulSoup(session.get(url, timeout=30).text, "lxml")
                next_data = json.loads(
                    soup.find("script", {"id": "__NEXT_DATA__"}).text
                )

                for container in next_data["props"]["pageProps"]["page"]["containers"]:
                    if container["key"] == "main-right":
                        showcase_container = container
                        break
                else:
                    raise Exception("No showcase container found")

                if not showcase_container["components"]:
                    continue

                slides = showcase_container["components"][0]["data"]["slides"]

                for idx, slide in enumerate(slides):
                    main_url = slide.get("mainUrl", None)
                    if main_url:
                        destination_urls = [main_url]
                    elif slide["type"] == "background_image_only":
                        destination_urls = []
                    else:
                        destination_urls = list({slide["urlLeft"], slide["urlRight"]})
                    picture_url = slide["imgBackgroundDesktopUrl"]

                    banners.append(
                        {
                            "url": url,
                            "picture_url": picture_url,
                            "destination_urls": destination_urls,
                            "key": picture_url,
                            "position": idx + 1,
                            "section": section,
                            "subsection": subsection,
                            "type": subsection_type,
                        }
                    )
            elif subsection_type == bs.SUBSECTION_TYPE_MOSAIC:
                session = requests.Session(impersonate="chrome120")
                soup = BeautifulSoup(session.get(url).text, "lxml")
                banner = soup.find("div", "fb-huincha-main-wrap")

                if not banner:
                    print("No banner for " + url)
                    continue

                image_url = banner.find("source")["srcset"]
                dest_url = banner.find("a")["href"]

                banners.append(
                    {
                        "url": url,
                        "picture_url": image_url,
                        "destination_urls": [dest_url],
                        "key": image_url,
                        "position": 1,
                        "section": section,
                        "subsection": subsection,
                        "type": subsection_type,
                    }
                )

        return banners

    @classmethod
    def _get_picture_urls(cls, session, product_id):
        pictures_resource_url = (
            "https://falabella.scene7.com/is/image/"
            "Falabella/{}?req=set,json".format(product_id)
        )
        pictures_response = session.get(pictures_resource_url, timeout=30).text
        pictures_json = json.loads(
            re.search(r's7jsonResponse\((.+),""\);', pictures_response).groups()[0]
        )

        picture_urls = []

        picture_entries = pictures_json["set"]["item"]
        if not isinstance(picture_entries, list):
            picture_entries = [picture_entries]

        for picture_entry in picture_entries:
            picture_url = (
                "https://falabella.scene7.com/is/image/{}?"
                "wid=1500&hei=1500&qlt=70".format(picture_entry["i"]["n"])
            )
            picture_urls.append(picture_url)

        return picture_urls

    @classmethod
    def reviews_for_sku(cls, sku):
        print(sku)
        session = session_with_proxy(None)
        reviews = []
        offset = 0

        while True:
            print(offset)
            endpoint = (
                "https://api.bazaarvoice.com/data/batch.json?"
                "passkey=m8bzx1s49996pkz12xvk6gh2e&apiversion="
                "5.5&resource.q0=reviews&filter.q0=isratings"
                "only%3Aeq%3Afalse&filter.q0=productid%3Aeq"
                "%3A{}&limit.q0=100&offset.q0={}".format(sku, offset)
            )
            response = session.get(endpoint).json()["BatchedResults"]["q0"]["Results"]

            if not response:
                break

            for entry in response:
                review_date = parse(entry["SubmissionTime"])

                review = {
                    "store": "Falabella",
                    "sku": sku,
                    "rating": float(entry["Rating"]),
                    "text": entry["ReviewText"],
                    "date": review_date.isoformat(),
                }

                reviews.append(review)

            offset += 100

        return reviews

    @classmethod
    def preflight(cls, extra_args=None):
        sample_url = (
            "https://www.falabella.com/falabella-cl/category/cat1012/TV-y-Video"
        )
        session = cls.get_session(extra_args)
        response = session.get(sample_url)
        soup = BeautifulSoup(response.text, "lxml")
        script = soup.find("script", {"id": "__NEXT_DATA__"})
        json_data = json.loads(script.text)
        zones = json_data["props"]["appCtx"]["zones"]
        return {"zones": zones}
