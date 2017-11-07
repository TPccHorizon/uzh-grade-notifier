import requests
from bs4 import BeautifulSoup


def get_url_login(url_start):
    """Follow redirect on module booking start page to get URL of AAI login page"""

    # GET page
    page_start = requests.get(url_start)
    if page_start.status_code != 200:
        raise Exception("Redirect page returned code " + str(page_start.status_code))

    # extract redirect URL from meta tag
    soup_start = BeautifulSoup(page_start.content, "html.parser")
    html_meta = soup_start.find("meta", attrs={"http-equiv": "REFRESH"})
    if html_meta:
        html_meta_content = html_meta["content"]
        url_login = html_meta_content.split("url=", 1)[1]
    else:
        raise Exception("Could not find redirect URL to AAI login page")

    return url_login


def login(url_login, username, password):
    """Enter authentication information on AAI login page and follow redirects to get HTML of module
    booking page"""

    # start session (for storing cookies)
    with requests.Session() as session:

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
            raise Exception("Could not find POST URL of login form")

        # login page: set up POST parameters
        payload_login = {
            "j_username": username,
            "j_password": password,
            "_eventId_proceed": ""
        }

        # POST to login form URL to get confirmation page
        page_confirm = session.post("https://aai-idp.uzh.ch" + url_confirm, data=payload_login)
        if page_confirm.status_code != 200:
            raise Exception("POST on login form returned code " + str(page_confirm.status_code))

        # confirmation page: extract POST URL from confirmation form
        soup_confirm = BeautifulSoup(page_confirm.content, "html.parser")
        form_confirm = soup_confirm.find("form", attrs={"method": "post"})
        if form_confirm:
            url_module_booking = form_confirm["action"]
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
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 '
                          '(KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

        # POST to confirmation form URL to get module booking page
        page_module_booking = session.post(url_module_booking, data=payload_confirm,
                                           headers=headers_confirm)
        print(page_module_booking.text)
        return page_module_booking.content
