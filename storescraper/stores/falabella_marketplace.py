import logging
from storescraper.categories import TELEVISION
from storescraper.stores import Falabella


class FalabellaMarketplace(Falabella):
    category_paths = [
        ["LG ELECTRONICS INC CHILE LIMITADA", TELEVISION, None],
        ["LG Electronics", TELEVISION, None],
        ["SAMSUNG", TELEVISION, None],
    ]

    @classmethod
    def _get_product_urls(
        cls,
        session,
        category_id,
        extra_params,
        seller_id,
        zones,
        add_sponsored_data=False,
    ):
        # In the context of FalabellaMarketplace "category_id" maps to the name of the seller
        discovered_urls = set()
        page = 1
        while True:
            if page > 210:
                raise Exception(f"Page overflow: {category_id}")

            url = f"https://www.falabella.com/s/browse/v1/seller/cl?name=undefined&page={page}&sellerName={category_id}&pgid=96&pid=d83bd30c-804e-438a-a097-8bbc915b7a9d"
            print(url)
            res = cls.retrieve_json_page(session, url)

            if "results" not in res or not res["results"]:
                if page == 1:
                    logging.warning(f"Empty page: {category_id} - {extra_params}")
                break

            for result in res["results"]:
                product_url = cls.product_url_template.format(
                    result["productId"], result["skuId"]
                )

                if product_url not in discovered_urls:
                    discovered_urls.add(product_url)
                    yield product_url
            page += 1

    @classmethod
    def sections(cls):
        raise NotImplementedError("This method is not needed for this scraper")

    @classmethod
    def section_positions(cls, section, extra_args=None):
        raise NotImplementedError("This method is not needed for this scraper")

    @classmethod
    def banners(cls, extra_args=None):
        raise AttributeError("This method is not needed for this scraper")
