import dataset
import datetime
import os
import re
import requests
import time
from bs4 import BeautifulSoup
from re import sub, search
from sqlalchemy.types import Integer
from string import Template
from tabulate import tabulate
from urllib.parse import quote
from yaspin import yaspin


def query_to_search_url(results_per_page=15, result_offset=0, sort_value=9, price_range="500,13000",
                        mileage_range="10000,100001", distance_from_me=50, province="Ontario",
                        postal="M5H 2N2", transmission="Automatic", car_status="New-Used"):
    """
    Given an autotrader query generate a dir url.
    :param results_per_page: # of results to display on a single page
    :param result_offset: offset of search
    :param sort_value: sorting value
    :param price_range: price range as string seperating low and highbound with a comma
    :param mileage_range: mileage range as a string seperating low and highbound with a comma
    :param distance_from_me: the search radius
    :param province: province of search
    :param postal: postcode (incl space) that AT will use to base their allowable distance from dealer
    :param transmission: transmission type ("Automatic, Manual")
    :param car_status: Whether to get new or used
    :return: string af a search
    """
    at_search_template = Template(
        "https://www.autotrader.ca/cars/on/toronto/?"
        + "rcp=$results_per_page&"
        + "rcs=$result_offset&"
        + "srt=$sort_value&"
        + "pRng=$price_range&"
        + "oRng=$mileage_range&"
        + "prx=$distance_from_me&"
        + "prv=$province&"
        + "loc=$postal&"
        + "trans=$transmission&"
        + "hprc=True&"
        + "wcp=True&"
        + "sts=$car_status&"
        + "inMarket=advancedSearch"
    )

    search_query = {
        "results_per_page": results_per_page,
        "result_offset": result_offset,
        "sort_value": sort_value,
        "price_range": quote(price_range),
        "mileage_range": quote(mileage_range),
        "distance_from_me": distance_from_me,
        "province": province,
        "postal": quote(postal),
        "transmission": transmission,
        "car_status": car_status
    }

    return at_search_template.substitute(search_query)


def url_to_content(given_url):
    """
    Given any url it will return HTTP content, checks if the return code is 200 and that content is pure utf-8
    :param given_url: any URL string
    :return: Either the content as string or blank
    """
    headers = {
        'User-Agent': 'Google Chrome Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36.',
    }

    r = requests.get(given_url, headers=headers)

    if r.status_code == 200:
        try:
            return r.content.decode("utf-8")
        except UnicodeDecodeError:
            return ""
    else:
        return ""


def search_url_to_car_detail_urls(given_url):
    """
    Given an autotrader.ca url that points to a search query result.  Return
    the Car Detail URLs -- called CompositeURLs (if any)  these URLs contain full vehicle details
    :param given_url:
    :return:
    """
    content_at_url = url_to_content(given_url)
    if "CompositeIdUrls" in content_at_url:
        m = re.search('"compositeIdUrls":\[(.*)\]', content_at_url)
        if m:
            return ["https://www.autotrader.ca" + p.strip("\"") for p in m.group(1).split(",")]
    else:
        return []


def get_info_from_detail_urls_only(given_cardetail_url):
    """
    Given a car detail URL this will extract details from the URL only (not do a GET)
    :param given_cardetail_url: AT page where full details are shown
    :return: dict
    """
    result = {
        "sales_type": "",
        "car_brand": "",
        "car_model": "",
        "sales_area": "",
        "sales_province": "",
        "url": "",
    }

    url_split_regex = "https://www.autotrader.ca/(a|ico)/(.+?)/(.+?)/(.+?)/(.+?)/"
    m = re.search(url_split_regex, given_cardetail_url)
    if m is not None:
        if len(m.groups()) == 5:
            if m.group(1) == "ico":
                result["sales_type"] = "Private"
            else:
                result["sales_type"] = "Dealer"

            result["car_brand"] = m.group(2).replace("%20", " ").title()
            result["car_model"] = m.group(3).replace("%20", " ").title()
            result["sales_area"] = m.group(4).replace("%20", " ").title()
            result["sales_province"] = m.group(5).replace("%20", " ").title()
            result["url"] = given_cardetail_url.split("?showcpo")[0]

    return result


def currencystr_to_float(given_str):
    """
    Given a string representing currency convert to float
    :param given_str: ex: "$1,000"
    :return: ex: float(1000.0)
    """
    return float(sub(r'[^\d.]', '', given_str))


def kmstr_to_int(given_str):
    """
    Given a string reprenting km convert it to an int
    :param given_str: ex: "1,000 km"
    :return: ex: 1000
    """
    return int(sub(r'[^\d.]', '', given_str))


