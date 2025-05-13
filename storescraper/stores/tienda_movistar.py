from storescraper.categories import (
    HEADPHONES,
    TABLET,
    CELL,
    STEREO_SYSTEM,
    TELEVISION,
)
from .movistar import Movistar


class TiendaMovistar(Movistar):
    variations = []
    category_paths = [
        ("Electronica > Comunicacion > Telefonia > Telefonos moviles", CELL),
        ("Electronica > Ordenadores > Tablets", TABLET),
        ("Electrónica > Audio > Equipo de sonido > Auriculares", HEADPHONES),
        ("Electrónica > Video > Televisores", TELEVISION),
        ("Electrónica > Audio > Equipo de sonido > Altavoces", STEREO_SYSTEM),
    ]

    @classmethod
    def categories(cls):
        return [
            CELL,
            TABLET,
            HEADPHONES,
            TELEVISION,
            STEREO_SYSTEM,
        ]

    @classmethod
    def products_for_url(cls, url, category=None, extra_args=None):
        products = super().products_for_url(url, category, extra_args)

        for product in products:
            product.key = product.sku

        return products
