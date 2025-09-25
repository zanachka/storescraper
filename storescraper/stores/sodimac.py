from storescraper import banner_sections as bs
from .falabella import Falabella


class Sodimac(Falabella):
    store_and_subdomain = "sodimac"
    section_position_variants = [
        {
            "section_prefix": "SODIMAC",
            "seller_filter": "f.derived.variant.sellerId=SODIMAC",
        },
        {
            "section_prefix": "GRUPO",
            "seller_filter": None,
        },
    ]
    seller_filter = "f.derived.variant.sellerId=SODIMAC"
    banners_base_url = "https://sodimac.falabella.com/sodimac-cl/{}"
    banners_sections_data = [
        [bs.HOME, "Home", bs.SUBSECTION_TYPE_HOME, ""],
    ]
    product_url_template = "https://www.sodimac.cl/sodimac-cl/articulo/{}/product/{}"

    @classmethod
    def products_for_url(cls, url, category=None, extra_args=None):
        products = super().products_for_url(
            url, category=category, extra_args=extra_args
        )

        for product in products:
            product.url = url
            product.discovery_url = url
            product.seller = None

        return products