def spec_table_to_dict(given_soup):
    """
    Pulls the spec table from car detail page
    :param given_soup: given bs4 soup object
    :return: dict
    """
    equiv_table = {
        "KILOMETRES": "mileage",
        "STATUS": "status",
        "TRIM": "trim",
        "BODY TYPE": "body_type",
        "ENGINE": "engine",
        "CYLINDER": "cyl",
        "TRANSMISSION": "transmission",
        "DRIVETRAIN": "drivetrain",
        "STOCK NUMBER": "stock_num",
        "EXTERIOR COLOUR": "ext_color",
        "INTERIOR COLOUR": "int_color",
        "PASSENGERS": "passengers",
        "DOORS": "doors",
        "FUEL TYPE": "fuel",
        "CITY FUEL ECONOMY": "city_fuel_econ",
        "HWY FUEL ECONOMY": "hwy_fuel_econ"
    }

    maybe_tables = given_soup.find_all('table')
    spec = {}

    if len(maybe_tables) > 1:
        spec_table = given_soup.find_all('table')[0]
        spec_rows = spec_table.findChildren(['th', 'tr'])
        for row in spec_rows:
            cells = row.findChildren('td')
            for cell in cells:
                if row.th is not None:
                    this_field = row.th.text
                    this_value = cell.text

                    if this_value == "-":
                        this_value = None

                    if this_field == "KILOMETRES":
                        try:
                            this_value = kmstr_to_int(this_value)
                        except ValueError:
                            this_value = 0
                    elif this_field == "CYLINDER" and this_value is not None:
                        try:
                            this_value = int(this_value)
                        except ValueError:
                            this_value = 0
                    elif this_field == "DOORS" and this_value is not None:
                        this_value = re.sub("[^0-9]", "", this_value)
                        try:
                            this_value = int(this_value)
                        except ValueError:
                            this_value = 0

                    if this_field in equiv_table:
                        this_field = equiv_table[this_field]

                        spec[this_field] = this_value

    return spec


def check_text_against_wordlist(given_text, given_list):
    for check_against_this_word in given_list:
        if check_against_this_word in given_text:
            return True
    return False


def extract_text_from_class(given_soup, tag_name, class_name):
    text_to_ret = ""
    if given_soup.find(tag_name, class_=class_name):
        text_to_ret = given_soup.find(tag_name, class_=class_name).text.strip(" ")

    return text_to_ret


def extract_text(given_soup):
    # title
    text = extract_title_and_year(given_soup)[0] + "\n*************\n"
    # highlights
    text += extract_text_from_class(given_soup, "ul", "vdp-highlight-features")
    # description
    text += extract_text_from_class(given_soup, "div", "vdp-option-content")
    # options
    if given_soup.find("div", {"id": "vdp-options-list"}):
        text += given_soup.find("div", {"id": "vdp-options-list"}).text.strip(" ")
    return text


def extract_title_and_year(given_soup):
    title = ""
    year = ""
    if given_soup.find("h1", class_="vdp-hero-title"):
        title = given_soup.find("h1", class_="vdp-hero-title").text.strip(" ")
        title_regex = "(\d{4})(.+?) - (.*)"
        m = search(title_regex, title)
        if m is not None and len(m.groups()) == 3:
            year = m.group(1)
            title = m.group(2).strip(" ")

    return title, year


def scrape_details_from_detail_page_contents(given_content):
    """
    Does most of the scraping from car detail page contents
    :param given_content: the page contents either bytestring or string
    :return: details as dict
    """

    result = {
        "title": None,
        "model_year": None,
        "price": None,
        "assess_dollar": None,
        "assess_comp": None,
        "mileage": None,
        "status": None,
        "trim": None,
        "body_type": None,
        "engine": None,
        "cyl": None,
        "transmission": None,
        "drivetrain": None,
        "stock_num": None,
        "ext_color": None,
        "int_color": None,
        "passengers": None,
        "doors": None,
        "fuel": None,
        "city_fuel_econ": None,
        "hwy_fuel_econ": None,
        "text": None,
        "one_owner": False,
        "backup_cam": False,
        "no_accident": False,
        "abs": False,
        "dealer_name": None,
        "dealer_address": None
    }

    backup_cam_words = [
        "camera",
        "rear cam",
        "rearview cam",
        "backupcam",
        "backup cam",
        "cam/",
        " cam ",
    ]

    no_accident_words = [
        "no accident",
        "no-accident",
        "noaccident"
    ]

    one_owner_words = [
        "one owner",
        "1 owner",
        "one-owner",
        "1owner",
        "oneowner",
    ]

    abs_words = [
        "abs",
        "antilock",
        "anti-lock",
    ]

    soup = BeautifulSoup(given_content, 'html.parser')

    # extract text and search it for features bools
    just_text = extract_text(soup)
    result["text"] = just_text

    # for comparisons lets just make it all lower case
    just_text = just_text.lower()
    result["one_owner"] = check_text_against_wordlist(just_text, one_owner_words)
    result["backup_cam"] = check_text_against_wordlist(just_text, backup_cam_words)
    result["no_accident"] = check_text_against_wordlist(just_text, no_accident_words)
    result["abs"] = check_text_against_wordlist(just_text, abs_words)

    # get dealer name and address (needs cleaning)
    result["dealer_name"] = extract_text_from_class(soup, "p", "dealer-name")

    dealer_address = ""
    if soup.find("div", {"id": "vdp-dealer-content"}):
        dealer_address += soup.find("div", {"id": "vdp-dealer-content"}).text.strip(" ")

    to_remove_from_address_list = [
        'Mechanical & Cosmetic Reconditioning',
        'Finance options available',
        'Vehicle History Report',
        'Dealer website',
        'View map',
        'View all inventory',
        'Click to show',
        'Get an instant offer',
        'open sundays',
        'award winning customer service',
        'large selection of inventory',
        "'",
        "`",
    ]

    for remove_this in to_remove_from_address_list:
        dealer_address = dealer_address.lower().replace(remove_this.lower(), "")

    dealer_address = dealer_address.lstrip().rstrip()
    dealer_address_list = dealer_address.split('\n')[1:]

    dealer_address_list_final = []
    for this_line in dealer_address_list:
        if len(this_line) > 2:
            dealer_address_list_final.append(this_line)

    dealer_address = "\n".join(dealer_address_list_final)
    result["dealer_address"] = dealer_address

    # get title and model year
    result["title"], result["model_year"] = extract_title_and_year(soup)

    # get price
    if soup.find("h3", class_="vdp-check-bar-price"):
        result["price"] = currencystr_to_float(soup.find("h3", class_="vdp-check-bar-price").text)

    # get assessment details
    check_assess = soup.find("p", class_="vdp-pa-makeModelYear")
    if check_assess is not None:
        raw_assess = soup.find("p", class_="vdp-pa-makeModelYear").text.strip(" ")

        m = search("This vehicle is (.+?) (ABOVE|BELOW) MARKET", raw_assess)
        if m is not None:
            if len(m.groups()) == 2:
                result["assess_dollar"] = currencystr_to_float(m.group(1))
                result["assess_comp"] = m.group(2)

    # add spec table to results (kms, etc)
    result = {**result, **spec_table_to_dict(soup)}

    # sometimes mileage isn't in the spec table, lets pull it from highlights if we haven't got it
    if result["mileage"] is None:
        if soup.find("li", class_="vdp-highlights-icon-1"):
            result["mileage"] = kmstr_to_int(soup.find("li", class_="vdp-highlights-icon-1").text)

    return result


