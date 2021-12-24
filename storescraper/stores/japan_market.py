import logging
from decimal import Decimal

from bs4 import BeautifulSoup

from storescraper.categories import VIDEO_CARD, MOUSE
from storescraper.product import Product
from storescraper.store import Store
from storescraper.utils import session_with_proxy, remove_words


class JapanMarket(Store):
    @classmethod
    def categories(cls):
        return [
            VIDEO_CARD,
            MOUSE
        ]

    @classmethod
    def discover_urls_for_category(cls, category, extra_args=None):
        url_extensions = [
            ['graphics-cards', VIDEO_CARD],
            ['computer-parts/mouse-mousepad', MOUSE]
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

                url_webpage = 'https://japanmarket.ne.jp/product-category/' \
                              'electronics/{}/page/{}/'.format(url_extension,
                                                               page)
                print(url_webpage)
                response = session.get(url_webpage)
                soup = BeautifulSoup(response.text, 'html.parser')
                product_containers = soup.findAll('div', 'product-small')

                if not product_containers:
                    if page == 1:
                        logging.warning('empty category: ' + url_extension)
                    break
                for container in product_containers:
                    product_url = container.find('a')['href']
                    product_urls.append(product_url + '?currency=CLP')
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
        name = soup.find('h1', 'product-title').text.strip()
        sku = soup.find('link', {'rel': 'shortlink'})['href'].split('p=')[-1]
        if soup.find('p', 'stock in-stock'):
            stock = int(soup.find('p', 'stock').text.strip().split()[0])
        else:
            stock = -1
        price_container = soup.find('p', 'price')
        if price_container.find('ins'):
            price = Decimal(remove_words(
                price_container.find('ins').text.strip()))
        else:
            price = Decimal(remove_words(
                price_container.text.strip()))

        picture_urls = [tag['src'] for tag in
                        soup.find('div', 'product-gallery').findAll('img')]

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
            picture_urls=picture_urls)
        return [p]
