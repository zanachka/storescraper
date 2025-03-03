import json
from bs4 import BeautifulSoup
from storescraper.store_with_url_extensions import StoreWithUrlExtensions
from storescraper.utils import session_with_proxy
from storescraper.categories import (
    STOVE,
    OVEN,
    CELL_ACCESORY,
    REFRIGERATOR,
    KITCHEN_APPLIANCE,
    VACUUM_CLEANER,
    WASHING_MACHINE,
    WATER_HEATER,
    AIR_CONDITIONER,
    SPACE_HEATER,
)


class Sindelen(StoreWithUrlExtensions):
    url_extensions = [
        ("10152/cocinas-y-encimeras", STOVE),
        ("10022/hornos-electricos", OVEN),
        ("10023/hornos-electricos", OVEN),
        ("10026/hornos-electricos", OVEN),
        ("10012/campanas", CELL_ACCESORY),
        ("10116/Refrigeracion", REFRIGERATOR),
        ("10154/batidoras-y-picadoras", KITCHEN_APPLIANCE),
        ("10155/licuadoras-y-extractores", KITCHEN_APPLIANCE),
        ("10156/cafeteras-y-hervidores", KITCHEN_APPLIANCE),
        ("10157/freidoras-y-parrillas", KITCHEN_APPLIANCE),
        ("10027/ollas-electricas", KITCHEN_APPLIANCE),
        ("10158/tostadores-y-sandwicheras", KITCHEN_APPLIANCE),
        ("10071/cocedor-de-huevos", KITCHEN_APPLIANCE),
        ("10072/maquina-para-hacer-pan", KITCHEN_APPLIANCE),
        ("10073/soup-maker", KITCHEN_APPLIANCE),
        ("10074/robot-de-cocina", KITCHEN_APPLIANCE),
        ("10036/aspiradoras", VACUUM_CLEANER),
        ("10037/enceradoras-y-mopas", CELL_ACCESORY),
        ("10159/lavadoras-y-secadoras", WASHING_MACHINE),
        ("10034/planchas", CELL_ACCESORY),
        ("10050/secadores-de-pelo", CELL_ACCESORY),
        ("10042/calefonts", WATER_HEATER),
        ("10040/enfriadores", AIR_CONDITIONER),
        ("10043/calienta-camas", CELL_ACCESORY),
        ("10160/estufas", SPACE_HEATER),
        ("10046/calefactores-electricos", SPACE_HEATER),
        ("10041/ventiladores", CELL_ACCESORY),
    ]

    @classmethod
    def discover_urls_for_url_extension(cls, url_extension, extra_args):
        product_urls = []
        session = session_with_proxy(extra_args)
        category_id = url_extension.split("/")[0]
        url = f"https://www.sindelen.cl/digitag/category/products/{category_id}.json"
        response = session.get(url)
        products_data = json.loads(response.text)

        for product in products_data:
            product_urls.append(product["product_url"])

        return product_urls
