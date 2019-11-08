from unofficialautotraderscraper.autotraderca import query_to_search_url, db_write_for_search_query_url

price_min = 500
price_max = 13000
price_range = "%d,%d" % (price_min, price_max)

mil_min = 10000
mil_max = 100001
mileage = "%d,%d" % (mil_min, mil_max)

distance_from_postal_range = 50  # in km i think?
postal = "M5H 2N2"               # defaults to center of toronto (city hall)
transmission = "Automatic"
car_status = "New-Used"

max_results = 15    # or 10000

at_query = query_to_search_url(results_per_page=max_results, price_range=price_range,
                               mileage_range=mileage, distance_from_me=distance_from_postal_range,
                               postal=postal, transmission=transmission, car_status=car_status)

print(at_query)
#db_write_for_search_query_url(at_query, timeout=0.5)

def stub():
    pass