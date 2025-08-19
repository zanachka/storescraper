import time
import urllib
from decimal import Decimal
from storescraper.categories import GROCERIES
from storescraper.product import Product
from storescraper.store_with_url_extensions import StoreWithUrlExtensions
from storescraper.utils import (
    html_to_markdown,
    session_with_proxy,
)


class LiderSupermercado(StoreWithUrlExtensions):
    base_url = "https://apps.lider.cl/supermercado"
    headers = {
        "tenant": "supermercado",
        "x-channel": "SOD",
    }
    user_agents = [
        "Mozilla/5.0 (X11; Fedora; Linux x86_64; rv:124.0) Gecko/20100101 Firefox/124.0",
        "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:123.0) Gecko/20100101 Firefox/123.0",
        "Mozilla/5.0 (X11; Debian; Linux x86_64; rv:122.0) Gecko/20100101 Firefox/122.0",
        "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:115.0) Gecko/20100101 Firefox/115.0",
        "Mozilla/5.0 (X11; Linux x86_64; rv:130.0) Gecko/20100101 Firefox/130.0",
        "Mozilla/5.0 (X11; Arch Linux; Linux x86_64; rv:124.0) Gecko/20100101 Firefox/124.0",
        "Mozilla/5.0 (Linux; Android 13; Redmi Note 11) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.6778.135 Mobile Safari/537.36",
        "Mozilla/5.0 (Linux; Android 11; Pixel 4a) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.6778.135 Mobile Safari/537.36 EdgA/131.0.2903.87",
        "Mozilla/5.0 (Linux; Android 12; SM-G998B) AppleWebKit/537.36 (KHTML, like Gecko) SamsungBrowser/24.0 Chrome/131.0.6778.135 Mobile Safari/537.36",
        "Mozilla/5.0 (Linux; Android 13; SAMSUNG SM-G990B) AppleWebKit/537.36 (KHTML, like Gecko) SamsungBrowser/24.0 Chrome/123.0.6312.105 Mobile Safari/537.36",
        "Mozilla/5.0 (Linux; Android 12; 220733SG Build/SP1A.210812.016) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.6778.135 Mobile Safari/537.3",
        "Mozilla/5.0 (iPhone; CPU iPhone OS 16_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.4 Mobile/15E148 Safari/604.1",
        "Mozilla/5.0 (iPad; CPU OS 16_4 like Mac OS X) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36 Edg/123.0.2420.65",
    ]
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
    def discover_urls_for_url_extension(cls, url_extension, extra_args=None):
        return [f"{cls.base_url}/category/{url_extension.replace(' ', '_')}"]

    @classmethod
    def products_for_url(cls, url, category=None, extra_args=None):
        session = session_with_proxy(extra_args)
        session.headers = cls.headers
        page = 1
        seen_keys = set()
        section = url.split(f"{cls.base_url}/category/")[-1].replace("_", " ")

        while True:
            if page >= 50:
                raise Exception(f"Page overflow: {section}")

            print(f"{section} page {page}")

            payload = {
                "categories": section,
                "page": page,
                "facets": [],
                "sortBy": "",
                "hitsPerPage": 16,
            }
            tries = 0

            while True:
                try:
                    user_agent = cls.user_agents[tries]
                    session.headers["User-Agent"] = user_agent
                    response = session.post(
                        f"{cls.base_url}/bff/category", json=payload
                    )
                    json_data = response.json()
                    products = json_data["products"]

                    break
                except Exception as e:
                    tries += 1
                    time.sleep(10)

                    if tries > len(cls.user_agents) - 1:
                        raise e

            if not products:
                if page == 1:
                    raise Exception(f"Empty section: {section}")
                break

            for product in products:
                key = product["ID"]

                if key in seen_keys:
                    continue

                seen_keys.add(key)
                brand = product["brand"]
                specs = [
                    f"- {item['name']}: {item['value']}"
                    for item in product["specifications"]
                ]
                specs_str = "\n".join(specs)
                specs = f"- Marca: {brand}\n{specs_str}\n\n"
                description = f"{specs}{html_to_markdown(product['longDescription'])}"
                name = f"{brand} - {product['displayName']}"
                price = Decimal(product["price"]["BasePriceSales"])
                stock = -1 if product["available"] else 0
                images = product.get("images", {})

                if "largeImage" in images:
                    picture_urls = [images["largeImage"]]
                elif "defaultImage" in images:
                    picture_urls = [images["defaultImage"]]
                else:
                    picture_urls = []

                sku = product["itemNumber"]
                product_url = f"{cls.base_url}/product/sku/{key.split('PROD_')[1]}"

                p = Product(
                    name,
                    cls.__name__,
                    category,
                    product_url,
                    url,
                    key,
                    stock,
                    price,
                    price,
                    "CLP",
                    sku=sku,
                    picture_urls=picture_urls,
                    description=description,
                    skip_picture_url_validation=True,
                )

                yield p

            page += 1
