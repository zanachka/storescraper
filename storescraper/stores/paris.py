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
        ("tecCompTablet", TABLET, "Tecno > Computadores > iPad y Tablet"),
        ("elcAudAudifonos", HEADPHONES, "TV y Audio > Audio > Audífonos"),
        (
            "elcAudParlantes",
            STEREO_SYSTEM,
            "TV y Audio > Audio > Parlantes Bluetooth y Portables",
        ),
        ("elcTelevision", TELEVISION, "TV y Audio > Televisión"),
        ("elcTvSmartTV", TELEVISION, "TV y Audio > Televisión > Smart TV"),
        ("elcTVLED", TELEVISION, "TV y Audio > Televisión > Televisores LED"),
        ("elcTvCurvoOled", TELEVISION, "television > Oled, Qled y NanoCell"),
        (
            "elcTVSoundbarHomeTheater",
            STEREO_SYSTEM,
            "TV y Audio > Televisión > Soundbar y Home Theater",
        ),
        ("elcAudio", STEREO_SYSTEM, "TV y Audio > Audio"),
        (
            "elcAudMicroMinicomponentes",
            STEREO_SYSTEM,
            "TV y Audio > Audio > Micro y Minicomponentes",
        ),
        (
            "elcAudAudifonosInalambricos",
            HEADPHONES,
            "TV y Audio > Audio > Audífonos Inalámbricos",
        ),
        ("elcHifi", STEREO_SYSTEM, "TV y Audio > HIFI"),
        ("elcHifiAudifonos", HEADPHONES, "TV y Audio > HIFI > Audifonos HiFi"),
        ("elcHifiHomeCinema", STEREO_SYSTEM, "TV y Audio > HIFI > Home Cinema"),
        ("elcHifiAudio", STEREO_SYSTEM, "TV y Audio > HIFI > Audio HIFI"),
        ("elcHifiParlantes", STEREO_SYSTEM, "TV y Audio > HIFI > Parlantes HIFI"),
        ("elcTvPulgadas", TELEVISION, "TV y Audio > Elige tu pulgada"),
        ("elcTvPulg39", TELEVISION, 'TV y Audio > Elige tu pulgada > 30" a 39"'),
        ("elcTvPulg49", TELEVISION, 'TV y Audio > Elige tu pulgada > 40" a 49"'),
        ("elcTvPulg59", TELEVISION, 'TV y Audio > Elige tu pulgada > 50" a 59"'),
        ("elcTvPulg60", TELEVISION, 'TV y Audio > Elige tu pulgada > 60" a 69"'),
        ("elcTvPulg70", TELEVISION, 'TV y Audio > Elige tu pulgada > 70" o más'),
        ("tecCelulares", CELL, "Tecno > Celulares"),
        ("tecCelSmartphones", CELL, "Tecno > Celulares > Smartphones"),
        ("tecCeliPhone", CELL, "Tecno > Celulares > iPhone"),
        ("tecCelSamsung", CELL, "Tecno > Celulares > Celulares Samsung"),
        ("tecCelXiaomi", CELL, "Tecno > Celulares > Celulares Xiaomi"),
        ("tecCelMotorola", CELL, "Tecno > Celulares > Celulares Motorola"),
        ("tecCelHonor", CELL, "Tecno > Celulares > Celulares Honor"),
        ("tecCelVivo", CELL, "Tecno > Celulares > Celulares Vivo"),
        ("tecCelBasicos", CELL, "Tecno > Celulares > Celulares Básicos"),
        ("tecCelOppo", CELL, "Tecno > Celulares > Celulares Oppo"),
        (
            "tecCompDesktopAllinOne",
            ALL_IN_ONE,
            "Tecno > Computadores > Desktop y All InOne",
        ),
        ("tecCompNotebooks", NOTEBOOK, "Tecno > Computadores > Notebooks"),
        ("tecCompTabletNinos", TABLET, "Tecno > Computadores > Tablets Niños"),
        ("tecCompApple", NOTEBOOK, "Tecno > Computadores > Apple"),
        ("tecCelSmartwatchWearables", WEARABLE, "Tecno > Wearables"),
        ("tecSmartwatches", WEARABLE, "Tecno > Wearables > Smartwatches"),
        ("tecSmartwatchesNinos", WEARABLE, "Tecno > Wearables > Smartwatches Niños"),
        ("tecSmartband", WEARABLE, "Tecno > Wearables > Smartband"),
        ("tecConsolas", VIDEO_GAME_CONSOLE, "Tecno > Consolas y VideoJuegos"),
        ("tecImpresion", PRINTER, "Tecno > Impresoras"),
        ("tecImpLaser", PRINTER, "Tecno > Impresoras > Impresión Láser"),
        ("tecImpTinta", PRINTER, "Tecno > Impresoras > Impresión de Tinta"),
        (
            "tecImpTermicasPortatiles",
            PRINTER,
            "Tecno > Impresoras > Térmicas y Portátiles",
        ),
        ("tecImp3D", PRINTER, "Tecno > Impresoras > Impresoras 3D"),
        ("tecImpIndustrial", PRINTER, "Tecno > Impresoras > Impresión Industrial"),
        ("tecImpRotuladores", PRINTER, "Tecno > Impresoras > Rotuladores"),
        ("tecAccesorioscomputacion", ACCESORIES, "Tecno > Accesorios Computación"),
        (
            "tecAccompOtros",
            ACCESORIES,
            "Tecno > Accesorios Computación > Otros Accesorios",
        ),
        (
            "tecAccompMonitorGamer",
            MONITOR,
            "Tecno > Accesorios Computación > Monitores",
        ),
        (
            "tecAccompDiscosDuros",
            SOLID_STATE_DRIVE,
            "Tecno > Accesorios Computación > Discos Duros",
        ),
        (
            "tecAccompProyectores",
            PROJECTOR,
            "Tecno > Accesorios Computación > Proyectores",
        ),
        (
            "tecAccompMouseTeclados",
            MOUSE,
            "Tecno > Accesorios Computación > Mouse y Teclados",
        ),
        (
            "tecAccompAudifonosMicrofonos",
            HEADPHONES,
            "Tecno > Accesorios Computación > Audífonos y Micrófonos",
        ),
        (
            "tecAccompPendrives",
            USB_FLASH_DRIVE,
            "Tecno > Accesorios Computación > Pendrives",
        ),
        ("tecCompComputadoresGamers", NOTEBOOK, "Tecno > Computadores > PC Gamers"),
        (
            "tecAcfotoMemorias",
            MEMORY_CARD,
            "Tecno > Accesorios Fotografía > Tarjetas de Memoria",
        ),
        (
            "lblElectrodomesticos",
            AIR_FRYER,
            "Electro y Línea Blanca > Electrodomésticos",
            {
                "key": "tipoProductoAll",
                "stringValues": "Freidoras de Aire",
            },
        ),
        (
            "lblElcBatidorasLicuadoras",
            BLENDER,
            "Electro y Línea Blanca > Electrodomésticos > Batidoras y Licuadoras",
        ),
        (
            "lblElcCafeteras",
            COFFE_MAKER,
            "Electro y Línea Blanca > Electrodomésticos > Cafeteras",
        ),
        (
            "lblElcRobotCocina",
            COOKING_ROBOT,
            "Electro y Línea Blanca > Electrodomésticos > Robot de Cocina",
        ),
        (
            "lblElcSacajugosExprimidores",
            JUICER,
            "Electro y Línea Blanca > Electrodomésticos > Sacajugos y Exprimidores",
        ),
        (
            "lblElcHervidores",
            KETTLE,
            "Electro y Línea Blanca > Electrodomésticos > Hervidores",
        ),
        (
            "lblElcParrillasElectricas",
            ELECTRIC_GRILL,
            "Electro y Línea Blanca > Electrodomésticos > Parrillas Eléctricas",
        ),
        (
            "lblElcProcesadoresAlimentos",
            FOOD_PROCESSOR,
            "Electro y Línea Blanca > Electrodomésticos > Procesadores y Picadoras",
        ),
        (
            "lblElcTostadoresElectricos",
            SANDWICH_MAKER,
            "Electro y Línea Blanca > Electrodomésticos > Sandwicheras y Tostadores Eléctricos",
        ),
        (
            "lblElcArrocerasFreidoras",
            ELECTRIC_POT,
            "Electro y Línea Blanca > Electrodomésticos > Ollas Eléctricas y Arroceras",
        ),
        (
            "lblElcOtrosArticulos",
            ACCESORIES,
            "Electro y Línea Blanca > Electrodomésticos > Otros Electrodomésticos",
        ),
        ("lblCcnCampanas", ACCESORIES, "Electro y Línea Blanca > Cocina > Campanas"),
        ("lblRefrigeracion", REFRIGERATOR, "Electro y Línea Blanca > Refrigeración"),
        (
            "lblRfrFreezer",
            REFRIGERATOR,
            "Electro y Línea Blanca > Refrigeración > Freezer y Congeladores",
        ),
        (
            "lblRfrRefrigeradores",
            REFRIGERATOR,
            "Electro y Línea Blanca > Refrigeración > Refrigeradores",
        ),
        (
            "lblRfrNoFrost",
            REFRIGERATOR,
            "Electro y Línea Blanca > Refrigeración > No Frost",
        ),
        (
            "lblRfrFrigobarCavas",
            REFRIGERATOR,
            "Electro y Línea Blanca > Refrigeración > Frigobares y Cavas",
        ),
        (
            "lblLavadosecado",
            WASHING_MACHINE,
            "Electro y Línea Blanca > Lavado y Secado",
        ),
        (
            "lblLvsLavadorasFrontal",
            WASHING_MACHINE,
            "Electro y Línea Blanca > Lavado y Secado > Lavadoras Carga Frontal",
        ),
        (
            "lblLvsLavadorasSuperior",
            WASHING_MACHINE,
            "Electro y Línea Blanca > Lavado y Secado > Lavadoras Carga Superior",
        ),
        (
            "lblLvsLavadorasTodas",
            WASHING_MACHINE,
            "Electro y Línea Blanca > Lavado y Secado > Todas las Lavadoras",
        ),
        (
            "lblLvsLavadoraSecadoras",
            WASHING_MACHINE,
            "Electro y Línea Blanca > Lavado y Secado > Lavadora-Secadoras",
        ),
        (
            "lblLvsSecadorasCentrifugas",
            WASHING_MACHINE,
            "Electro y Línea Blanca > Lavado y Secado > Secadoras de Ropa",
        ),
        (
            "lblLvsLavavajillas",
            DISH_WASHER,
            "Electro y Línea Blanca > Lavado y Secado > Lavavajillas",
        ),
        ("lblCocina", STOVE, "Electro y Línea Blanca > Cocina"),
        ("lblCcnCocinas", STOVE, "Electro y Línea Blanca > Cocina > Cocinas"),
        ("lblCcnEncimeras", STOVE, "Electro y Línea Blanca > Cocina > Encimeras"),
        (
            "lblCcnHornosMicroondas",
            OVEN,
            "Electro y Línea Blanca > Cocina > Hornos y Microondas Empotrables",
        ),
        (
            "lblCcnKitEmpotrables",
            STOVE,
            "Electro y Línea Blanca > Cocina > Kit Empotrables",
        ),
        (
            "lblElcMicroondas",
            OVEN,
            "Electro y Línea Blanca > Electrodomésticos > Microondas",
        ),
        (
            "lblElcHornoElectrico",
            OVEN,
            "Electro y Línea Blanca > Electrodomésticos > Hornos Eléctricos",
        ),
        ("lblCalefaccion", SPACE_HEATER, "Electro y Línea Blanca > Calefacción"),
        (
            "lblEstElectricas",
            SPACE_HEATER,
            "Electro y Línea Blanca > Calefacción > Estufas Eléctricas",
        ),
        (
            "lblEstParafina",
            SPACE_HEATER,
            "Electro y Línea Blanca > Calefacción > Estufas a Parafina",
        ),
        (
            "lblEstGas",
            SPACE_HEATER,
            "Electro y Línea Blanca > Calefacción > Estufas a Gas",
        ),
        (
            "lblEstLenaPellets",
            SPACE_HEATER,
            "Electro y Línea Blanca > Calefacción > Leña y Pellets",
        ),
        (
            "lblEstCalefaccionExterior",
            SPACE_HEATER,
            "Electro y Línea Blanca > Calefacción > Calefacción Exterior",
        ),
        (
            "lblEstCalefontTermos",
            WATER_HEATER,
            "Electro y Línea Blanca > Calefacción > Calefonts y Termos",
        ),
        (
            "lblElcAspiradorasEnceradoras",
            VACUUM_CLEANER,
            "Electro y Línea Blanca > Electrodomésticos > Aspirado y Limpieza",
        ),
        (
            "lblAspLimArrastre",
            VACUUM_CLEANER,
            "Electro y Línea Blanca > aspirado-limpieza > Aspiradoras de Arrastre",
        ),
        (
            "lblAspLimRobot",
            VACUUM_CLEANER,
            "Electro y Línea Blanca > aspirado-limpieza > Aspiradoras Robot",
        ),
        (
            "lblAspLimVertical",
            VACUUM_CLEANER,
            "Electro y Línea Blanca > aspirado-limpieza > Aspiradoras Verticales y Portátiles",
        ),
        (
            "lblClimatizacion",
            SPLIT_AIR_CONDITIONER,
            "Electro y Línea Blanca > Climatización",
        ),
        (
            "lblClmAireAcondicionado",
            SPLIT_AIR_CONDITIONER,
            "Electro y Línea Blanca > Climatización > Todo Aire Acondicionado",
        ),
        (
            "lblClmVentilacion",
            SPLIT_AIR_CONDITIONER,
            "Electro y Línea Blanca > Climatización > Ventilación",
        ),
        (
            "lblElectrodomesticos",
            ACCESORIES,
            "Electro y Línea Blanca > Electrodomésticos",
        ),
        (
            "tecImpTintasRepuestos",
            PRINTER_SUPPLY,
            "Tecno > Impresoras > Insumos y Accesorios",
        ),
        ("blzPerfumes", PERFUME, "Belleza > Perfumes"),
        ("OutElcTV", TELEVISION, "Outlet > TV y Audio Outlet > Televisores Outlet"),
        ("OutElcAudio", HEADPHONES, "Outlet > TV y Audio Outlet > Audio Outlet"),
        ("OutElcHifi", STEREO_SYSTEM, "Outlet > TV y Audio Outlet > HIFI Outlet"),
        (
            "OutLblRfr",
            REFRIGERATOR,
            "Outlet > Electro y Línea Blanca Outlet > Refrigeradores, Freezer y Frigobares Outlet",
        ),
        ("OutTecCel", CELL, "Outlet > Tecno Outlet > Celulares Outlet"),
        ("OutTecComp", NOTEBOOK, "Outlet > Tecno Outlet > Computadores Outlet"),
        ("OutTecTablet", TABLET, "Outlet > Tecno Outlet > Tablets Outlet"),
        ("OutTecImpr", PRINTER_SUPPLY, "Outlet > Tecno Outlet > Impresoras Outlet"),
        ("OutTecSmartwatch", WEARABLE, "Outlet > Tecno Outlet > Smartwatch Outlet"),
        (
            "lblElcPlanchas",
            IRON,
            "Electro y Línea Blanca > Electrodomésticos > Planchas",
        ),
        (
            "blzCapilar",
            HAIR_CARE,
            "Belleza > Cuidado Capilar",
            {
                "key": "tipoProductoAll",
                "stringValues": [
                    "Cepillos Alisadores",
                    "Alisadores de Pelo",
                    "Secadores de Pelo",
                    "Onduladores de Pelo",
                ],
            },
        ),
        (
            "jugFigurasJuegos",
            ACCESORIES,
            "Juguetes > Figuras y Juegos de Acción",
            {"key": "brand", "stringValues": ["Beyblade"]},
        ),
    ]

    @classmethod
    def categories(cls):
        return list({x[1] for x in cls.category_paths})

    @classmethod
    def discover_urls_for_category(cls, category, extra_args=None):
        for e in cls.category_paths:
            category_id, local_category, section_name = e[:3]
            if category != local_category:
                continue

            if len(e) == 4:
                additional_filter = e[3]
            else:
                additional_filter = None

            yield from cls._get_product_urls(
                category_id,
                exclude_marketplace=True,
                extra_args=extra_args,
                additional_filter=additional_filter,
            )

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
            -1,
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
    def sections(cls):
        return list({x[2] for x in cls.category_paths})

    @classmethod
    def section_positions(cls, section, extra_args=None):
        for e in cls.category_paths:
            category_id, local_category, section_name = e[:3]
            if section_name != section:
                continue

            if len(e) == 4:
                additional_filter = e[3]
            else:
                additional_filter = {}

            section_urls = cls._get_product_urls(
                category_id,
                exclude_marketplace=False,
                extra_args=extra_args,
                additional_filter=additional_filter,
                add_sponsored_data=True,
            )

            for idx, data in enumerate(section_urls):
                if idx >= 300:
                    break

                section_position = {
                    "field": "discovery_url",
                    "value": data[0],
                    "position": idx + 1,
                    "section": section,
                    "is_sponsored": data[1],
                }

                yield section_position

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

    @classmethod
    def _get_product_urls(
        cls,
        category_id,
        exclude_marketplace,
        extra_args=None,
        additional_filter=None,
        add_sponsored_data=False,
    ):
        session = cls.get_session(extra_args)
        page = 1

        while True:
            if page > (15000 / cls.RESULTS_PER_PAGE):
                raise Exception("Page overflow: " + category_id)

            payload = {
                "filters": [{"key": "group_id", "stringValues": [category_id]}],
                "pagination": {"page": page, "pageSize": 30},
                "sortBy": "relevance",
                "serviceAbility": {
                    "sameDayDelivery": False,
                    "nextDayDelivery": False,
                    "storePickUp": False,
                },
                "sponsoredProducts": True,
                "applicationId": "34bb8686968a85a272a6c546ddcb9860db1ea14ee72f5207ef0c028280a6e7bc",
                "term": "",
            }

            if additional_filter:
                payload["filters"].append(additional_filter)

            if exclude_marketplace:
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

            for container in containers_data:
                product_url = f"https://www.paris.cl/{container['slug']['es-CL']}.html"

                if add_sponsored_data:
                    yield (product_url, "resolvedBidId" in container)
                else:
                    yield product_url

            page += 1
