import argparse
import json
import logging
import sys

sys.path.append("../..")

from storescraper.utils import get_store_class_by_name, chunks, create_celery_group
from storescraper.product import Product


def main():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(message)s",
        filename="products.log",
        filemode="w",
    )

    parser = argparse.ArgumentParser(
        description="Retrieves the products of the given store."
    )

    parser.add_argument("store", type=str, help="The name of the store to be parsed")

    parser.add_argument(
        "--categories", type=str, nargs="*", help="Specific categories to be parsed"
    )

    parser.add_argument(
        "--with_async",
        type=bool,
        nargs="?",
        default=False,
        const=True,
        help="Use async tasks (celery)",
    )

    parser.add_argument(
        "--extra_args",
        type=json.loads,
        nargs="?",
        default={},
        help="Optional arguments to pass to the parser "
        "(usually username/password) for private sites)",
    )

    args = parser.parse_args()
    store = get_store_class_by_name(args.store)

    if args.categories:
        for category in args.categories:
            assert (
                category in store.categories()
            ), f"{category} is not a valid category for {args.store}"
        categories = args.categories
    else:
        categories = store.categories()

    extra_args = store.extra_args_with_preflight(extra_args=args.extra_args)

    available_products = 0
    unavailable_products = 0
    discovery_urls_with_error = []
    seen_urls = set()

    if args.with_async:
        for category_chunk in chunks(
            categories, store.preferred_discover_urls_concurrency
        ):
            discover_urls_for_category_tasks = []
            print("Discovering URLs for: {}".format(category_chunk))

            for category in category_chunk:
                task = store.discover_urls_for_category_task.s(
                    store.__name__, category, extra_args=extra_args
                )
                task.set(queue="storescraper")
                discover_urls_for_category_tasks.append(task)

            tasks_group = create_celery_group(discover_urls_for_category_tasks)
            for category, discovery_urls in zip(category_chunk, tasks_group.get()):
                filtered_discovery_urls = []
                for discovery_url in discovery_urls:
                    if discovery_url not in seen_urls:
                        seen_urls.add(discovery_url)
                        filtered_discovery_urls.append(discovery_url)

                discovery_url_chunks = chunks(
                    filtered_discovery_urls,
                    store.preferred_products_for_url_concurrency,
                )
                for discovery_url_chunk in discovery_url_chunks:
                    products_for_url_tasks = []
                    for discovery_url in discovery_url_chunk:
                        task = store.products_for_url_task.s(
                            store.__name__,
                            discovery_url,
                            category=category,
                            extra_args=extra_args,
                        )
                        task.set(queue="storescraper")
                        products_for_url_tasks.append(task)
                    products_for_url_tasks_group = create_celery_group(
                        products_for_url_tasks
                    )
                    for discovery_url, products_for_discovery_url in zip(
                        discovery_url_chunk, products_for_url_tasks_group.get()
                    ):
                        retrieved_products_for_url = False
                        for serialized_product in products_for_discovery_url:
                            product = Product.deserialize(serialized_product)
                            retrieved_products_for_url = True
                            if product.is_available():
                                available_products += 1
                            else:
                                unavailable_products += 1
                            print(product, "\n")
                        if not retrieved_products_for_url:
                            discovery_urls_with_error.append(discovery_url)

    else:
        for category in categories:
            print(f"Discovering URLs for: {category}")
            for discovery_url in store.discover_urls_for_category(
                category, extra_args=extra_args
            ):
                if discovery_url not in seen_urls:
                    seen_urls.add(discovery_url)
                    retrieved_products_for_url = False
                    for product in store.products_for_url(
                        discovery_url, category=category, extra_args=extra_args
                    ):
                        retrieved_products_for_url = True
                        if product.is_available():
                            available_products += 1
                        else:
                            unavailable_products += 1
                        print(product, "\n")
                    if not retrieved_products_for_url:
                        discovery_urls_with_error.append(discovery_url)
    print()
    print("Available: {}".format(available_products))
    print("Unavailable: {}".format(unavailable_products))
    if discovery_urls_with_error:
        print("Discovery URLs with errors:")
        for discovery_url in discovery_urls_with_error:
            print(f"* {discovery_url}")
    else:
        print("No discovery URLs with errors found.")
    print(
        "Total: {}".format(
            available_products + unavailable_products + len(discovery_urls_with_error)
        )
    )


if __name__ == "__main__":
    main()
