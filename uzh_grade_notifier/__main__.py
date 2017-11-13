import os.path

import grade_checker
import notifier
import page_scraper

path_cache = os.path.dirname(__file__) + "/../.grades-cache.json"
path_config = os.path.dirname(__file__) + "/../config/config.json"
url_start_page = "https://idagreen.uzh.ch/re/"


# open start page and extract URL of AAI login page
url_login_page = page_scraper.get_login_url(url_start_page)

# log into AAI and fetch HTML of grades page
html_grades = page_scraper.get_grades_page(url_login_page, path_config)

# analyze the grades page and get a list of newly released grades
new_grades = grade_checker.update_grades(html_grades, path_cache)

# if new grades have been released, display notification
if new_grades:
    notifier.send_grade_notification(new_grades,path_config)
