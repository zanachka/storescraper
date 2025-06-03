import re
from decimal import Decimal
from storescraper.categories import TELEVISION
from storescraper.product import Product
from storescraper.store import Store
from storescraper.utils import session_with_proxy


class Diunsa(Store):
    @classmethod
    def categories(cls):
        return [TELEVISION]

    @classmethod
    def discover_urls_for_category(cls, category, extra_args=None):
        # Only gets LG products

        if category != TELEVISION:
            return []

        session = session_with_proxy(extra_args)
        session.headers["Content-Type"] = "application/json"
        offset = 0
        done = False

        while not done:
            if offset > 1000:
                raise Exception("Page overflow")

            url = f"https://apicsm.dapplications.tech/api/em/material/paginate?skip={offset}&take=15"
            print(url)
            payload = '{"businessPartner":1,"storeId":null,"groupCode":"0","officeCode":"0","type":"PD","sortBy":"category","sortOption":"ASC","search":"lg","filter":{"priceMin":null,"priceMax":null,"brand":null,"supplier":null},"source":"WEB","hidden":"0"}'
            response = session.post(url, payload).json()

            if response["data"] == []:
                break

            for product in response["data"]:
                if product["brandName"] != "LG":
                    continue
                product_url = f"https://www.diunsa.hn/producto/{product['name'].lower().replace(' ', '-').replace('/', '-').replace('--', '-')}-{product['code']}"
                yield product_url

            offset += 15

    @classmethod
    def products_for_url(cls, url, category=None, extra_args=None):
        print(url)
        sku = re.search(r"([^-]+-[^-]+)$", url).group(1)
        session = session_with_proxy(extra_args)
        endpoint = f"https://apicsm.dapplications.tech/api/em/material/get/{sku}/PD/0"
        response = session.get(endpoint).json()[0]
        assert response["variants"] == []
        name = response["name"]
        part_number = response["nameAlias"]
        price = Decimal(response["newPrice"])
        description = response["descriptionLong"]
        picture_urls = [img["fileLink"] for img in response["images"]]

        p = Product(
            name,
            cls.__name__,
            category,
            url,
            url,
            sku,
            -1,
            price,
            price,
            "HNL",
            sku=sku,
            part_number=part_number,
            description=description,
            picture_urls=picture_urls,
        )

        return [p]
