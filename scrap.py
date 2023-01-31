from bs4 import BeautifulSoup
import requests
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import lxml
import csv


url = 'http://result.neaea.gov.et/'


def getStudentInfo(url, studentId):
    for _ in range(10):
        browser.get(url)
        time.sleep(1)
        try:
            search = browser.find_element_by_name('Registration_Number')
            search.send_keys(studentId)
            print(studentId)

            time.sleep(1)
            search.send_keys(Keys.RETURN)
            time.sleep(3)
            break
        except:
            continue
    return browser.page_source


def saveParsedDataToCsv(response):
    response = BeautifulSoup(response, 'lxml')
    stre = response.find('div', class_="ml-sm-auto mt-2 mt-sm-0")
    if stre.text in ['Natural Science', 'Social Science']:
        try:
            resultCard = response.find_all('td')
            name = response.find('h6', class_="font-weight-semibold")
            m = [resultCard[y].text for y in range(0, len(resultCard), 2)]
            s = [resultCard[y].text for y in range(1, len(resultCard), 2)]
            g = dict(zip(m, s))
            c = sum(map(int, s))
            o = (int(s[m.index('Civics')]))
            t = {"#": name.text, studentId: g, 'SUM': f"{c} |--| {   c -  o  }",
                 'SUM_ALL': c, "stream": stre.text}
            with open("test_enzi.txt", 'a+', encoding='utf-8') as f:
                f.write(f"{t},\n")

            # print(t)
            # print(len(lop))
        except:
            with open("empty.txt", 'a+', encoding='utf-8') as f:
                f.write(f"{studentId},\n")
    else:
        with open("tmi.txt", 'a+', encoding='utf-8') as f:
            f.write(f"{studentId},\n")


for _ in range(10):
    res = requests.get(url)
    print(_)
    if res.status_code == 200:
        break

if res.status_code != 200:
    print("Dude the service is unavailable, Please try again!")
else:

    for studentId in range(696510, 696810):
        browser = webdriver.Firefox(
            executable_path="/home/d3mah/Downloads/Compressed/geckodriver-v0.30.0-linux64/geckodriver")

        response = getStudentInfo(url, str(studentId))
        browser.close()
        try:
            saveParsedDataToCsv(response)
        except:

            while 1:
                browser = webdriver.Firefox(
                    executable_path="/home/d3mah/Downloads/Compressed/geckodriver-v0.30.0-linux64/geckodriver")
                response = getStudentInfo(url, str(studentId))
                browser.close()
                try:
                    saveParsedDataToCsv(response)
                    break
                except:
                    continue
