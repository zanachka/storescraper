from decimal import Decimal
from urllib.parse import quote, urlsplit, urlunsplit
from storescraper.categories import GROCERIES
from storescraper.product import Product
from storescraper.store import Store
from storescraper.utils import html_to_markdown, session_with_proxy


class Jumbo(Store):
    preferred_products_for_url_concurrency = 20
    base_url = "https://www.jumbo.cl"
    api_key = "be-reg-groceries-jumbo-catalog-w54byfvkmju5"
    store = "jumboclj512"

    url_extensions = [
        # Supermercado
        ("congelados", GROCERIES),
        ("desayuno", GROCERIES),
        ("chocolates-galletas-y-dulces", GROCERIES),
        ("fiambreria-y-encurtidos", GROCERIES),
        ("panaderia-y-pasteleria", GROCERIES),
        ("pescaderia", GROCERIES),
        ("comidas-preparadas", GROCERIES),
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
        # Frutas y Verdurasfdesc
        ("frutas-y-verduras/frutas", GROCERIES),
        ("frutas-y-verduras/verduras", GROCERIES),
        ("frutas-y-verduras/frutas-y-verduras-organicas", GROCERIES),
        ("frutas-y-verduras/frutos-secos-y-semillas", GROCERIES),
        # Carnicería
        ("carniceria/vacuno", GROCERIES),
        ("carniceria/cerdo", GROCERIES),
        ("carniceria/cordero", GROCERIES),
        ("carniceria/pavo", GROCERIES),
        ("carniceria/pollo", GROCERIES),
        # Licores, Bebidas y Aguas
        ("licores-bebidas-y-aguas/sin-alcohol", GROCERIES),
        ("licores-bebidas-y-aguas/bebidas-gaseosas", GROCERIES),
        ("licores-bebidas-y-aguas/aguas", GROCERIES),
        ("licores-bebidas-y-aguas/agua-tonica-y-ginger-beer", GROCERIES),
        ("licores-bebidas-y-aguas/jugos", GROCERIES),
        ("licores-bebidas-y-aguas/bebidas-energeticas", GROCERIES),
        ("licores-bebidas-y-aguas/bebidas-isotonicas-y-sueros", GROCERIES),
        ("licores-bebidas-y-aguas/infusiones-frias", GROCERIES),
    ]

    @classmethod
    def categories(cls):
        return [GROCERIES]

    @classmethod
    def discover_urls_for_category(cls, category, extra_args=None):
        session = session_with_proxy(extra_args)
        session.headers["apikey"] = cls.api_key

        for (
            url_extension,
            local_category,
        ) in cls.url_extensions:
            if category != local_category:
                continue

            page_size = 40
            index_from = 0

            while True:
                index_to = index_from + page_size

                if index_from >= 2000:
                    raise Exception(f"Page overflow: {url_extension}")

                print(f"{url_extension} from {index_from} to {index_to}")

                payload = {
                    "store": cls.store,
                    "from": index_from,
                    "to": index_to,
                    "selectedFacets": [
                        {"key": "category1", "value": f"/{url_extension}"}
                    ],
                    "promotionalCards": True,
                    "sponsoredProducts": True,
                }

                response = session.post(
                    "https://bff.jumbo.cl/catalog/plp", json=payload
                )
                json_data = response.json()
                products = [
                    product
                    for product in json_data["products"]
                    if product.get("type") != "card"
                ]

                if not products:
                    if index_from == 0:
                        raise Exception(f"Empty section: {url_extension}")
                    break

                for product in products:
                    product_url = f"{cls.base_url}/{product['slug']}/p"
                    yield product_url

                index_from += page_size

    @classmethod
    def products_for_url(cls, url, category=None, extra_args=None):
        print(url)
        session = session_with_proxy(extra_args)
        session.headers["apikey"] = cls.api_key
        payload = {
            "slug": url.split(f"{cls.base_url}/")[1].split("/p")[0],
            "store": cls.store,
        }
        response = session.post("https://bff.jumbo.cl/catalog/pdp", json=payload)

        if response.status_code == 204:
            return []

        product_data = response.json()
        brand = product_data["brand"]
        specs = [
            f"- {item['key']}: {item['value']}"
            for item in product_data["characteristicsTable"]
        ]
        specs_str = "\n".join(specs)
        specs = f"- Marca: {brand}\n{specs_str}\n\n"
        description = f"{specs}{html_to_markdown(product_data['description'])}"
        items = product_data["items"]

        for item in items:
            name = f"{brand} - {item['name']}"

            multiplier = item["unitMultiplier"]
            measurement = item["measurementUnit"]

            if multiplier != 1 or measurement != "un":
                name += f" ({item['unitMultiplier']} {item['measurementUnit']})"

            sku = item["skuId"]
            price = Decimal(item["price"])
            promotions = item["promotions"]

            cencosud_promotions = [
                promotion["unitPrice"]
                for promotion in promotions
                if promotion["paymentMethods"] == "CENCOSUD_CARD"
            ]

            offer_price = (
                Decimal(min(cencosud_promotions)) if cencosud_promotions else price
            )
            stock = -1 if item["stock"] else 0
            picture_urls = []

            for img in item["images"]:
                parts = urlsplit(img.split("?")[0])
                safe_path = quote(parts.path, safe="/")
                safe_url = urlunsplit((parts.scheme, parts.netloc, safe_path, "", ""))
                picture_urls.append(safe_url)

            p = Product(
                name,
                cls.__name__,
                category,
                url,
                url,
                sku,
                stock,
                price,
                offer_price,
                "CLP",
                sku=sku,
                picture_urls=picture_urls,
                description=description,
            )

            yield p
