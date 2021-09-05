import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait as WD
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd
from datetime import datetime



currentDay = datetime.now()
a = str(currentDay)
b = a.split(':')[0]
c =a.split(':')[1]
driver =webdriver.Chrome(r'C:\Program Files\chromedriver.exe')
driver.maximize_window()
stocks = ['Uflex','Tata steel','Tata motors','HUL','ITC','Prestige estate','l and t tech','Shriram city union','TCS','India bull']

b_stocks = []
ecel = []


for i in stocks:
    url = f'https://www.google.com/search?q={i}+share+price'
    driver.get(url)
    time.sleep(2)
    cmp = driver.find_element_by_xpath('//span[@jsname="vWLAgc"]')
    name = driver.find_element_by_xpath('//div[@class="oPhL2e"]')

    data = driver.find_elements_by_xpath('//td[@class="iyjjgb"]')

    ecel_1 = {'Company name':name.text,
    'current price':cmp.text,
    'Open':data[0].text,
    'High':data[1].text,
    'Low':data[2].text,
    'Mkt cap':data[3].text,
    'P/E ratio':data[4].text,
    'Div yeild':data[5].text,
    'prev close':data[6].text,
    '52 wk high':data[7].text,
    '52 wk low':data[8].text
    }
    ecel.append(ecel_1)
    df = pd.DataFrame(ecel)
    df.to_excel(f'MY Stock data {b}-{c}.xlsx',index=False,encoding='UTF-8')

driver.quit()
