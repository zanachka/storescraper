import logging
import time
from collections import defaultdict
from decimal import Decimal
from bs4 import BeautifulSoup
import validators
from storescraper.categories import (
    ALL_IN_ONE,
    TELEVISION,
    VACUUM_CLEANER,
    WATER_HEATER,
    STOVE,
    STEREO_SYSTEM,
    HEADPHONES,
    CELL,
    WEARABLE,
    TABLET,
    NOTEBOOK,
    VIDEO_GAME_CONSOLE,
    PRINTER,
    MONITOR,
    SOLID_STATE_DRIVE,
    PROJECTOR,
    MOUSE,
    REFRIGERATOR,
    WASHING_MACHINE,
    DISH_WASHER,
    OVEN,
    SPACE_HEATER,
    SPLIT_AIR_CONDITIONER,
    ACCESORIES,
    PRINTER_SUPPLY,
    PERFUME,
    USB_FLASH_DRIVE,
    MEMORY_CARD,
    AIR_FRYER,
    BLENDER,
    COFFE_MAKER,
    COOKING_ROBOT,
    JUICER,
    KETTLE,
    ELECTRIC_GRILL,
    FOOD_PROCESSOR,
    SANDWICH_MAKER,
    ELECTRIC_POT,
    IRON,
    HAIR_CARE,
)
from storescraper.product import Product
from storescraper.store import Store
from storescraper.utils import html_to_markdown, session_with_proxy
from storescraper import banner_sections as bs


