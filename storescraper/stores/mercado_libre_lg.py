from .mercado_libre_chile import MercadoLibreChile
from ..categories import (
    STEREO_SYSTEM,
    TELEVISION,
)


class MercadoLibreLg(MercadoLibreChile):
    store = "lg"
    categories_path = [
        (
            "electronica-audio-video/televisores",
            TELEVISION,
            "Tiendas oficiales > LG > Electrónica, Audio y Video > Televisores",
        ),
        (
            "electronica-audio-video/audio",
            STEREO_SYSTEM,
            "Tiendas oficiales > LG > Electrónica, Audio y Video > Audio",
        ),
    ]

    @classmethod
    def products_for_url(cls, url, category=None, extra_args=None):
        # Remove the seller because we consider MecadoLibreLg to be a
        # standalone retailer, in particular because the LG WTB system
        # only displays entries without a seller (not from marketplaces)
        # and we want to consider MercadoLibreLG for that.
        products = super().products_for_url(
            url, category=category, extra_args=extra_args
        )

        for product in products:
            product.seller = None
            yield product

    @classmethod
    def preflight(cls, extra_args=None):
        extra_args["cookie"] += ";_d2id=cbec39c3-857e-42a5-9bf5-7fefc694f6ae"
        return super().preflight(extra_args)
