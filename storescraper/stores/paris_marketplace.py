from storescraper.categories import TELEVISION
from storescraper.stores import Paris
from storescraper.store import Store


class ParisMarketplace(Store):
    category_paths = [
        "https://www.paris.cl/refrigerador-bottom-mount-290l-all-around-cooling-MKQRIMTEY5.html",
        "https://www.paris.cl/refrigerador-top-mount-freezer-391-l-space-max-MKR5W06Q1N.html",
        "https://www.paris.cl/refrigerador-french-door-de-576-l-con-dual-ice-maker-MK4EA862YR.html",
        "https://www.paris.cl/refrigerador-top-mount-freezer-407l-space-max-MK7MKKUFKK.html",
        "https://www.paris.cl/refrigerador-bottom-mount-de-311l-all-around-cooling-MKN5ZPW6WK.html",
        "https://www.paris.cl/refrigerador-bottom-mount-462l-freezer-space-max-MK83B6ESB2.html",
        "https://www.paris.cl/refrigerador-top-mount-freezer-255l-all-around-cooling-MKCRA1M9Q6.html",
        "https://www.paris.cl/refrigerador-top-mount-521-lt-no-frost-silver-MKVY6M47EJ.html",
        "https://www.paris.cl/refrigerador-side-by-side-con-dispensador-560l-negro-MKVNZZS5EF.html",
        "https://www.paris.cl/refrigerador-side-by-side-564l-gris-MKJQT7HJD7.html",
        "https://www.paris.cl/refrigerador-top-mount-freezer-234l-all-around-cooling-MKZ0MSVJXO.html",
        "https://www.paris.cl/refrigerador-top-mount-freezer-341l-space-max-MK68SEHDQS.html",
        "https://www.paris.cl/refrigerador-bottom-mount-freezer-328l-space-max-MKXPC3Y9R6.html",
        "https://www.paris.cl/refrigerador-459-lt-bottom-mount-freezer-no-frost-MKL1U172R3.html",
        "https://www.paris.cl/refrigerador-french-door-699l-bespoke-ai-family-hub-MKG146O13M.html",
        "https://www.paris.cl/refrigerador-top-mount-freezer-384l-space-max-MKF9HNZ5C6.html",
        "https://www.paris.cl/refrigerador-side-by-side-585l-family-hub-MKYJ8CS76N.html",
        "https://www.paris.cl/refrigerador-top-mount-freezer-298l-space-max-MKSLB4UKNU.html",
        "https://www.paris.cl/samsung-refrigerador-384-l-top-freezer-MKKO4PYBJP.html",
        "https://www.paris.cl/samsung-lavadorasecadora-de-117-kg-con-eco-bubbletm-MK24OJJXQ8.html",
        "https://www.paris.cl/samsung-lavadorasecadora-de-117-kg-con-eco-bubbletm-MKGY0CHBNV.html",
        "https://www.paris.cl/lavavajillas-14-cubiertos-con-smart-things-MK704WHQ4Y.html",
        "https://www.paris.cl/lavadora-secadora-de-ropa-125kg-7kg-con-int-artificial-blanco-samsung-MKGCWH2WUW.html",
        "https://www.paris.cl/lavadora-de-carga-superior-15kg-con-eco-bubbletm-blanca-MK99E4FUDT.html",
        "https://www.paris.cl/lavadora-secadora-125kg-7kg-con-inteligencia-artificial-en-panel-de-control-negra-MKLJCYYP0X.html",
        "https://www.paris.cl/lavadora-de-carga-superior-9kg-con-tecnologia-digital-inverter-MKZN8U3XB4.html",
        "https://www.paris.cl/lavadora-de-carga-superior-22kg-con-eco-bubble-MK0BJKCATO.html",
        "https://www.paris.cl/lavadora-secadora-20kg-12kg-con-inteligencia-artificial-en-panel-de-control-MK64BTMHNX.html",
        "https://www.paris.cl/lavadora-secadora-95kg-6kg-con-eco-bubble-MKRT3THS4Q.html",
        "https://www.paris.cl/lavadora-secadora-bespoke-14kg-9kg-con-inteligencia-artificial-en-ecobubble-MK1JOHCS5U.html",
        "https://www.paris.cl/lavavajillas-14-cubiertos-silver-con-flexible-3rd-rack-MKV5BZFV8O.html",
        "https://www.paris.cl/lavadora-de-carga-superior-24kg-con-eco-bubble-MK0CN3HK96.html",
        "https://www.paris.cl/lavadora-de-carga-superior-19kg-con-eco-bubble-MKFZY8KCCP.html",
        "https://www.paris.cl/lavadora-de-carga-superior-15kg-con-eco-bubbletm-MKURT8IGWP.html",
        "https://www.paris.cl/lavadora-de-carga-superior-17kg-con-eco-bubbletm-MKOCWLB37I.html",
        "https://www.paris.cl/lavadora-secadora-11kg-7kg-MKLZHNO8NU.html",
        "https://www.paris.cl/lavadora-de-carga-superior-13kg-con-eco-bubble-MKJ2OB1GMX.html",
        "https://www.paris.cl/lavavajillas-13-cubiertos-blanca-con-pantalla-led-MKCQ2E4K7T.html",
        "https://www.paris.cl/lavadora-de-carga-superior-19kg-con-eco-bubbletm-blanca-MKN2X6DB8O.html",
        "https://www.paris.cl/samsung-lavavajillas-14-cubiertos-con-smart-things-MKDQFOLEVQ.html",
        "https://www.paris.cl/lavadora-de-carga-superior-17kg-con-eco-bubbletm-blanca-MK1GOJ9E46.html",
        "https://www.paris.cl/lavadora-secadora-22kg-13kg-con-inteligencia-artificial-en-panel-de-control-MKOAY5ZX6K.html",
        "https://www.paris.cl/refrigerador-bottom-mount-freezer-321l-space-max-MKSP7RC4KK.html",
        "https://www.paris.cl/qled-samsung-50-the-serif-ls01d-4k-smart-tv-2024-MKYLH497MA.html",
        "https://www.paris.cl/65-neo-qled-4k-qn70f-vision-ai-smart-tv-2025-MKDB8UW59L.html",
        "https://www.paris.cl/qled-samsung-85-q65d-4k-uhd-smart-tv-2024-MK76NJOGWA.html",
        "https://www.paris.cl/55-oled-s95f-4k-vision-ai-smart-tv-2025-MK4OC7357E.html",
        "https://www.paris.cl/75-crystal-uhd-u8000f-4k-smart-tv-2025-MKIVRDEU9Z.html",
        "https://www.paris.cl/43-fhd-t5203-smart-tv-2024-MK278TBJG7.html",
        "https://www.paris.cl/qled-samsung-55-the-serif-ls01d-4k-smart-tv-2024-MKDGLP6XJ6.html",
        "https://www.paris.cl/neo-qled-samsung-75-qn900d-8k-uhd-smart-tv-2024-MKIIZBXZTA.html",
        "https://www.paris.cl/55-neo-qled-4k-qn70f-vision-ai-smart-tv-2025-MK57EDINMX.html",
        "https://www.paris.cl/led-samsung-32-t4202-hd-smart-tv-2020-MKZEWL8BFQ.html",
        "https://www.paris.cl/85-neo-qled-4k-qn70f-vision-ai-smart-tv-2025-MKVAO3QAO2.html",
        "https://www.paris.cl/50-qled-q7fa-4k-vision-ai-smart-tv-2025-MKHPB387IL.html",
        "https://www.paris.cl/55-qled-q7fa-4k-vision-ai-smart-tv-2025-MKGQ5NEVTD.html",
        "https://www.paris.cl/led-samsung-85-du7000-4k-uhd-smart-tv-2024-MKL6557B12.html",
        "https://www.paris.cl/led-samsung-55-du7000-4k-uhd-smart-tv-2024-MKR5NS5SLZ.html",
        "https://www.paris.cl/qled-samsung-43-the-serif-ls01d-4k-smart-tv-2024-MK226XDKSQ.html",
        "https://www.paris.cl/neo-qled-samsung-85-qn90d-4k-uhd-smart-tv-2024-MKUHM77U0J.html",
        "https://www.paris.cl/75-neo-qled-8k-qn900f-vision-ai-smart-tv-2025-MKPJHFE77Q.html",
        "https://www.paris.cl/65-neo-qled-4k-qn90f-vision-ai-smart-tv-2025-MKCHIDMXLS.html",
        "https://www.paris.cl/oled-samsung-83-s90d-4k-uhd-smart-tv-2024-MKGZA5JLCS.html",
        "https://www.paris.cl/oled-samsung-77-s90d-4k-uhd-smart-tv-2024-MKIBUUGJ9F.html",
        "https://www.paris.cl/neo-qled-samsung-85-qn900d-8k-uhd-smart-tv-2024-MK8BMEWBD6.html",
        "https://www.paris.cl/65-neo-qled-4k-qn85f-vision-ai-smart-tv-2025-MKJ3UOZ7VN.html",
        "https://www.paris.cl/65-crystal-uhd-u8000f-4k-smart-tv-2025-MKH8FLGVJP.html",
        "https://www.paris.cl/55-crystal-uhd-u8000f-4k-smart-tv-2025-MKIFV4S2BJ.html",
        "https://www.paris.cl/65-neo-qled-8k-qn900f-vision-ai-smart-tv-2025-MKAVMW63RZ.html",
        "https://www.paris.cl/65-oled-s95f-4k-vision-ai-smart-tv-2025-MKOHDVLMLE.html",
        "https://www.paris.cl/85-crystal-uhd-u8200f-4k-smart-tv-2025-MK6NA2Q1PY.html",
        "https://www.paris.cl/85-crystal-uhd-u8000f-4k-smart-tv-2025-MKCGUNTN93.html",
        "https://www.paris.cl/70-crystal-uhd-u8000f-4k-smart-tv-2025-MKBDJKA64P.html",
        "https://www.paris.cl/55-qled-q8f-4k-vision-ai-smart-tv-2025-MKMGXO15H5.html",
        "https://www.paris.cl/55-neo-qled-4k-qn90f-vision-ai-smart-tv-2025-MK8N7MKH4O.html",
        "https://www.paris.cl/neo-qled-samsung-55-qn85d-4k-uhd-smart-tv-2024-MKCZJFT1QP.html",
        "https://www.paris.cl/75-neo-qled-8k-qn990f-vision-ai-smart-tv-2025-MKLOFKX3IN.html",
        "https://www.paris.cl/85-neo-qled-8k-qn990f-vision-ai-smart-tv-2025-MKUEVSPWXC.html",
        "https://www.paris.cl/77-oled-s95f-4k-vision-ai-smart-tv-2025-MKWHTSC7FN.html",
        "https://www.paris.cl/50-neo-qled-4k-qn90f-vision-ai-smart-tv-2025-MKNZY7YDDS.html",
        "https://www.paris.cl/75-neo-qled-4k-qn1ef-vision-ai-smart-tv-2025-MKX9OLCDOX.html",
        "https://www.paris.cl/85-qled-q7f5-4k-vision-ai-smart-tv-2025-MK74JBA1RS.html",
        "https://www.paris.cl/55-oled-s85f-4k-vision-ai-smart-tv-2025-MKB6CGHH1U.html",
        "https://www.paris.cl/85-neo-qled-4k-qn1ef-vision-ai-smart-tv-2025-MKT7IOUL4P.html",
        "https://www.paris.cl/43-neo-qled-4k-qn90f-vision-ai-smart-tv-2025-MK5BVHBSFY.html",
        "https://www.paris.cl/43-qled-q8f-4k-vision-ai-smart-tv-2025-MK2KA9ZJKB.html",
        "https://www.paris.cl/50-qled-q8f-4k-vision-ai-smart-tv-2025-MKVGIMPVG8.html",
        "https://www.paris.cl/65-neo-qled-4k-qn1ef-vision-ai-smart-tv-2025-MKTP27GAD6.html",
        "https://www.paris.cl/83-oled-s85f-4k-vision-ai-smart-tv-2025-MKZ7I6UNZB.html",
        "https://www.paris.cl/85-qled-qef1-4k-vision-ai-smart-tv-2025-MKWB0N7NV8.html",
        "https://www.paris.cl/75-qled-q7fa-4k-vision-ai-smart-tv-2025-MK09Q6WRKW.html",
        "https://www.paris.cl/75-qled-q7f5-4k-vision-ai-smart-tv-2025-MKA4VBRI4C.html",
        "https://www.paris.cl/samsung-ultra-slim-soundbar-hw-s801d-312-ch-sub-woofer-MKPE699GQ8.html",
        "https://www.paris.cl/soundbar-hw-q600c-312-ch-MKZUITLZT1.html",
        "https://www.paris.cl/sound-tower-mx-t70-MKSFVV7CPE.html",
        "https://www.paris.cl/music-frame-hw-ls60d-frame-design-wireless-speaker-MKURDBZ7MX.html",
        "https://www.paris.cl/samsung-soundbar-s-series-hw-s61d-MK6T3XE7DV.html",
        "https://www.paris.cl/samsung-soundbar-hw-c400-MK23UJSCY4.html",
        "https://www.paris.cl/samsung-soundbar-hw-c450-21-ch-MKWMVRFS2V.html",
        "https://www.paris.cl/sound-tower-mx-t40-MKTFB8ASPK.html",
        "https://www.paris.cl/sound-tower-mx-t50-MK9PW42N72.html",
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
