# UZH Grade Notifier

**This is a Python script which notifies you when new grades of your exams at the University of Zurich are released.**

The script fetches your grades from the university website and compares them to the ones which were fetched at the last script execution. If there are any new ones, a notification is displayed.

The program works on macOS, Windows, and Ubuntu.


## Installation

You need to have Python 3 and [Pipenv](https://github.com/kennethreitz/pipenv) (for package management) installed. 

Clone/download this project to your computer. Use the following command to install the dependencies using Pipenv:

```
pipenv install
```


## Setup

To get the script working, open the `config` folder. Rename the [`sample-config.json`](config/sample-config.json) file to `config.json` and fill in your AAI login information (`username` and `password`).

If you also wish to receive notification to your PushBullet account, enter your access token under `pbToken`. For Telegram, enter `tgBotToken` and `tgChatId`.

```json
{
    "username": "your-uzh-shortname",
    "password": "your-uzh-password",
    "pbToken": "optional-pushbullet-token",
    "tgBotToken": "optional-telegram-bot-token",
    "tgChatId": "optional-telegram-chat-id"
}
```

## Scheduled script execution

Follow these steps to make your operating system execute the script periodically. In the examples, the script is executed every 15 minutes.

### macOS/Linux

Enter the following command in your terminal to edit your list of cronjobs:
```
crontab -e
```
Add the following job to the list (and edit the paths to Python and the script):
```
*/15 * * * * /path/to/python3 /path/to/script/uzh_grade_notifier/__main__.py
```

### Windows 8+

Enter the following command in the Windows command prompt (and edit the paths to Python and the script):
```
schtasks /Create /SC MINUTE /MO 15 /TN UZHGradeNotifier /TR /path/to/python3 /path/to/script/uzh_grade_notifier/__main__.py
```
If you want to remove the task again:
```
schtasks /delete /tn UZHGradeNotifier /f
```

## Optional command line arguments

To run script use:
```
/path/to/python3 path/to/script/uzh_grade_notifier/__main__.py [--config /path/to/config.json path/to/cache] [--headless]
```
The ```--config``` flag lets you set your own config.json path (config.json must already exist) and the path where your grades-cache should be saved.
The ```--headless``` flag lets you turn desktop notifications off. Useful for servers.

## Contributing

Contributors:

- [quasebaum](https://github.com/quasebaum)
- [twildh](https://github.com/twildh)

Pull requests are welcome!