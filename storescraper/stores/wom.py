import json
from decimal import Decimal

from storescraper.categories import CELL_PLAN, CELL
from storescraper.product import Product
from storescraper.store import Store
from storescraper.utils import session_with_proxy


class Wom(Store):
    prepago_url = "https://www.wom.cl/prepago/"
    planes_url = "https://store.wom.cl/planes/"

    @classmethod
    def categories(cls):
        return [CELL_PLAN, CELL]

    @classmethod
    def discover_urls_for_category(cls, category, extra_args=None):
        if category == CELL_PLAN:
            yield cls.prepago_url
            yield cls.planes_url

        elif category == CELL:
            session = session_with_proxy(extra_args)
            equipos_url = (
                "https://store-srv.wom.cl/rest/V1/content/getList?"
                "searchCriteria[filterGroups][0][filters][0]"
                "[field]=attribute_set_id&searchCriteria"
                "[filterGroups][0][filters][0][value]=11&"
                "searchCriteria[filterGroups][1][filters][0]"
                "[field]=type_id&searchCriteria[filterGroups][1]"
                "[filters][0][value]=configurable&searchCriteria"
                "[pageSize]=200&searchCriteria[currentPage]=1&"
                "searchCriteria[filterGroups][2][filters][0]"
                "[field]=name&searchCriteria[filterGroups][2]"
                "[filters][0][value]=%25%25&searchCriteria"
                "[filterGroups][2][filters][0]"
                "[condition_type]=like&searchCriteria[sortOrders]"
                "[0][field]=&searchCriteria[filterGroups][10]"
                "[filters][0][field]=status&searchCriteria"
                "[filterGroups][10][filters][0][value]=1"
            )
            response = session.get(equipos_url)

            json_response = json.loads(response.text)

            for idx, cell_entry in enumerate(json_response["items"]):
                cell_url = (
                    "https://store.wom.cl/equipos/"
                    + str(cell_entry["sku"])
                    + "/"
                    + cell_entry["name"]
                    .replace("+", "plus")
                    .replace(".", "-")
                    .replace(" ", "-")
                )
                yield cell_url

    @classmethod
    def products_for_url(cls, url, category=None, extra_args=None):
        products = []
        if url == cls.prepago_url:
            # Plan Prepago
            p = Product(
                "WOM Prepago",
                cls.__name__,
                category,
                url,
                url,
                "WOM Prepago",
                -1,
                Decimal(0),
                Decimal(0),
                "CLP",
                allow_zero_prices=True,
            )
            products.append(p)
        elif url == cls.planes_url:
            # Plan Postpago
            products.extend(cls._plans(url, extra_args))
        elif "/equipos/" in url:
            # Equipo postpago
            products.extend(cls._celular_postpago(url, extra_args))
        else:
            raise Exception("Invalid URL: " + url)
        return products

    @classmethod
    def _plans(cls, url, extra_args):
        variants = [
            "sin cuota de arriendo",
            "con cuota de arriendo",
        ]
        products = []

        for plan_json in extra_args["plans_json"]:
            plan_name = plan_json["name"]
            product_data = json.loads(plan_json["context"]["context"])
            plan_price = Decimal(product_data["price"])

            for variant in variants:
                for suffix in ["", " Portabilidad"]:
                    adjusted_plan_name = "{}{} ({})".format(plan_name, suffix, variant)

                    products.append(
                        Product(
                            adjusted_plan_name,
                            cls.__name__,
                            "CellPlan",
                            url,
                            url,
                            adjusted_plan_name,
                            -1,
                            plan_price,
                            plan_price,
                            "CLP",
                        )
                    )

        return products

    @classmethod
    def _celular_postpago(cls, url, extra_args):
        print(url)
        session = session_with_proxy(extra_args)

        path = url.split("/", 3)[-1]
        endpoint = "https://store.wom.cl/page-data/{}/page-data.json".format(path)
        response = session.get(endpoint)

        if response.status_code == 404:
            return []

        json_data = response.json()
        page_id = json_data["result"]["pageContext"]["id"]

        stock_endpoint = (
            "https://store-srv.wom.cl/rest/V1/content/getList?"
            "searchCriteria[filterGroups][0][filters][0][field]=attribute_set_id&"
            "searchCriteria[filterGroups][0][filters][0][value]=11&"
            "searchCriteria[filterGroups][1][filters][0][field]=sku&"
            f"searchCriteria[filterGroups][1][filters][0][value]={page_id}&"
            "searchCriteria[filterGroups][1][filters][0][condition_type]=eq&"
            "searchCriteria[pageSize]=1&searchCriteria[currentPage]=1&"
            "searchCriteria[sortOrders][0][direction]=DESC"
        )
        response = session.get(stock_endpoint)
        stock_json = response.json()
        stock_dict = {}

        for x in stock_json["items"][0]["child"]:
            if x["saleable_info"]:
                stock_dict[x["sku"]] = x["saleable_info"][0]["qty"]
            else:
                stock_dict[x["sku"]] = 0

        if "SEMI" in json_data["result"]["data"]["contentfulProduct"]["name"].upper():
            condition = "https://schema.org/RefurbishedCondition"
        else:
            condition = "https://schema.org/NewCondition"

        products = []
        plans = [
            "WOM " + plan_choice["name"] for plan_choice in extra_args["plans_json"]
        ]

        variations = json_data["result"]["data"]["contentfulProduct"][
            "productVariations"
        ]

        if not variations:
            return []

        for entry in variations:
            name = entry["name"]
            context = json.loads(entry["context"]["context"])
            if not context["graphql_data"]:
                continue
            graphql_data = json.loads(context["graphql_data"])

            try:
                stock = stock_dict[entry["referenceId"]]
            except KeyError:
                continue

            portability_choices = [
                ("", "newConnection"),
                (" Portabilidad", "portIn"),
            ]

            for portability_name_suffix, portability_json_field in portability_choices:
                price_without_installments = None
                initial_price_with_installments = None
                installment_price = None

                for related_price in graphql_data["productOfferingPrice"][
                    portability_json_field
                ]["relatedPrice"]:
                    if related_price["priceType"] == "price":
                        price_without_installments = Decimal(
                            related_price["price"]["value"]
                        )
                    elif related_price["priceType"] == "initialPrice":
                        initial_price_with_installments = Decimal(
                            related_price["price"]["value"]
                        )
                    elif (
                        related_price["priceType"] == "installmentPrice"
                        and related_price["recurringChargePeriodType"]
                    ):
                        installment_price = Decimal(related_price["price"]["value"])

                if (
                    price_without_installments is None
                    or initial_price_with_installments is None
                    or installment_price is None
                ):
                    return []

                assert price_without_installments is not None
                assert initial_price_with_installments is not None
                assert installment_price is not None

                for plan in plans:
                    # Without installments
                    products.append(
                        Product(
                            name,
                            cls.__name__,
                            "Cell",
                            url,
                            url,
                            "{} {}{}".format(name, plan, portability_name_suffix),
                            stock,
                            price_without_installments,
                            price_without_installments,
                            "CLP",
                            condition=condition,
                            cell_plan_name="{}{}".format(
                                plan,
                                portability_name_suffix,
                            ),
                            cell_monthly_payment=Decimal(0),
                            allow_zero_prices=True,
                        )
                    )

                    # With installments
                    products.append(
                        Product(
                            name,
                            cls.__name__,
                            "Cell",
                            url,
                            url,
                            "{} {}{} Cuotas".format(
                                name, plan, portability_name_suffix
                            ),
                            stock,
                            initial_price_with_installments,
                            initial_price_with_installments,
                            "CLP",
                            condition=condition,
                            cell_plan_name="{}{} Cuotas".format(
                                plan,
                                portability_name_suffix,
                            ),
                            cell_monthly_payment=installment_price,
                            allow_zero_prices=True,
                        )
                    )

            # Prepaid
            prepaid_price = Decimal(
                graphql_data["productOfferingPrice"]["standard"]["relatedPrice"][0][
                    "price"
                ]["value"]
            )

            products.append(
                Product(
                    name,
                    cls.__name__,
                    "Cell",
                    url,
                    url,
                    "{} Prepago".format(name),
                    stock,
                    prepaid_price,
                    prepaid_price,
                    "CLP",
                    condition=condition,
                    cell_plan_name="WOM Prepago",
                )
            )

        return products

    @classmethod
    def preflight(cls, extra_args=None):
        # Obtain valid plans
        session = session_with_proxy(extra_args)

        response = session.get("https://store.wom.cl/page-data/sq/d/" "2591293040.json")

        data = response.json()
        plans_json = []
        import re

        for product_entry in data["data"]["allContentfulProduct"]["nodes"]:
            try:
                plan_context = json.loads(product_entry["context"]["context"])
            except json.decoder.JSONDecodeError:
                json_string = product_entry["context"]["context"]
                fixed_json_string = re.sub(
                    r',\s*\{\s*"price_newline_campaing"',
                    r', "price_newline_campaing"',
                    json_string,
                )
                fixed_json_string = re.sub(
                    r'price_newline_campaing":\s*([0-9]+)\s*\},',
                    r'price_newline_campaing": \1,',
                    fixed_json_string,
                )
                plan_context = json.loads(fixed_json_string)

            if not product_entry["offer"] and not product_entry["offerPdp"]:
                continue
            if plan_context.get("clientCampaignOnly", False):
                continue

            plans_json.append(product_entry)

        return {"plans_json": plans_json}
