import json
import logging

import re
import urllib
from decimal import Decimal
import urllib.parse

from bs4 import BeautifulSoup

from storescraper.categories import (
    ACCESORIES,
    CELL,
    NOTEBOOK,
    STEREO_SYSTEM,
    KEYBOARD,
    MOUSE,
    WEARABLE,
    TABLET,
    REFRIGERATOR,
    HEADPHONES,
    KEYBOARD_MOUSE_COMBO,
    VIDEO_GAME_CONSOLE,
    MONITOR,
    MEMORY_CARD,
    GAMING_CHAIR,
    POWER_SUPPLY,
    COMPUTER_CASE,
    USB_FLASH_DRIVE,
    RAM,
    TELEVISION,
    SPLIT_AIR_CONDITIONER,
    OVEN,
    WASHING_MACHINE,
    ALL_IN_ONE,
    VACUUM_CLEANER,
    PRINTER,
    MICROPHONE,
    VIDEO_CARD,
    MOTHERBOARD,
    PRINTER_SUPPLY,
    SOLID_STATE_DRIVE,
    PROCESSOR,
    CPU_COOLER,
    IRON,
    UPS,
    SPACE_HEATER,
    WATER_HEATER,
    BLENDER,
    FOOD_PROCESSOR,
    ELECTRIC_GRILL,
    COOKING_ROBOT,
    ELECTRIC_POT,
    MIXER,
    COFFE_MAKER,
    TOASTER,
    KETTLE,
    AIR_FRYER,
    JUICER,
    SANDWICH_MAKER,
    HAIR_CARE,
)
from storescraper.product import Product
from storescraper.store import Store
from storescraper.utils import chunks, cf_session_with_proxy


