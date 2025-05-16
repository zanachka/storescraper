from .store import Store


class StoreWithUrlExtensions(Store):
    url_extensions = []

    @classmethod
    def categories(cls):
        cats = []
        for _category_path, category in cls.url_extensions:
            if category not in cats:
                cats.append(category)
        return cats

    @classmethod
    def discover_urls_for_category(cls, category, extra_args=None):
        for url_extension, local_category in cls.url_extensions:
            if local_category != category:
                continue

            yield from cls.discover_urls_for_url_extension(url_extension, extra_args)

    @classmethod
    def discover_urls_for_url_extension(cls, url_extension, extra_args):
        raise NotImplementedError("This method must be provided by subclasses")
