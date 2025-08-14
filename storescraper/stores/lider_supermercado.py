from decimal import Decimal
from storescraper.categories import GROCERIES
from storescraper.product import Product
from storescraper.store import Store
from storescraper.utils import (
    html_to_markdown,
    session_with_proxy,
)


class LiderSupermercado(Store):
    base_url = "https://apps.lider.cl/supermercado"
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Fedora; Linux x86_64; rv:124.0) Gecko/20100101 Firefox/124.0",
        "tenant": "supermercado",
        "x-channel": "SOD",
    }
    url_extensions = [
        # Marcas Propias
        ("Marcas Propias/Despensa", GROCERIES),
        ("Marcas Propias/Complementos y Snacks", GROCERIES),
        ("Marcas Propias/Lácteos", GROCERIES),
        ("Marcas Propias/Congelados", GROCERIES),
        ("Marcas Propias/Hay Carnes", GROCERIES),
        ("Marcas Propias/Desayuno", GROCERIES),
        ("Marcas Propias/Dulce Momento", GROCERIES),
        # Marcas Americanas
        ("Marcas Americanas/Carnes y Congelados", GROCERIES),
        ("Marcas Americanas/Desayuno", GROCERIES),
        ("Marcas Americanas/Despensa", GROCERIES),
        ("Marcas Americanas/Complementos", GROCERIES),
        ("Marcas Americanas/Dulces y Snacks", GROCERIES),
        # Soy Pyme
        ("Soy Pyme/Alimentos preparados", GROCERIES),
        ("Soy Pyme/Carnes pescados y parrilleros", GROCERIES),
        ("Soy Pyme/Desayuno y dulces", GROCERIES),
        ("Soy Pyme/Despensa", GROCERIES),
        ("Soy Pyme/Frescos y lácteos", GROCERIES),
        ("Soy Pyme/Helados y Postres congelados", GROCERIES),
        ("Soy Pyme/Panadería y pastelería", GROCERIES),
        # La Boti
        ("La Boti/Sin Alcohol", GROCERIES),
        # Carnes y Pescados
        ("Carnes y Pescados/Todas las Carnes", GROCERIES),
        ("Carnes y Pescados/Vacuno", GROCERIES),
        ("Carnes y Pescados/Pollo", GROCERIES),
        ("Carnes y Pescados/Cerdo", GROCERIES),
        ("Carnes y Pescados/Pavo", GROCERIES),
        ("Carnes y Pescados/Cordero", GROCERIES),
        ("Carnes y Pescados/Pescados y Mariscos", GROCERIES),
        ("Carnes y Pescados/Para Parrilla", GROCERIES),
        # Bebidas y Snacks
        ("Bebidas y Snacks/Bebidas", GROCERIES),
        ("Bebidas y Snacks/Jugos", GROCERIES),
        ("Bebidas y Snacks/Refrigerados", GROCERIES),
        ("Bebidas y Snacks/Bebidas Funcionales", GROCERIES),
        ("Bebidas y Snacks/Aguas", GROCERIES),
        ("Bebidas y Snacks/Snacks y Picoteo", GROCERIES),
        # Despensa
        ("Despensa/Pastas y Salsas", GROCERIES),
        ("Despensa/Harinas y Polvos", GROCERIES),
        ("Despensa/Arroz y Legumbres", GROCERIES),
        ("Despensa/Salsas", GROCERIES),
        ("Despensa/Aceites y Aderezos", GROCERIES),
        ("Despensa/Conservas", GROCERIES),
        ("Despensa/Alimentos Instantáneos", GROCERIES),
        ("Despensa/Cocina Internacional", GROCERIES),
        # Frutas y Verduras
        ("Frutas y Verduras/Frutas", GROCERIES),
        ("Frutas y Verduras/Verduras", GROCERIES),
        ("Frutas y Verduras/Frutos Secos", GROCERIES),
        ("Frutas y Verduras/Orgánicos", GROCERIES),
        ("Frutas y Verduras/Frutas y Ensaladas Listas", GROCERIES),
        # Panadería y Pastelería
        ("Panadería y Pastelería/Panadería Envasada", GROCERIES),
        ("Panadería y Pastelería/Panadería Granel", GROCERIES),
        ("Panadería y Pastelería/Pastelería", GROCERIES),
        ("Panadería y Pastelería/Repostería", GROCERIES),
        # Frescos y Lácteos
        ("Frescos y Lácteos/Fiambres y Embutidos", GROCERIES),
        ("Frescos y Lácteos/Quesos", GROCERIES),
        ("Frescos y Lácteos/Leche", GROCERIES),
        ("Frescos y Lácteos/Cremas", GROCERIES),
        ("Frescos y Lácteos/Bebidas Vegetales", GROCERIES),
        ("Frescos y Lácteos/Yoghurt", GROCERIES),
        ("Frescos y Lácteos/Postres Refrigerados", GROCERIES),
        ("Frescos y Lácteos/Huevos y Mantequillas", GROCERIES),
        ("Frescos y Lácteos/Platos Preparados", GROCERIES),
        ("Frescos y Lácteos/Masas Refrigeradas", GROCERIES),
        # Congelados
        ("Congelados/Verduras y Frutas Congeladas", GROCERIES),
        ("Congelados/Hamburguesas y Churrascos", GROCERIES),
        ("Congelados/Comidas Congeladas", GROCERIES),
        ("Congelados/Helados", GROCERIES),
        # Chocolates
        ("Chocolates/Variedad", GROCERIES),
        ("Chocolates/Tipos", GROCERIES),
        # Desayunos y Dulces
        ("Desayunos y Dulces/Café Té y Hierbas", GROCERIES),
        ("Desayunos y Dulces/Cereales", GROCERIES),
        ("Desayunos y Dulces/Galletas y Colaciones Dulces", GROCERIES),
        ("Desayunos y Dulces/Dulces Mermeladas y Manjar", GROCERIES),
        ("Desayunos y Dulces/Chocolates y Candy", GROCERIES),
        ("Desayunos y Dulces/Postres para Preparar", GROCERIES),
        # Colaciones
        ("Colaciones/Fruta Colación", GROCERIES),
        ("Colaciones/Barritas y cereales", GROCERIES),
        ("Colaciones/Galletas y Snack colación", GROCERIES),
        ("Colaciones/Jugos Colación", GROCERIES),
        ("Colaciones/Leches Colación", GROCERIES),
        ("Colaciones/Yoghurt", GROCERIES),
        # Platos Preparados
        ("Platos Preparados/Cóctel", GROCERIES),
        ("Platos Preparados/Para Terminar en Casa", GROCERIES),
        ("Platos Preparados/Platos Listos Familiar", GROCERIES),
        ("Platos Preparados/Platos Listos Individuales", GROCERIES),
        ("Platos Preparados/Platos Listos", GROCERIES),
        ("Platos Preparados/Postres", GROCERIES),
    ]

    @classmethod
    def categories(cls):
        return [GROCERIES]

    @classmethod
    def discover_urls_for_category(cls, category, extra_args=None):
        session = session_with_proxy(extra_args)
        session.headers = cls.headers

        for (
            url_extension,
            local_category,
        ) in cls.url_extensions:
            if category != local_category:
                continue

            page = 1

            while True:
                if page >= 50:
                    raise Exception(f"Page overflow: {url_extension}")

                print(f"{url_extension} page {page}")

                payload = {
                    "categories": url_extension,
                    "page": page,
                    "facets": [],
                    "sortBy": "",
                    "hitsPerPage": 16,
                }
                response = session.post(f"{cls.base_url}/bff/category", json=payload)
                json_data = response.json()
                products = [product for product in json_data["products"]]

                if not products:
                    if page == 1:
                        raise Exception(f"Empty section: {url_extension}")
                    break

                for product in products:
                    product_url = f"{cls.base_url}/product/sku/{product['sku']}"
                    yield product_url

                page += 1

    @classmethod
    def products_for_url(cls, url, category=None, extra_args=None):
        print(url)
        key = url.split("/")[-1]
        session = session_with_proxy(extra_args)
        session.headers = cls.headers
        response = session.get(f"{cls.base_url}/bff/products/{key}")
        product_data = response.json()

        brand = product_data["brand"]
        specs = [
            f"- {item['name']}: {item['value']}"
            for item in product_data["specifications"]
        ]
        specs_str = "\n".join(specs)
        specs = f"- Marca: {brand}\n{specs_str}\n\n"
        description = f"{specs}{html_to_markdown(product_data['longDescription'])}"
        name = f"{brand} - {product_data['displayName']}"
        price = Decimal(product_data["price"]["BasePriceSales"])
        stock = -1 if product_data["available"] else 0
        picture_urls = [f"{img}=0" for img in product_data["images"]["availableImages"]]
        sku = product_data["itemNumber"]

        p = Product(
            name,
            cls.__name__,
            category,
            url,
            url,
            key,
            stock,
            price,
            price,
            "CLP",
            sku=sku,
            picture_urls=picture_urls,
            description=description,
        )

        yield p
