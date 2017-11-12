import os


def display_alert(title, text):
    # TODO Ubuntu, Windows
    # macOS: display alert using AppleScript
    os.system("""
        osascript -e 'display alert "{}" message "{}"'
    """.format(title, text))


def send_grade_notification(grades):
    if len(grades) > 1:
        alert_title = "New grades"
    else:
        alert_title = "New grade"

    alert_text = ""
    for grade in grades:
        alert_text += grade.module_name + ": " + grade.grade + "\n"

    display_alert(alert_title, alert_text)
