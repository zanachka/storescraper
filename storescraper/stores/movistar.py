import json
from bs4 import BeautifulSoup
from decimal import Decimal
from storescraper.categories import CELL, CELL_PLAN
from storescraper.product import Product
from storescraper.store import Store
from storescraper.utils import remove_words, session_with_proxy


class Movistar(Store):
    category_paths = [
        ("https://ww2.movistar.cl/ofertas/equipo-plan/equipos.min.json", CELL),
        ("https://ww2.movistar.cl/movil/planes-portabilidad/", CELL_PLAN),
    ]
    AVAILABLE_PLANS = [
        "5G Libre Inicia",
        "5G Libre Inicia Cuotas",
        "5G Libre Inicia Portabilidad",
        "5G Libre Inicia Portabilidad Cuotas",
        "5G Libre Full",
        "5G Libre Full Cuotas",
        "5G Libre Full Portabilidad",
        "5G Libre Full Portabilidad Cuotas",
        "5G Libre Pro",
        "5G Libre Pro Cuotas",
        "5G Libre Pro Portabilidad",
        "5G Libre Pro Portabilidad Cuotas",
        "5G Libre Ultra",
        "5G Libre Ultra Cuotas",
        "5G Libre Ultra Portabilidad",
        "5G Libre Ultra Portabilidad Cuotas",
    ]

    @classmethod
    def categories(cls):
        return [CELL, CELL_PLAN]

    @classmethod
    def discover_urls_for_category(cls, category, extra_args=None):
        return [category]

    @classmethod
    def _cellphones(cls, url, extra_args):
        session = session_with_proxy(extra_args)
        response = session.get(url)
        data = response.json()
        products = []
        filtered_entries = [entry for entry in data if entry["movistarone"] == ""]

        for entry in filtered_entries:
            for plan in cls.AVAILABLE_PLANS:
                product_url = (
                    "https://ww2.movistar.cl/ofertas/equipo-plan/"
                    if "Portabilidad" in plan
                    else "https://ww2.movistar.cl/ofertas/linea-nueva/"
                )
                price = Decimal(0) if "Cuotas" in plan else Decimal(entry["valor"])
                monthly_price = (
                    Decimal(entry["pcuota"]) if "Cuotas" in plan else Decimal(0)
                )

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
                    cell_monthly_payment=monthly_price,
                    currency="CLP",
                    sku=entry["equipo"],
                    description=json.dumps(entry["caracteristicas"]),
                    picture_urls=[
                        f"https://ww2.movistar.cl/ofertas/img/equipos/{entry['img']}"
                    ],
                    allow_zero_prices="Cuotas" in plan,
                )
                products.append(p)

        return products

    @classmethod
    def _plans(cls, url, extra_args):
        session = session_with_proxy(extra_args)
        soup = BeautifulSoup(session.get(url).text, "lxml")
        products = []

        for plan_container in soup.findAll("div", "card"):
            plan_link = plan_container.find("a")
            plan_url = plan_link["href"]
            base_plan_name = plan_container.find("p").text.strip()
            price_text = plan_container.find("div", "precio").find("span").text
            price = Decimal(remove_words(price_text.split()[0]))
            portability_suffixes = ["", " Portabilidad"]
            cuotas_suffixes = [" (sin cuota de arriendo)", " (con cuota de arriendo)"]

            for portability_suffix in portability_suffixes:
                for cuota_suffix in cuotas_suffixes:
                    plan_name = f"{base_plan_name}{portability_suffix}{cuota_suffix}"
                    products.append(
                        Product(
                            plan_name,
                            cls.__name__,
                            CELL_PLAN,
                            plan_url,
                            url,
                            plan_name,
                            -1,
                            price,
                            price,
                            "CLP",
                        )
                    )

        return products

    @classmethod
    def products_for_url(cls, url, category=None, extra_args=None):
        for category_path, local_category in cls.category_paths:
            if local_category != category:
                continue

            print(category_path)

            if category == CELL:
                return cls._cellphones(category_path, extra_args)
            elif category == CELL_PLAN:
                return cls._plans(category_path, extra_args)
        raise Exception("Invalid category")
