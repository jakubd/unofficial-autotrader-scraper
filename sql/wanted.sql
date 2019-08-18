-- Sort by Mileage Descending

SELECT
    model_year, car_brand, car_model, mileage, sales_type,
    price, assess_comp, assess_dollar,
    backup_cam, abs, no_accident, one_owner,
    sales_area, dealer_name, dealer_address,
    url, text
    FROM
        car_details
    WHERE
        lower(car_model) like '%camry%' or
        lower(car_model) like '%corolla%' or
        lower(car_model) like '%civic%' or
        lower(car_model) like '%mazda3%' or
        lower(car_model) like '%mazda 3%' or
        lower(car_model) like '%fit%' or
        lower(car_model) like '%matrix%' or
        lower(car_model) like '%yaris%' or
        lower(car_model) like '%rav 4%' or
        lower(car_model) like '%rav4%' or
        lower(car_model) like '%legacy%' or
        lower(car_model) like '%impreza%' or
        lower(car_brand) like '%suzuki%' or
        lower(car_brand) like '%lexus%' or
        lower(car_brand) like '%scion%' or
        lower(car_model) like '%accord%'
    ORDER BY
        mileage
;

-- Sort by Mileage Descending (DEALER ONLY)

SELECT
    model_year, car_brand, car_model, mileage, sales_type,
    price, assess_comp, assess_dollar,
    backup_cam, abs, no_accident, one_owner,
    sales_area, dealer_name, dealer_address,
    url, text
    FROM
        car_details
    WHERE
        sales_type = 'Dealer' and
          (
            lower(car_model) like '%camry%' or
            lower(car_model) like '%corolla%' or
            lower(car_model) like '%civic%' or
            lower(car_model) like '%mazda3%' or
            lower(car_model) like '%mazda 3%' or
            lower(car_model) like '%fit%' or
            lower(car_model) like '%matrix%' or
            lower(car_model) like '%yaris%' or
            lower(car_model) like '%rav 4%' or
            lower(car_model) like '%rav4%' or
            lower(car_brand) like '%suzuki%' or
            lower(car_brand) like '%lexus%' or
            lower(car_brand) like '%scion%' or
            lower(car_model) like '%accord%'
            )
    ORDER BY
        mileage
;


-- Sort by Price Descending

SELECT
    model_year, car_brand, car_model, mileage, sales_type,
    price, assess_comp, assess_dollar,
    backup_cam, abs, no_accident, one_owner,
    sales_area, dealer_name, dealer_address,
    url, text
    FROM
        car_details
    WHERE
        lower(car_model) like '%camry%' or
        lower(car_model) like '%corolla%' or
        lower(car_model) like '%civic%' or
        lower(car_model) like '%mazda3%' or
        lower(car_model) like '%mazda 3%' or
        lower(car_model) like '%fit%' or
        lower(car_model) like '%matrix%' or
        lower(car_model) like '%yaris%' or
        lower(car_model) like '%rav 4%' or
        lower(car_model) like '%rav4%' or
        lower(car_brand) like '%suzuki%' or
        lower(car_brand) like '%lexus%' or
        lower(car_brand) like '%scion%' or
        lower(car_model) like '%accord%'
    ORDER BY
        price
;

-- Sort by Price Descending (Dealer Only)

SELECT
    model_year, car_brand, car_model, mileage, sales_type,
    price, assess_comp, assess_dollar,
    backup_cam, abs, no_accident, one_owner,
    sales_area, dealer_name, dealer_address,
    url, text
    FROM
        car_details
    WHERE
        sales_type = 'Dealer' and
          (
            lower(car_model) like '%camry%' or
            lower(car_model) like '%corolla%' or
            lower(car_model) like '%civic%' or
            lower(car_model) like '%mazda3%' or
            lower(car_model) like '%mazda 3%' or
            lower(car_model) like '%fit%' or
            lower(car_model) like '%matrix%' or
            lower(car_model) like '%yaris%' or
            lower(car_model) like '%rav 4%' or
            lower(car_model) like '%rav4%' or
            lower(car_brand) like '%suzuki%' or
            lower(car_brand) like '%lexus%' or
            lower(car_brand) like '%scion%' or
            lower(car_model) like '%accord%'
            )
    ORDER BY
        price
;