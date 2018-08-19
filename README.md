# Instagram-Bot
A like and comment automation tool for Instagram, completely free and opensource.  Can be used for marketing purposes 

Made with Selenium lib with Python 3.5.2, doesn't need the instagram API. Thus it bypasses the GDPR changes that instagram did.

Please feel free to contribute to the code or the coder

HOW TO USE:
Make sure you have Python and Selenium as well as a selenium compatable browser installed.
call the doSearch function and pass theses params
  doSearch(path_to_browser, usename, password, list_of_tags, likes_per_day, headless--> OPTIONAL PARAM)
  
  EXAMPLE:
  doSearch("D:\\Programs\\chromedriver.exe", "MYACCOUNT",'MYPASS', ["morning", "dawn", "Electrical", "engineering","computer","Mechanical", "electronics", "photography",
"goldenHour", "sunrise","sunset","hike","nature","mountain","programmer","Spiderman","like4like", "like4follow","instagood","wanderlust","travel" ], None, False)



''' TODO
replace the sleep statments by proper 'is page loaded' logic:
make a function that randomizes the tags:
make a control mech that controls the amounts of likes a day and likes a tag:
handle phone number request page when login at times
--lower piriority: make it so you can like and not comment and vice versa.


Please feel free to contribute to the code or the coder.
