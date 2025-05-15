import json
from decimal import Decimal
from storescraper.categories import CELL
from storescraper.product import Product
from storescraper.store import Store
from storescraper.utils import session_with_proxy


class MovistarOne(Store):
    URL = "https://ww2.movistar.cl/ofertas/equipo-plan/equipos.min.json"
    AVAILABLE_PLANS = {
        "plan_libre_full": [
            "5G Libre Full Cuotas",
            "5G Libre Full Portabilidad Cuotas",
        ],
        "plan_libre_pro": [
            "5G Libre Pro Cuotas",
            "5G Libre Pro Portabilidad Cuotas",
        ],
        "plan_libre_ultra": [
            "5G Libre Ultra Cuotas",
            "5G Libre Ultra Portabilidad Cuotas",
        ],
    }

    @classmethod
    def categories(cls):
        return [CELL]

    @classmethod
    def discover_urls_for_category(cls, category, extra_args=None):
        return [category]

    @classmethod
    def products_for_url(cls, url, category=None, extra_args=None):
        print(cls.URL)
        session = session_with_proxy(extra_args)
        response = session.get(cls.URL)
        data = response.json()
        products = []
        product_url = "https://ww2.movistar.cl/ofertas/equipo-plan/"
        filtered_entries = [entry for entry in data if entry["movistarone"] == 1]

        for entry in filtered_entries:
            available_plans = cls.AVAILABLE_PLANS[entry["movistaroneTipo"]]

            for plan in available_plans:
                price = Decimal(entry["pie"])
                p = Product(
                    name=entry["equipo"],
                    store=cls.__name__,
                    category=CELL,
                    url=product_url,
                    discovery_url=url,
                    key=f"{entry['id']} - {plan}",
                    stock=-1,
                    normal_price=price,
                    offer_price=price,
                    cell_plan_name=plan,
                    cell_monthly_payment=Decimal(entry["pcuota"]),
                    currency="CLP",
                    sku=entry["equipo"],
                    description=json.dumps(entry["caracteristicas"]),
                    picture_urls=[
                        f"https://ww2.movistar.cl/ofertas/img/equipos/{entry['img']}"
                    ],
                    allow_zero_prices=price == 0,
                )
                products.append(p)

        return products
