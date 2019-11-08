Unofficial Autotrader.ca Scraper
---------------

**Not affliated with autotrader.ca in anyway**

This program will scrape the `autotrader.ca` website and dump some general information about results
to a Sqlite database.  This will include things that are typically not contained in the search parameters
of the site.  For example you can order by dealer to plan visiting many in one trip.  

I originally made this program in order to find trends in used car postings in my area as well as to satisfy my basic
safety requirements in a vehicle.  However I ended up abandoning this project entirely. The fact that insurance claims are 
often obscured from non commercialized interfaces (ie carfax) basically leads to a hidden variable that explains
most "well priced" used vehicles I have found. I also noticed that all high volume official dealerships in my area did not 
use autotrader.  

## Note:  This is not actively maintained

Data captured includes model, car brand, price, mileage.  It tries some fuzzy terms in order to determine
whether the vehicle posted has a backup camera, has ABS and whether the seller mentions that there is only 
one previous owner.