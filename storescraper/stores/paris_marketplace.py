from storescraper.categories import TELEVISION
from storescraper.stores import Paris
from storescraper.store import Store


class ParisMarketplace(Store):
    category_paths = [
        "https://www.paris.cl/refrigerador-bottom-mount-freezer-321l-space-max-MKSP7RC4KK.html",
        "https://www.paris.cl/refrigerador-bottom-mount-de-311l-all-around-cooling-MKN5ZPW6WK.html",
        "https://www.paris.cl/refrigerador-french-door-de-564l-family-hub-MKGUJ08PGD.html",
        "https://www.paris.cl/refrigerador-bottom-mount-290l-all-around-cooling-MKQRIMTEY5.html",
        "https://www.paris.cl/refrigerador-french-door-de-576-l-con-dual-ice-maker-MK4EA862YR.html",
        "https://www.paris.cl/refrigerador-side-by-side-con-dispensador-560l-negro-MKVNZZS5EF.html",
        "https://www.paris.cl/refrigerador-bottom-mount-462l-freezer-space-max-MK83B6ESB2.html",
        "https://www.paris.cl/refrigerador-top-mount-freezer-391-l-space-max-MKR5W06Q1N.html",
        "https://www.paris.cl/refrigerador-side-by-side-564l-gris-MKJQT7HJD7.html",
        "https://www.paris.cl/refrigerador-459-lt-bottom-mount-freezer-no-frost-MKL1U172R3.html",
        "https://www.paris.cl/refrigerador-top-mount-freezer-407l-space-max-MK7MKKUFKK.html",
        "https://www.paris.cl/refrigerador-side-by-side-585l-family-hub-MKYJ8CS76N.html",
        "https://www.paris.cl/refrigerador-bottom-mount-freezer-328l-space-max-MKXPC3Y9R6.html",
        "https://www.paris.cl/refrigerador-top-mount-freezer-234l-all-around-cooling-MKZ0MSVJXO.html",
        "https://www.paris.cl/refrigerador-top-mount-freezer-255l-all-around-cooling-MKCRA1M9Q6.html",
        "https://www.paris.cl/refrigerador-top-mount-freezer-384l-space-max-MKF9HNZ5C6.html",
        "https://www.paris.cl/refrigerador-top-mount-521-lt-no-frost-silver-MKVY6M47EJ.html",
        "https://www.paris.cl/refrigerador-top-mount-freezer-341l-space-max-MK68SEHDQS.html",
        "https://www.paris.cl/refrigerador-top-mount-freezer-298l-space-max-MKSLB4UKNU.html",
        "https://www.paris.cl/refrigerador-french-door-699l-bespoke-ai-family-hub-MKG146O13M.html",
        "https://www.paris.cl/samsung-refrigerador-384-l-top-freezer-MKKO4PYBJP.html",
        "https://www.paris.cl/refrigerador-fensa-436l-no-frost-side-by-side-sfx440b-negro-MKEZKFBOIC.html",
        "https://www.paris.cl/refrigerador-166l-frio-directo-bottom-freezer-med165b-MKA7MTV3DZ.html",
        "https://www.paris.cl/refrigerador-mademsa-231l-bottom-freezer-nordik-mr-415-plus-MKSZ92NU0Q.html",
        "https://www.paris.cl/refrigerador-540l-no-frost-3-puertas-advantage-plus-7790-MKEGO5QBNJ.html",
        "https://www.paris.cl/refrigerador-mademsa-303l-bottom-freezer-nordik-480-plus-MKYQCJT0EI.html",
        "https://www.paris.cl/refrigerador-cross-door-tcl-424-litros-p460cd-MK5T049UGN.html",
        "https://www.paris.cl/refrigerador-247l-no-frost-top-freezer-inverter-altus-1250-b-MK4VJU4X41.html",
        "https://www.paris.cl/refrigerador-fensa-298l-no-frost-3-puertas-inverter-dm64s-MKKQG8M78V.html",
        "https://www.paris.cl/refrigerador-fensa-401l-no-frost-4-puertas-inverter-dq79su-MK6B3ZR0FA.html",
        "https://www.paris.cl/refrigerador-side-by-side-tcl-488l-p520sbs-MKZKIQJ5NU.html",
        "https://www.paris.cl/refrigerador-488l-no-frost-bottom-freezer-inverter-ib55s-MKUKR86GNT.html",
        "https://www.paris.cl/refrigerador-top-mount-tcl-420-litros-p425tm-MKF342Q4MQ.html",
        "https://www.paris.cl/refrigerador-bottom-freezer-frio-directo-light-silver-259-lts-MKDD4ELNFL.html",
        "https://www.paris.cl/refrigerador-fensa-409l-no-frost-top-freezer-inverter-iw45s-MKG5GXP9X8.html",
        "https://www.paris.cl/lavadorasecadora-automatica-1511-kg-midea-MK2C2DOR73.html",
        "https://www.paris.cl/lavadora-automatica-95kg-fuzzy-automatico-95-szg-gris-MKC8PYRSBY.html",
        "https://www.paris.cl/lavadora-automatica-12kg-fuzzy-automatico-12-bzg-blanca-MKY8A25P3I.html",
        "https://www.paris.cl/lavadora-carga-frontal-12kg-MKDFA4GMXH.html",
        "https://www.paris.cl/lavadora-de-carga-superior-19kg-con-eco-bubbletm-blanca-MKN2X6DB8O.html",
        "https://www.paris.cl/samsung-lavadorasecadora-de-117-kg-con-eco-bubbletm-MKGY0CHBNV.html",
        "https://www.paris.cl/lavadora-automatica-18kg-carga-superior-premium-care-18-MKF2G1K21B.html",
        "https://www.paris.cl/lavadora-de-carga-superior-15kg-con-eco-bubbletm-blanca-MK99E4FUDT.html",
        "https://www.paris.cl/lavadora-de-carga-superior-15kg-con-eco-bubbletm-blanca-MK99E4FUDT.html",
        "https://www.paris.cl/samsung-lavadora-secadora-bespoke-ai-25-kg-MK1ZAAOD0I.html",
        "https://www.paris.cl/lavadora-de-carga-superior-9kg-con-tecnologia-digital-inverter-MKZN8U3XB4.html",
        "https://www.paris.cl/lavadora-secadora-125kg-7kg-con-inteligencia-artificial-en-panel-de-control-negra-MKLJCYYP0X.html",
        "https://www.paris.cl/samsung-lavadorasecadora-de-117-kg-con-eco-bubbletm-MK24OJJXQ8.html",
        "https://www.paris.cl/lavadora-automatica-16kg-disolucion-maxima-16-szg-gris-MKSZXR0WBQ.html",
        "https://www.paris.cl/lavadora-de-carga-superior-15kg-con-eco-bubbletm-MKURT8IGWP.html",
        "https://www.paris.cl/lavadora-de-carga-superior-15kg-con-eco-bubbletm-MKURT8IGWP.html",
        "https://www.paris.cl/lavadora-de-carga-superior-19kg-con-eco-bubble-MKFZY8KCCP.html",
        "https://www.paris.cl/lavadora-secadora-22kg-13kg-con-inteligencia-artificial-en-panel-de-control-MKOAY5ZX6K.html",
        "https://www.paris.cl/lavadora-de-carga-superior-13kg-con-eco-bubble-MKJ2OB1GMX.html",
        "https://www.paris.cl/lavadora-secadora-frontal-tcl-10kg7kg-c2210wd-MKN43IZLKR.html",
        "https://www.paris.cl/lavadora-carga-superior-tcl-11kg-f711tl-MK7WJNTKJ9.html",
        "https://www.paris.cl/lavadora-secadora-bespoke-14kg-9kg-con-inteligencia-artificial-en-ecobubble-MK1JOHCS5U.html",
        "https://www.paris.cl/lavadora-secadora-95kg-6kg-con-eco-bubble-MKRT3THS4Q.html",
        "https://www.paris.cl/lavadora-de-carga-superior-22kg-con-eco-bubble-MK0BJKCATO.html",
        "https://www.paris.cl/lavadora-automatica-carga-superior-deep-clean-16kg-midea-MK2RDAMGK2.html",
        "https://www.paris.cl/lavadora-de-carga-superior-17kg-con-eco-bubbletm-MKOCWLB37I.html",
        "https://www.paris.cl/lavadora-automatica-9kg-ultra-cube-3g-midea-MKX2DO35ZK.html",
        "https://www.paris.cl/lavadora-carga-superior-21-kg-ai-wash-MKUBF7LX12.html",
        "https://www.paris.cl/secadora-9kg-por-bomba-de-calor-MK31BJ6YER.html",
        "https://www.paris.cl/lavadora-automatica-18kg-disolucion-maxima-18-bzg-blanca-MKSKM1VHOS.html",
        "https://www.paris.cl/lavadora-secadora-fensa-8kg-carga-frontal-vapour-care-8wd-MK7M467ZTB.html",
        "https://www.paris.cl/lavadora-automatica-115kg-lavado-diferido-efficace-115-bzg-MK081B9I1B.html",
        "https://www.paris.cl/lavadora-secadora-25-kg-15-kg-bespoke-ai-lite-MK8WJ6O094.html",
        "https://www.paris.cl/lavadora-automatica-14kg-disolucion-maxima-14-bzg-blanca-MKN94ZMLGJ.html",
        "https://www.paris.cl/lavadora-automatica-11kg-carga-frontal-inverter-vapor-11w-MK2H95KQJG.html",
        "https://www.paris.cl/lavadora-secadora-18kg-10kg-con-smartthings-MKENYYMV13.html",
        "https://www.paris.cl/lavavajillas-14-cubiertos-con-smart-things-MK704WHQ4Y.html",
        "https://www.paris.cl/lavadora-secadora-20kg-12kg-con-inteligencia-artificial-en-panel-de-control-MK64BTMHNX.html",
        "https://www.paris.cl/lavadora-secadora-fensa-11kg-lavado-inteligente-11wd-gris-MKVKA0XVVR.html",
        "https://www.paris.cl/lavadora-de-carga-frontal-bespoke-25kg-con-sistema-de-lavado-inteligente-MKVI98VPWY.html",
        "https://www.paris.cl/lavavajillas-13-cubiertos-blanca-con-pantalla-led-MKCQ2E4K7T.html",
        "https://www.paris.cl/lavavajillas-9-cubiertos-programa-economico-9sz-inox-MKWKRVNVYG.html",
        "https://www.paris.cl/lavavajillas-14-cubiertos-funcion-higienzar-14-szg-inox-MKFI3H5LXP.html",
        "https://www.paris.cl/lavavajillas-14-cubiertos-funcion-higienzar-14-bzg-blanca-MKO62RQF5C.html",
        "https://www.paris.cl/samsung-lavavajillas-14-cubiertos-con-smart-things-MKDQFOLEVQ.html",
        "https://www.paris.cl/aire-acondicionado-portatil-12000-btu-friocalor-MK5U3L4HIO.html",
        "https://www.paris.cl/aire-acondicionado-split-muro-wind-inverter-9000-btu-MKADL4LWPI.html",
        "https://www.paris.cl/purificador-de-aire-wll-a7-60-m2-ultra-silencioso-MKLTFV5SPD.html",
        "https://www.paris.cl/estufa-parafina-laser-fensa-9-litros-465kw-eco-fhk-990-MKR95IU8WR.html",
        "https://www.paris.cl/aire-acondicionado-efficient-inverter-9000-btu-MKD61LE8ZL.html",
        "https://www.paris.cl/aire-acondicionado-split-muro-wind-inverter-18000-btu-MKYJBLT7QG.html",
        "https://www.paris.cl/aire-acondicionado-split-muro-wind-free-inverter-9000-btu-MK18J505DZ.html",
        "https://www.paris.cl/aire-acondicionado-efficient-inverter-12000-btu-MKD7G1FOPR.html",
        "https://www.paris.cl/aire-acondicionado-split-muro-wind-inverter-24000-btu-MKLJB6HIRF.html",
        "https://www.paris.cl/aire-acondicionado-split-muro-wind-free-inverter-18000-btu-MK8IVYDOW0.html",
        "https://www.paris.cl/aire-acondicionado-split-muro-wind-free-inverter-12000-btu-MK0F57MBD5.html",
        "https://www.paris.cl/aire-acondicionado-splitt-muro-wind-free-inverter-24000-btu-MKLWSXS2K1.html",
        "https://www.paris.cl/aire-acondicionado-split-muro-wind-inverter-12000-btu-MK9KYK9DN4.html",
        "https://www.paris.cl/lavadora-secadora-de-ropa-125kg-7kg-con-int-artificial-blanco-samsung-MKGCWH2WUW.html",
        "https://www.paris.cl/lavavajillas-14-cubiertos-silver-con-flexible-3rd-rack-MKV5BZFV8O.html",
        "https://www.paris.cl/lavadora-de-carga-superior-24kg-con-eco-bubble-MK0CN3HK96.html",
        "https://www.paris.cl/lavadora-secadora-11kg-7kg-MKLZHNO8NU.html",
        "https://www.paris.cl/lavadora-de-carga-superior-17kg-con-eco-bubbletm-blanca-MK1GOJ9E46.html",
        "https://www.paris.cl/55-crystal-uhd-u8000f-4k-smart-tv-2025-MKIFV4S2BJ.html",
        "https://www.paris.cl/65-oled-s95f-4k-vision-ai-smart-tv-2025-MKOHDVLMLE.html",
        "https://www.paris.cl/85-crystal-uhd-u8200f-4k-smart-tv-2025-MK6NA2Q1PY.html",
        "https://www.paris.cl/85-crystal-uhd-u8000f-4k-smart-tv-2025-MKCGUNTN93.html",
        "https://www.paris.cl/70-crystal-uhd-u8000f-4k-smart-tv-2025-MKBDJKA64P.html",
        "https://www.paris.cl/55-qled-q8f-4k-vision-ai-smart-tv-2025-MKMGXO15H5.html",
        "https://www.paris.cl/neo-qled-samsung-55-qn85d-4k-uhd-smart-tv-2024-MKCZJFT1QP.html",
        "https://www.paris.cl/77-oled-s95f-4k-vision-ai-smart-tv-2025-MKWHTSC7FN.html",
        "https://www.paris.cl/83-oled-s85f-4k-vision-ai-smart-tv-2025-MKZ7I6UNZB.html",
    ]

    @classmethod
    def categories(cls):
        return [TELEVISION]

    @classmethod
    def discover_urls_for_category(cls, category, extra_args=None):
        if category != TELEVISION:
            return []

        return cls.category_paths

    @classmethod
    def products_for_url(cls, url, category=None, extra_args=None):
        products = Paris.products_for_url(url, category, extra_args)

        for product in products:
            product.store = cls.__name__

        return products
