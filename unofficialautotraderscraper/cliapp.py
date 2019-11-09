import argparse
from unofficialautotraderscraper.autotraderca import query_to_search_url, db_write_for_search_query_url

default_price = "500-1000"
default_mileage = "10000-100001"

parser = argparse.ArgumentParser()
parser.add_argument('-p', '--price', type=str, default=default_price, help="Price range as a string for example: 1-1000.")
parser.add_argument('-m', '--mileage', type=str,  default=default_mileage, help="Mileage range as a string for example: 1-1000.")
parser.add_argument('-l', '--location', type=str,  default="M5H 2N2", help="Location as a Canadian postal code")
parser.add_argument('-d', '--distance', type=int,  default="50", help="Distance in Km that you are searching from the --location")
parser.add_argument('-at', '--automatictransmission', action='store_true',  default=True, help="Show only automatic transmission")
parser.add_argument('-mt', '--manual-transmission', action='store_true',  default=False, help="Show only manual transmission")
parser.add_argument('-o', '--output', type=str, default="cars.db", help="Output SQLite3 database name (default-  carss.db)")

args = parser.parse_args()

def verify_range(givenstr):
    if len(givenstr) <= 3:
        return False
    elif str(givenstr).find("-") < 0:
        return False

    split = str(givenstr).split("-")

    if split is None:
        return False
    elif len(split) != 2:
        return False

    try:
        int(split[0]) & int(split[1])
    except ValueError:
        return False

    return True


if not verify_range(args.price):
    args.price = default_price

if not verify_range(args.mileage):
    args.mileage = default_mileage

if args.manual_transmission:
    transmission = "Manual"
else:
    transmission = "Automatic"

at_query = query_to_search_url(results_per_page=10000, price_range=args.price,
                               mileage_range=args.mileage, distance_from_me=args.distance,
                               postal=args.location, transmission=transmission, car_status="New-Used")


db_write_for_search_query_url(at_query, timeout=0.5, sqlite_fn=args.output)

def stub():
    pass