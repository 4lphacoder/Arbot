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
	driver.delete_all_cookies()
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


if __name__ == "__main__":
	banner()
	(optlist,args) = parsing_args()
	update_global_variables(optlist,args)
	print('[ + ] Loading Web Browser')
	driver = initialising_selenium()
	print('[ + ] Web Browser loaded')

	print('[ + ] Opening Webpage')
	driver.get('https://www.trademe.co.nz/')
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
	client_list = client_bundle.find_elements_by_tag_name('a')
	
	for i in range(len(client_list)):
		print(client_list[i].text)

	#wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="ListViewList"]')))