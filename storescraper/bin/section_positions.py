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
        "--sections", type=str, nargs="+", help="Specific sections to be parsed"
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
    scraper_sections = store.sections()
    if args.sections:
        for section in args.sections:
            assert (
                section in scraper_sections
            ), f"{section} is not a valid section for {args.store}"
        sections = args.sections
    else:
        sections = scraper_sections

    extra_args = store.extra_args_with_preflight(extra_args=args.extra_args)

    if args.with_async:
        pass
        for section_chunk in chunks(
            sections, store.preferred_discover_urls_concurrency
        ):
            chunk_tasks = []
            print("Obtaining section positions for: {}".format(section_chunk))

            for section in section_chunk:
                task = store.section_positions_task.s(
                    store.__name__, section, extra_args=extra_args
                )
                task.set(queue="storescraper")
                chunk_tasks.append(task)

            tasks_group = create_celery_group(chunk_tasks)
            for section, section_positions in zip(section_chunk, tasks_group.get()):
                print(f"Section positions for {section}")
                for section_position in section_positions:
                    print(section_position)
    else:
        for section in sections:
            print(f"Discovering section positions for: {section}")
            for section_position in store.section_positions(
                section, extra_args=extra_args
            ):
                print(section_position)


if __name__ == "__main__":
    main()
