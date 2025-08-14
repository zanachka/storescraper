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
            response = session.post(f"{cls.base_url}/bff/category", json=payload)
            json_data = response.json()
            products = json_data["products"]

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
                picture_urls = [
                    f"{img}=0" for img in product["images"]["availableImages"]
                ]
                sku = product["itemNumber"]
                discovery_url = f"{cls.base_url}/product/sku/{key.split('PROD_')[1]}"

                p = Product(
                    name,
                    cls.__name__,
                    category,
                    url,
                    discovery_url,
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

            page += 1
