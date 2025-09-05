import json
from storescraper.stores.lider import Lider
import validators
from decimal import Decimal
from pathlib import Path
from storescraper.product import Product
from storescraper.utils import (
    html_to_markdown,
    remove_words,
    cf_session_with_proxy,
)


class LiderV2(Lider):
    @classmethod
    def discover_urls_for_category(cls, category, extra_args=None):
        seen_urls = set()

        for category_id, local_category, _ in cls.category_paths:
            if category != local_category:
                continue

            for product_url in cls._get_product_urls(category_id, extra_args):
                if product_url not in seen_urls:
                    seen_urls.add(product_url)
                    yield product_url

    @classmethod
    def _get_product_urls(cls, category_id, extra_args, exclude_marketplace=True):
        query_url = "https://www.lider.cl/orchestra/graphql/browse"
        path = Path(__file__).with_name("lider_request.txt")

        with path.open("r") as f:
            graphql_query = f.read()

        page = 1

        while True:
            print(f"{category_id} Page: {page}")
            graphql_variables = {
                "page": page,
                "prg": "desktop",
                "catId": category_id,
                "sort": "best_match",
                "ps": 44,
                "fetchMarquee": True,
                "fetchSkyline": True,
                "fetchSbaTop": False,
                "fetchGallery": False,
                "fetchDac": False,
                "tenant": "CHILE_EA_GLASS",
                "enablePromoData": True,
            }

            if exclude_marketplace:
                graphql_variables["facet"] = "ss_sellertype:Lider"

            graphql_request_body = {
                "query": graphql_query,
                "variables": graphql_variables,
            }
            data = cls._run_impersonators(query_url, graphql_request_body, extra_args)
            products_data = data["data"]["search"]["searchResult"]["itemStacks"][0][
                "itemsV2"
            ]

            if not products_data:
                break

            for entry in products_data:
                product_url = f"https://www.lider.cl{entry['canonicalUrl']}"
                yield product_url

            page += 1

    @classmethod
    def section_positions(cls, section, extra_args=None):
        for category_id, _, section_path in cls.category_paths:
            if section != section_path:
                continue

            for idx, product_url in enumerate(
                cls._get_product_urls(
                    category_id,
                    extra_args,
                    exclude_marketplace=False,
                )
            ):
                if idx >= 300:
                    break

                yield {
                    "field": "discovery_url",
                    "value": product_url,
                    "position": idx + 1,
                    "section": section,
                    "is_sponsored": False,
                }

    @classmethod
    def products_for_url(cls, url, category=None, extra_args=None):
        print(url)
        sku = url.split("/")[-1]
        query_url = f"https://www.lider.cl/orchestra/graphql/ip/{sku}"
        p = Path(__file__).with_name("lider_product_request.txt")

        with p.open("r") as f:
            graphql_query = f.read()

        graphql_variables = {
            "pageType": "ItemPageGlobal",
            "tenant": "CHILE_EA_GLASS",
            "iId": sku,
            "fBBAd": True,
            "eLLBBAds": False,
            "fSL": True,
            "fIdml": True,
            "fMrkDscrp": False,
            "fRev": True,
            "fFit": True,
            "fSeo": True,
            "fP13": True,
            "fAff": True,
            "fMq": True,
            "fGalAd": False,
            "fSCar": True,
            "fDac": False,
            "spVid": False,
            "spSBA": False,
            "fBB": True,
            "eItIb": True,
            "fIlc": False,
            "fSId": True,
            "eSb": True,
            "eCc": False,
            "eSsm": False,
            "enableRelatedSearch": False,
            "enableDetailedBeacon": False,
            "sV": False,
            "sVC": False,
            "enablePromoData": True,
        }

        graphql_request_body = {"query": graphql_query, "variables": graphql_variables}
        data = cls._run_impersonators(query_url, graphql_request_body, extra_args)
        product_data = data["data"]["product"]

        name = f"{product_data['brand']} {product_data['name']}"
        key = product_data["offerId"]
        price_info = product_data["priceInfo"]
        normal_price = Decimal(price_info["currentPrice"]["price"])
        offer_price = normal_price
        promo_data = [
            promo_entry
            for promo_entry in product_data["promoData"]
            if promo_entry["type"] == "liderBCI"
        ]

        if promo_data:
            assert len(promo_data) == 1
            offer_price = Decimal(
                remove_words(promo_data[0]["templateData"]["priceString"].split(".")[0])
            )

        sku = product_data["usItemId"]
        picture_urls = [
            img["url"]
            for img in product_data["imageInfo"]["allImages"]
            if validators.url(img["url"])
        ]
        seller_name = product_data["sellerName"]
        seller = None if seller_name == "Lider" else seller_name
        stock = (
            -1
            if (
                product_data["availabilityStatusV2"]["value"] == "IN_STOCK"
                and seller_name == "Lider"
            )
            else 0
        )
        description_value = product_data["shortDescription"]
        description = html_to_markdown(description_value) if description_value else None

        product = Product(
            name,
            cls.__name__,
            category,
            url,
            url,
            key,
            stock,
            normal_price,
            offer_price,
            "CLP",
            sku=sku,
            picture_urls=picture_urls,
            description=description,
            seller=seller,
        )

        yield product

    @classmethod
    def _run_impersonators(cls, query_url, graphql_request_body, extra_args):
        for impersonator in cls.USER_AGENTS:
            print("Trying " + impersonator)
            extra_args = extra_args or {}
            extra_args["impersonate"] = impersonator
            session = cf_session_with_proxy(extra_args)

            session.headers.update(
                {
                    "Content-Type": "application/json",
                    "x-o-bu": "LIDER-CL",
                    "x-o-mart": "B2C",
                    "x-o-vertical": "EA",
                    "X-APOLLO-OPERATION-NAME": (
                        "Browse" if "browse" in query_url else "ItemById"
                    ),
                }
            )

            response = session.post(query_url, json=graphql_request_body)

            try:
                data = json.loads(response.text)
                return data
            except Exception:
                continue
        else:
            raise Exception("No user agents left")
