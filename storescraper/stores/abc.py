from bs4 import BeautifulSoup

from .abcdin import AbcDin
from storescraper import banner_sections as bs
from storescraper.utils import session_with_proxy


class Abc(AbcDin):
    base_url = "https://www.abc.cl"
    site_name = "Abc"
