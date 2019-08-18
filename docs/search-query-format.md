# Searches

How are the search URLs formed from our chosen queies

a sample URL from a selection: 

"https://www.autotrader.ca/cars/on/toronto/?rcp=15&rcs=0&srt=9&pRng=500%2C13000&oRng=10000%2C100001&prx=50&prv=Ontario&loc=M5H%202N2&trans=Automatic&hprc=True&wcp=True&sts=New-Used&inMarket=advancedSearch"

Fields

* rcp=15  
    * results per page 
    * will accept 15, 25, 50, 100 
    * will also accept ludacris high values like 1000, 10000          
* rcs=0
    * page offset
    * if rcp is 15, then page 2 rcs is 15 then 30 etc
* srt=9
    * sort value
* pRng=500%2C13000
    * price range
* oRng=10000%2C100001
    * mileage range
* prx=50 
    * "distance from me"
* prv=Ontario
    * province
* loc=M5H%202N2
    * location postal code to make its determinations (from center of Toronto)
* trans=Automatic
    * transmission pref
* hprc=True
* wcp=True
* sts=New-Used
    * condition value
* inMarket=advancedSearch


Basically I wont need a pager, just boost the rcp value to be more than max result

# timeout notes

my average query has ~1,700 results.  this 19 default size pages.

For a single page average time without any timeout is 31 seconds which for the whole result set
is 4165 seconds (about an hour)

with a 0.5 sec timout average time for a single page is 51 seconds which for the whole result
set is 6069 seconds (~ 1.5 hour)

a decent initial timeout should be about 0.5 seconds between GETs until proven otherwise.