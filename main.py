###		Note
### the program works with the 2018-Augest version of instagram, it may not work if the UI change in the future.
##Auther: Mohammed
### URL: https://github.com/brilliant-ember/Instagram-Bot
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from time import sleep
import random
import itertools as itertools


''' TODO
implement the is_liked function: CHECK √
replace the sleep statments by proper 'is page loaded' logic:
implemet a comment function: CHECK √
replace the double search.send_keys(Keys.RETURN) by down arrow then enter: DEPRICATED X
make a function that randomizes the tags:
make a control mech that controls the amounts of likes a day and likes a tag:
--lower piriority: make it so you can like and not comment and vice versa.
'''

#####		definition of helper functions start here			#####

def automate_search_tag(driver, tag):
	'''OBSELETE, DEPRECATED
	this function uses the search box to look up tags. The better approch is to use the url. Method kept for future reference '''
	try:# this is for the pop up that askes about the turning on notifications, may be obselete in the future
		driver.find_element_by_css_selector('''button.aOOlW.HoLwm ''').click()
	except Exception as e:
		print(e)
		pass
	search = driver.find_element_by_xpath('''//*[@id="react-root"]/section/nav/div[2]/div/div/div[2]/input''')
	search.send_keys("#"+tag)
	sleep(1) # do not replace
	search.send_keys(Keys.DOWN)
	sleep(1) # do not replace
	search.send_keys(Keys.RETURN)

def is_liked(driver):
	'''takes the driver and uses xpath to get if it is liked --> retruns true if liked '''
	sleep(1)
	isLiked = driver.find_element_by_xpath('''/html/body/div[3]/div/div[2]/div/article/div[2]/section[1]/span[1]/button/span''').get_attribute("aria-label")
	if isLiked == "Like":
		return True
	elif isLiked == "Unlike":
		return False

def generate_comment():
	c_list = list(itertools.product(
								["this", "the", "your"],
								["photo", "picture", "shot", "snapshot"],
								["is", "looks", "feels"],
								["great", "super", "good", "very good",
								"good", "wow", "WOW", "cool",
								"GREAT", "magnificent", "magical", "very cool",
								"stylish", "so stylish", "beautiful",
								"so beautiful", "so stylish", "so professional",
								"so glorious", "very glorious",
								"fantastick", "excellent", "amazing"],
								[".", "..", "...", "!", "!!"]))

	repl = [("  ", " "), (" .", "."), (" !", "!")]
	res = " ".join(random.choice(c_list))
	for s, r in repl:
		res = res.replace(s, r)
	return res.capitalize()

def do_comment(driver):
	txt_area = driver.find_element_by_css_selector("textarea.Ypffh")
	txt_area.click()
	txt_area = driver.find_element_by_css_selector("textarea.Ypffh") # doing it again to avoid the reference lost error :stale element reference: element is not attached to the page document
	sleep(2)
	txt_area.send_keys(generate_comment())
	txt_area.send_keys(Keys.RETURN)

def login(driver, username, password):
	usern = driver.find_element_by_name('''username''')
	passw =  driver.find_element_by_name('''password''')
	usern.send_keys(username)
	passw.send_keys(password)
	driver.find_element_by_xpath('''//*[@id="react-root"]/section/main/div/article/div/div[1]/div/form/span/button''').click()

def go_to_tag(list_of_tags, driver):
	'''picks a tag at random and makes the driver go there'''
	assert len(list_of_tags) > 0, "Make sure your list of tags is populated!"
	random_index = random.randrange(0,len(list_of_tags))
	tag = list_of_tags[random_index]
	driver.get("https://www.instagram.com/explore/tags/"+tag)

def sudden_login(driver, list_of_tags):
	try:
		driver.find_element_by_xpath('''//*[@id="react-root"]/section/nav/div[2]/div/div/div[3]/div/div/section/div/div/span[2]/a[1]/span/button''').click()
		sleep(1)
		login(driver)
		sleep(1.6)
		go_to_tag(list_of_tags, driver)
		sleep(3)
		return False
	except Exception as e:
		print("didnt find Login")
		return True

def botting(driver, list_of_tags):
	go_to_tag(list_of_tags, driver)
	sleep(1)
	try: # for the weired error of element not click able
		driver.find_element_by_xpath('''//*[@id="react-root"]/section/main/article/div[2]/div/div[1]/div[1]/a/div''').click()
		
	except:
		elem = driver.find_element_by_tag_name("html")
		elem.send_keys(Keys.HOME)
		sleep(1)
		elem.send_keys(Keys.END)
		sleep(1)
		elem.send_keys(Keys.HOME)

		driver.find_element_by_xpath('''//*[@id="react-root"]/section/main/article/div[2]/div/div[1]/div[1]/a/div''').click()
	sleep(1)
	#add if it is liked or not
	if is_liked(driver):
		btn = driver.find_element_by_css_selector("button.coreSpriteHeartOpen.oF4XW.dCJp8")
		btn.click()
		do_comment(driver)
	else:
		print (" I am already liked!!")

	driver.find_element_by_link_text("Next").click()
	randSleep = random.randrange(0,18)
	if (randSleep >= 9):#some random condtino to change the tag
		go_to_tag(list_of_tags, driver)
	sleep(randSleep)	


# def match_likes_per_day(likes_per_day):
# 	'''spaces out the likes for one day randomly by generating random integers that add up to the amount of seconds in a day, 
# 	to be used in the sleep function to randomly space out likes'''

# 	per_hour = likes_per_day // 24
# 	per_minute = per_hour // 60




#######		def of functions end		#########

def doSearch(driverPath,username, password, list_of_tags, likes_per_day, headless = False): 
	'''list_of tags is a list of strings, you dont include the #. headless is mostly for development use it just tells the function to use a visable or a headless browser
	username and password are both strings
	'''
	# Chrome requires the complete path with the executable
	if headless:
		chrome_options = Options()
		chrome_options.add_argument("--headless")
		driver = webdriver.Chrome(chrome_options=chrome_options, executable_path = driverPath)
	else:
		driver = webdriver.Chrome(driverPath)

	url = "https://www.instagram.com/accounts/login/"
	driver.get(url)
	login(driver, username, password)

	go_to_tag(list_of_tags, driver)
	
	sleep(2)
#	this is for the sudden login pop-up
	
	
	while True:
		if sudden_login(driver, list_of_tags):
			botting(driver, list_of_tags )



