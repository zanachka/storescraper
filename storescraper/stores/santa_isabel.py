from decimal import Decimal
import json
from urllib.parse import quote, urlsplit, urlunsplit
from bs4 import BeautifulSoup
from storescraper.categories import GROCERIES
from storescraper.product import Product
from storescraper.store import Store
from storescraper.utils import check_ean13, html_to_markdown, session_with_proxy


class SantaIsabel(Store):
    url_extensions = [
        # Supermercado
        ("bebidas-aguas-y-jugos", GROCERIES),
        ("fiambreria-y-encurtidos", GROCERIES),
        ("panaderia-y-pasteleria", GROCERIES),
        ("desayuno", GROCERIES),
        ("chocolates-galletas-y-dulces", GROCERIES),
        ("congelados", GROCERIES),
        ("pescaderia", GROCERIES),
        ("comidas-preparadas", GROCERIES),
        ("mundo-vegano", GROCERIES),
        # Lácteos y Quesos
        ("lacteos-y-quesos/queseria", GROCERIES),
        ("lacteos-y-quesos/leches", GROCERIES),
        ("lacteos-y-quesos/yoghurt", GROCERIES),
        ("lacteos-y-quesos/postres", GROCERIES),
        ("lacteos-y-quesos/mantequillas-y-margarinas", GROCERIES),
        ("lacteos-y-quesos/huevos", GROCERIES),
        ("despensa/reposteria/cremas", GROCERIES),
        ("lacteos-y-quesos/leches-cultivadas-y-bebidas-lacteas", GROCERIES),
        # Despensa
        ("despensa/pastas-y-salsas", GROCERIES),
        ("despensa/arroz-y-legumbres", GROCERIES),
        ("despensa/aceites-sal-y-condimentos", GROCERIES),
        ("despensa/conservas", GROCERIES),
        ("despensa/coctel-y-snacks", GROCERIES),
        ("despensa/aderezos-y-salsas", GROCERIES),
        ("despensa/instantaneos-y-sopas", GROCERIES),
        ("despensa/harina-y-complementos", GROCERIES),
        ("despensa/reposteria", GROCERIES),
        ("despensa/comidas-etnicas", GROCERIES),
        # Frutas y Verduras
        ("frutas-y-verduras/frutas", GROCERIES),
        ("frutas-y-verduras/verduras", GROCERIES),
        ("frutas-y-verduras/frutas-y-verduras-organicas", GROCERIES),
        ("frutas-y-verduras/frutos-secos-y-semillas", GROCERIES),
        # Carnicería
        ("carniceria/vacuno", GROCERIES),
        ("carniceria/cerdo", GROCERIES),
        ("carniceria/pavo", GROCERIES),
        ("carniceria/pollo", GROCERIES),
        # Botillería
        ("vinos-cervezas-y-licores/sin-alcohol", GROCERIES),
        ("bebidas-aguas-y-jugos/bebidas-gaseosas", GROCERIES),
        ("bebidas-aguas-y-jugos/aguas", GROCERIES),
        ("bebidas-aguas-y-jugos/agua-tonica-y-ginger-beer", GROCERIES),
        ("bebidas-aguas-y-jugos/jugos", GROCERIES),
        ("bebidas-aguas-y-jugos/bebidas-energeticas", GROCERIES),
        ("bebidas-aguas-y-jugos/bebidas-isotonicas-y-sueros", GROCERIES),
        ("bebidas-aguas-y-jugos/infusiones-frias", GROCERIES),
    ]

    @classmethod
    def categories(cls):
        return [GROCERIES]

    @classmethod
    def discover_urls_for_category(cls, category, extra_args=None):
        session = session_with_proxy(extra_args)

        for (
            url_extension,
            local_category,
        ) in cls.url_extensions:
            if category != local_category:
                continue

            page = 1
            session.headers = {
                "x-consumer": "santaisabel",
                "apikey": "WlVnnB7c1BblmgUPOfg",
            }

            while True:
                if page >= 30:
                    raise Exception(f"Page overflow: {url_extension}")

                print(f"{url_extension} page {page}")

                response = session.get(
                    f"https://sm-web-api.ecomm.cencosud.com/catalog/api/v4/pedrofontova/products/{url_extension}?page={page}&sc=1"
                )
                json_data = response.json()
                products = json_data["products"]

                if not products:
                    if page == 1:
                        raise Exception(f"Empty section: {url_extension}")
                    break

                for product in json_data["products"]:
                    items = product["items"]
                    assert len(items) == 1
                    sellers = items[0]["sellers"]
                    assert len(sellers) == 1

                    if sellers[0]["commertialOffer"]["AvailableQuantity"] > 0:
                        product_url = (
                            f"https://www.santaisabel.cl/{product['linkText']}/p"
                        )
                        yield product_url

                page += 1

    @classmethod
    def products_for_url(cls, url, category=None, extra_args=None):
        print(url)
        session = session_with_proxy(extra_args)
        promotions_data = session.get(
            "https://assets.jumbo.cl/json/santaisabel/promotions-v2.json"
        ).json()
        response = session.get(url)

        if response.status_code == 404:
            return []

        soup = BeautifulSoup(response.text, "lxml")
        raw_data = soup.find("body", "santaisabel").find("script").string
        raw_product_data = raw_data.split("=", 1)[1].strip()

        if raw_product_data.endswith(";"):
            raw_product_data = raw_product_data[:-1]

        intermediate = json.loads(raw_product_data)
        product_data = json.loads(intermediate)["pdp"]["product"]

        assert len(product_data) == 1

        product_data = product_data[0]
        spec_names = [
            "Tipo de Producto",
            "Pack-Unitario",
            "Contenido",
            "Envase",
            "Formato",
            "Variedad",
            "Cantidad",
            "País de Origen",
            "Duración",
            "Almacenamiento",
            "Característica Sustentable",
        ]
        specs = [
            "- " + spec_name + ": " + ", ".join(product_data[spec_name]) + "\n"
            for spec_name in spec_names
            if spec_name in product_data
        ]
        specs = "".join(specs)
        description = (
            "Marca: "
            + product_data["brand"]
            + "\n"
            + specs
            + "\n"
            + html_to_markdown(product_data["description"])
        )
        product_id = product_data["productId"]

        for item in product_data["items"]:
            sellers = item["sellers"]

            assert len(sellers) == 1

            seller = sellers[0]
            name = f"{product_data['brand']} - {item['name']}"
            offer = seller["commertialOffer"]
            price = Decimal(int(offer["Price"]))

            if price == 0:
                return []

            key = item["itemId"]
            ean = item["ean"]

            promotions = promotions_data["products"].get(product_id, [])
            promotion_prices = [
                promotions_data["promotions"][promo]["value"]
                for promo in promotions
                if promotions_data["promotions"][promo]["group"] == "t-cenco"
            ]
            offer_price = (
                Decimal(int(min(promotion_prices))) if promotion_prices else price
            )

            stock = offer["AvailableQuantity"]
            raw_picture_urls = [img["imageUrl"].split("?")[0] for img in item["images"]]
            picture_urls = []

            for img in raw_picture_urls:
                parts = urlsplit(img)
                safe_path = quote(parts.path, safe="/")
                safe_url = urlunsplit((parts.scheme, parts.netloc, safe_path, "", ""))
                picture_urls.append(safe_url)

            p = Product(
                name,
                cls.__name__,
                category,
                url,
                url,
                key,
                stock,
                price,
                offer_price,
                "CLP",
                picture_urls=picture_urls,
                ean=ean if check_ean13(ean) else None,
                description=description,
            )

            yield p
