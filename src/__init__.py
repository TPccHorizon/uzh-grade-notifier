import json
import os.path

from src import scraping

url_start_page = "https://idagreen.uzh.ch/re/"


# check if config.json file exists
if not os.path.exists("config.json"):
    raise Exception("Configuration file not found - Please create a config.json file with the"
                    "attributes 'username' and 'password' in the project directory.")

# import AAI login data from config.json file
with open("config.json") as json_data_file:
    data = json.load(json_data_file)
    username = data["username"]
    password = data["password"]

# open start page and get URL of AAI login page
url_login_page = scraping.get_url_login(url_start_page)

# log into AAI and fetch the grades page
html_grades = scraping.login(url_login_page, username, password)
