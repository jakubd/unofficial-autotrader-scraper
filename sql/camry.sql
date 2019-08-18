-- Sort by Mileage Descending

SELECT
    model_year, title, mileage, sales_type,
    price, assess_comp, assess_dollar,
    backup_cam, abs, no_accident, one_owner,
    sales_area, dealer_name, dealer_address,
    url, text
    FROM
        car_details
    WHERE
        lower(car_model) like '%camry%'
    ORDER BY
        mileage
;

-- Sort by Mileage Descending (DEALER ONLY)

SELECT
    model_year, title, mileage, sales_type,
    price, assess_comp, assess_dollar,
    backup_cam, abs, no_accident, one_owner,
    sales_area, dealer_name, dealer_address,
    url, text
    FROM
        car_details
    WHERE
        sales_type = 'Dealer' and
          (
            lower(car_model) like '%camry%'
          )
    ORDER BY
        mileage
;


-- Sort by Price Descending

SELECT
    model_year, title, mileage, sales_type,
    price, assess_comp, assess_dollar,
    backup_cam, abs, no_accident, one_owner,
    sales_area, dealer_name, dealer_address,
    url, text
    FROM
        car_details
    WHERE
        lower(car_model) like '%camry%'
    ORDER BY
        price
;

-- Sort by Price Descending (Dealer Only)

SELECT
    model_year, title, mileage, sales_type,
    price, assess_comp, assess_dollar,
    backup_cam, abs, no_accident, one_owner,
    sales_area, dealer_name, dealer_address,
    url, text
    FROM
        car_details
    WHERE
        sales_type = 'Dealer' and
          (
            lower(car_model) like '%camry%'
            )
    ORDER BY
        price
;