class MercadoLibreChile(Store):
    price_accuracy = "0"
    store = "all"
    categories_path = [
        (
            "celulares-telefonia/celulares-smartphones",
            CELL,
            "Celulares y Telefonía > Celulares y Smartphones",
        ),
        (
            "celulares-telefonia/accesorios-celulares/memorias",
            MEMORY_CARD,
            "Celulares y Telefonía > Accesorios para Celulares > Memorias",
        ),
        (
            "computacion/notebooks-accesorios/notebooks",
            NOTEBOOK,
            "Computación > Notebooks y Accesorios > Notebooks",
        ),
        (
            "computacion/tablets-accesorios/tablets",
            TABLET,
            "Computación > Tablets y Accesorios > Tablets",
        ),
        (
            "computacion/impresion/impresoras",
            PRINTER,
            "Computación > Impresión > Impresoras",
        ),
        (
            "computacion/almacenamiento/discos-accesorios/discos-duros-ssds",
            SOLID_STATE_DRIVE,
            "Computación > AlmacenamientoDiscos y Accesorios > Discos Duros y SSDs",
        ),
        (
            "electronica-audio-video/audio/audifonos",
            HEADPHONES,
            "Electrónica, Audio y Video > Audio > Audífonos",
        ),
        (
            "electronica-audio-video/audio/audio-portatil-accesorios",
            STEREO_SYSTEM,
            "Audio Portátil y Accesorios",
        ),
        (
            "electronica-audio-video/televisores",
            TELEVISION,
            "Electrónica, Audio y Video > Televisores",
        ),
        (
            "perifericos-pc-parlantes",
            STEREO_SYSTEM,
            "Computación > Periféricos de PC > Parlantes para PC",
        ),
        (
            "mouses-teclados-controles-kits-mouse-teclado",
            KEYBOARD_MOUSE_COMBO,
            "Mouses y Teclados Kits de Mouse y Teclado",
        ),
        (
            "computacion/perifericos-accesorios/mouses",
            MOUSE,
            "Computación > Periféricos de PC > Mouses y Teclados > Mouses",
        ),
        (
            "computacion/perifericos-accesorios/teclados",
            KEYBOARD,
            "Computación > Periféricos de PC > Mouses y Teclados > Teclados",
        ),
        (
            "celulares-telefonia/smartwatches-accesoriossmartwatch",
            WEARABLE,
            "Celulares y Telefonía > Smartwatches y Accesorios > Smartwatches",
        ),
        (
            "computacion/monitores-accesorios/monitores",
            MONITOR,
            "Computación > Monitores y Accesorios > Monitores",
        ),
        (
            "computacion/accesorios-pc-gaming/sillas-gamer",
            GAMING_CHAIR,
            "Computación > Accesorios para PC Gaming > Sillas Gamer",
        ),
        (
            "consolas-videojuegos/consolas/xbox-series",
            VIDEO_GAME_CONSOLE,
            "Consolas y Videojuegos > Consolas Xbox Series",
        ),
        (
            "consolas-videojuegos/consolas/playstation-4",
            VIDEO_GAME_CONSOLE,
            "Consolas y Videojuegos > Consolas PlayStation 4",
        ),
        (
            "consolas-videojuegos/consolas/playstation-5",
            VIDEO_GAME_CONSOLE,
            "Consolas y Videojuegos > Consolas PlayStation 5",
        ),
        (
            "consolas-videojuegos/consolas/switch",
            VIDEO_GAME_CONSOLE,
            "Consolas y Videojuegos > Consolas Switch",
        ),
        (
            "computacion/componentes-pc/fuentes-alimentacion/fuentes",
            POWER_SUPPLY,
            "Computación > Componentes de PC > Fuentes de Alimentación > Fuentes",
        ),
        (
            "computacion/componentes-pc/gabinetes-soportes-pc/gabinetes",
            COMPUTER_CASE,
            "Computación > Componentes de PC > Gabinetes y Soportes de PC > Gabinetes",
        ),
        (
            "computacion/componentes-pc/memorias-ram",
            RAM,
            "Computación > Componentes de PC > Memorias RAM",
        ),
        (
            "computacion/componentes-pc/procesadores",
            PROCESSOR,
            "Computación > Componentes de PC > Procesadores",
        ),
        (
            "computacion/componentes-pc/refrigeracion/coolers-ventiladores",
            CPU_COOLER,
            "Computación > Componentes de PC > Refrigeración > Coolers y Ventiladores > Refrigeración Coolers y Ventiladores",
        ),
        (
            "computacion/componentes-pc/tarjetas/placas-madre",
            MOTHERBOARD,
            "Computación > Componentes de PC > Tarjetas > Placas Madre > Tarjetas Placas Madre",
        ),
        (
            "computacion/componentes-pc/tarjetas/tarjetas-video",
            VIDEO_CARD,
            "Computación > Componentes de PC > Tarjetas > Tarjetas de Video",
        ),
        (
            "computacion/almacenamiento/pen-drives",
            USB_FLASH_DRIVE,
            "Computación > Almacenamiento > Pen Drives",
        ),
        (
            "mouses-teclados-controles-tabletas-digitalizadoras",
            TABLET,
            "Computación > Periféricos de PC > Mouses y Teclados > Tabletas Digitalizadoras",
        ),
        (
            "audio-home-theaters",
            STEREO_SYSTEM,
            "Electrónica, Audio y Video > Audio > Home Theaters",
        ),
        (
            "electronica-audio-video/audio/microfonos-preamplificadores/microfonos",
            MICROPHONE,
            "Electrónica, Audio y Video > Audio > Micrófonos y Preamplificadores > Micrófonos",
        ),
        (
            "electronica-audio-video/audio/parlantes-subwoofers",
            STEREO_SYSTEM,
            "Electrónica, Audio y Video > Audio > Parlantes y Subwoofers",
        ),
        (
            "electronica-audio-video/audio/torres-sonido",
            STEREO_SYSTEM,
            "Electrónica, Audio y Video > Audio > Torres de Sonido",
        ),
        (
            "electrodomesticos/climatizacion/aires-acondicionados",
            SPLIT_AIR_CONDITIONER,
            "Electrodomésticos > Climatización > Aires Acondicionados",
        ),
        (
            "electrodomesticos/hornos-cocinas",
            OVEN,
            "Electrodomésticos > Hornos y Cocinas",
        ),
        (
            "electrodomesticos/lavado/lavadora-secadoras",
            WASHING_MACHINE,
            "Electrodomésticos > Lavado > Lavadora-Secadoras",
        ),
        (
            "electrodomesticos/refrigeracion",
            REFRIGERATOR,
            "Electrodomésticos > Refrigeración",
        ),
        (
            "electrodomesticos/pequenos-electrodomesticos/hogar/aspiradoras",
            VACUUM_CLEANER,
            "Electrodomésticos > Pequeños Electrodomésticos > Para Hogar > Aspiradoras",
        ),
        (
            "electrodomesticos/pequenos-electrodomesticos/hogar/aspiradoras-robot",
            VACUUM_CLEANER,
            "Electrodomésticos > Pequeños Electrodomésticos > Para Hogar > Aspiradoras",
        ),
        (
            "electrodomesticos/pequenos-electrodomesticos/hogar/planchas",
            IRON,
            "Para Hogar Planchas",
        ),
        (
            "electrodomesticos/lavado/secadoras",
            WASHING_MACHINE,
            "Electrodomésticos > Lavado > Secadoras",
        ),
        (
            "computacion/estabilizadores-ups/ups",
            UPS,
            "Computación > Estabilizadores y UPS > UPS",
        ),
        (
            "pc-escritorio-all-in-one",
            ALL_IN_ONE,
            "Computación > PC de Escritorio > All In One",
        ),
        (
            "electronica-audio-video/audio/micro-minicomponentes",
            STEREO_SYSTEM,
            "Electrónica, Audio y Video > Audio > Micro y Minicomponentes",
        ),
        (
            "electrodomesticos/hornos-cocinas/microondas",
            OVEN,
            "Electrodomésticos > Hornos y Cocinas > Microondas",
        ),
        (
            "electrodomesticos/refrigeracion/refrigeradores",
            REFRIGERATOR,
            "Electrodomésticos > Refrigeración > Refrigeradores",
        ),
        (
            "computacion/impresion/insumos-impresion/cartuchos-tinta",
            PRINTER_SUPPLY,
            "Computación > Impresión > Insumos de Impresión > Cartuchos de Tinta",
        ),
        (
            "computacion/impresion/insumos-impresion/toners",
            PRINTER_SUPPLY,
            "Computación > Impresión > Insumos de Impresión > Tóners",
        ),
        (
            "computacion/impresion/insumos-impresion/sets-insumos-impresion",
            PRINTER_SUPPLY,
            "Computación > Impresión > Insumos de Impresión > Sets de Insumos de Impresión",
        ),
        (
            "computacion/impresion/insumos-impresion/tintas",
            PRINTER_SUPPLY,
            "Computación > Impresión > Insumos de Impresión > Tintas",
        ),
        (
            "electrodomesticos/climatizacion/estufas-calefactores",
            SPACE_HEATER,
            "Electrodomésticos > Climatización > Estufas y Calefactores",
        ),
        (
            "electrodomesticos/pequenos-electrodomesticos/hogar/planchas",
            IRON,
            "Electrodomésticos > Pequeños Electrodomésticos > Para Hogar > Planchas",
        ),
        (
            "electrodomesticos/pequenos-electrodomesticos/cocina/hervidores",
            KETTLE,
            "Electrodomésticos > Pequeños Electrodomésticos > Para Cocina > Hervidores",
        ),
        (
            "electrodomesticos/pequenos-electrodomesticos/cocina/preparacion-alimentos/procesadores",
            FOOD_PROCESSOR,
            "Electrodomésticos > Pequeños Electrodomésticos > Para Cocina > Preparación de Alimentos > Procesadores",
        ),
        (
            "electrodomesticos/pequenos-electrodomesticos/cocina/preparacion-alimentos/arroceras",
            ELECTRIC_POT,
            "Electrodomésticos > Pequeños Electrodomésticos > Para Cocina > Preparación de Alimentos > Arroceras",
        ),
        (
            "electrodomesticos/pequenos-electrodomesticos/cocina/preparacion-alimentos/batidoras",
            MIXER,
            "Electrodomésticos > Pequeños Electrodomésticos > Para Cocina > Preparación de Alimentos > Batidoras",
        ),
        (
            "electrodomesticos/pequenos-electrodomesticos/cocina/preparacion-alimentos/ollas-electricas",
            ELECTRIC_POT,
            "Electrodomésticos > Pequeños Electrodomésticos > Para Cocina > Preparación de Alimentos > Ollas Eléctricas",
        ),
        (
            "electrodomesticos/pequenos-electrodomesticos/cocina/cafeteras",
            COFFE_MAKER,
            "Electrodomésticos > Pequeños Electrodomésticos > Para Cocina > Cafeteras",
        ),
        (
            "electrodomesticos/pequenos-electrodomesticos/cocina/preparacion-alimentos/tostadoras",
            TOASTER,
            "Electrodomésticos > Pequeños Electrodomésticos > Para Cocina > Preparación de Alimentos > Tostadoras",
        ),
        (
            "electrodomesticos/hornos-cocinas/cocinas",
            OVEN,
            "ElectrodomésticosHornos y Cocinas",
        ),
        (
            "electrodomesticos/pequenos-electrodomesticos/cocina/preparacion-bebidas/licuadoras",
            BLENDER,
            "Electrodomésticos > Pequeños Electrodomésticos > Para Cocina > Preparación de Bebidas > Licuadoras",
        ),
        (
            "electrodomesticos/climatizacion/calefonts-termos/calefonts",
            WATER_HEATER,
            "Electrodomésticos > Climatización > Calefonts y Termos > Calefonts",
        ),
        (
            "electrodomesticos/climatizacion/calefonts-termos/termos",
            WATER_HEATER,
            "Electrodomésticos > Climatización > Calefonts y Termos > Termos",
        ),
        (
            "electrodomesticos/pequenos-electrodomesticos/cocina/preparacion-alimentos/freidoras/aire",
            AIR_FRYER,
            "Electrodomésticos > Pequeños Electrodomésticos > Para Cocina > Preparación de Alimentos > Freidoras > De Aire",
        ),
        (
            "electrodomesticos/pequenos-electrodomesticos/cocina/preparacion-bebidas/jugueras",
            JUICER,
            "Electrodomésticos > Pequeños Electrodomésticos > Para Cocina > Preparación de Bebidas > Jugueras",
        ),
        (
            "electrodomesticos/pequenos-electrodomesticos/cocina/preparacion-alimentos/licuadoras-mano",
            FOOD_PROCESSOR,
            "Electrodomésticos > Pequeños Electrodomésticos > Para Cocina > Preparación de Alimentos > Licuadoras de Mano",
        ),
        (
            "hogar-muebles/jardin-aire-libre/hornos-parrillas-accesorios/parrillas/parrillas-electricas",
            ELECTRIC_GRILL,
            "Hogar y Muebles > Jardín y Aire Libre > Hornos, Parrillas y Accesorios > Parrillas > Parrillas Eléctricas",
        ),
        (
            "electrodomesticos/pequenos-electrodomesticos/cocina/preparacion-alimentos/sandwicheras",
            SANDWICH_MAKER,
            "Electrodomésticos > Pequeños Electrodomésticos > Para Cocina > Preparación de Alimentos > Sandwicheras",
        ),
        (
            "belleza-cuidado-personal/artefactos-cabello/cepillos-electricos/alisadores",
            HAIR_CARE,
            "Belleza y Cuidado Personal > Artefactos para el Cabello > Cepillos Eléctricos",
        ),
        (
            "belleza-cuidado-personal/artefactos-cabello/secadores-pelo",
            HAIR_CARE,
            "Belleza y Cuidado Personal > Artefactos para el Cabello > Secadores de Pelo",
        ),
        (
            "belleza-cuidado-personal/artefactos-cabello/rizadores-onduladores",
            HAIR_CARE,
            "Belleza y Cuidado Personal > Artefactos para el Cabello > Rizadores y Onduladores",
        ),
        (
            "electrodomesticos/pequenos-electrodomesticos/cocina/preparacion-alimentos/robots-cocina",
            COOKING_ROBOT,
            "Electrodomésticos > Pequeños Electrodomésticos > Para Cocina > Preparación de Alimentos > Robots de Cocina",
        ),
    ]

    seller_whitelist = [
        "Acer",
        "ACER STORE",
        "ADATA",
        "Anker",
        "ANKERTIENDAOFICIAL2024",
        "ANOVO ANDES",
        "AOC",
        "Apple",
        "ASUS",
        "BENQ",
        "BENQ_CHILE",
        "Black+Decker",
        "Black+Decker Home",
        "Blanik",
        "BLANIK OFICIAL",
        "Blik",
        "BLIKTECHNICA",
        "Bose",
        "Brother",
        "Caixun",
        "CAIXUN",
        "Crucial",
        "Epson",
        "Garmin",
        "Gasei",
        "GASEI S.A.",
        "Hamilton Beach",
        "Harman Kardon",
        "Harman Professional",
        "Hisense",
        "Honor",
        "HP",
        "HP TIENDAOFICIAL",
        "Huawei",
        "JBL",
        "Kärcher",
        "Kensington",
        "KINGSTON",
        "KINGSTONCHILE",
        "Kitchen Center",
        "Lenovo",
        "LENOVOAGENCIAENCHILE",
        "LG",
        "Libero",
        "Logitech",
        "Logitech G",
        "Mabe",
        "MABE CHILE",
        "Mademsa",
        "Master G",
        "Mercado Envios",
        "Mercado Libre",
        "Mercado Libre Electronica",
        "MERCADOLIBRE ELECTRONICA_CL",
        "Midea",
        "MIDEA CARRIER",
        "MISTORECHILE",
        "Nintendo",
        "Oster",
        "Philips",
        "Philips TV & Sound",
        "PlayStation",
        "RADIOVICTORIATCLCHILESPARA",
        "Razer",
        "RAZER OFICIAL",
        "Redragon",
        "Samsung",
        "SAMSUNG_CHILE",
        "Sandisk",
        "Sennheiser",
        "Sindelen",
        "SINDELEN",
        "TCL",
        "Thomas",
        "Thorben",
        "TIENDAOFICIAL HUAWEICL",
        "Toshiba",
        "Western Digital",
        "Xiaomi",
    ]

    @classmethod
    def categories(cls):
        return list({local_category for _, local_category, _ in cls.categories_path})

    @classmethod
    def discover_urls_for_category(cls, category, extra_args=None):
        seen_urls = set()

        for category_path, local_category, _ in cls.categories_path:
            if category != local_category:
                continue

            session = cf_session_with_proxy(extra_args)
            session.headers["Cookie"] = extra_args["cookie"]
            # session.headers["Authorization"] = "Bearer {}".format(
            #     extra_args["access_token"]
            # )
            offset = 0

            while True:
                if offset >= 10000:
                    logging.warning(f"Overflow reached in: {category}")
                    break

                url = f"https://listado.mercadolibre.cl/{category_path}/*_Desde_{offset}_Tienda_{cls.store}_NoIndex_True"
                print(url)
                response = session.get(url)
                soup = BeautifulSoup(response.text, "lxml")
                product_containers = soup.find_all("li", "ui-search-layout__item")

                if not product_containers:
                    if offset == 0:
                        logging.warning(f"Empty category: {category}")
                    break

                for product in product_containers:
                    seller = product.find("span", "poly-component__seller")

                    if (
                        seller
                        and seller.text.split("Por ")[-1].strip()
                        in cls.seller_whitelist
                    ) or cls.store != "all":
                        product_url = cls._clean_product_url(
                            product.find("a", "poly-component__title")["href"]
                        )

                        if product_url not in seen_urls:
                            seen_urls.add(product_url)
                            yield product_url

                offset += 50

    @classmethod
    def _clean_product_url(cls, url):
        cleaned_url = url.split("#")[0]
        parsed = urllib.parse.urlparse(cleaned_url)
        query_params = urllib.parse.parse_qs(parsed.query)
        pdp_filters = query_params.get("pdp_filters", [None])[0]
        search_variation = query_params.get("searchVariation", [None])[0]
        cleaned_url = cleaned_url.split("?")[0]

        if pdp_filters:
            cleaned_url += f"?pdp_filters={pdp_filters}"
        if search_variation:
            connector = "&" if "?" in cleaned_url else "?"
            cleaned_url += f"{connector}searchVariation={search_variation}"

        return cleaned_url

    @classmethod
    def products_for_url(cls, url, category=None, extra_args=None):
        print(url)
        session = cf_session_with_proxy(extra_args)
        session.headers["Cookie"] = extra_args["cookie"]
        session.headers["User-Agent"] = (
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
            "(KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36"
        )
        tries = 0

        while tries < 3:
            try:
                page_source = session.get(url).text
                soup = BeautifulSoup(page_source, "lxml")
                new_mode_data = soup.find("script", {"id": "__PRELOADED_STATE__"})
                data = json.loads(new_mode_data.text)["pageState"]
                break
            except Exception:
                tries += 1
                if tries == 3:
                    return []

        for entry in data["initialState"]["components"].get("head", []):
            if (
                entry["id"] == "item_status_message"
                and "PAUSADA" in entry["body"]["text"].upper()
            ):
                return []

        try:
            data["initialState"]["components"]["description"]["content"]
            return cls.retrieve_type2_products(
                session, url, soup, category, data, extra_args
            )
        except KeyError:
            return cls.retrieve_type3_products(
                url, data, soup, extra_args, category, url
            )

    @classmethod
    def retrieve_type3_products(
        cls, discovery_url, data, soup, extra_args, category, url=None
    ):
        print("Type3")
        api_session = cf_session_with_proxy(extra_args)
        api_session.headers["Authorization"] = "Bearer {}".format(
            extra_args["access_token"]
        )
        variations = set()
        pickers = (
            data["initialState"]["components"]
            .get("variations", {})
            .get("pickers", None)
        )

        official_store_or_seller_filter = data["initialState"].get("filters", None)

        if pickers:
            for picker in pickers:
                for product in picker["products"]:
                    variations.add(product["id"])
        else:
            variations.add(data["initialState"]["id"])

        review_entry = data["initialState"]["components"]["track"]
        review_entry = review_entry["melidata_event"]["event_data"]

        if "item_id" in review_entry:
            review_endpoint = (
                "https://api.mercadolibre.com/reviews/item/" "{}"
            ).format(review_entry["item_id"])
            reviews_response = api_session.get(review_endpoint)
            reviews_data = reviews_response.json()

            if "paging" in reviews_data:
                review_count = reviews_data["paging"]["total"]
                review_avg_score = float(reviews_data["rating_average"])
            else:
                return []
        else:
            review_count = None
            review_avg_score = None

        skip_whitelist = extra_args and extra_args.get("skip_whitelist", False)

        description, part_number = cls.get_description_and_part_number(data)

        for variation in variations:
            sku = variation
            endpoint = "https://api.mercadolibre.com/products/" "{}".format(variation)

            if official_store_or_seller_filter:
                endpoint += f"?{official_store_or_seller_filter.replace(':', '=')}"

            variation_response = api_session.get(endpoint)

            if variation_response.status_code == 403:
                continue

            variation_data = json.loads(variation_response.text)

            if variation_data.get("status", None) != "active":
                continue

            box_winner = variation_data["buy_box_winner"]
            name = variation_data["name"]
            permalink = variation_data["permalink"]
            url = permalink if permalink != "" else url
            price = (
                Decimal(box_winner["price"]).quantize(Decimal(cls.price_accuracy))
                if box_winner
                else Decimal(
                    soup.find("meta", {"itemprop": "price"})["content"]
                ).quantize(Decimal(cls.price_accuracy))
            )

            if box_winner:
                seller_endpoint = "https://api.mercadolibre.com/users/" "{}".format(
                    box_winner["seller_id"]
                )
                seller_info = json.loads(api_session.get(seller_endpoint).text)
                seller = seller_info["nickname"]
            else:
                seller_tag = soup.find("h2", "ui-seller-data-header__title")
                seller = seller_tag.text if seller_tag else None

            stock = -1 if skip_whitelist or seller in cls.seller_whitelist else 0
            picture_urls = [p["url"] for p in variation_data["pictures"]]
            description += ", ".join(
                [
                    f"{attribute['name']}: {attribute['value_name']}"
                    for attribute in variation_data["attributes"]
                ]
                + [variation_data["short_description"]["content"]]
            )

            product = Product(
                name,
                cls.__name__,
                category,
                url,
                discovery_url,
                sku,
                stock,
                price,
                price,
                "CLP",
                sku=sku,
                seller=seller,
                part_number=part_number,
                picture_urls=picture_urls,
                review_count=review_count,
                review_avg_score=review_avg_score,
                description=f"{description} - Type3",
            )

            yield product

    @classmethod
    def retrieve_type2_products(cls, session, url, soup, category, data, extra_args):
        print("Type2")
        seller = data["initialState"]["components"]["track"]["analytics_event"][
            "custom_dimensions"
        ]["customDimensions"]["collectorNickname"]
        skip_whitelist = extra_args and extra_args.get("skip_whitelist", False)
        stock = -1 if skip_whitelist or seller in cls.seller_whitelist else 0
        sku = data["initialState"]["id"]
        base_name = data["initialState"]["schema"][0]["name"]
        price = Decimal(data["initialState"]["schema"][0]["offers"]["price"]).quantize(
            Decimal(cls.price_accuracy)
        )

        if price == 0:
            return []

        description, part_number = cls.get_description_and_part_number(data)

        if "description" in data["initialState"]["components"]:
            description += data["initialState"]["components"]["description"]["content"]

        picker = None
        condition = "https://schema.org/NewCondition"

        if (
            "USADO"
            in data["initialState"]["components"]["header"].get("subtitle", "").upper()
        ):
            condition = "https://schema.org/UsedCondition"

        review_count = None
        review_avg_score = None

        if "short_description" in data["initialState"]["components"]:
            for x in data["initialState"]["components"]["short_description"]:
                if x["id"] == "variations" and "pickers" in x:
                    if len(x["pickers"]) == 1:
                        picker = x["pickers"][0]
                    else:
                        # I'm not sure how to handle multiple pickers
                        # https://articulo.mercadolibre.cl/MLC-547289939-
                        # samartband-huawei-band-4-pro-_JM
                        picker = None
                if x["id"] == "header" and "tag" in x:
                    if "REACONDICIONADO" in x["tag"]["text"].upper():
                        condition = "https://schema.org/RefurbishedCondition"

                if "reviews" in x:
                    review_count = x["reviews"]["amount"]
                    review_avg_score = float(x["reviews"]["rating"])

        gallery = data["initialState"]["components"]["gallery"]["pictures"]

        if picker:
            picker_id = picker["id"]
            for variation in picker["products"]:
                color_name = variation["label"]["text"]
                name = "{} ({})".format(base_name, color_name)
                color_id = variation["attribute_id"]

                if "?" in url:
                    separator = "&"
                else:
                    separator = "?"

                variation_url = "{}{}attributes={}:{}".format(
                    url, separator, picker_id, color_id
                )
                res = session.get(variation_url)
                key_match = re.search(r"variation=(\d+)", res.url)

                if key_match:
                    key = key_match.groups()[0]
                    variation_url = "{}?variation={}".format(url, key)
                else:
                    key = variation["id"]

                picture_urls = [
                    f"https://http2.mlstatic.com/D_NQ_NP_{picture['id']}-O.webp"
                    for picture in gallery
                ]

                product = Product(
                    name,
                    cls.__name__,
                    category,
                    variation_url,
                    url,
                    key,
                    stock,
                    price,
                    price,
                    "CLP",
                    sku=sku,
                    part_number=part_number,
                    seller=seller,
                    condition=condition,
                    review_count=review_count,
                    review_avg_score=review_avg_score,
                    description="{} Type2".format(description),
                    picture_urls=picture_urls,
                )

                yield product

        else:
            picture_urls = [
                x["data-zoom"]
                for x in soup.findAll("img", "ui-pdp-image")[1::2]
                if "data-zoom" in x.attrs
            ]
            product = Product(
                base_name,
                cls.__name__,
                category,
                url,
                url,
                sku,
                stock,
                price,
                price,
                "CLP",
                sku=sku,
                part_number=part_number,
                seller=seller,
                picture_urls=picture_urls,
                condition=condition,
                review_count=review_count,
                review_avg_score=review_avg_score,
                description="{} Type2".format(description),
            )
            yield product

    @classmethod
    def discover_urls_for_keyword(cls, keyword, threshold, extra_args=None):
        session = cf_session_with_proxy(extra_args)
        offset = 0
        result = []

        while offset < threshold:
            endpoint = (
                "https://api.mercadolibre.com/sites/MLC/search?q={}"
                "&offset={}&official_store=all".format(
                    urllib.parse.quote(keyword), offset
                )
            )
            json_results = json.loads(session.get(endpoint).text)
            for product_entry in json_results["results"]:
                result.append(product_entry["permalink"])
                if len(result) >= threshold:
                    break
            offset += 50

        return result

    @classmethod
    def _products_for_url_with_custom_price(
        cls, url, category=None, extra_args=None, min_price=None
    ):
        # Custom method for e-commerce sites that use MercadoShops platform
        # with custom domains. In those cases the price returned by
        # MercadoLibre API does not match the listed price, so it has to be
        # scraped manually.
        # Also fixes the url, discovery_url and seller of the products
        print(url)

        extra_args = extra_args or {}
        retries = extra_args.get("retries", 3)
        extra_args["skip_whitelist"] = True
        session = cf_session_with_proxy(extra_args)
        session.headers["User-Agent"] = (
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, "
            "like Gecko) Chrome/66.0.3359.117 Safari/537.36"
        )

        res = session.get(url)
        soup = BeautifulSoup(res.text, "lxml")
        price_tag = soup.find("meta", {"itemprop": "price"})

        if not price_tag:
            return []

        price = Decimal(price_tag["content"])

        if not min_price or price < min_price:
            min_price = price

        products = MercadoLibreChile.products_for_url(
            url, category=category, extra_args=extra_args
        )

        final_products = []
        for product in products:
            print(product.url)

            if product.offer_price == min_price:
                if retries:
                    extra_args["retries"] = retries - 1
                    return cls._products_for_url_with_custom_price(
                        url,
                        category=category,
                        extra_args=extra_args,
                        min_price=min_price,
                    )
                else:
                    # Sometimes the ML price actually matches the original one,
                    # so keep it
                    pass
            elif product.offer_price < min_price:
                min_price = product.offer_price

            product.url = url
            product.discovery_url = url
            product.offer_price = min_price
            product.normal_price = min_price
            product.seller = None
            final_products.append(product)

        return final_products

    @classmethod
    def preflight(cls, extra_args=None):
        # In case the refresh token expires follow these instructions
        # 1. Execute
        # curl -v https://auth.mercadolibre.cl/authorization?response_type=code&
        # client_id=$CLIENT_ID&redirect_uri=https://www.solotodo.com
        # Replacing CLIENT_ID with the app_id
        # 2. Follow the given link in a browser
        # 3. Copy the code at the end of the redirect url https://www.solotodo.cl/?code=[CODE]
        # 4. Execute the command
        # curl -X POST \
        # -H 'accept: application/json' \
        # -H 'content-type: application/x-www-form-urlencoded' \
        # 'https://api.mercadolibre.com/oauth/token' \
        # -d 'grant_type=authorization_code' \
        # -d 'client_id=$APP_ID' \
        # -d 'client_secret=$APP_SECRET' \
        # -d 'code=$CODE' \
        # -d 'redirect_uri=https://www.solotodo.com'
        # Replacing the APP_ID, APP_SECRET and CODE accordingly
        # 5. Copy the refresh token returned in the previous step
        session = cf_session_with_proxy(extra_args)
        url = "https://api.mercadolibre.com/oauth/token"
        session.headers["accept"] = "application/json"
        session.headers["content-type"] = "application/x-www-form-urlencoded"
        extra_args["cookie"] += ";_d2id=cbec39c3-857e-42a5-9bf5-7fefc694f6ae"

        payload = (
            "grant_type=refresh_token"
            "&client_id={}"
            "&client_secret={}"
            "&refresh_token={}"
        ).format(
            extra_args["app_id"],
            extra_args["app_secret"],
            extra_args["refresh_token"],
        )

        response = session.post(url, data=payload)
        access_token = response.json()["access_token"]
        return {"access_token": access_token}

    @classmethod
    def get_catalog_competitors_for_seller(cls, seller_id, access_token):
        offset = 50
        page = 0
        session = cf_session_with_proxy(None)
        session.headers["Authorization"] = "Bearer {}".format(access_token)
        result = []
        seller_data = {}
        seller_ids = []

        while True:
            print(page)
            items_page_url = "https://api.mercadolibre.com/sites/MLC/search?seller_id={}&offset={}".format(
                seller_id, page * offset
            )
            response = session.get(items_page_url).json()
            if not response["results"]:
                break

            for item in response["results"]:
                catalog_product_id = item["catalog_product_id"]
                print(catalog_product_id)
                if not catalog_product_id:
                    continue
                catalog_url = "https://api.mercadolibre.com/products/{}".format(
                    catalog_product_id
                )
                catalog_response = session.get(catalog_url).json()
                if catalog_response["buy_box_winner"]:
                    seller_ids.append(
                        str(catalog_response["buy_box_winner"]["seller_id"])
                    )
                catalog_items_url = (
                    "https://api.mercadolibre.com/products/{}/items".format(
                        catalog_product_id
                    )
                )
                catalog_items_response = session.get(catalog_items_url).json()

                result.append(
                    {
                        "item": item,
                        "catalog": catalog_response,
                        "catalog_items": catalog_items_response,
                    }
                )

            page += 1

        seller_chunks = chunks(seller_ids, 20)

        for seller_chunk in seller_chunks:
            seller_url = "https://api.mercadolibre.com/users/?ids={}".format(
                ",".join(seller_chunk)
            )
            seller_response = session.get(seller_url).json()
            for seller_entry in seller_response:
                seller_data[seller_entry["body"]["id"]] = seller_entry["body"][
                    "nickname"
                ]
        return result, seller_data

    @classmethod
    def get_description_and_part_number(cls, data):
        model = None
        mpn = None
        description = ""

        if (
            "components"
            not in data["initialState"]["components"]["highlighted_specs_attrs"]
        ):
            return description, mpn

        for attr_group in data["initialState"]["components"]["highlighted_specs_attrs"][
            "components"
        ]:
            if "specs" not in attr_group:
                continue
            for spec_group in attr_group["specs"]:
                for attribute_entry in spec_group["attributes"]:
                    description += (
                        f'{attribute_entry["id"]}: {attribute_entry["text"]}\n'
                    )
                    if attribute_entry["id"] == "Modelo":
                        model = attribute_entry["text"]
                    if attribute_entry["id"] == "Modelo alfanumérico":
                        mpn = attribute_entry["text"]

        tech_name = " - ".join([x for x in [model, mpn] if x])
        part_number = tech_name[:50] or None
        return description, part_number
