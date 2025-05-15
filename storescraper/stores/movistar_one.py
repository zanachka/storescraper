import json
import requests
from decimal import Decimal
from storescraper.product import Product
from .movistar import Movistar


class MovistarOne(Movistar):
    AVAILABLE_PLANS = {
        "plan_libre_full": [
            "Plan 5G Libre Full Cuotas",
            "Plan 5G Libre Full Portabilidad Cuotas",
        ],
        "plan_libre_pro": [
            "Plan 5G Libre Pro Cuotas",
            "Plan 5G Libre Pro Portabilidad Cuotas",
        ],
        "plan_libre_ultra": [
            "Plan 5G Libre Ultra Cuotas",
            "Plan 5G Libre Ultra Portabilidad Cuotas",
        ],
    }

    @classmethod
    def products_for_url(cls, url, category=None, extra_args=None):
        products = []

        for category_path, local_category in cls.category_paths:
            if local_category != category:
                continue

            print(category_path)
            response = requests.get(category_path)
            data = response.json()
            discovery_url = "https://ww2.movistar.cl/ofertas/equipo-plan/"
            filtered_entries = [entry for entry in data if entry["movistarone"] == 1]

            for entry in filtered_entries:
                available_planes = cls.AVAILABLE_PLANS[entry["movistaroneTipo"]]

                for plan in available_planes:
                    price = Decimal(entry["pie"])
                    allow_zero_prices = price == 0

                    p = Product(
                        name=entry["equipo"],
                        store=cls.__name__,
                        category=category,
                        url=discovery_url,
                        discovery_url=discovery_url,
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
                        allow_zero_prices=allow_zero_prices,
                    )
                    products.append(p)

        return products
