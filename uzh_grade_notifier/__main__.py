import argparse
import logging
import os.path
import sys
from logging import handlers

import grade_checker
import notifier
import page_scraper

desktop_notifications_on = True
path_cache = os.path.dirname(__file__) + "/../cache/grades-cache.json"
path_config = os.path.dirname(__file__) + "/../config/config.json"
path_logger = os.path.dirname(__file__) + "/../cache/log.log"
url_start_page = "https://idagreen.uzh.ch/re/"


# get logger
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

# specify log format
formatter = logging.Formatter("%(asctime)s %(name)-12s %(levelname)-8s %(message)s")

# log to console
console_handler = logging.StreamHandler(stream=sys.stdout)
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)

# log to file
file_handler = handlers.RotatingFileHandler(filename=path_logger, maxBytes=1000*1000)
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)


# creates arguments parser from argparse to deal with arguments
parser = argparse.ArgumentParser()

# add the argument config to let you enter your own path for config.json and .grades_cache.json
parser.add_argument('-config', '--config', nargs='*', action='store',
                    help='lets you add separate path for config and grades_cache'
                         + '  usage: --config /path/to/config.json /path/to/cache')

# add the argument headless to avoid desktop notifications
parser.add_argument('-headless', '--headless', help='Disables notifications for the desktop', action="store_true")

# parse known arguments into args and unknown into unknown_args
args, unknown_args = parser.parse_known_args()

# check if there was a config flag and if yes if there are the right amount of arguments
if args.config is not None:
    if len(args.config) == 2:
        path_config = args.config[0]
        path_cache = args.config[1]
    else:
        # tell the user there was a mistake with the flag usage
        print("-config usage: --config /path/to/config.json /path/to/cache")

# check if there was a headless flag and if yes turn the desktop notifications off
if args.headless:
    desktop_notifications_on = False


# open start page and extract URL of AAI login page
url_login_page = page_scraper.get_login_url(url_start_page)

# log into AAI and fetch HTML of grades page
html_grades = page_scraper.get_grades_page(url_login_page, path_config)

# analyze the grades page and get a list of newly released grades
new_grades = grade_checker.update_grades(html_grades, path_cache)

# if new grades have been released, display notification
if new_grades:
    notifier.send_grade_notification(new_grades, path_config, desktop_notifications_on)
else:
    logger.info("No new grades received")
