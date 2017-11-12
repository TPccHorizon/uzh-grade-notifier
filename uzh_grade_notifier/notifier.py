import subprocess
import json
import requests
import os
from sys import platform


def display_alert(title, text, path_config):
    if platform == "darwin":
        # macOS: display alert using AppleScript
        subprocess.Popen("""osascript -e 'display alert "{}" "{}"'""".format(title, text))
    elif platform == "win32":
        # windows: display alert using cscript and a vbs script
        subprocess.Popen("""cscript "{}"/mb.vbs "{}: {}" """.format(os.path.dirname(__file__), title, text))
    elif platform == "linux" or platform == "linux2":
        # linux: display alert using notify-send()
        subprocess.Popen("""notify-send {} {}""".format(title, text))

    # Check if pbToken was filled in and send notification to pushBullet token owner
    with open(path_config) as json_config:
        config = json.load(json_config)
        pbtoken = config["pbToken"]

        # Is pbToken not empty
        if pbtoken != "":
            headers = {'Content-Type': 'application/json', 'Access-Token': pbtoken}
            url = 'https://api.pushbullet.com/v2/pushes'
            payload = {'body': text, 'title': title, 'type': 'note'}
            # Send post request to pushbullet server
            requests.post(url, data=json.dumps(payload), headers=headers)
        else:
            print("No pushbullet token found")


def send_grade_notification(grades, path):
    if len(grades) > 1:
        alert_title = "New grades"
    else:
        alert_title = "New grade"

    alert_text = ""
    for grade in grades:
        alert_text += grade.module_name + ": " + grade.grade + "\n"

    display_alert(alert_title, alert_text, path)
