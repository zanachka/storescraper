from decimal import Decimal

from storescraper.categories import (
    ACCESORIES,
    ALL_IN_ONE,
    CELL,
    COMPUTER_CASE,
    CPU_COOLER,
    EXTERNAL_STORAGE_DRIVE,
    GAMING_CHAIR,
    HEADPHONES,
    KEYBOARD,
    KEYBOARD_MOUSE_COMBO,
    MEMORY_CARD,
    MONITOR,
    MOTHERBOARD,
    MOUSE,
    NOTEBOOK,
    OVEN,
    POWER_SUPPLY,
    PRINTER,
    PRINTER_SUPPLY,
    PROCESSOR,
    PROJECTOR,
    RAM,
    SOLID_STATE_DRIVE,
    SPACE_HEATER,
    STEREO_SYSTEM,
    STORAGE_DRIVE,
    TABLET,
    TELEVISION,
    UPS,
    USB_FLASH_DRIVE,
    VIDEO_CARD,
    WEARABLE,
)
from storescraper.product import Product
from storescraper.store_with_url_extensions import StoreWithUrlExtensions
from storescraper.utils import session_with_proxy


class ZonaPortatil(StoreWithUrlExtensions):
    url_extensions = [
        ("0204ce76-e551-4b0f-9fc0-9695abb53b9b", HEADPHONES),
        ("32e0920d-c46e-4a83-b84d-6cc98d56e998", STEREO_SYSTEM),
        ("d40bbab2-7885-43eb-8f08-96249e3d69a0", ACCESORIES),
        ("b20bdfb9-eebf-4ca3-ba5f-07db3bff495e", RAM),
        ("ae821fc9-31c2-44d7-affc-089e88e48b4b", RAM),
        ("de901580-3e10-48df-bf94-db2340977d8a", RAM),
        ("c81a39a0-a93f-4fb6-9e4b-92d6a254ca2a", USB_FLASH_DRIVE),
        ("e1df34cc-6d2c-4a38-b798-3d725444e12e", MEMORY_CARD),
        ("e769bc5d-07b9-4a62-bbba-5ccdf8edbcce", NOTEBOOK),
        ("f4fd9a6b-194f-4e27-b0a9-cecf84243a73", ALL_IN_ONE),
        ("ab5ced88-d056-4d26-ba84-ac2782912e6a", TABLET),
        ("6b5ed6b5-7849-4b53-a8cc-68b3e7a41f5d", NOTEBOOK),
        ("ccff56c2-3b69-4059-a527-80ad36a4afcd", MONITOR),
        ("e7a51952-f018-493e-82c9-db5f2423ce6d", TELEVISION),
        ("25dade18-1879-4f15-92dc-8609b2edbade", PROJECTOR),
        ("6d3d9155-b9cc-42d0-8a7f-cae889b1e54a", SOLID_STATE_DRIVE),
        ("4401c79d-3ece-4243-94c1-060ec6892740", EXTERNAL_STORAGE_DRIVE),
        ("8c92973e-96f7-4316-af18-184988ef5743", STORAGE_DRIVE),
        ("9504e13e-8f9c-406f-9b98-dbb357168b53", EXTERNAL_STORAGE_DRIVE),
        ("a7aaf0f1-10b3-4bde-97bc-1545e2bc419d", MOUSE),
        ("30785fe1-b336-420b-9d2a-a8b25f16a83c", HEADPHONES),
        ("22090844-46ac-4147-85e1-24be056981ca", TABLET),
        ("7f8c2041-fe5d-4db8-a836-678fac22e526", STEREO_SYSTEM),
        ("a04b14fd-50fd-4dd5-b9bb-9ebd281d6fc6", KEYBOARD_MOUSE_COMBO),
        ("f3860ccc-b305-4839-b052-08cb4a4e6097", KEYBOARD),
        ("202fa576-5095-4b8e-99e9-845d1c1ff5d7", PROCESSOR),
        ("84e7d4cd-92f2-4bd7-98eb-c1492d3c3755", MOTHERBOARD),
        ("4e5e9ad6-c9f8-4fb8-a2d7-a1b3a0a813b3", CPU_COOLER),
        ("567972cb-02fc-49c6-9547-1fae72ee70dd", POWER_SUPPLY),
        ("2b9c675d-fdcc-43a0-9df6-78c81a1233a5", VIDEO_CARD),
        ("55adcb0f-ef21-4490-b2c5-dd060837ecd1", COMPUTER_CASE),
        ("f3339873-5aca-4bd2-8ecb-46fe43483acb", UPS),
        ("e6829f33-690e-41e5-9fc8-9079e9fd4548", STEREO_SYSTEM),
        ("62d06711-8c68-4e43-b4f2-ed2df5fa3e1e", HEADPHONES),
        ("fa64c581-aa58-4aa2-a8b1-bd970c21abd5", STEREO_SYSTEM),
        ("e98f4206-6aed-45b6-89e0-dfb48b8c7d44", OVEN),
        ("c0a5895a-c077-4636-b00a-689bbf7f4b3c", SPACE_HEATER),
        ("62ea0ecf-dd5b-4343-a649-e66738361fe0", STORAGE_DRIVE),
        ("b9a1216b-5577-4b73-9ec2-32830216e84a", EXTERNAL_STORAGE_DRIVE),
        ("a7897f04-cd47-458b-b88d-bf1b43e00abd", MOUSE),
        ("1c582563-fbfe-4e45-868d-752302919f7f", KEYBOARD),
        ("656f4b11-a2c9-4eeb-884d-8237ba5c9408", KEYBOARD_MOUSE_COMBO),
        ("833806d1-78e1-4866-a381-7f1c10f599e4", HEADPHONES),
        ("cb3845c7-b47c-4b37-9ad9-663dab30b24e", COMPUTER_CASE),
        ("e66f1ac4-db92-495a-b216-d51a983d0f11", VIDEO_CARD),
        ("ab291f65-4318-4f47-926b-52f07e04e73d", PROCESSOR),
        ("d97ba9ba-1add-4d53-9998-1021e5d2b4e3", CPU_COOLER),
        ("add751d5-fbea-4d44-82f1-b9cc447e92f7", MOTHERBOARD),
        ("2a0423af-75cd-4619-b63b-6ef2889756c2", POWER_SUPPLY),
        ("bc12b3dc-40b3-4ee0-97d0-3c5de384fb16", NOTEBOOK),
        ("316e5ad0-b951-4b22-b5fc-87fcc430b411", RAM),
        ("51ab965d-8184-4886-b967-8c71f4d97d20", RAM),
        ("ae40b2e1-5183-43b6-8000-38efa032d1e3", UPS),
        ("6d17f312-4c68-4775-a05c-d4e546e81740", RAM),
        ("086fec30-b268-4eb5-8cf6-9072889b6a83", TABLET),
        ("7e983fb2-0fac-4137-a08b-3b205d1b28ea", CELL),
        ("b2be9aab-e4f3-4cd6-80f9-bca6e3e25e8b", WEARABLE),
        ("15036c1a-7c17-44ca-80ae-852d5f462ce3", PRINTER),
        ("32636625-bdaa-4c18-8db7-947856212557", PRINTER),
        ("fee80a53-0298-4f28-bc82-04e5e1b22159", PRINTER),
        ("ded2313f-5773-47a6-8ccf-8b73acb54e5f", PRINTER),
        ("9d17db5b-75f1-465b-9b47-ba48d80fa4ce", PRINTER_SUPPLY),
        ("37d9008b-8458-4462-a185-e7707fae0605", GAMING_CHAIR),
    ]

    @classmethod
    def discover_urls_for_url_extension(cls, url_extension, extra_args=None):
        session = session_with_proxy(extra_args)
        product_urls = []
        endpoint = (
            "https://api-zonaprod.zonaportatil.cl/product/get-all-active-products"
        )
        print(url_extension)
        response = session.get(endpoint)

        if response.status_code != 200:
            raise Exception(f"Invalid category: {url_extension}")

        products = [
            p
            for p in response.json()["products"]["data"]
            if p["subcategory"]["id"] == url_extension
        ]

        for product in products:
            product_urls.append(
                f"https://www.zonaportatil.cl/producto_completo.php?idProduct={product['id']}"
            )

        return product_urls

    @classmethod
    def products_for_url(cls, url, category=None, extra_args=None):
        print(url)
        session = session_with_proxy(extra_args)
        key = url.split("?idProduct=")[-1]
        endpoint = f"https://api-zonaprod.zonaportatil.cl/product/{key}"
        response = session.get(endpoint)

        if response.status_code != 200:
            return []

        product = response.json()["product"]["data"]
        name = product["name"]
        stock = product["stock"]
        normal_price = Decimal(product["normal_prince"])
        offer_price = (normal_price * Decimal(0.95)).quantize(0)
        condition = (
            "https://schema.org/OpenBoxCondition"
            if "OPEN" in name.upper()
            else "https://schema.org/NewCondition"
        )
        sku = product["sku"]
        picture_urls = [img["path"] for img in product["images"]]
        description = product["broadDescription"]

        p = Product(
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
            part_number=sku,
            picture_urls=picture_urls,
            condition=condition,
            description=description,
        )

        return [p]
