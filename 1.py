import requests
from bs4 import BeautifulSoup
from asyncio.windows_events import NULL
from base64 import standard_b64decode
# import keyword
import undetected_chromedriver as uc
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.proxy import Proxy, ProxyType
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time
import threading
import pyperclip
import os
import random
import json
import glob
import zipfile
import requests
import smtplib
# import asyncio
from email.mime.text import MIMEText
import tkinter as tk
import re
from bs4 import BeautifulSoup
import pandas as pd
import openpyxl
op = uc.ChromeOptions()

      

custom_user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
       


op.add_argument("--disable-blink-feature=AutomationControlled")
op.add_argument(f'--user-agent={custom_user_agent}')
      
driver = uc.Chrome(options=op)

driver.execute_script(
            "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
driver.maximize_window()


# headers = {
#     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'
# }
# URL of the Indeed search results page for your desired job and location
search_url = "https://fr.indeed.com/jobs?q=python+developer&l=Paris&fromage=1"
driver.get(search_url)
time.sleep(1)


try:
    iframe = WebDriverWait(driver,10).until(EC.presence_of_element_located((By.TAG_NAME, "iframe")))
    driver.switch_to.frame(iframe)
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//input[@type='checkbox']"))).click()
    driver.switch_to.window(driver.window_handles[0])
except: 
    pass
job = []
active_flag = True
driver.get(search_url)

def job_fetch():

    left = WebDriverWait(driver,30).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".jobsearch-LeftPane")))
    # left = driver.find_element(By.CSS_SELECTOR, ".jobsearch-LeftPane")
    data = WebDriverWait(left,10).until(EC.presence_of_all_elements_located((By.TAG_NAME, 'li')))
    for i in data:
        indeedjob = {}

        try:
            # adata= WebDriverWait(i,20).until(EC.presence_of_element_located((By.TAG_NAME, "a")))
            adata = i.find_element(By.TAG_NAME, 'a')
            jobtitle = adata.get_attribute("id")
            print(jobtitle)
            if jobtitle[:3] == "job":
                indeedjob["title"] = adata.text
                indeedjob["job_link"] = adata.get_attribute("href")
                indeedjob["company"] = i.find_element(By.XPATH, ".//span[@class='companyName']").text
                indeedjob["location"]= i.find_element(By.XPATH, ".//div[@class='companyLocation']").text
                try:
                    indeedjob["salary"] = i.find_element(By.XPATH, ".//div[@data-testid='attribute_snippet_testid']").text
                except:
                    indeedjob["salary"] = i.find_element(By.XPATH, ".//span[@class='estimated-salary']").text
                    pass
                tmp_date = i.find_element(By.XPATH, ".//div[@class='heading6 tapItem-gutter result-footer']/span[@class='date']").text
                indeedjob["post_date"] = tmp_date[6:]
                print("title------",indeedjob["title"])
                print("job_link------",indeedjob["job_link"])
                print("company------",indeedjob["company"])
                print("location------",indeedjob["location"])
                print("salary------",indeedjob["salary"])
                print("post_date------",indeedjob["post_date"])
                adata.click()
                right = WebDriverWait(driver,10).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".jobsearch-RightPane")))
                try:
                    r_company_link=''
                    r_company_link = WebDriverWait(right,6).until(EC.presence_of_element_located((By.XPATH, ".//div[@data-testid='inlineHeader-companyName']/span/a"))).get_attribute('href')
                    # rdata = right.find_element(By.XPATH, "//div[@testid='inlineHeader-companyName']/span/a")
                    print("company_link----",r_company_link)
                    indeedjob["company_link"] = r_company_link
                except:
                    pass
                try:
                    tmp_jobdescription_p = WebDriverWait(right,30).until(EC.presence_of_element_located((By.XPATH, ".//div[@id='jobDescriptionText']")))
                    print("ttttt",tmp_jobdescription_p)
                    tmp_jobdescription_ptags = WebDriverWait(tmp_jobdescription_p, 30).until(EC.presence_of_all_elements_located((By.XPATH, ".//*")))
                    tmp_des_text=''
                    for j in tmp_jobdescription_ptags:
                        if j.text:
                            tmp_des_text += j.text
                            print(j.text)
                    indeedjob["job_description"] = tmp_des_text
                except: pass
                job.append(indeedjob)
        except:pass
        time.sleep(.2)
        

    try: 
        next = WebDriverWait(left, 10).until(EC.element_to_be_clickable((By.XPATH, ".//a[@data-testid='pagination-page-next']")))
        next.click()

    except: 
        global active_flag
        
        active_flag = False
        pass
try:
    
    job_fetch()
    while active_flag:
        time.sleep(2)
        job_fetch()
except:
    pass
excel = "job.xlsx"
file = open(excel,"a")
file.close()
df = pd.DataFrame(job)
df.to_excel(excel)
print(df)

input("fff")