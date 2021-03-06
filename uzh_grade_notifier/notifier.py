import json
import logging
import os
from subprocess import Popen
from sys import platform

import requests

logger = logging.getLogger()


def display_alert(title, text, path_config, desktop_notifications_on):
    """Send notifications with the tools specified in the configuration file"""

    logger.debug("Reading config.json for desired notification methods and tokens")

    # Check if pbToken was filled in and send notification to pushBullet token owner
    with open(path_config) as json_config:
        config = json.load(json_config)
        if "pbToken" in config:
            logger.info("Sending PushBullet notification")
            pb_token = config["pbToken"]
            headers = {'Content-Type': 'application/json', 'Access-Token': pb_token}
            url = 'https://api.pushbullet.com/v2/pushes'
            payload = {'body': text, 'title': title, 'type': 'note'}
            # Send post request to pushbullet server
            requests.post(url, data=json.dumps(payload), headers=headers)

        # Check if tgBotToken and tgChatId was filled in and send notification to telegram chat
        if "tgBotToken" in config and "tgChatId" in config:
            logger.info("Sending Telegram notification")
            tg_token = config["tgBotToken"]
            tg_id = config["tgChatId"]
            headers = {'Content-Type': 'application/json'}
            url = 'https://api.telegram.org/bot' + tg_token + '/sendMessage'
            message = '*{}*\n{}'.format(title, text)
            payload = {'chat_id': tg_id, 'text': message, 'parse_mode': 'Markdown'}
            # Send post request to telegram server
            requests.post(url, data=json.dumps(payload), headers=headers)

    # check if desktop notifications are on
    if desktop_notifications_on:
        if platform == "darwin":
            # macOS: display alert using AppleScript
            logger.info("Sending macOS notification")
            os.system("""osascript -e 'display alert "{}" message "{}"'""".format(title, text))
        elif platform == "win32":
            # windows: display alert using cscript and a vbs script
            logger.info("Sending Windows notification")
            Popen("""cscript "{}"/win_msgbox.vbs "{}: {}" """.format(os.path.dirname(__file__), title, text))
        elif platform == "linux" or platform == "linux2":
            # linux: display alert using notify-send()
            logger.info("Sending Linux notification")
            os.system("""notify-send "{}" "{}" """.format(title, text))
        else:
            raise EnvironmentError("Notifications for the platform '{}' are not supported."
                                   .format(platform))


def send_grade_notification(grades, path, desktop_notifications_on):
    """Generate notification title and text"""

    if len(grades) > 1:
        alert_title = "New grades"
    else:
        alert_title = "New grade"

    alert_text = ""
    for grade in grades:
        alert_text += grade.module_name + ": " + grade.grade + "\n"

    display_alert(alert_title, alert_text, path, desktop_notifications_on)
