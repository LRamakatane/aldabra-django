"""
"""
# imports
import datetime
import copy
import requests
from config.settings import env as getvar

# other functions


def generate_timestamp():
    now = datetime.datetime.now()
    return now.timestamp


def generate_30min_timestamp():
    # Get the current time
    current_time = datetime.datetime.now()

    # Add 30 minutes to the current time
    time_30_minutes_from_now = current_time + datetime.timedelta(minutes=30)

    # Convert the result to a timestamp (Unix timestamp, which is the number of seconds since January 1, 1970)
    timestamp = int(time_30_minutes_from_now.timestamp())

    return timestamp


def format_response_data(data: dict, status: int, message="success!", next_resource_link='http://127.0.0.1'):
    return {
        "message": "success!",
        "status_code": status,
        "payload": data,
        "next_resource_link": next_resource_link,
    }


def get_exchange_rate(base_currency: str, target) -> dict:
    api_key = getvar("OPEN_ER_API_KEY")

    # Endpoint for Open Exchange Rates API
    base_url = "https://v6.exchangerate-api.com/v6/"

    # Specify the base currency and target currencies
    base_currency = base_currency
    target_currencies = target

    # Construct the API URL
    api_url = f"{base_url}{api_key}/latest/{base_currency}"

    try:
        # Send a GET request to the API
        response = requests.get(api_url)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            data = response.json()

            # Extract exchange rates for target currencies
            exchange_rates = {
                currency: data["conversion_rates"][currency]
                for currency in target_currencies
            }

            # return exchange rates
            return exchange_rates
        else:
            print(
                f"Failed to fetch exchange rates. Status code: {response.status_code}"
            )

    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")

    return {}


def round_to_nearest_multiple(value, multiple):
    return round(value / multiple) * multiple


def ngn_to_usd(amount_in_naira):
    ex_rate: dict = get_exchange_rate("NGN", ["USD"])
    return amount_in_naira * ex_rate["USD"]


def lbs_to_kg(lbs):
    return lbs / 2.2046


def kg_to_lbs(kg):
    return kg * 2.2046


def get_weight(aw, dw):
    # -- aw = actual weight
    # dw = dimensional weight -- #
    return aw if aw > dw else dw


def convert_datetime_string(datetime_string):
    return str(datetime_string.replace(" ", "T")) + "GMT+01:00"


def five_days_from_now():  # sourcery skip: inline-immediately-returned-variable
    # Get the current datetime
    now = datetime.datetime.now()
    future = now + datetime.timedelta(days=5)
    rounded = future.replace(microsecond=0, second=future.second)
    datetime_string = str(rounded)
    formatted_string = convert_datetime_string(datetime_string)

    return formatted_string


def today():  # sourcery skip: inline-immediately-returned-variable
    # Get the current date
    current_date = datetime.date.today()
    # Convert the date to a string in the desired format
    current_date_string = current_date.strftime("%Y-%m-%d")
    # Return the date string
    return current_date_string


def today_string():
    initial_date = str(today())
    date_list = initial_date.split("-")
    return "".join(date_list)


def total_package_weight(packages):
    w = []
    for package in packages:
        dimension = package.get("packageDimension")
        w.append(dimension["weight"])
    return sum(w)


def get_unit_weight(packages):
    weight = total_package_weight(packages["packages"])
    item_number = len(packages["items"])

    return weight * item_number


def get_item_list_with_weight(packages):
    unit_weight = get_unit_weight(packages)
    items_copy = copy.deepcopy(packages["items"])
    for item in items_copy:
        item["weight"] = unit_weight

    return items_copy


def flatten_list(data):
    flattened_list = []
    for sublist in data:
        flattened_list.extend(iter(sublist))
    return flattened_list
