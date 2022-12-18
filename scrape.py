import requests
from bs4 import BeautifulSoup
import re
import array
from collections import defaultdict

def getCourseCodes(periode):
    URL = "https://natfak.sdu.dk/laeseplan/kurser.php?periode="+ periode +"&lang=da&institutid=alle&phd="
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, "html.parser")
    results = soup.find(id="viskursusinfo")
    coursecodes = results.find_all("tr")
    coursecodes_arr = []
    for coursecode_element in coursecodes:
        course = coursecode_element.text
        match_course = re.search("[a-åA-Å]*\d[0-9]*", course)
        if not match_course:
            continue
        coursecodes_arr.append(course[0:match_course.end()])
    return coursecodes_arr


def getPageContent(courseCode):
    URL = "https://odin.sdu.dk/sitecore/index.php?a=searchfagbesk&internkode=" + courseCode + "&lang=da"
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, "html.parser")
    match = re.search("Der kunne ikke findes en fagbeskrivelse", soup.text.strip())
    if match:
        URL = "https://odin.sdu.dk/sitecore/index.php?a=searchfagbesk&internkode=" + courseCode + " " +"&lang=da"
        page = requests.get(URL)
        soup = BeautifulSoup(page.content, "html.parser")
    return soup

#Web scraping the title of the course
def title(soup):
    results = soup.find(id="page-title")

    title_elements = results.find("h1")

    return title_elements.text

#Udbudsterminer
def termin(soup):
    results = soup.find(id="main-container")

    termin_elements = results.find("div", class_="pull-left")

    termin1 = termin_elements.find_all('div')[6:7]

    termin2 = termin1[0]

    return termin2.text.strip()

#Indgangskrav
def indgangskrav(soup):
    result = soup.find(id="main-container")

    indgang_elements = result.find_all("div", class_="panel-body")[1].text

    match_indgang = re.search("Indgangskrav", indgang_elements)

    match_fag = re.search("Faglige forudsætninger", indgang_elements)

    if not match_indgang:
        return "Ingen"

    x = match_indgang.end() + 1
    y = match_fag.start()

    return indgang_elements[x:y]

#ECTS
def ects(soup):
    results = soup.find(id="main-container")

    ects_elements = results.find("div", class_="pull-right text-right")

    ects = ects_elements.find_all('div')[1:2]

    ects1 = ects[0].text.strip()

    match = re.search("ECTS-point:", ects1)

    x = match.end() + 1
    y = len(ects1)

    return ects1[x:y]

#Eksamen
def eksamen(soup):
    result = soup.find(id="main-container")

    eksamen_elements = result.find_all("div", class_="panel-body")[1].text

    match_eksamen = re.search("Mundtlig eksamen", eksamen_elements)

    if match_eksamen:
        return match_eksamen.group()
    else:
        return "Ingen mundtlig eksamen"