class Paris(Store):
    USER_AGENT = "solotodobot"
    RESULTS_PER_PAGE = 200

    category_paths = [
        ["tecnologia/computadores/ipad-tablet/", TABLET],
        ["electro/audio/audifonos/", HEADPHONES],
        ["electro/audio/parlantes-bluetooth-portables/", STEREO_SYSTEM],
        ["electro/television/", TELEVISION],
        ["electro/television/smart-tv/", TELEVISION],
        ["electro/television/televisores-led/", TELEVISION],
        ["television/televisores-oled-qled/", TELEVISION],
        ["electro/television/soundbar-home-theater/", STEREO_SYSTEM],
        ["electro/audio/", STEREO_SYSTEM],
        ["electro/audio/micro-minicomponentes/", STEREO_SYSTEM],
        ["electro/audio/audifonos-inalambricos/", HEADPHONES],
        ["electro/audio-hifi/", STEREO_SYSTEM],
        ["electro/audio-hifi/audifonos/", HEADPHONES],
        ["electro/audio-hifi/home-theater/", STEREO_SYSTEM],
        ["electro/audio-hifi/audio/", STEREO_SYSTEM],
        ["electro/audio-hifi/parlantes/", STEREO_SYSTEM],
        ["electro/elige-tu-pulgada/", TELEVISION],
        ["electro/elige-tu-pulgada/30-a-39-pulgadas/", TELEVISION],
        ["electro/elige-tu-pulgada/40-a-49-pulgadas/", TELEVISION],
        ["electro/elige-tu-pulgada/50-a-59-pulgadas/", TELEVISION],
        ["electro/elige-tu-pulgada/60-o-mas-pulgadas/", TELEVISION],
        ["electro/elige-tu-pulgada/70-o-mas-pulgadas/", TELEVISION],
        ["tecnologia/celulares/", CELL],
        ["tecnologia/celulares/smartphone/", CELL],
        ["tecnologia/celulares/iphone/", CELL],
        ["tecnologia/celulares/samsung/", CELL],
        ["tecnologia/celulares/xiaomi/", CELL],
        ["tecnologia/celulares/motorola/", CELL],
        ["tecnologia/celulares/honor/", CELL],
        ["tecnologia/celulares/vivo/", CELL],
        ["tecnologia/celulares/basicos/", CELL],
        ["tecnologia/celulares/oppo/", CELL],
        ["tecnologia/computadores/desktop-all-in-one", ALL_IN_ONE],
        ["tecnologia/computadores/notebooks/", NOTEBOOK],
        ["tecnologia/computadores/ipad-tablet/", TABLET],
        ["tecnologia/computadores/tablets-ninos/", TABLET],
        ["tecnologia/computadores/apple/", NOTEBOOK],
        ["tecnologia/wearables/", WEARABLE],
        ["tecnologia/wearables/smartwatches/", WEARABLE],
        ["tecnologia/wearables/smartwatches-ninos/", WEARABLE],
        ["tecnologia/wearables/smartband/", WEARABLE],
        ["tecnologia/consolas-videojuegos/", VIDEO_GAME_CONSOLE],
        ["tecnologia/consolas-videojuegos/playstation-marca/", VIDEO_GAME_CONSOLE],
        ["tecnologia/consolas-videojuegos/nintendo-marca/", VIDEO_GAME_CONSOLE],
        ["tecnologia/consolas-videojuegos/xbox-marca/", VIDEO_GAME_CONSOLE],
        ["tecnologia/impresoras/", PRINTER],
        ["tecnologia/impresoras/laser/", PRINTER],
        ["tecnologia/impresoras/tinta/", PRINTER],
        ["tecnologia/impresoras/termicas-portatiles/", PRINTER],
        ["tecnologia/impresoras/impresoras-3d/", PRINTER],
        ["tecnologia/impresoras/impresion-industrial/", PRINTER],
        ["tecnologia/impresoras/rotuladores/", PRINTER],
        ["tecnologia/accesorios-computacion/", ACCESORIES],
        ["tecnologia/accesorios-computacion/otros/", ACCESORIES],
        ["tecnologia/accesorios-computacion/monitor-gamer/", MONITOR],
        ["tecnologia/accesorios-computacion/disco-duro/", SOLID_STATE_DRIVE],
        ["tecnologia/accesorios-computacion/proyectores/", PROJECTOR],
        ["tecnologia/accesorios-computacion/mouse-teclados/", MOUSE],
        ["tecnologia/accesorios-computacion/audifonos-microfonos/", HEADPHONES],
        ["tecnologia/accesorios-computacion/pendrives/", USB_FLASH_DRIVE],
        ["tecnologia/computadores/pc-gamer/", NOTEBOOK],
        # ["tecnologia/gamer/teclados/", KEYBOARD],
        # ["tecnologia/gamer/headset/", HEADPHONES],
        # ["tecnologia/gamer/sillas-escritorios-gamer/", GAMING_CHAIR],
        # ["tecnologia/gamer/gabinetes/", COMPUTER_CASE],
        ["tecnologia/gamer/monitores/", MONITOR],
        ["tecnologia/accesorios-fotografia/tarjetas-memoria/", MEMORY_CARD],
        [
            "linea-blanca/electrodomesticos/?tipoProductoAll=Freidoras de Aire",
            AIR_FRYER,
        ],
        ["linea-blanca/electrodomesticos/batidoras-licuadoras/", BLENDER],
        ["linea-blanca/electrodomesticos/cafeteras/", COFFE_MAKER],
        ["linea-blanca/electrodomesticos/robot-cocina/", COOKING_ROBOT],
        ["linea-blanca/electrodomesticos/sacajugos-exprimidores/", JUICER],
        ["linea-blanca/electrodomesticos/hervidores/", KETTLE],
        ["linea-blanca/electrodomesticos/parrillas-electricas/", ELECTRIC_GRILL],
        ["linea-blanca/electrodomesticos/procesadores-picadoras/", FOOD_PROCESSOR],
        ["linea-blanca/electrodomesticos/tostadores-sandwicheras/", SANDWICH_MAKER],
        [
            "linea-blanca/electrodomesticos/arroceras-vaporeras-freidoras",
            ELECTRIC_POT,
        ],
        ["linea-blanca/electrodomesticos/otros-articulos/", ACCESORIES],
        ["linea-blanca/cocina/campanas/", ACCESORIES],
        ["linea-blanca/refrigeracion/", REFRIGERATOR],
        ["linea-blanca/refrigeracion/freezer/", REFRIGERATOR],
        [
            "linea-blanca/refrigeracion/refrigeradores/refrigerador-side-by-side/",
            REFRIGERATOR,
        ],
        ["linea-blanca/refrigeracion/refrigeradores/", REFRIGERATOR],
        ["linea-blanca/refrigeracion/no-frost/", REFRIGERATOR],
        ["linea-blanca/refrigeracion/frigobar-cavas/", REFRIGERATOR],
        # ["linea-blanca/equipamiento-industrial/refrigeracion/", REFRIGERATOR],
        ["linea-blanca/lavado-secado/", WASHING_MACHINE],
        [
            "linea-blanca/lavado-secado/lavadoras-carga-frontal",
            WASHING_MACHINE,
        ],
        [
            "linea-blanca/lavado-secado/lavadoras-carga-superior",
            WASHING_MACHINE,
        ],
        ["linea-blanca/lavado-secado/todas/", WASHING_MACHINE],
        ["linea-blanca/lavado-secado/lavadoras-secadoras/", WASHING_MACHINE],
        ["linea-blanca/lavado-secado/secadoras-centrifugas/", WASHING_MACHINE],
        ["linea-blanca/lavado-secado/lavavajillas/", DISH_WASHER],
        ["linea-blanca/cocina/", STOVE],
        ["linea-blanca/cocina/cocinas/", STOVE],
        ["linea-blanca/cocina/encimeras/", STOVE],
        ["linea-blanca/cocina/hornos-empotrables/", OVEN],
        ["linea-blanca/cocina/kit-empotrables/", STOVE],
        ["linea-blanca/electrodomesticos/microondas/", OVEN],
        ["linea-blanca/electrodomesticos/hornos-electricos/", OVEN],
        ["linea-blanca/estufas/", SPACE_HEATER],
        ["linea-blanca/estufas/electricas/", SPACE_HEATER],
        ["linea-blanca/estufas/parafina/", SPACE_HEATER],
        ["linea-blanca/estufas/gas/", SPACE_HEATER],
        ["linea-blanca/estufas/lena-pellets/", SPACE_HEATER],
        ["linea-blanca/estufas/calefaccion-exterior/", SPACE_HEATER],
        ["linea-blanca/estufas/calefones-termos/", WATER_HEATER],
        ["linea-blanca/electrodomesticos/aspiradoras-enceradoras/", VACUUM_CLEANER],
        ["linea-blanca/aspirado-limpieza/aspiradoras-arrastre/", VACUUM_CLEANER],
        ["linea-blanca/aspirado-limpieza/aspiradoras-robot/", VACUUM_CLEANER],
        ["linea-blanca/aspirado-limpieza/aspiradoras-verticales/", VACUUM_CLEANER],
        ["linea-blanca/climatizacion/", SPLIT_AIR_CONDITIONER],
        # [
        #    "linea-blanca/estufas/calefactores-split/",
        #    SPLIT_AIR_CONDITIONER,
        #    1,
        # ],
        [
            "linea-blanca/calefaccion/aire-acondicionado/",
            SPLIT_AIR_CONDITIONER,
        ],
        ["linea-blanca/climatizacion/ventilacion/", SPLIT_AIR_CONDITIONER],
        ["linea-blanca/electrodomesticos/", ACCESORIES],
        ["tecnologia/impresoras/insumos-accesorios/", PRINTER_SUPPLY],
        ["belleza/perfumes/", PERFUME],
        ["outlet/outlet-electro/outlet-televisores/", TELEVISION],
        ["outlet/outlet-electro/outlet-audio/", HEADPHONES],
        ["outlet/outlet-electro/outlet-hifi/", STEREO_SYSTEM],
        ["outlet/outlet-linea-blanca/outlet-refrigeracion/", REFRIGERATOR],
        # ["outlet/outlet-linea-blanca/outlet-lavadoras/", WASHING_MACHINE],
        # ["outlet/outlet-linea-blanca/outlet-cocinas/", STOVE],
        # ["outlet/outlet-linea-blanca/outlet-calefaccion/", SPACE_HEATER],
        # ["outlet/outlet-linea-blanca/outlet-electrodomesticos/", ACCESORIES],
        ["outlet/outlet-tecno/outlet-celulares/", CELL],
        ["outlet/outlet-tecno/outlet-computadores/", NOTEBOOK],
        ["outlet/outlet-tecno/outlet-ipads-y-tablets/", TABLET],
        ["outlet/outlet-tecno/outlet-impresoras/", PRINTER_SUPPLY],
        ["outlet/outlet-tecno/outlet-smartwatch/", WEARABLE],
        ["linea-blanca/electrodomesticos/planchas/", IRON],
        [
            "belleza/cuidado-capilar/?tipoProductoAll=Cepillos Alisadores,Alisadores de Pelo,Secadores de Pelo,Onduladores de Pelo",
            HAIR_CARE,
        ],
    ]

    @classmethod
    def categories(cls):
        cats = []
        for entry in cls.category_paths:
            assert len(entry) == 2, entry
            cat = entry[1]
            if cat not in cats:
                cats.append(cat)

        return cats

    @classmethod
    def discover_entries_for_category(cls, category, extra_args=None):
        fast_mode = extra_args and extra_args.get("fast_mode", False)

        session = session_with_proxy(extra_args)
        product_entries = defaultdict(lambda: [])

        for category_path, local_category, weight in cls.category_paths:
            if local_category != category:
                continue

            base_url = "https://www.paris.cl/" + category_path
            logging.info("Obtaining base section data from " + base_url)
            retries = 0

            while retries < 2:
                response = session.get(base_url)

                if response.url == "https://www.paris.cl/404":
                    raise Exception("Invalid section: " + category_path)

                if "<h2>Estamos mejorando tu experiencia</h2>" in response.text:
                    retries += 1
                    time.sleep(30)
                else:
                    break

            soup = BeautifulSoup(response.text, "lxml")
            breadcrumbs_tag = soup.find("nav", {"aria-label": "breadcrumb"})

            if not breadcrumbs_tag:
                raise Exception(f"{base_url}, {response.status_code}, {response.text}")

            breadcrumbs = []

            for link_tag in breadcrumbs_tag.find_all("a"):
                breadcrumbs.append(link_tag.text.strip())

            breadcrumbs.append(soup.find("span", {"aria-current": "page"}).text.strip())
            section_name = " > ".join(breadcrumbs)
            category_group_id = soup.find("div", {"data-cnstrc-filter-value": True})[
                "data-cnstrc-filter-value"
            ]

            page = 1

            while True:
                if page > (15000 / cls.RESULTS_PER_PAGE):
                    raise Exception("Page overflow: " + category_path)

                payload = {
                    "filters": [
                        {"key": "group_id", "stringValues": [category_group_id]}
                    ],
                    "pagination": {"page": page, "pageSize": cls.RESULTS_PER_PAGE},
                    "sortBy": "relevance",
                    "serviceAbility": {
                        "sameDayDelivery": False,
                        "nextDayDelivery": False,
                        "storePickUp": False,
                    },
                    "sponsoredProducts": True,
                }

                if "tipoProductoAll=" in category_path:
                    payload["filters"].append(
                        {
                            "key": "tipoProductoAll",
                            "stringValues": category_path.split("?tipoProductoAll=")[
                                -1
                            ].split(","),
                        }
                    )

                if fast_mode:
                    payload["filters"].append(
                        {"key": "isMarketplace", "stringValues": ["false"]}
                    )

                response = session.post(
                    "https://be-paris-backend-cl-ms-api.ccom.paris.cl/products/",
                    json=payload,
                )

                json_response = response.json()
                containers_data = json_response["results"]

                if not containers_data:
                    break

                for idx, container in enumerate(containers_data):
                    product_url = (
                        f"https://www.paris.cl/{container['slug']['es-CL']}.html"
                    )

                    product_entries[product_url].append(
                        {
                            "category_weight": weight,
                            "section_name": section_name,
                            "value": cls.RESULTS_PER_PAGE * (page - 1) + idx + 1,
                        }
                    )

                page += 1

        if fast_mode:
            # Since the fast mode filters the results, it messes up the position data, so remove it altogether
            for url in product_entries.keys():
                product_entries[url] = []
        return product_entries

    @classmethod
    def discover_urls_for_keyword(cls, keyword, threshold, extra_args=None):
        session = session_with_proxy(extra_args)
        session.headers["User-Agent"] = cls.USER_AGENT
        product_urls = []

        page = 0

        while True:
            if page > 40:
                raise Exception("Page overflow")

            search_url = "https://www.paris.cl/search?q={}&sz={}&start={}".format(
                keyword, cls.RESULTS_PER_PAGE, page * cls.RESULTS_PER_PAGE
            )

            soup = BeautifulSoup(session.get(search_url).text, "lxml")
            containers = soup.findAll("li", "flex-item-products")

            if not containers:
                break

            for container in containers:
                product_url = container.find("a")["href"].split("?")[0]
                if "https" not in product_url:
                    product_url = "https://www.paris.cl" + product_url

                product_urls.append(product_url)

                if len(product_urls) == threshold:
                    return product_urls

            page += 1

        return product_urls

    @classmethod
    def products_for_url(cls, url, category=None, extra_args=None):
        print(url)
        session = session_with_proxy(extra_args)
        session.headers["User-Agent"] = cls.USER_AGENT
        search_term = url.split("-")[-1].replace(".html", "")

        payload = {"term": search_term, "pagination": {"pageSize": 30}}
        response = session.post(
            "https://be-paris-backend-cl-ms-api.ccom.paris.cl/products/",
            json=payload,
        )

        json_response = response.json()

        if not json_response["results"]:
            return []

        if len(json_response["results"]) == 1:
            product_data = json_response["results"][0]
        else:
            for entry in json_response["results"]:
                if entry["key"] == url.split("-")[-1].replace(".html", ""):
                    product_data = entry
                    break

        name = f"{product_data['brand']} {product_data['name']['es-CL']}"

        sellers = product_data["sellers"]
        assert len(sellers) == 1
        seller = sellers[0] if sellers[0] != "Paris" else None
        master_variant = product_data["masterVariant"]
        sku = master_variant["sku"]
        normal_price_key = "offer" if "offer" in master_variant["prices"] else "regular"
        normal_price = Decimal(
            master_variant["prices"][normal_price_key]["value"]["centAmount"]
        )
        if "paymentMethod" in master_variant["prices"]:
            offer_price = Decimal(
                master_variant["prices"]["paymentMethod"]["value"]["centAmount"]
            )
            if offer_price > normal_price:
                offer_price = normal_price
        else:
            offer_price = normal_price

        picture_urls = [x["url"] for x in master_variant["images"]]
        cleaned_picture_urls = []

        for picture_url in picture_urls:
            if validators.url(picture_url):
                cleaned_picture_urls.append(picture_url)

        stock = 0 if seller else -1

        if "description" in product_data:
            description = html_to_markdown(product_data["description"]["es-CL"])
        else:
            description = ""

        for attribute in master_variant.get("attributes", []):
            description += f"\n{attribute['name']}: {str(attribute['value'])}"

        review_count = product_data.get("countRating", 0)
        if "averageRating" in product_data:
            review_avg_score = float(product_data["averageRating"])
        else:
            review_avg_score = None

        if "REACONDICIONADO" in name.upper():
            condition = "https://schema.org/RefurbishedCondition"
        else:
            condition = "https://schema.org/NewCondition"

        p = Product(
            name[:200],
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
            description=description,
            picture_urls=cleaned_picture_urls,
            review_count=review_count,
            review_avg_score=review_avg_score,
            seller=seller,
            condition=condition,
        )

        return [p]

    @classmethod
    def banners(cls, extra_args=None):
        base_url = "https://www.paris.cl/"
        session = session_with_proxy(extra_args)
        session.headers["User-Agent"] = (
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
            "(KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36"
        )
        banners = []

        res = session.get(base_url)
        soup = BeautifulSoup(res.text, "lxml")
        slide_containers = soup.find_all("div", "flex-none rounded-lg relative")

        for idx, banner_entry in enumerate(slide_containers):
            destination_url = banner_entry.find("a")
            picture_url = destination_url.find("source")["srcset"]

            banners.append(
                {
                    "url": base_url,
                    "picture_url": picture_url,
                    "destination_urls": [destination_url["href"]],
                    "key": picture_url,
                    "position": idx + 1,
                    "section": bs.HOME,
                    "subsection": bs.HOME,
                    "type": bs.SUBSECTION_TYPE_HOME,
                }
            )

        if not banners:
            raise Exception("No banners for Home section: " + base_url)

        return banners
