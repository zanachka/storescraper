import json
from decimal import Decimal

from bs4 import BeautifulSoup

from storescraper.categories import NOTEBOOK, CELL, TABLET, WEARABLE, HEADPHONES
from storescraper.product import Product
from storescraper.store_with_url_extensions import StoreWithUrlExtensions
from storescraper.utils import html_to_markdown, session_with_proxy


class HuaweiShop(StoreWithUrlExtensions):
    url_extensions = [
        # Cells
        ["smartphones", CELL],
        # Notebooks
        ["notebooks", NOTEBOOK],
        # Tablets
        ["tablets", TABLET],
        # Wearables
        ["wearables", WEARABLE],
        # Headphones
        ["audio", HEADPHONES],
    ]

    @classmethod
    def discover_urls_for_url_extension(cls, url_extension, extra_args=None):
        if url_extension == "notebooks":
            # Discontinued category, just return the sole product remaining
            return ["https://consumer.huawei.com/cl/laptops/matebook-d-16-2024/buy/"]

        session = session_with_proxy(extra_args)
        product_urls = []
        url_webpage = "https://consumer.huawei.com/cl/offer/{}/".format(url_extension)

        data = session.get(url_webpage).text
        soup = BeautifulSoup(data, "lxml")

        candidate_tags = soup.findAll("item", {"data-key": "card-instance"})
        for tag in candidate_tags:
            tag_value = json.loads(tag["data-value"])
            try:
                product_list = tag_value["props"]["configuration"]["custom"][
                    "cardParameter"
                ]["allEnds"]["moduleData"]["productList"]
                for product_entry in product_list:
                    product_url = cls._clean_discovery_url(product_entry["linkUrl"])
                    if product_url not in product_urls:
                        product_urls.append(product_url)
            except KeyError:
                pass

            try:
                product_list = tag_value["props"]["configuration"]["custom"][
                    "cardParameter"
                ]["allEnds"]["moduleData"]["productSets"]["productInfo"]
                for product_entry in product_list:
                    product_url = cls._clean_discovery_url(product_entry["linkUrl"])
                    if product_url not in product_urls:
                        product_urls.append(product_url)
            except KeyError:
                pass

        return product_urls

    @classmethod
    def _clean_discovery_url(cls, product_url):
        if product_url.startswith("http://consumer.huawei.com"):
            product_url = product_url.replace("http", "https")
        if not product_url.startswith("https"):
            product_url = "https://consumer.huawei.com" + product_url
        if "huawei.com//" in product_url:
            product_url = product_url.replace("huawei.com//", "huawei.com/")
        if not product_url.startswith("https://consumer.huawei.com/cl/product/buy/"):
            product_url = product_url.split("?")[0]

        return product_url

    @classmethod
    def products_for_url(cls, url, category=None, extra_args=None):
        print(url)
        session = session_with_proxy(extra_args)
        response = session.get(url)
        soup = BeautifulSoup(response.text, "lxml")

        base_products_tag = soup.find("input", {"id": "productAssembleData"})
        if base_products_tag:
            base_products = json.loads(base_products_tag["value"])
            product_ids = [x["productId"] for x in base_products]
        else:
            product_id_tag = soup.find("input", {"id": "productId"})
            if product_id_tag:
                product_ids = [product_id_tag["value"]]
            elif "productId" in url:
                product_ids = [url.split("productId=")[1]]
            else:
                return []
        products = []

        for product_id in product_ids:
            query_url = (
                "https://itrinity-sg.c.huawei.com/eCommerce/queryPrd"
                "DisplayDetailInfo?productId={}&siteCode=CL".format(product_id)
            )
            product_json = json.loads(session.get(query_url).text)
            sbom_codes = []

            if "errorDetail" in product_json["data"]:
                continue

            for product_entry in product_json["data"]["sbomList"]:
                sbom_codes.append(product_entry["sbomCode"])
                for subvariant in product_entry["sbomPackageList"] or []:
                    for package in subvariant["packageList"]:
                        sbom_codes.append(package["sbomCode"])

            products_id = "%2C".join(sbom_codes)
            json_stock = json.loads(
                session.get(
                    "https://itrinity-sg.c.huawei."
                    "com/eCommerce/querySkuInventory?"
                    "skuCodes={}&siteCode=CL".format(products_id)
                ).text
            )

            if "inventoryReqVOs" not in json_stock["data"]:
                return []

            stock_dict = {
                x["skuCode"]: x["inventoryQty"]
                for x in json_stock["data"]["inventoryReqVOs"]
            }

            prices_endpoint = (
                "https://itrinity-sg.c.huawei.com/convert/"
                "querySkuDetailDispAndInv?skuCodes={}&"
                "groupFlag=true&siteCode=CL&loginFrom=1".format(products_id)
            )
            prices_res = session.get(prices_endpoint).json()
            price_per_sbom = {
                x["skuPriceInfo"]["sbomCode"]: Decimal(x["skuPriceInfo"]["salePrice"])
                for x in prices_res["data"]["detailDispInfos"]
            }

            specs_res = session.get(f"{url}/specs/")
            specs_soup = BeautifulSoup(specs_res.text, "lxml")
            specs_tag = specs_soup.find("ul", "large-accordion__list")
            description = html_to_markdown(specs_tag.text) if specs_tag else None

            for product in product_json["data"]["sbomList"]:
                base_stock = stock_dict[product["sbomCode"]]
                name = product["name"]
                picture_urls = [
                    "https://img01.huaweifile.com/sg/ms/cl/pms"
                    + product["photoPath"]
                    + "800_800_"
                    + product["photoName"]
                ]

                if product["sbomPackageList"]:
                    for subvariant in product["sbomPackageList"]:
                        sku = f'{product["sbomCode"]} - {subvariant["packageCode"]}'
                        subvariant_name = "{} {}".format(name, subvariant["name"])
                        packages_stock = [
                            stock_dict[package["sbomCode"]]
                            for package in subvariant["packageList"]
                        ]
                        subvariant_stock = min(packages_stock + [base_stock])
                        price = Decimal(subvariant["packageTotalPrice"])
                        p = Product(
                            subvariant_name,
                            cls.__name__,
                            category,
                            url,
                            url,
                            sku,
                            subvariant_stock,
                            price,
                            price,
                            "CLP",
                            sku=sku,
                            picture_urls=picture_urls,
                            description=description,
                        )
                        products.append(p)

                sku = product["sbomCode"]

                if sku not in price_per_sbom:
                    continue

                price = price_per_sbom[sku]

                p = Product(
                    name,
                    cls.__name__,
                    category,
                    url,
                    url,
                    sku,
                    base_stock,
                    price,
                    price,
                    "CLP",
                    sku=sku,
                    picture_urls=picture_urls,
                    description=description,
                )
                products.append(p)

        return products
