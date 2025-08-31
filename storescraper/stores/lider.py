import json
import validators
from decimal import Decimal
from pathlib import Path
from storescraper.categories import (
    SPLIT_AIR_CONDITIONER,
    CELL,
    DISH_WASHER,
    EXTERNAL_STORAGE_DRIVE,
    GAMING_CHAIR,
    KEYBOARD,
    ACCESORIES,
    MEMORY_CARD,
    MONITOR,
    NOTEBOOK,
    MOUSE,
    HEADPHONES,
    OVEN,
    PRINTER,
    REFRIGERATOR,
    SOLID_STATE_DRIVE,
    STEREO_SYSTEM,
    TABLET,
    TELEVISION,
    USB_FLASH_DRIVE,
    VACUUM_CLEANER,
    VIDEO_GAME_CONSOLE,
    WASHING_MACHINE,
    WEARABLE,
    PRINTER_SUPPLY,
    IRON,
    HAIR_CARE,
)
from storescraper.product import Product
from storescraper.store import Store
from storescraper.utils import (
    html_to_markdown,
    remove_words,
    cf_session_with_proxy,
)
from storescraper import banner_sections as bs


class Lider(Store):
    preferred_discover_urls_concurrency = 3
    preferred_products_for_url_concurrency = 3
    USER_AGENTS = [
        # "chrome99",
        # "chrome100",
        # "chrome101",
        # "chrome104",
        # "chrome107",
        # "chrome110",
        # "chrome116",
        # "chrome119",
        # "chrome120",
        # "chrome123",
        # "chrome124",
        # ----
        "chrome131",
        "chrome133a",
        "chrome136",
        "chrome99_android",
        "chrome131_android",
        "edge99",
        "edge101",
        "safari153",
        "safari155",
        "safari170",
        "safari172_ios",
        "safari180",
        "safari180_ios",
        "safari184",
        "safari184_ios",
        "safari260",
        "safari260_ios",
        "firefox133",
    ]

    tenant = "catalogo"
    category_paths = [
        # TECNO
        ["66849718_44699651", TELEVISION, "Tecno > TV"],
        ["66849718_44699651_73841472", TELEVISION, "Tecno > TV > Smart TV"],
        [
            "66849718_44699651_99349146",
            TELEVISION,
            "Tecno > TV > Smart TV Hasta 50 Pulgadas",
        ],
        [
            "66849718_44699651_60780062",
            TELEVISION,
            "Tecno > TV > Smart TV Sobre 50 Pulgadas",
        ],
        ["66849718_44699651_64332442", STEREO_SYSTEM, "Tecno > TV > Home Theater"],
        # ["66849718_44699651_68838150", PROJECTOR, "Tecno > TV > Proyectores"],
        ["66849718_14621386", STEREO_SYSTEM, "Tecno > Audio"],
        [
            "66849718_14621386_88231649",
            STEREO_SYSTEM,
            "Tecno > Audio > Equipos de Música y Karaoke",
        ],
        [
            "66849718_14621386_95114916",
            STEREO_SYSTEM,
            "Tecno > Audio > Equipos de Música y Karaoke",
        ],
        ["66849718_14621386_49644492", STEREO_SYSTEM, "Tecno > Audio > Audio Portable"],
        [
            "66849718_14621386_25354977",
            STEREO_SYSTEM,
            "Tecno > Audio > Micro y Mini Componentes",
        ],
        ["66849718_14621386_31940338", HEADPHONES, "Tecno > Audio > Audífonos"],
        [
            "66849718_14621386_27642866",
            STEREO_SYSTEM,
            "Tecno > Audio > Tornamesas y Vinilos",
        ],
        ["66849718_14621386_98336174", STEREO_SYSTEM, "Tecno > Audio > Audio HI-FI"],
        [
            "66849718_80980590_45869788",
            VIDEO_GAME_CONSOLE,
            "Tecno > Videojuegos > Consolas",
        ],
        [
            "66849718_80980590_97449970",
            VIDEO_GAME_CONSOLE,
            "Tecno > Videojuegos > Nintendo",
        ],
        [
            "66849718_80980590_45368401",
            VIDEO_GAME_CONSOLE,
            "Tecno > Videojuegos > PlayStation",
        ],
        [
            "66849718_80980590_47691134",
            VIDEO_GAME_CONSOLE,
            "Tecno > Videojuegos > XBOX",
        ],
        # CELULARES
        ["34388900_60412644", CELL, "Celulares > Celulares y Teléfonos"],
        ["34388900_13662451", WEARABLE, "Celulares > Smartwatches y Wearables"],
        # COMPUTACION
        [
            "89057520_72573679_94067303",
            NOTEBOOK,
            "Computación > Computadores > Notebooks",
        ],
        ["89057520_72573679_62826909", TABLET, "Computación > Computadores > Tablets"],
        # [
        #     "89057520_72573679_56612565",
        #     ALL_IN_ONE,
        #     "Computación > Computadores > Computadores All in One",
        # ],
        [
            "89057520_28386364_21832538",
            MONITOR,
            "Computación > Accesorios Computación > Monitores y Proyectores",
        ],
        [
            "89057520_28386364",
            MOUSE,
            "Computación > Computadores > Accesorios Computación",
        ],
        [
            "89057520_92341690_33654871",
            NOTEBOOK,
            "Computación > Mundo Gamer > Computación Gamer",
        ],
        [
            "89057520_92341690_99170494",
            KEYBOARD,
            "Computación > Mundo Gamer > Mouse y Teclados",
        ],
        [
            "89057520_92341690_27961626",
            HEADPHONES,
            "Computación > Mundo Gamer > Audífonos",
        ],
        [
            "89057520_92341690_04804406",
            GAMING_CHAIR,
            "Computación > Mundo Gamer > Sillas Gamer",
        ],
        [
            "89057520_18938454_77669169",
            PRINTER,
            "Computación > Impresión > Impresoras y Multifuncionales",
        ],
        [
            "89057520_98848773_69232935",
            EXTERNAL_STORAGE_DRIVE,
            "Computación > Almacenamiento > Discos Duros",
        ],
        [
            "89057520_98848773_37896447",
            SOLID_STATE_DRIVE,
            "Computación > Almacenamiento > Discos Duros SSD",
        ],
        [
            "89057520_98848773_32568051",
            MEMORY_CARD,
            "Computación > Almacenamiento > Tarjetas de Memoria",
        ],
        [
            "89057520_98848773_93306813",
            USB_FLASH_DRIVE,
            "Computación > Almacenamiento > Pendrives",
        ],
        # ELECTROHOGAR
        ["23989399_93795889", REFRIGERATOR, "Electrohogar > Refrigeración"],
        [
            "23989399_93795889_28605677",
            REFRIGERATOR,
            "Electrohogar > Refrigeración > No Frost",
        ],
        [
            "23989399_93795889_24472802",
            REFRIGERATOR,
            "Electrohogar > Refrigeración > Frio Directo",
        ],
        [
            "23989399_93795889_98442409",
            REFRIGERATOR,
            "Electrohogar > Refrigeración > Side By Side",
        ],
        [
            "23989399_93795889_83823051",
            REFRIGERATOR,
            "Electrohogar > Refrigeración > Freezer",
        ],
        [
            "23989399_93795889_10449779",
            REFRIGERATOR,
            "Electrohogar > Refrigeración > Frigobar",
        ],
        ["23989399_75788044", WASHING_MACHINE, "Electrohogar > Lavado y Planchado"],
        [
            "23989399_75788044_27277508",
            WASHING_MACHINE,
            "Electrohogar > Lavado y Planchado > Lavadoras",
        ],
        [
            "23989399_75788044_75760841",
            WASHING_MACHINE,
            "Electrohogar > Lavado y Planchado > Lavadoras Secadoras",
        ],
        [
            "23989399_75788044_83679483",
            WASHING_MACHINE,
            "Electrohogar > Lavado y Planchado > Secadoras",
        ],
        [
            "23989399_75788044_84624586",
            DISH_WASHER,
            "Electrohogar > Lavado y Planchado > Lavavajillas",
        ],
        ["23989399_85011192", VACUUM_CLEANER, "Electrohogar > Aspiradoras y Limpieza"],
        [
            "23989399_53512871_73118366",
            OVEN,
            "Electrohogar > Electrodomésticos Cocina > Hornos Eléctricos",
        ],
        [
            "23989399_53512871_12048011",
            OVEN,
            "Electrohogar > Electrodomésticos Cocina > Microondas",
        ],
        [
            "23989399_74640407_68912278",
            OVEN,
            "Electrohogar > Cocinas > Hornos Empotrables",
        ],
        # [
        #     "Climatización/Calefacción",
        #     SPACE_HEATER,
        #     "Electrohogar > Climatización > Calefacción"
        # ],
        [
            "23989399_29216192_32962208",
            SPLIT_AIR_CONDITIONER,
            "Electrohogar > Climatización > Ventilación",
        ],
        # [
        #     "Climatización/Calefacción/Termos y Calefonts",
        #     WATER_HEATER,
        #     "Electrohogar > Climatización > Calefacción > Termos y Calefonts"
        # ],
        ["23989399_53512871", ACCESORIES, "Electrohogar > Electrodomésticos Cocina"],
        [
            "89057520_18938454_30849678",
            PRINTER_SUPPLY,
            "Computación > Impresión > Tintas y Toners",
        ],
        [
            "23989399_75788044_32008261",
            IRON,
            "Electrohogar > Lavado y Planchado > Planchado",
        ],
        [
            "59721722_76091226_92571610",
            HAIR_CARE,
            "Belleza y Cuidado Personal > Cuidado Personal > Secadores de Pelo",
        ],
        [
            "59721722_76091226_89836448",
            HAIR_CARE,
            "Belleza y Cuidado Personal > Cuidado Personal > Alisadores y Onduladores",
        ],
    ]

    @classmethod
    def categories(cls):
        cats = []
        for _, local_category, _ in cls.category_paths:
            if local_category not in cats:
                cats.append(local_category)
        return cats

    @classmethod
    def discover_urls_for_category(cls, category, extra_args=None):
        url = cls.generate_discover_url_for_category(category)
        return [url]

    @classmethod
    def discover_urls_for_keyword(cls, keyword, threshold, extra_args=None):
        extra_args = extra_args or {}
        extra_args["impersonate"] = "chrome"
        session = cf_session_with_proxy(extra_args)
        session.headers["tenant"] = cls.tenant
        product_urls = []

        query_url = (
            "https://529cv9h7mw-dsn.algolia.net/1/indexes/*/"
            "queries?x-algolia-application-id=529CV9H7MW&x-"
            "algolia-api-key=c6ab9bc3e19c260e6bad42abe143d5f4"
        )

        query_params = {
            "requests": [
                {
                    "indexName": "campaigns_production",
                    "params": "query={}&hitsPerPage=1000".format(keyword),
                }
            ]
        }

        response = session.post(query_url, json.dumps(query_params))
        data = json.loads(response.text)

        if not data["results"][0]["hits"]:
            return []

        for entry in data["results"][0]["hits"]:
            product_url = "https://www.lider.cl/catalogo/product/sku/{}/{}".format(
                entry["sku"], entry.get("slug", "a")
            )
            product_urls.append(product_url)

            if len(product_urls) == threshold:
                return product_urls

        return product_urls

    @classmethod
    def products_for_url(cls, url, category=None, extra_args=None):
        print(url)
        seen_urls = set()

        if not category:
            category = url.split("?category=")[1]

        for category_id, local_category, _ in cls.category_paths:
            if category != local_category:
                continue

            for product in cls._get_products(
                category_id,
                local_category,
                exclude_marketplace=True,
                extra_args=extra_args,
            ):
                if product not in seen_urls:
                    seen_urls.add(product)
                    yield product

    @classmethod
    def banners(cls, extra_args=None):
        extra_args = extra_args or {}
        base_url = "https://apps.lider.cl/catalogo/bff/banners?v=2"
        destination_url_base = "https://www.lider.cl/{}"
        extra_args["impersonate"] = "chrome"
        session = cf_session_with_proxy(extra_args)
        banners = []
        response = session.get(base_url)

        banners_json = json.loads(response.text)
        sliders = banners_json["bannersHome"]

        for idx, slider in enumerate(sliders):
            destination_urls = [destination_url_base.format(slider["link"])[:250]]
            picture_url = slider["backgroundDesktop"]
            if not picture_url.startswith("http"):
                picture_url = "https://apps.lider.cl/landing/" + picture_url

            banners.append(
                {
                    "url": destination_url_base.format(""),
                    "picture_url": picture_url,
                    "destination_urls": destination_urls,
                    "key": picture_url,
                    "position": idx + 1,
                    "section": bs.HOME,
                    "subsection": bs.HOME,
                    "type": bs.SUBSECTION_TYPE_HOME,
                }
            )

        if not banners:
            raise Exception(
                "No banners for Home section: " + destination_url_base.format("")
            )

        return banners

    @classmethod
    def _get_products(
        cls, category_id, local_category, exclude_marketplace, extra_args=None
    ):
        print(category_id)
        query_url = "https://www.lider.cl/orchestra/graphql/browse"
        path = Path(__file__).with_name("lider_request.txt")

        with path.open("r") as f:
            graphql_query = f.read()

        discovery_url = cls.generate_discover_url_for_category(local_category)
        page = 1

        while True:
            print(page)
            graphql_variables = {
                "page": page,
                "prg": "desktop",
                "catId": category_id,
                "sort": "best_match",
                "ps": 44,
                "fetchMarquee": True,
                "fetchSkyline": True,
                "fetchSbaTop": False,
                "fetchGallery": False,
                "fetchDac": False,
                "tenant": "CHILE_EA_GLASS",
                "enablePromoData": True,
            }

            if exclude_marketplace:
                graphql_variables["facet"] = "ss_sellertype:Lider"

            graphql_request_body = {
                "query": graphql_query,
                "variables": graphql_variables,
            }

            for impersonator in cls.USER_AGENTS:
                print("Trying " + impersonator)
                extra_args = extra_args or {}
                extra_args["impersonate"] = impersonator
                session = cf_session_with_proxy(extra_args)

                session.headers.update(
                    {
                        "Content-Type": "application/json",
                        "x-o-bu": "LIDER-CL",
                        "x-o-mart": "B2C",
                        "x-o-vertical": "EA",
                        "X-APOLLO-OPERATION-NAME": "Browse",
                    }
                )

                response = session.post(query_url, json=graphql_request_body)
                try:
                    data = json.loads(response.text)
                    break
                except Exception:
                    continue
            else:
                raise Exception("No user agents left")
            products_data = data["data"]["search"]["searchResult"]["itemStacks"][0][
                "itemsV2"
            ]

            if not products_data:
                break

            for entry in products_data:
                product_url = f"https://www.lider.cl{entry['canonicalUrl']}"
                name = f"{entry['brand']} {entry['name']}"
                key = entry["offerId"]
                price_info = entry["priceInfo"]
                normal_price = Decimal(price_info["currentPrice"]["price"])
                offer_price = normal_price
                promo_data = [
                    promo_entry
                    for promo_entry in entry["promoData"]
                    if promo_entry["type"] == "liderBCI"
                ]

                if promo_data:
                    assert len(promo_data) == 1
                    offer_price = Decimal(
                        remove_words(
                            promo_data[0]["templateData"]["priceString"].split(".")[0]
                        )
                    )

                sku = entry["usItemId"]
                picture_urls = [
                    img["url"]
                    for img in entry["imageInfo"]["allImages"]
                    if validators.url(img["url"])
                ]
                seller_name = entry["sellerName"]
                seller = None if seller_name == "Lider" else seller_name
                stock = (
                    -1
                    if (
                        entry["availabilityStatusV2"]["value"] == "IN_STOCK"
                        and seller_name == "Lider"
                    )
                    else 0
                )
                description_value = entry["shortDescription"]
                description = (
                    html_to_markdown(description_value) if description_value else None
                )

                product = Product(
                    name,
                    cls.__name__,
                    local_category,
                    product_url,
                    discovery_url,
                    key,
                    stock,
                    normal_price,
                    offer_price,
                    "CLP",
                    sku=sku,
                    picture_urls=picture_urls,
                    description=description,
                    seller=seller,
                )

                yield product

            page += 1

    @classmethod
    def sections(cls):
        return [section for _, _, section in cls.category_paths]

    @classmethod
    def section_positions(cls, section, extra_args=None):
        for category_id, local_category, section_path in cls.category_paths:
            if section != section_path:
                continue

            for idx, product in enumerate(
                cls._get_products(
                    category_id,
                    local_category,
                    exclude_marketplace=False,
                    extra_args=extra_args,
                )
            ):
                if idx >= 300:
                    break

                yield {
                    "field": "key",
                    "value": product.key,
                    "position": idx + 1,
                    "section": section,
                    "is_sponsored": False,
                }

    @classmethod
    def generate_discover_url_for_category(cls, category):
        return "https://www.lider.cl/?category={}".format(category)
