import argparse
import json
import logging
import sys

sys.path.append("../..")

from storescraper.product import Product
from storescraper.utils import (
    get_store_class_by_name,
    chunks,
    create_celery_group,
)


def main():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(message)s",
        filename="products.log",
        filemode="w",
    )

    parser = argparse.ArgumentParser(
        description="Discovers the URLs of the given store and keyword"
    )

    parser.add_argument("store", type=str, help="The name of the store to be parsed")

    parser.add_argument("keyword", type=str, help="Specific keyword to be searched")

    parser.add_argument("threshold", type=int, help="The amount of urls to retrieve")

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
        help="Optional arguments to pass to the parser",
    )

    args = parser.parse_args()
    store = get_store_class_by_name(args.store)
    keyword = args.keyword
    threshold = args.threshold
    extra_args = store.extra_args_with_preflight(extra_args=args.extra_args)

    available_products = 0
    unavailable_products = 0
    discovery_urls_with_error = []

    discovery_urls = store.discover_urls_for_keyword(
        keyword, threshold, extra_args=extra_args
    )

    if args.with_async:
        discovery_url_chunks = chunks(
            discovery_urls,
            store.preferred_products_for_url_concurrency,
        )
        for discovery_url_chunk in discovery_url_chunks:
            products_for_url_tasks = []
            for discovery_url in discovery_url_chunk:
                task = store.products_for_url_task.s(
                    store.__name__,
                    discovery_url,
                    category=None,
                    extra_args=extra_args,
                )
                task.set(queue="storescraper")
                products_for_url_tasks.append(task)
            products_for_url_tasks_group = create_celery_group(products_for_url_tasks)
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
        for discovery_url in discovery_urls:
            retrieved_products_for_url = False
            for product in store.products_for_url(
                discovery_url, category=None, extra_args=extra_args
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
