from .mercado_libre_chile import MercadoLibreChile
from storescraper.categories import (
    STEREO_SYSTEM,
    TELEVISION,
    CELL,
    WEARABLE,
    VACUUM_CLEANER,
    REFRIGERATOR,
    SPLIT_AIR_CONDITIONER,
    OVEN,
    WASHING_MACHINE,
    TABLET,
    DISH_WASHER,
    MONITOR,
    PROJECTOR,
)


class MercadoLibreSamsung(MercadoLibreChile):
    store = "samsung"
    categories_path = [
        (
            "electronica-audio-video/audio",
            STEREO_SYSTEM,
            "Tiendas oficiales > Samsung > Electrónica, Audio y Video > Audio",
        ),
        (
            "electronica-audio-video/televisores",
            TELEVISION,
            "Tiendas oficiales > Samsung > Electrónica, Audio y Video > Televisores",
        ),
        (
            "celulares-telefonia/celulares-smartphones",
            CELL,
            "Tiendas oficiales > Samsung > Celulares y Telefonía > Celulares y Smartphones",
        ),
        (
            "celulares-telefonia/smartwatches-accesorios",
            WEARABLE,
            "Tiendas oficiales > Samsung > Celulares y Telefonía > Smartwatches y Accesorios",
        ),
        (
            "electrodomesticos/pequenos-electrodomesticos/hogar/aspiradoras",
            VACUUM_CLEANER,
            "Tiendas oficiales > Samsung > Electrodomésticos > Pequeños Electrodomésticos > Para Hogar > Aspiradoras",
        ),
        (
            "electrodomesticos/refrigeracion/refrigeradores",
            REFRIGERATOR,
            "Tiendas oficiales > Samsung > Electrodomésticos > Refrigeración > Refrigeradores",
        ),
        (
            "electrodomesticos/climatizacion/aires-acondicionados",
            SPLIT_AIR_CONDITIONER,
            "Tiendas oficiales > Samsung > Electrodomésticos > Climatización > Aires Acondicionados",
        ),
        (
            "electrodomesticos/hornos-cocinas/cocinas",
            OVEN,
            "Tiendas oficiales > Samsung > Electrodomésticos > Hornos y Cocinas > Cocinas",
        ),
        (
            "electrodomesticos/hornos-cocinas/microondas",
            OVEN,
            "Tiendas oficiales > Samsung > Electrodomésticos > Hornos y Cocinas > Microondas",
        ),
        (
            "electrodomesticos/lavado/lavavajillas",
            DISH_WASHER,
            "Tiendas oficiales > Samsung > Electrodomésticos > Lavado > Lavavajillas",
        ),
        (
            "electrodomesticos/lavado/lavadora-secadoras",
            WASHING_MACHINE,
            "Tiendas oficiales > Samsung > Electrodomésticos > Lavado > Lavadora-Secadoras",
        ),
        (
            "computacion/tablets-accesorios/tablets",
            TABLET,
            "Tiendas oficiales > Samsung > Computación > Tablets y Accesorios > Tablets",
        ),
        (
            "computacion/monitores-accesorios",
            MONITOR,
            "Tiendas oficiales > Samsung > Computación > Monitores y Accesorios",
        ),
        (
            "electronica-audio-video/proyectores-telones",
            PROJECTOR,
            "Tiendas oficiales > Samsung > Electrónica, Audio y Video > Proyectores y Telones",
        ),
    ]

    @classmethod
    def products_for_url(cls, url, category=None, extra_args=None):
        # Remove the seller because we consider MecadoLibreSamsung to be a
        # standalone retailer, in particular because the Samsung WTB system
        # only displays entries without a seller (not from marketplaces)
        # and we want to consider MercadoLibreSamsung for that.
        products = super().products_for_url(
            url, category=category, extra_args=extra_args
        )

        for product in products:
            product.seller = None
            yield product
