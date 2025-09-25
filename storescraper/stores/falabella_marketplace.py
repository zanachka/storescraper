import logging
from storescraper.categories import TELEVISION
from storescraper.stores import Falabella


class FalabellaMarketplace(Falabella):
    seller_filter = "f.derived.variant.sellerId_popularBrand=FALABELLA Y MEJORES MARCAS"
    seller_blacklist = ["FALABELLA", "SODIMAC", "TOTTUS"]

    @classmethod
    def sections(cls):
        raise NotImplementedError("This method is not needed for this scraper")

    @classmethod
    def section_positions(cls, section, extra_args=None):
        raise NotImplementedError("This method is not needed for this scraper")

    @classmethod
    def banners(cls, extra_args=None):
        raise AttributeError("This method is not needed for this scraper")
