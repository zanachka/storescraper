from .lg_v6 import LgV6
from storescraper.categories import (
    TELEVISION,
    STEREO_SYSTEM,
    REFRIGERATOR,
    WASHING_MACHINE,
    MONITOR,
    PROJECTOR,
    DISH_WASHER,
    SPLIT_AIR_CONDITIONER,
    OVEN,
    VACUUM_CLEANER,
)
from storescraper import banner_sections as bs


class LgCl(LgV6):
    region_code = "CL"
    currency = "CLP"
    price_approximation = "0"

    @classmethod
    def _category_paths(cls):
        return [
            # Todos los TVs y Soundbars
            ("CT52000104", TELEVISION),
            # Bundles TV - Soundbar
            ("PM00024763", TELEVISION),
            # Object collection - Pose
            ("CT52000790", TELEVISION),
            # Flex
            ("CT52000799", TELEVISION),
            # StandbyMe
            ("CT52020281", TELEVISION),
            # To do Audio
            ("CT52000100", STEREO_SYSTEM),
            # Proyectores
            ("CT52000784", PROJECTOR),
            # Refrigeradores
            ("CT52000103", REFRIGERATOR),
            # Lavadoras
            ("CT52000102", WASHING_MACHINE),
            # Lavavajillas
            ("CT52000105", DISH_WASHER),
            # Monitores
            ("CT52000106", MONITOR),
            # Aires acondicionados
            ("CT52002586", SPLIT_AIR_CONDITIONER),
            # Microondas
            ("CT52020321", OVEN),
            # Aspiradoras
            ("CT52020323", VACUUM_CLEANER),
        ]

    @classmethod
    def banners(cls, extra_args=None):
        import time
        import base64
        from playwright.sync_api import sync_playwright

        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            context = browser.new_context(viewport={"width": 1920, "height": 1080})
            url = "https://www.lg.com/cl/"

            page = context.new_page()
            page.goto(url)
            page.wait_for_selector(".ST0048 .c-carousel-controls__action--pause")
            pause_button = page.query_selector(
                ".ST0048 .c-carousel-controls__action--pause"
            )
            pause_button.click()

            container = page.query_selector(".ST0048")
            buttons = container.query_selector_all(".c-carousel-controls__bullet")

            banners = []
            for idx, button in enumerate(buttons):
                button.click()
                time.sleep(2)
                picture_bytes = container.screenshot()
                picture = base64.b64encode(picture_bytes).decode()
                key = button.get_attribute("aria-label")
                banners.append(
                    {
                        "url": url,
                        "picture": picture,
                        "destination_urls": [],
                        "key": key,
                        "position": idx + 1,
                        "section": bs.HOME,
                        "subsection": bs.HOME,
                        "type": bs.SUBSECTION_TYPE_HOME,
                    }
                )
            browser.close()
            return banners
