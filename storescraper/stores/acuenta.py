from decimal import Decimal
from storescraper.categories import GROCERIES
from storescraper.product import Product
from storescraper.store_with_url_extensions import StoreWithUrlExtensions
from storescraper.utils import (
    html_to_markdown,
    session_with_proxy,
)


class Acuenta(StoreWithUrlExtensions):
    base_url = "https://www.acuenta.cl"
    url_extensions = [
        # Bodegazo
        ("600106", GROCERIES),
        ("600107", GROCERIES),
        ("600109", GROCERIES),
        ("600105", GROCERIES),
        ("600103", GROCERIES),
        ("600112", GROCERIES),
        ("600206", GROCERIES),
        ("600207", GROCERIES),
        ("600208", GROCERIES),
        ("600205", GROCERIES),
        ("600203", GROCERIES),
        ("600211", GROCERIES),
        ("600306", GROCERIES),
        ("600308", GROCERIES),
        ("600305", GROCERIES),
        ("600303", GROCERIES),
        ("600311", GROCERIES),
        # Despensa
        ("050101", GROCERIES),
        ("050102", GROCERIES),
        ("050103", GROCERIES),
        ("051601", GROCERIES),
        ("051602", GROCERIES),
        ("051603", GROCERIES),
        ("051201", GROCERIES),
        ("051202", GROCERIES),
        ("051203", GROCERIES),
        ("051204", GROCERIES),
        ("050301", GROCERIES),
        ("050302", GROCERIES),
        ("050601", GROCERIES),
        ("050602", GROCERIES),
        ("050603", GROCERIES),
        ("050201", GROCERIES),
        ("050202", GROCERIES),
        ("050204", GROCERIES),
        ("050203", GROCERIES),
        ("050205", GROCERIES),
        ("051501", GROCERIES),
        ("051503", GROCERIES),
        ("051502", GROCERIES),
        ("051506", GROCERIES),
        ("051504", GROCERIES),
        ("051507", GROCERIES),
        ("051901", GROCERIES),
        ("051902", GROCERIES),
        ("051903", GROCERIES),
        ("051904", GROCERIES),
        ("051905", GROCERIES),
        ("051801", GROCERIES),
        ("051802", GROCERIES),
        ("051803", GROCERIES),
        ("052002", GROCERIES),
        ("052001", GROCERIES),
        ("052003", GROCERIES),
        ("051703", GROCERIES),
        ("051702", GROCERIES),
        ("051701", GROCERIES),
        ("051704", GROCERIES),
        # Frescos y Lácteos
        ("070301", GROCERIES),
        ("070302", GROCERIES),
        ("070309", GROCERIES),
        ("070303", GROCERIES),
        ("070305", GROCERIES),
        ("070307", GROCERIES),
        ("070308", GROCERIES),
        ("070306", GROCERIES),
        ("070304", GROCERIES),
        ("070801", GROCERIES),
        ("070803", GROCERIES),
        ("070802", GROCERIES),
        ("070201", GROCERIES),
        ("070202", GROCERIES),
        ("070203", GROCERIES),
        ("070204", GROCERIES),
        ("070701", GROCERIES),
        ("070702", GROCERIES),
        ("070703", GROCERIES),
        ("070704", GROCERIES),
        ("070102", GROCERIES),
        ("070103", GROCERIES),
        ("070101", GROCERIES),
        ("070104", GROCERIES),
        ("070601", GROCERIES),
        ("070602", GROCERIES),
        ("070603", GROCERIES),
        ("070901", GROCERIES),
        ("070902", GROCERIES),
        # Carnes y Pescados
        ("0305", GROCERIES),
        ("0304", GROCERIES),
        ("0302", GROCERIES),
        # ("0306", GROCERIES),
        ("0303", GROCERIES),
        ("0309", GROCERIES),
        ("0307", GROCERIES),
        ("0310", GROCERIES),
        # Bebidas y Snacks
        ("020101", GROCERIES),
        ("020102", GROCERIES),
        ("020103", GROCERIES),
        ("020201", GROCERIES),
        ("020202", GROCERIES),
        ("020203", GROCERIES),
        ("020204", GROCERIES),
        ("020502", GROCERIES),
        ("020503", GROCERIES),
        ("020501", GROCERIES),
        ("020505", GROCERIES),
        ("020901", GROCERIES),
        ("020902", GROCERIES),
        ("020801", GROCERIES),
        ("020802", GROCERIES),
        ("020803", GROCERIES),
        ("020804", GROCERIES),
        ("020805", GROCERIES),
        ("020806", GROCERIES),
        ("020807", GROCERIES),
        ("020808", GROCERIES),
        ("020701", GROCERIES),
        ("020702", GROCERIES),
        ("020703", GROCERIES),
        # Desayuno y Dulces
        ("440101", GROCERIES),
        ("440102", GROCERIES),
        ("440105", GROCERIES),
        ("440103", GROCERIES),
        ("440106", GROCERIES),
        ("440107", GROCERIES),
        ("440108", GROCERIES),
        ("440401", GROCERIES),
        ("440402", GROCERIES),
        ("440403", GROCERIES),
        ("440404", GROCERIES),
        ("440406", GROCERIES),
        ("440304", GROCERIES),
        ("440303", GROCERIES),
        ("440301", GROCERIES),
        ("440302", GROCERIES),
        ("440604", GROCERIES),
        ("440601", GROCERIES),
        ("440602", GROCERIES),
        ("440603", GROCERIES),
        ("440503", GROCERIES),
        ("440501", GROCERIES),
        ("440504", GROCERIES),
        ("440506", GROCERIES),
        ("440505", GROCERIES),
        ("440507", GROCERIES),
        # El Bar
        ("8004", GROCERIES),
        # Congelados
        ("0409", GROCERIES),
        ("0407", GROCERIES),
        ("0403", GROCERIES),
        ("0406", GROCERIES),
        ("0402", GROCERIES),
        ("0405", GROCERIES),
        # Frutas y Verduras
        ("0601", GROCERIES),
        ("0602", GROCERIES),
        # Panadería y Pastelería
        ("100101", GROCERIES),
        ("100102", GROCERIES),
        ("100103", GROCERIES),
        ("100104", GROCERIES),
        ("100201", GROCERIES),
        ("100202", GROCERIES),
        ("1004", GROCERIES),
    ]

    @classmethod
    def discover_urls_for_url_extension(cls, url_extension, extra_args=None):
        return [f"{cls.base_url}/ca/{url_extension}"]

    @classmethod
    def products_for_url(cls, url, category=None, extra_args=None):
        session = session_with_proxy(extra_args)
        page = 1
        payload = [
            {
                "operationName": "GetProductsByCategory",
                "variables": {
                    "getProductsByCategoryInput": {
                        "categoryReference": url.split(f"{cls.base_url}/ca/")[1],
                        "clientId": "SUPER_BODEGA",
                        "storeReference": "580",
                        "pageSize": 100,
                    }
                },
                "query": "query GetProductsByCategory($getProductsByCategoryInput: GetProductsByCategoryInput!) {\
                    getProductsByCategory(getProductsByCategoryInput: $getProductsByCategoryInput) {\
                        category {\
                            products {\
                                brand\
                                description\
                                name\
                                photosUrl\
                                price\
                                promotion {\
                                    type\
                                    isActive\
                                    conditions {\
                                        price\
                                    }\
                                }\
                                sku\
                                slug\
                                stock\
                                unit\
                                subUnit\
                                subQty\
                            }\
                        }\
                    }\
                }",
            }
        ]

        while True:
            if page >= 10:
                raise Exception(f"Page overflow: {url}")

            print(f"{url} page {page}")

            payload[0]["variables"]["getProductsByCategoryInput"]["currentPage"] = page
            response = session.post(
                "https://nextgentheadless.instaleap.io/api/v3", json=payload
            )
            json_data = response.json()
            products = json_data[0]["data"]["getProductsByCategory"]["category"][
                "products"
            ]

            if not products:
                if page == 1:
                    raise Exception(f"Empty section: {url}")
                break

            for product in products:
                brand = product["brand"]
                suffix = product["unit"]
                sub_qty = product["subQty"]

                if sub_qty:
                    suffix += f" / {product['subQty']} {product['subUnit']}"

                name = f"{brand} - {product['name']} ({suffix})"
                price = Decimal(product["price"])
                promotion = product["promotion"]

                if (
                    promotion
                    and promotion["type"] == "specialPrice"
                    and promotion["isActive"]
                ):
                    conditions = promotion["conditions"]
                    assert len(conditions) == 1
                    price = Decimal(conditions[0]["price"])

                product_url = f"{cls.base_url}/p/{product['slug']}"
                sku = product["sku"]
                specs = f"- Marca: {brand}\n\n"
                stock = product["stock"]
                picture_urls = [f"{img}=0" for img in product["photosUrl"]]
                description = f"{specs}{html_to_markdown(product['description'])}"

                p = Product(
                    name,
                    cls.__name__,
                    category,
                    product_url,
                    url,
                    sku,
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
