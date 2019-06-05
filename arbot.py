import getopt
import sys

# Global Variables
USERID = ''
PASSWD = ''
KEYWORD = ''
CATEGORY = ''
NUMBER = 5

try:
	from selenium import webdriver
	from selenium.webdriver.common.keys import Keys
	from selenium.webdriver.common.by import By
	from selenium.webdriver.support.ui import WebDriverWait
	from selenium.webdriver.support.select import Select
	from selenium.webdriver.support import expected_conditions as EC

except ModuleNotFoundError:
	print('''
		\033[91m 
		[   ERROR  ] Selenium API not installed in system...\033[97m
		[ SOLUTION ] Install selenium using pip tool...
		''')
	sys.exit()

def initialising_selenium():
	chrome_options = webdriver.ChromeOptions()
	chrome_options.add_argument('--disable-extensions')
	chrome_options.add_argument('--profile-directory=Default')
	chrome_options.add_argument('--incognito')
	chrome_options.add_argument('disable-plugins-discovery')
	try:
		driver = webdriver.Chrome(options=chrome_options)
	except TypeError:
		print('''
			\033[91m 
			[   ERROR  ] Chrome drivers not installed...\033[97m
			[ SOLUTION ] Download Chrome browser & chrome webdrivers and make the path of chrome drivers Global Path variable...
			''')
		sys.exit()
	# Uncomment for deleting cookies
	# driver.delete_all_cookies() 
	return driver

def banner():
# 	print('''

#        db                   88                              
#       d88b                  88                       ,d     
#      d8'`8b                 88                       88     
#     d8'  `8b     8b,dPPYba, 88,dPPYba,   ,adPPYba, MM88MMM  
#    d8YaaaaY8b    88P'   "Y8 88P'    "8a a8"     "8a  88     
#   d8""""""""8b   88         88       d8 8b       d8  88     
#  d8'        `8b  88         88b,   ,a8" "8a,   ,a8"  88,    
# d8'          `8b 88         8Y"Ybbd8"'   `"YbbdP"'   "Y888  

# 					\033[91m[ TradeMe Scrapper ]\033[93m
# 										-version : 1.0.0
# 										-author : Prashant Varshney <c>\033[97m
# 			''')
	print('---------------------------------------------------------')
	print('TradeMe Scrapper')
	print('\t\t\tversion: 1.0.1\n\t\t\tauthor: Prashant Varshney')
	print('---------------------------------------------------------')
	
def usage():
	print('''
	usage :
		python3 arbot.py [ options ]
		
		-u : userid
		-p : password
		-s : searching keyword
		-c : category
		-n : number of queries
		''')

def parsing_args():
	options = 'u:p:s:c:n:'
	optlist,args = getopt.getopt(sys.argv[1:],options)
	if len(optlist) != 5:
		print('''
		\033[91m 
	[   ERROR  ] Invalid / Incomplete system arguments...\033[97m
		''')
		usage()
		sys.exit()
	return (optlist,args)

def update_global_variables(optlist,args):
	global USERID
	global PASSWD
	global KEYWORD
	global CATEGORY
	global NUMBER
	for i in range(len(optlist)):
		if optlist[i][0] == '-u':
			USERID = optlist[i][1]
		if optlist[i][0] == '-p':
			PASSWD = optlist[i][1]
		if optlist[i][0] == '-s':
			KEYWORD = optlist[i][1]
		if optlist[i][0] == '-c':
			CATEGORY = optlist[i][1]
		if optlist[i][0] == '-n':
			NUMBER = int(optlist[i][1])

def login(driver):
	global USERID
	global PASSWD
	print('[ + ] Requesting login page')
	driver.get('https://www.trademe.co.nz/Members/Login.aspx?url=%2fdefault.aspx')
	print('[ + ] Login page recieved')
	print('[ + ] Entering credentials')
	driver.find_element_by_xpath('//*[@id="page_email"]').send_keys(USERID)
	driver.find_element_by_xpath('//*[@id="page_password"]').send_keys(PASSWD)
	input('[ + ] Captcha found, press return after filling it')
	print('[ + ] Logging In')
	driver.find_element_by_xpath('//*[@id="LoginPageButton"]').click()


if __name__ == "__main__":
	banner()
	(optlist,args) = parsing_args()
	update_global_variables(optlist,args)
	print('[ + ] Loading Web Browser')
	driver = initialising_selenium()
	print('[ + ] Web Browser loaded')

	print('[ + ] Opening Webpage')
	login(driver)   # login redirects to home page
	print('[ + ] Webpage Loaded Completely')
	wait = WebDriverWait(driver, 20)
	search_field = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="searchString"]')))
	
	print('[ + ] Sending Keyword')
	search_field.send_keys(KEYWORD)

	print('[ + ] Selecting Category')
	category_selection = Select(driver.find_element_by_xpath('//*[@id="SearchType"]'))
	category_selection.select_by_visible_text(CATEGORY)
	
	driver.find_element_by_xpath('//*[@id="generalSearch"]/div[2]/button').click()
	print('[ + ] Searching')

	client_bundle = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="ListViewList"]')))
	print('[ + ] Bundling list of clients')

	print('[ + ] Creating list of client')
	client_list = client_bundle.find_elements_by_class_name('listingTitle')	
	for i in range(len(client_list)):
		client_list[i] = client_list[i].find_element_by_tag_name('a').get_attribute('href')
	
	print('[ + ] Storing clients address in file client_addr.txt')
	fd = open('client_addr.txt','w')
	for client_addr in client_list:
		fd.write(client_addr)
		fd.write('\n')
	fd.close()

	print('[ + ] Extraction started')
	fd = open(str('scraping_on_keyword_'+KEYWORD+'.csv'),'w')
	client_name = ''
	client_num1 = ''
	client_num2 = ''
	client_location = ''
	business_name = ''
	about = ''
	for client_addr in client_list:
		print('\n[ + ] Extracting from '+client_addr)
		driver.get(client_addr)
		print('[ + ] Client\'s page loaded')
		try:
			client_name = driver.find_element_by_xpath('//*[@id="ClassifiedActions_ServiceContactName"]').text.replace('\n',', ')
		except:
			pass
		try:
			client_num1 = driver.find_element_by_xpath('//*[@id="ClassifiedActions_ServicePhone1"]').text
		except:
			pass
		try:
			client_num2 = driver.find_element_by_xpath('//*[@id="ClassifiedActions_ServicePhone2"]').text
		except:
			pass
		try:
			client_location = driver.find_element_by_xpath('//*[@id="ClassifiedActions_ServiceLocation"]').text.replace('\n',', ')
		except:
			pass
		try:
			business_name = driver.find_element_by_xpath('//*[@id="ListingAttributes"]/tbody/tr[1]/td').text.replace('\n',', ')
		except:
			pass
		try:
			about = driver.find_element_by_xpath('//*[@id="ListingAttributes"]/tbody/tr[3]/td').text.replace('\n',',')
		except:
			pass

		print('[ + ] Extraction from '+client_addr+' completed')
		print('Name : '+client_name+'\nBusiness Name : '+business_name+'\nPhone : '+client_num1+' , '+client_num2+'\nClient\'s Location : '+client_location+'\nAbout : '+about+'\n')
		fd.write(client_name+';'+business_name+';'+client_num1+';'+client_num2+';'+KEYWORD+';'+client_location+';'+about+'\n')
		fd.flush()
		input('[ + ] Press return to continue')
		
	
	#wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="ListViewList"]')))