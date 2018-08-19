## The program works with the 2018-Augest version of instagram, it may not work if the UI change in the future.
## Auther: Mohammed
## URL: https://github.com/brilliant-ember/Instagram-Bot

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
#from selenium.common.exceptions import InvalidSelectorException
from time import sleep
import random
import itertools as itertools

class Instagram_bot:
	def __init__(self, driverPath,username, password, list_of_tags, likes_per_day, headless = False ):
		self.username = username
		self.password = password
		self.list_of_tags =	list_of_tags
		self.likes_per_day = likes_per_day
		self.counter = 0

		# Chrome requires the complete path with the executable
		if headless:
			chrome_options = Options()
			chrome_options.add_argument("--headless")
			self.driver = webdriver.Chrome(chrome_options=chrome_options, executable_path = driverPath)
		else:
			self.driver = webdriver.Chrome(driverPath)

	def caller(self):
		url = "https://www.instagram.com/accounts/login/"
		self.driver.get(url)
		self.login()
		self.go_to_tag()
		sleep(1.5) #replace sleep with something that tells u when the page loads rather than waiting for it to hopefull load

		while True:
			if self.sudden_login():
				self.botting()
				


	def login(self):
		'''assumes you're at the login url'''
		try:
			usern = self.driver.find_element_by_name('''username''')
			passw =  self.driver.find_element_by_name('''password''')
			usern.send_keys(self.username)
			passw.send_keys(self.password)
			self.driver.find_element_by_xpath('''//*[@id="react-root"]/section/main/div/article/div/div[1]/div/form/span/button''').click()
		except Exception as e:
			print("INSTAGRAM_BOT: unable to login")
			print(e)


	def go_to_tag(self):
		'''picks a tag at random and makes the driver go there'''
		assert len(self.list_of_tags) > 0, "Make sure your list of tags is populated!"
		random_index = random.randrange(0,len(self.list_of_tags))
		tag = self.list_of_tags[random_index]
		self.driver.get("https://www.instagram.com/explore/tags/" + tag)



	def sudden_login(self):
		'''this method deals with the login page suddenly poping up outta no where'''
		try:
			self.driver.find_element_by_xpath('''//*[@id="react-root"]/section/nav/div[2]/div/div/div[3]/div/div/section/div/div/span[2]/a[1]/span/button''').click()
			sleep(1)
			self.login(driver)
			sleep(1.6)
			self.go_to_tag()
			sleep(1.9)
			return False
		except Exception as e:
			#print("didnt find Login")
			return True

	def select_post(self):
		'''finds the first post in the most recent section, if there is no recent section it will chage tag'''
		sleep(1)
		try:
			self.handle_nonclickable_error()
		except:
			self.go_to_tag()
			sleep(0.5)
			self.select_post()

			
	def handle_nonclickable_error(self):
		went_through_except = False  #this is to track if it went through except
		try: 
			#this clicks on the first post of the most recent NOT the most popular
			self.driver.find_element_by_xpath('''//*[@id="react-root"]/section/main/article/div[2]/div/div[1]/div[1]/a/div''').click()
			print("INSTAGRAM_BOT: went clicked a post on try if catch Encountered then try catch block not working")
		except:
			# for the weird error of element not being clickable, u have to scroll up and down
			elem = self.driver.find_element_by_tag_name("html")
			elem.send_keys(Keys.HOME)	#scrolls all the way up
			sleep(1)
			elem.send_keys(Keys.END)	#scrolls all the way down
			sleep(1)
			elem.send_keys(Keys.HOME)
			print("INSTAGRAMBOT: Encountered Unclickable error")
			self.driver.find_element_by_xpath('''//*[@id="react-root"]/section/main/article/div[2]/div/div[1]/div[1]/a/div''').click()


	def botting(self):
		self.select_post()
		sleep(1)
		self.like_and_comment()
		self.driver.find_element_by_link_text("Next").click()
		sleep(0.3)
		self.like_and_comment()
		randSleep = random.randrange(0,18)
		if (randSleep >= 9):	#some random condtion to change the tag
			self.go_to_tag()
		sleep(randSleep)	

	def like_and_comment(self):
	#check if post is liked or not
		post_liked_already = self.is_liked()
		if not post_liked_already:
			btn = self.driver.find_element_by_css_selector("button.coreSpriteHeartOpen.oF4XW.dCJp8")
			btn.click()
			self.do_comment()
			self.counter += 1
			print("INSTAGRAM_BOT: Like and comment successful, number:  "+ str(self.counter))
		elif post_liked_already:
			print (" INSTAGRAM_BOT: like and comment unsucessful, post already liked, number: " + str(self.counter))
		else:
			print("INSTAGRAM_BOT: error on botting function")



	def is_liked(self):
		'''retruns true if post is liked '''
		sleep(2)
		isLiked = self.driver.find_element_by_xpath('''/html/body/div[3]/div/div[2]/div/article/div[2]/section[1]/span[1]/button/span''').get_attribute("aria-label")
		if isLiked == "Like":
			return False
		elif isLiked == "Unlike":
			return True
		else:
			print("INSTAGRAM_BOT: error on is_liked()")


	def generate_comment(self):
		c_list = list(itertools.product(
									["this", "the", "your"],
									["photo", "picture", "shot", "snapshot","post"],
									["is", "looks", "feels"],
									["great", "super", "good", "very good",
									"good", "wow", "WOW", "cool",
									"GREAT", "magnificent", "magical", "very cool",
									"stylish", "so stylish", "beautiful",
									"so beautiful", "so stylish", "so professional",
									"so glorious", "very glorious","magestic",
									"fantastick", "excellent", "amazing"],
									[".", "..", "...", "!", "!!"]))

		repl = [("  ", " "), (" .", "."), (" !", "!")]
		res = " ".join(random.choice(c_list))
		for s, r in repl:
			res = res.replace(s, r)
		return res.capitalize()

	def do_comment(self):
		try:
			txt_area = self.driver.find_element_by_css_selector("textarea.Ypffh")
			txt_area.click()
			txt_area = self.driver.find_element_by_css_selector("textarea.Ypffh") # doing it again to avoid the reference lost error :stale element reference: element is not attached to the page document
			sleep(2)
			txt_area.send_keys(self.generate_comment())
			txt_area.send_keys(Keys.RETURN)
		except:
			print("INSTAGRAM_BOT: cannot comment, maybe commets disabled for this post, note that there are other cases where I can't comment and dont print any log")








