from decimal import Decimal
import requests
import json
from storescraper.categories import CELL
from storescraper.product import Product
from storescraper.store import Store


class Movistar(Store):
    category_paths = [
        ("https://ww2.movistar.cl/ofertas/equipo-plan/equipos.min.json", CELL)
    ]
    AVAILABLE_PLANS = [
        "Plan 5G Libre Inicia",
        "Plan 5G Libre Inicia Cuotas",
        "Plan 5G Libre Inicia Portabilidad",
        "Plan 5G Libre Inicia Portabilidad Cuotas",
        "Plan 5G Libre Full",
        "Plan 5G Libre Full Cuotas",
        "Plan 5G Libre Full Portabilidad",
        "Plan 5G Libre Full Portabilidad Cuotas",
        "Plan 5G Libre Pro",
        "Plan 5G Libre Pro Cuotas",
        "Plan 5G Libre Pro Portabilidad",
        "Plan 5G Libre Pro Portabilidad Cuotas",
        "Plan 5G Libre Ultra",
        "Plan 5G Libre Ultra Cuotas",
        "Plan 5G Libre Ultra Portabilidad",
        "Plan 5G Libre Ultra Portabilidad Cuotas",
    ]

    @classmethod
    def categories(cls):
        return [CELL]

    @classmethod
    def discover_urls_for_category(cls, category, extra_args=None):
        return [category]

    @classmethod
    def products_for_url(cls, url, category=None, extra_args=None):
        products = []

        for category_path, local_category in cls.category_paths:
            if local_category != category:
                continue

            print(category_path)
            response = requests.get(category_path)
            data = response.json()
            filtered_entries = [entry for entry in data if entry["movistarone"] == ""]

            for entry in filtered_entries:
                for plan in cls.AVAILABLE_PLANS:
                    discovery_url = (
                        "https://ww2.movistar.cl/ofertas/equipo-plan/"
                        if "Portabilidad" in plan
                        else "https://ww2.movistar.cl/ofertas/linea-nueva/"
                    )
                    price = Decimal(0) if "Cuotas" in plan else Decimal(entry["valor"])
                    monthly_price = (
                        Decimal(entry["pcuota"]) if "Cuotas" in plan else Decimal(0)
                    )
                    allow_zero_prices = "Cuotas" in plan

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
                        cell_monthly_payment=monthly_price,
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