def get_all_details_from_detail_url(given_compurl):
    """
    Given an AT car detail URL return all details (from URL and page contents)
    This will perform the GET
    :param given_compurl: Given AT car detail url
    :return: returns a dict of all the details
    """
    compurl_contents = url_to_content(given_compurl)
    details = scrape_details_from_detail_page_contents(compurl_contents)
    url_details = get_info_from_detail_urls_only(given_compurl)
    return {**details, **url_details}


def get_results_for_search_query_url(given_url, timeout=0.0):
    """
    Given a search query URL, returns a list of dicts with all details it can
    :param timeout: number of seconds to wait between query (cooloff)
    :param given_url: a search query URL
    :return: dict
    """
    my_atcomps = search_url_to_car_detail_urls(given_url)
    result_list = []
    for idx, this_url in enumerate(my_atcomps):
        if idx != 0:
            time.sleep(timeout)
        result_list.append(get_all_details_from_detail_url(this_url))
    return result_list


def print_results_for_search_query_url(given_url, timeout=0.0):
    """
    Given a search query URL, print all details to screen
    :param timeout: number of seconds to wait between query (cooloff)
    :param given_url: a search query URL
    :return:
    """
    result_list = get_results_for_search_query_url(given_url, timeout=timeout)
    print(tabulate(result_list, headers="keys"))


def db_has_runid_col(sqlite_fn="cars.db"):
    """
    Checks the table if a "runid" column exists
    :param sqlite_fn:
    :return:
    """

    if os.path.isfile(sqlite_fn):
        db = dataset.connect('sqlite:///%s' % sqlite_fn)
        q1 = "PRAGMA table_info(car_details);"
        res = db.query(q1)
        for row in res:
            if row["name"] == "runid":
                return True
    return False


def db_get_last_runid(sqlite_fn="cars.db"):
    if os.path.isfile(sqlite_fn):
        if db_has_runid_col(sqlite_fn=sqlite_fn):
            db = dataset.connect('sqlite:///%s' % sqlite_fn)
            q1 = "SELECT max(runid) from car_details;"
            res = db.query(q1)
            for row in res:
                for k, v in row.items():
                    if v is not None:
                        return v
    return 0

@yaspin(text="Fetching results now (this may take a while)...")
def db_write_for_search_query_url(given_url, sqlite_fn="cars.db", timeout=0.0):
    """
    Given a search query URL, print all details to a given sqlite file
    :param sqlite_fn: given filename
    :param timeout: number of seconds to wait between query (cooloff)
    :param given_url: a search query URL
    :return:
    """
    result_list = get_results_for_search_query_url(given_url, timeout=timeout)

    db = dataset.connect('sqlite:///%s' % sqlite_fn)
    table = db["car_details"]
    last_run_id = db_get_last_runid(sqlite_fn)
    run_on = datetime.datetime.now()

    for this_result in result_list:
        this_result["runid"] = last_run_id+1
        this_result["run_on"] = run_on
        table.insert(this_result, types={"mileage": Integer})

