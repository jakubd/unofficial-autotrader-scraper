Unofficial Autotrader.ca Scraper
---------------

This program will scrape `autotrader.ca` website and dump some general information about results
to a Sqlite3 database.

Data captured includes model, car brand, price, mileage.  It tries some fuzzy terms in order to determine
whether the vehicle posted has a backup camera, has ABS and whether the seller mentions that there is only 
one previous owner.

## Note:  This project is abandoned

I originally made this program in order to find trends in used car postings in my area as well as to satisfy my basic
safety requirements in a vehicle.  However I ended up abandoning this project entirely. The fact that insurance claims are 
often obscured from non commercialized source interfaces (ie carfax) basically leads to a hidden variable that explains
most "good price" used vehicles. Additionally I noticed that all high volume official dealerships in my area did not 
use autotrader.  