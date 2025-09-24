import json

from bs4 import BeautifulSoup

from storescraper.stores.lider import Lider
import validators
from decimal import Decimal
from storescraper.product import Product
from storescraper.utils import (
    html_to_markdown,
    remove_words,
    cf_session_with_proxy,
)


class LiderV2(Lider):
    preferred_products_for_url_concurrency = 10

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

        base_url = f"https://www.lider.cl/browse/a/{category_id}"
        if exclude_marketplace:
            base_url += "?facet=ss_sellertype%3ALider"

        page = 1

        while True:
            print(f"{category_id} Page: {page}")
            separator = "&" if "?" in base_url else "?"
            url = f"{base_url}{separator}page={page}"
            print(url)
            page_data = cls.fetch_page(url, extra_args)

            products_data = page_data["props"]["pageProps"]["initialData"][
                "searchResult"
            ]["itemStacks"][0]["items"]

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
        page_data = cls.fetch_page(url, extra_args)
        product_data = page_data["props"]["pageProps"]["initialData"]["data"]["product"]

        name = f"{product_data['brand']} {product_data['name']}"
        key = product_data["offerId"]
        price_info = product_data["priceInfo"]
        current_price = price_info["currentPrice"]

        if not current_price:
            return []

        normal_price = Decimal(current_price["price"])
        offer_price = normal_price
        promo_data = [
            promo_entry
            for promo_entry in product_data["promoData"]
            if promo_entry["type"] == "liderBCI"
        ]

        if promo_data:
            assert len(promo_data) == 1
            offer_price = Decimal(
                remove_words(promo_data[0]["templateData"]["priceString"])
            )

        sku = product_data["usItemId"]
        picture_urls = [
            img["url"].split("?")[0]
            for img in product_data["imageInfo"]["allImages"]
            if validators.url(img["url"].split("?")[0])
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

        description = html_to_markdown(
            page_data["props"]["pageProps"]["initialData"]["data"]["idml"][
                "longDescription"
            ]
        )
        for entry in page_data["props"]["pageProps"]["initialData"]["data"]["idml"][
            "specifications"
        ]:
            description += f"\n{entry['name']}: {entry['value']}"

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
    def fetch_page(cls, url, extra_args):
        extra_args = extra_args or {}
        for user_agent in cls.USER_AGENTS:
            print(user_agent)
            extra_args["impersonate"] = user_agent
            session = cf_session_with_proxy(extra_args)
            response = session.get(url)
            soup = BeautifulSoup(response.text, "lxml")
            next_tag = soup.find("script", {"id": "__NEXT_DATA__"})
            if next_tag:
                return json.loads(next_tag.text)
        raise Exception("No user agents left")
