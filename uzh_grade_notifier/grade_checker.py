import json
import logging
import os.path
from datetime import datetime

from bs4 import BeautifulSoup

logger = logging.getLogger()


class NewGrade:
    """Information about a new exam grade of a module"""

    module_id = ""
    module_name = ""
    grade = -1

    def __init__(self, module_id, module_name, grade):
        self.module_id = module_id
        self.module_name = module_name
        self.grade = grade


def update_grades(html_grades, path_cache):
    """Compare the grades on the given HTML page to the cached ones from the last script execution
    and return a list of modules with newly released grades"""

    new_grades = []
    first_execution = False  # True if script is running for the first time (-> no notification)

    # if grades cache file does not exist: create it and remember not to send notification
    if not os.path.exists(path_cache):
        logger.info("No grades-cache.json found, will not send notifications")
        first_execution = True
        # write empty JSON file to disk
        with open(path_cache, "a") as new_json_file:
            json.dump({}, new_json_file)

    # parse HTML of grades page, get all module table rows
    logger.info("Parsing modules with grades from website and comparing them to the cache")
    soup_grades = BeautifulSoup(html_grades, "html.parser")
    table_rows = soup_grades.findAll("tr", attrs={"style": "font-size: 80%;"})

    # read cached module information from JSON file
    with open(path_cache, "r+") as json_grades_cache:
        grades_cache = json.load(json_grades_cache)

        # go through and filter table rows to get modules with grades, compare to modules in cache
        # file to find out which grades are new
        for row in table_rows:
            # read module information and grade
            row_cells = row.findAll("td")
            module_id = row_cells[0].text.strip()
            grade = row_cells[9].text.strip()

            # ignore non-module rows and modules without grades
            # "".join(x.split()) removes all whitespace characters (spaces, tabs, newlines, etc.)
            if not "".join(module_id.split()) == "" and not "".join(grade.split()) == "":
                module_name = row_cells[2].text.strip()
                booking_date = row_cells[4].text.strip()[0:10]

                # module is not in cache: new grade
                if module_id not in grades_cache:
                    logger.info("New grade found for module '" + module_name + "'")
                    # add information about new grade to new_grades list
                    new_grades.append(NewGrade(module_id, module_name, grade))
                    # update cache
                    grades_cache[module_id] = booking_date

                # module is already in cache
                else:
                    booking_date_html = datetime.strptime(booking_date, "%d.%m.%Y")
                    booking_date_cache = datetime.strptime(grades_cache[module_id], "%d.%m.%Y")

                    # if booking date on HTML page is more recent than cached one: new grade
                    if booking_date_html > booking_date_cache:
                        logger.info("New grade found for module '" + module_name + "'")
                        # add information about new grade to new_grades list
                        new_grades.append(NewGrade(module_id, module_name, grade))
                        # update cache
                        grades_cache[module_id] = booking_date

        # write updated cache to JSON file
        json_grades_cache.seek(0)
        json.dump(grades_cache, json_grades_cache)

    # return list of new grades (unless script has been executed for the first time)
    if first_execution:
        return []
    else:
        return new_grades
