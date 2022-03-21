import logging

from bs4 import BeautifulSoup

from storescraper.categories import MONITOR, MOTHERBOARD, MOUSE, KEYBOARD, HEADPHONES, COMPUTER_CASE
from storescraper.store import Store
from storescraper.utils import session_with_proxy


class PlayFactory(Store):

    @classmethod
    def categories(cls):
        return [
            MOUSE,
            KEYBOARD,
            HEADPHONES,
            COMPUTER_CASE,

            MOTHERBOARD,
            MONITOR
        ]

    @classmethod
    def discover_urls_for_category(cls, category, extra_args=None):
        url_extensions = [
            ['computacion/perifericos-accesorios/teclados', KEYBOARD],
            ['computacion/perifericos-accesorios/mouses', MOUSE],
            ['accesorios-pc-gaming-audifonos', HEADPHONES],
            ['componentes-pc-gabinetes-soportes', COMPUTER_CASE],

            ['componentes', MOTHERBOARD],
            ['gaming-y-streaming', HEADPHONES],
            ['monitores', MONITOR],
        ]
        session = session_with_proxy(extra_args)
        product_urls = []
        for url_extension, local_category in url_extensions:
            if local_category != category:
                continue
            page = 1
            while True:
                if page > 100:
                    raise Exception('page overflow: ' + url_extension)
                url_webpage = 'https://www.playfactory.cl/listado/{}/' \
                              '_Desde_{}'.format(url_extension, page)
                print(url_webpage)
                data = session.get(url_webpage).text
                soup = BeautifulSoup(data, 'html.parser')
                product_containers = soup.findAll('li',
                                                  'ui-search-layout__item')
                if not product_containers:
                    if page == 1:
                        logging.warning('Empty category: ' + url_extension)
                    break
                for container in product_containers:
                    product_url = container.find('a')['href']
                    if product_url in product_urls:
                        return product_urls
                    product_urls.append(product_url)
                page += 48
        return product_urls

    @classmethod
    def products_for_url(cls, url, category=None, extra_args=None):
        from .mercado_libre_chile import MercadoLibreChile
        products = MercadoLibreChile.products_for_url(url, category,
                                                      extra_args)
        for product in products:
            product.seller = None

        return products
