import time

import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException
from requests_html import HTMLSession
from selenium import webdriver

url = "https://www.indeed.com/jobs?q=developer&l=Los+Angeles&from=searchOnHP&vjk=89eb443ee8b65264"
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.get(url)
time.sleep(20)

container_contents = driver.find_elements(By.CLASS_NAME, 'mosaic-zone')
jobList = []
companyList = []
locationList = []
payList = []

while True:
    for i in range(1, len(container_contents) - 2):
        if i == 5:
            continue
        if i == 6:
            continue
        if i == 7:
            continue
        try:
            job = driver.find_element(By.XPATH, '/html/body/main/div/div[1]/div/div[5]/div[1]/div[5]/div/ul/li[{}]/div/div[1]/div/div[1]/div/table[1]/tbody/tr/td/div[1]/h2/a/span'.format(i)).text

            if driver.find_element(By.XPATH, '/html/body/main/div/div[1]/div/div[5]/div[1]/div[5]/div/ul/li[{}]/div/div[1]/div/div[1]/div/table[1]/tbody/tr/td/div[2]/div/span'.format(i)) is None:
                company = driver.find_element(By.XPATH, '/html/body/main/div/div[1]/div/div[5]/div[1]/div[5]/div/ul/li[{}]/div/div[1]/div/div[1]/div/table[1]/tbody/tr/td/div[2]/div[2]/span[1]'.format(i)).text
            else:
                company = driver.find_element(By.XPATH, '/html/body/main/div/div[1]/div/div[5]/div[1]/div[5]/div/ul/li[{}]/div/div[1]/div/div[1]/div/table[1]/tbody/tr/td/div[2]/div/span'.format(i)).text

            if driver.find_element(By.XPATH, '/html/body/main/div/div[1]/div/div[5]/div[1]/div[5]/div/ul/li[{}]/div/div[1]/div/div[1]/div/table[1]/tbody/tr/td/div[2]/div/div'.format(i)) is None:
                location = driver.find_element(By.XPATH, '/html/body/main/div/div[1]/div/div[5]/div[1]/div[5]/div/ul/li[1]/div/div[1]/div/div[1]/div/table[1]/tbody/tr/td/div[2]/div[2]/div'.format(i)).text
            else:
                location = driver.find_element(By.XPATH, '/html/body/main/div/div[1]/div/div[5]/div[1]/div[5]/div/ul/li[{}]/div/div[1]/div/div[1]/div/table[1]/tbody/tr/td/div[2]/div/div'.format(i)).text

            pay = driver.find_element(By.XPATH, '/html/body/main/div/div[1]/div/div[5]/div[1]/div[5]/div/ul/li[{}]/div/div[1]/div/div[1]/div/table[1]/tbody/tr/td/div[3]/div[1]'.format(i)).text

            jobList.append(job)
            companyList.append(company)
            locationList.append(location)
            payList.append(pay)

            print("{} / {} / {} / {}".format(job, company, location, pay))
        except NoSuchElementException:
            continue

    print("=============================================================")
    try:
        nextButton = driver.find_element(By.XPATH, "/html/body/main/div/div[1]/div/div[5]/div[1]/nav/ul/li[6]/a")
        nextButton.click()
    except NoSuchElementException:
        break

data = {"job": jobList, "company": companyList, "location": locationList, "pay": payList}
df = pd.DataFrame(data)
print(df.head(5))

df.to_csv("irvine-hw1.csv", encoding = "utf-8-sig")

