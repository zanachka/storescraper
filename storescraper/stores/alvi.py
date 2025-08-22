import json
import logging
from decimal import Decimal
from bs4 import BeautifulSoup
from storescraper.categories import GROCERIES
from storescraper.product import Product
from storescraper.store_with_url_extensions import StoreWithUrlExtensions
from storescraper.utils import check_ean13, session_with_proxy


class Alvi(StoreWithUrlExtensions):
    url_extensions = [
        # Abarrotes
        ("abarrotes/aceites", GROCERIES),
        ("abarrotes/arroz", GROCERIES),
        ("abarrotes/harina", GROCERIES),
        ("abarrotes/legumbres", GROCERIES),
        ("abarrotes/pastas", GROCERIES),
        ("abarrotes/azucar", GROCERIES),
        ("abarrotes/pure", GROCERIES),
        ("abarrotes/pescados-en-conserva", GROCERIES),
        ("abarrotes/mariscos-en-conserva", GROCERIES),
        ("abarrotes/frutas-en-conserva", GROCERIES),
        ("abarrotes/caldos-y-sopas-instantaneas", GROCERIES),
        ("abarrotes/vinagres-y-jugo-de-limon", GROCERIES),
        ("abarrotes/salsas-de-tomates", GROCERIES),
        ("abarrotes/cafe", GROCERIES),
        ("abarrotes/te-y-hierbas", GROCERIES),
        ("abarrotes/cereales", GROCERIES),
        ("abarrotes/endulzantes", GROCERIES),
        ("abarrotes/verduras-en-conserva", GROCERIES),
        ("abarrotes/condimentos", GROCERIES),
        # Confitería y snacks
        ("confiteria-y-snacks/galletas-dulces", GROCERIES),
        ("confiteria-y-snacks/galletas-colacion", GROCERIES),
        ("confiteria-y-snacks/confites", GROCERIES),
        ("confiteria-y-snacks/chocolates", GROCERIES),
        ("confiteria-y-snacks/snacks-y-coctel", GROCERIES),
        # Panadería y repostería
        ("panaderia-y-reposteria/pan", GROCERIES),
        ("panaderia-y-reposteria/tortillas-y-masas", GROCERIES),
        ("panaderia-y-reposteria/pasteles", GROCERIES),
        ("panaderia-y-reposteria/reposteria", GROCERIES),
        ("panaderia-y-reposteria/postres-en-polvo", GROCERIES),
        ("panaderia-y-reposteria/manjar-y-mermeladas", GROCERIES),
        # Lácteos, refrigerados y huevos
        ("lacteos-refrigerados-y-huevos/mantequillas", GROCERIES),
        ("lacteos-refrigerados-y-huevos/yoghurt", GROCERIES),
        ("lacteos-refrigerados-y-huevos/leches-liquidas", GROCERIES),
        ("lacteos-refrigerados-y-huevos/cremas", GROCERIES),
        ("lacteos-refrigerados-y-huevos/leche-en-polvo", GROCERIES),
        ("lacteos-refrigerados-y-huevos/postres", GROCERIES),
        ("lacteos-refrigerados-y-huevos/huevos", GROCERIES),
        ("lacteos-refrigerados-y-huevos/quesos", GROCERIES),
        ("lacteos-refrigerados-y-huevos/bebidas-vegetales", GROCERIES),
        # Fiambrería
        ("fiambreria/cecinas", GROCERIES),
        ("fiambreria/embutidos", GROCERIES),
        # Congelados
        ("congelados/pescaderia", GROCERIES),
        ("congelados/hamburguesas-y-apanados", GROCERIES),
        ("congelados/frutas-y-verduras-congeladas", GROCERIES),
        ("congelados/comida-congelada", GROCERIES),
        ("congelados/helados-y-hielo", GROCERIES),
        # Carnicería
        ("carniceria/vacuno", GROCERIES),
        ("carniceria/molida", GROCERIES),
        ("carniceria/cerdo", GROCERIES),
        ("carniceria/pollo", GROCERIES),
        ("carniceria/carbon", GROCERIES),
        # Bebidas
        ("bebidas/jugos-en-polvo", GROCERIES),
        ("bebidas/gaseosas", GROCERIES),
        ("bebidas/nectares-y-jugos-liquidos", GROCERIES),
        ("bebidas/energeticas-e-isotonicas", GROCERIES),
        ("bebidas/aguas", GROCERIES),
    ]

    @classmethod
    def discover_urls_for_url_extension(cls, url_extension, extra_args=None):
        session = session_with_proxy(extra_args)
        page = 1

        while True:
            if page >= 30:
                raise Exception(f"Page overflow: {url_extension}")

            print(f"{url_extension} page {page}")

            response = session.get(
                f"https://www.alvi.cl/category/{url_extension}?page={page}"
            )

            soup = BeautifulSoup(response.text, "lxml")
            page_script = soup.find("script", {"type": "application/json"})
            products_data = json.loads(page_script.text)["props"]["pageProps"][
                "dehydratedState"
            ]["queries"][0]["state"]["data"]

            available_products = products_data["availableProducts"]
            not_available_products = products_data["notAvailableProducts"]

            if not available_products and not not_available_products:
                if page == 1:
                    logging.warning(f"Empty section: {url_extension}")
                break

            for product in available_products + not_available_products:
                product_url = f"https://www.alvi.cl/product{product['detailUrl'][:-2]}"
                yield product_url

            page += 1

    @classmethod
    def products_for_url(cls, url, category=None, extra_args=None):
        print(url)
        session = session_with_proxy(extra_args)
        slug = url.split("https://www.alvi.cl/product/")[1]
        response = session.get(f"https://bff-alvi-web.alvi.cl/products/by-slug/{slug}")
        product_data = response.json()

        key = product_data["productId"]
        sku = product_data["refId"]
        brand = product_data["brand"]

        if (
            product_data["unitMultiplier"] == 1
            and product_data["measurementUnit"] == "un"
        ):
            # Use the given format or else the default (eg. https://www.alvi.cl/product/pan-blanco-bauducco-390gr)
            suffix = product_data["format"] or "1 un"
        else:
            suffix = (
                f"{product_data['unitMultiplier']} {product_data['measurementUnit']}"
            )

        name = f"{brand} - {product_data['name']} ({suffix})"
        description = f"- Marca: {brand}" + "\n\n" + product_data["description"]
        picture_urls = product_data["images"]
        raw_ean = product_data["ean"]
        ean = raw_ean if check_ean13(raw_ean) else None

        for seller in product_data["sellers"]:
            if seller["sellerName"] == "Alvi Supermercados Mayoristas S.A.":
                price = Decimal(seller["price"])
                in_offer = seller["inOffer"]
                stock = 0 if seller["availableQuantity"] == 0 else -1
                break
        else:
            return []

        offer_price = price

        if in_offer:
            for price_step in product_data.get("priceSteps", []):
                if price_step["minQuantity"] == 1:
                    offer_price = Decimal(price_step["promotionalPrice"])
                    break

        if offer_price > price:
            offer_price = price

        if price == 0:
            return []

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
            sku=sku,
            picture_urls=picture_urls,
            description=description,
            ean=ean,
        )

        return [p]
