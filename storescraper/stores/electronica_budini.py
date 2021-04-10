import logging
from decimal import Decimal

from bs4 import BeautifulSoup

from storescraper.categories import SOLID_STATE_DRIVE, STORAGE_DRIVE, \
    POWER_SUPPLY, COMPUTER_CASE, RAM, MONITOR, MOUSE, MOTHERBOARD, NOTEBOOK, \
    PROCESSOR, VIDEO_CARD, GAMING_CHAIR, CPU_COOLER, ALL_IN_ONE, HEADPHONES
from storescraper.product import Product
from storescraper.store import Store
from storescraper.utils import session_with_proxy, remove_words


class ElectronicaBudini(Store):
    @classmethod
    def categories(cls):
        return [
            SOLID_STATE_DRIVE,
            STORAGE_DRIVE,
            POWER_SUPPLY,
            COMPUTER_CASE,
            RAM,
            MONITOR,
            MOUSE,
            MOTHERBOARD,
            NOTEBOOK,
            PROCESSOR,
            VIDEO_CARD,
            GAMING_CHAIR,
            CPU_COOLER,
            ALL_IN_ONE,
            HEADPHONES
        ]

    @classmethod
    def discover_urls_for_category(cls, category, extra_args=None):
        url_extensions = [
            ['discos-de-estado-solido-ssd', SOLID_STATE_DRIVE],
            ['discos-duros-hdd', STORAGE_DRIVE],
            ['fuentes-de-poder', POWER_SUPPLY],
            ['gabinetes-gamer', COMPUTER_CASE],
            ['memoria-ram-pc', RAM],
            ['monitores', MONITOR],
            ['mouse-gamer', MOUSE],
            ['placas-madre-intel', MOTHERBOARD],
            ['placas-madre-amd-ryzen', MOTHERBOARD],
            ['notebooks', NOTEBOOK],
            ['procesadores', PROCESSOR],
            ['tarjetas-de-video', VIDEO_CARD],
            ['silla-gamer', GAMING_CHAIR],
            ['ventiladores-y-sistemas-de-enfriamiento', CPU_COOLER],
            ['todo-en-uno-aio', ALL_IN_ONE],
            ['auriculares-gamer', HEADPHONES]
        ]

        session = session_with_proxy(extra_args)
        session.headers['user-agent'] = \
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 ' \
            '(KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'
        product_urls = []
        for url_extension, local_category in url_extensions:
            if local_category != category:
                continue
            page = 1
            while True:
                if page > 10:
                    raise Exception('page overflow: ' + url_extension)

                url_webpage = 'https://electronicabudini.cl/categoria-prod' \
                              'ucto/{}/page/{}/'.format(url_extension, page)
                print(url_webpage)
                data = session.get(url_webpage).text
                soup = BeautifulSoup(data, 'html.parser')
                product_containers = soup.find('ul', 'products').findAll('li')
                if not product_containers or soup.find('div', 'error-404'):
                    if page == 1:
                        logging.warning('Empty category: ' + url_extension)
                    break
                for container in product_containers:
                    product_url = container.find('a')['href']
                    if 'categoria-producto' in product_url:
                        continue
                    product_urls.append(product_url)
                page += 1
        return product_urls

    @classmethod
    def products_for_url(cls, url, category=None, extra_args=None):
        print(url)
        session = session_with_proxy(extra_args)
        session.headers['user-agent'] = \
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 ' \
            '(KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'
        response = session.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        name = soup.find('h1', 'product_title').text
        sku = soup.find('link', {'rel': 'shortlink'})['href'].split('p=')[1]
        if soup.find('p', 'stock in-stock'):
            stock = int(soup.find('p', 'stock in-stock').text.split()[0])
        else:
            stock = 0
        if soup.find('p', 'price').find('ins'):
            price = Decimal(
                remove_words(soup.find('p', 'price').find('ins').text))
        else:
            price = Decimal(remove_words(soup.find('p', 'price').text))

        picture_urls = [tag['src'] for tag in soup.find('div',
                                                        'woocommerce'
                                                        '-product-'
                                                        'gallery').findAll(
            'img')]
        p = Product(
            name,
            cls.__name__,
            category,
            url,
            url,
            sku,
            stock,
            price,
            price,
            'CLP',
            sku=sku,
            picture_urls=picture_urls
        )
        return [p]
