import logging
from decimal import Decimal

from bs4 import BeautifulSoup

from storescraper.categories import CASE_FAN, MEMORY_CARD, PRINTER, \
    EXTERNAL_STORAGE_DRIVE, PROCESSOR, RAM, MOTHERBOARD, KEYBOARD, MOUSE, \
    KEYBOARD_MOUSE_COMBO, HEADPHONES, STEREO_SYSTEM, COMPUTER_CASE, UPS, \
    VIDEO_CARD, CPU_COOLER, MONITOR, GAMING_CHAIR, POWER_SUPPLY, MICROPHONE, \
    STORAGE_DRIVE, SOLID_STATE_DRIVE, USB_FLASH_DRIVE
from storescraper.product import Product

from storescraper.store import Store
from storescraper.utils import session_with_proxy


class MHWStore(Store):
    @classmethod
    def categories(cls):
        return [
            SOLID_STATE_DRIVE,
            STORAGE_DRIVE,
            EXTERNAL_STORAGE_DRIVE,
            PROCESSOR,
            RAM,
            MOTHERBOARD,
            KEYBOARD,
            MOUSE,
            KEYBOARD_MOUSE_COMBO,
            HEADPHONES,
            STEREO_SYSTEM,
            COMPUTER_CASE,
            VIDEO_CARD,
            CPU_COOLER,
            MONITOR,
            GAMING_CHAIR,
            POWER_SUPPLY,
            MICROPHONE,
            CASE_FAN,
            UPS,
            USB_FLASH_DRIVE,
            MEMORY_CARD,
            PRINTER,
        ]

    @classmethod
    def discover_urls_for_category(cls, category, extra_args=None):
        url_extensions = [
            ['11-procesadores', PROCESSOR],
            ['12-placas-madre', MOTHERBOARD],
            ['13-almacenamiento', SOLID_STATE_DRIVE],
            ['21-ssd', SOLID_STATE_DRIVE],
            ['22-hdd', STORAGE_DRIVE],
            ['14-memorias-ram', RAM],
            ['15-enfriamiento-cpu', CPU_COOLER],
            ['16-tarjetas-graficas', VIDEO_CARD],
            ['17-fuentes-de-poder', POWER_SUPPLY],
            ['18-gabinetes', COMPUTER_CASE],
            ['20-ventilacion', CASE_FAN],
            ['56-ups-y-baterias', UPS],
            ['24-mouse', MOUSE],
            ['25-teclados', KEYBOARD],
            ['26-combos', KEYBOARD_MOUSE_COMBO],
            ['29-discos-duros-externos', EXTERNAL_STORAGE_DRIVE],
            ['30-pendrives', USB_FLASH_DRIVE],
            ['31-tarjetas-de-memoria', MEMORY_CARD],
            ['34-audifonos', HEADPHONES],
            ['35-microfonos', MICROPHONE],
            ['36-parlantes', STEREO_SYSTEM],
            ['40-impresoras-y-escaners', PRINTER],
            ['41-monitores', MONITOR],
            ['42-sillas-gamer', GAMING_CHAIR],
        ]
        session = session_with_proxy(extra_args)
        session.headers['User-Agent'] = \
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 ' \
            '(KHTML, like Gecko) Chrome/62.0.3202.62 Safari/537.36'
        product_urls = []
        for url_extension, local_category in url_extensions:
            if local_category != category:
                continue
            page = 1
            while True:
                if page > 10:
                    raise Exception('page overflow: ' + url_extension)
                url_webpage = 'https://www.mhwstore.cl/{}?page={}'.format(
                    url_extension, page)
                data = session.get(url_webpage, timeout=20).text
                soup = BeautifulSoup(data, 'html.parser')
                product_containers = soup.findAll('article',
                                                  'product-miniature')
                if not product_containers:
                    if page == 1:
                        logging.warning('Empty category: ' + url_extension)
                    break
                for container in product_containers:
                    product_url = container.find('a')['href']
                    product_urls.append(product_url)
                page += 1
        return product_urls

    @classmethod
    def products_for_url(cls, url, category=None, extra_args=None):
        print(url)
        session = session_with_proxy(extra_args)
        session.headers['User-Agent'] = \
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 ' \
            '(KHTML, like Gecko) Chrome/62.0.3202.62 Safari/537.36'
        response = session.get(url, timeout=20)
        soup = BeautifulSoup(response.text, 'html.parser')
        name = soup.find('h1', 'h1').text
        key = soup.find('input', {'id': 'product_page_product_id'})['value']
        sku = soup.find(
            'div',
            'product-reference').text.replace('Referencia: ', '').strip()
        not_stock = soup.find('span', {'id': 'product-availability'}).text
        if 'Fuera de stock' in not_stock:
            stock = 0
        else:
            stock = int(soup.find('span', 'bon-stock-countdown-counter').text)
        price = Decimal(soup.find('span', {'itemprop': 'price'})['content'])
        picture_urls = [tag['src'] for tag in
                        soup.find('div', 'images-container').find(
            'div', 'product-cover').findAll('img')
            if tag['src']]
        p = Product(
            name,
            cls.__name__,
            category,
            url,
            url,
            key,
            stock,
            price,
            price,
            'CLP',
            sku=sku,
            picture_urls=picture_urls
        )
        return [p]
