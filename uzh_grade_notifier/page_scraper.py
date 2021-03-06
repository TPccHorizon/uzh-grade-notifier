import json
import logging
import os.path
import re

import requests
from bs4 import BeautifulSoup

logger = logging.getLogger()


def get_login_url(url_start):
    """Open start page and extract URL to AAI login page"""

    logger.info('Getting start page and extracting AAI login URL')

    # GET page
    page_start = requests.get(url_start)
    if page_start.status_code != 200:
        raise Exception("Redirect page returned code " + str(page_start.status_code))

    # extract redirect URL from meta tag
    soup_start = BeautifulSoup(page_start.content, "html.parser")
    scripts = soup_start.findAll("script")
    if scripts:
        # find server base address
        regex_server_address = re.compile("var server = \"(.*)\";")
        server_address = regex_server_address.search(scripts[0].string).group(1)

        # find server path
        regex_url = re.compile("location.href = \"(.*)\"\n")
        url = regex_url.search(scripts[1].string).group(1)

        # merge server base address and path
        url_login = url.replace("\" + server + \"", server_address)
        logger.info('Extracted AAI login URL: ' + url_login)
        return url_login
    else:
        raise Exception("Could not find redirect URL to AAI login page")


def get_grades_page(url_login, path_config):
    """Enter authentication information on AAI login page and follow redirects to get HTML of grades
    page"""

    logger.debug('Reading username and password from config.json file')

    # check if config.json file exists
    if not os.path.exists(path_config):
        raise Exception("Configuration file not found - Please create a config.json file with the"
                        "attributes 'username' and 'password' in the project directory.")

    # import AAI login data from config.json file
    with open(path_config) as json_config:
        config = json.load(json_config)
        username = config["username"]
        password = config["password"]

    # start session (for storing cookies)
    with requests.Session() as session:

        logger.info('Getting AAI login page and extracting form submit URL')

        # GET login page
        page_login = session.get(url_login)
        if page_login.status_code != 200:
            raise Exception("Login page returned code " + str(page_login.status_code))

        # login page: extract POST URL from login form
        soup_login = BeautifulSoup(page_login.content, "html.parser")
        form_login = soup_login.find("form", attrs={"method": "post"})
        if form_login:
            url_confirm = form_login["action"]
        else:
            raise Exception("Could not find submit URL of login form")

        # login page: set up POST parameters
        payload_login = {
            "j_username": username,
            "j_password": password,
            "_eventId_proceed": ""
        }

        # POST to login form URL to get confirmation page
        logger.debug('Sending POST request with login information to receive confirmation page')
        page_confirm = session.post("https://aai-idp.uzh.ch" + url_confirm, data=payload_login)
        if page_confirm.status_code != 200:
            raise Exception("POST on login form returned code " + str(page_confirm.status_code))

        # confirmation page: extract POST URL from confirmation form
        logger.debug('Extracting token and form submit URL from confirmation page')
        soup_confirm = BeautifulSoup(page_confirm.content, "html.parser")
        form_confirm = soup_confirm.find("form", attrs={"method": "post"})
        if form_confirm:
            url_grades = form_confirm["action"]
        else:
            raise Exception("Could not find POST URL of login form")

        # confirmation page: set up POST parameters and headers (to fake browser visit)
        relay_state = soup_confirm.find("input", attrs={"name": "RelayState"})
        saml_response = soup_confirm.find("input", attrs={"name": "SAMLResponse"})
        payload_confirm = {
            "RelayState": relay_state["value"],
            "SAMLResponse": saml_response["value"]
        }
        headers_confirm = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 "
                          "(KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36"}

        # POST to confirmation form URL to get grades page
        logger.debug('Sending POST request with token to receive grades page')
        page_grades = session.post(url_grades, data=payload_confirm, headers=headers_confirm)

        logger.info('Received grades page')
        return page_grades.content
