import argparse
import json
import logging
import sys

sys.path.append("../..")

from storescraper.utils import (
    get_store_class_by_name,
    chunks,
    create_celery_group,
)


def main():
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    logging.basicConfig(level=logging.WARNING, stream=sys.stdout)

    parser = argparse.ArgumentParser(
        description="Discovers the URLs of the given store and (optional) " "categories"
    )

    parser.add_argument("store", type=str, help="The name of the store to be parsed")

    parser.add_argument(
        "--categories", type=str, nargs="+", help="Specific categories to be parsed"
    )

    parser.add_argument(
        "--with_async",
        type=bool,
        nargs="?",
        default=False,
        const=True,
        help="Use asynchronous tasks (celery)",
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

    if args.with_async:
        for category_chunk in chunks(
            categories, store.preferred_discover_urls_concurrency
        ):
            chunk_tasks = []
            print("Discovering URLs for: {}".format(category_chunk))

            for category in category_chunk:
                task = store.discover_urls_for_category_task.s(
                    store.__name__, category, extra_args=args.extra_args
                )
                task.set(queue="storescraper")
                chunk_tasks.append(task)

            tasks_group = create_celery_group(chunk_tasks)
            for category, category_urls in zip(category_chunk, tasks_group.get()):
                print(f"URLs for {category}")
                for url in category_urls:
                    print(url)
    else:
        seen_urls = set()
        for category in categories:
            print(f"Discovering URLs for: {category}")
            for url in store.discover_urls_for_category_with_preflight(
                category, extra_args=args.extra_args
            ):
                if url not in seen_urls:
                    print(url)
                    seen_urls.add(url)

        print("Total: {} URLs".format(len(seen_urls)))


if __name__ == "__main__":
    main()
