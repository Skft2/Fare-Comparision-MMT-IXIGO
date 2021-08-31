import time
import mysql.connector as connection
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait as WD
from selenium.webdriver.support import expected_conditions as EC
import json
import requests
import pandas as pd 
import PySimpleGUI as sg
import os
from datetime import datetime
import numpy as np
import matplotlib.pyplot as plt

currentDay = datetime.now().day
currentMonth = datetime.now().month
currentYear = datetime.now().year
con = connection.connect(host='127.0.0.1',user='root',passwd='Oriental1',database='Flight',use_pure=True)
cur = con.cursor()
cur.execute('SELECT kinter from codes ORDER BY kinter ASC')
res = cur.fetchall()

from_t = []

for i in res:
    from_t.append(i[0])

sg.theme('DarkAmber')   # Add a touch of color
# All the stuff inside your window.
layout = [  [sg.Text('Flight fare comparision',size=(20,1),font=('century', 24))],
            [sg.Text('From',size=(5,1),font=('century', 16))],
            [sg.Combo(values=from_t,size=(42,30),enable_events=True, key='combo')],
            [sg.Text('To',size=(5,1),font=('century',16))],
            [sg.Combo(values=from_t,size=(42,30),enable_events=True, key='combo_1')],
            [sg.Text('Date(dd/mm/yyyy)',size=(14,1),font=('century',16)), sg.InputText(size=(16,1))],
            [sg.Button('Search')]]


# Create the Window
window = sg.Window('FFC', layout)
# Event Loop to process "events" and get the "values" of the inputs
while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'Cancel': # if user closes window or clicks cancel
        break
   
    if event == 'Search':
        c = values['combo']
        c = c.split(' ')[1]
        
        d = values['combo_1']
        d = d.split(' ')[1]
        if str(c) == str(d):
            pop = sg.PopupError('From & To cannot be same', title='Warning')
        else:
            pass
        try:
            a = datetime.strptime(values[0],"%d/%m/%Y")
            print(type(a))
            if a.day < int(currentDay) and a.month <= int(currentMonth) and a.year <= int(currentYear):
                popo = sg.PopupError('You cannot select past date', title='Warning')
        except ValueError as e:
            popo = sg.PopupError(e, title='Warning')
        window.close()

ts = int(time.time())

fro = c
to = d
day = a.day
month = a.month
year = a.year
data = []
when_mmt = f'{year}{month}{day}'

when_ixi = f'{day}{month}{year}'

def mmt():
  
  ts = int(time.time())
  url = f"https://flights-cb.makemytrip.com/api/search?pfm=PWA&lob=B2C&crId=4cd290d3-ac6a-492f-b8a2-a408cbb77ecb&cur=INR&lcl=en&shd=true&cc=E&pax=A-1_C-0_I-0&it={fro}-{to}-{when_mmt}&forwardFlowRequired=true&apiTimeStamp='{ts}'&region=in&currency=inr&language=eng"


  headers = {
    'Connection': 'keep-alive',
    'sec-ch-ua': '"Chromium";v="92", " Not A;Brand";v="99", "Google Chrome";v="92"',
    'src': 'mmt',
    'mcid': '59496871-b180-489c-a5e7-03aed9a3df43',
    'app-ver': '8.0.0',
    'lob': 'B2C',
    'pfm': 'PWA',
    'device-id': '59496871-b180-489c-a5e7-03aed9a3df43',
    'os': 'Android',
    'ab': '{"WCM":0,"REUSABLE":0,"INSGHT":0,"PCRDF":0,"PFA":1,"OTP":0,"mnthn":false,"CLS":1,"PFI":1,"ZC_Server_Side_experiment1":1,"CHMRK":0,"BFFL":0,"MMTFF":0,"FSA":1,"PFL":0,"BSG":0,"LFT":0,"PWA":1,"PFP":1,"DDDF":0,"mema":0,"MFEP":0,"LISTN":1,"DGF":0,"flightInfoOptionSequenceKey":"FNO","CABS":1,"FCN":false,"DGT":3,"SED":0,"ZCA":0,"SEM":0,"ZCE":1,"CABF":1,"travellerScan":0,"NTD":0,"NLA":0,"FLK":1,"dgi":1,"IRR":1,"RTM":1,"ZCS":1,"SNH":0,"FLS":1,"LPS":0,"FFBEN":0,"mal":1,"SFN":0,"mgsf":0,"ZC_Client_Side_exp":false,"NUG":1,"ALTFLT":0,"FUS":1,"COU":0,"USF":0,"MCC":1,"ALTFLTCORP":0,"BAGR":1,"SOR":0,"msa":1,"ALF":1,"MCS":0,"REUSABLERT":0,"PRB":0,"msf":0,"PRE":2,"mbrta":0,"PRG":0,"SPA":0,"pwa_login_type":0,"NDAST":0,"cnpn":1,"ITT":1,"PRO":0,"FLKT":0,"PBC":0,"AMD":0,"AME":0,"SHR":0,"IMB":0,"CYT":0,"CID":1,"bottomsheet_onetap_pwa":"1","BNTD":1,"mras":1,"mbrt":0,"TSC":0,"trvlr":true,"CAD":1,"bntdp":0,"IMS":0,"INSBTM":0,"UMF":1,"mbit":0,"mdl":1,"DTD":0,"ANC":0,"SIM":0,"PTA":0,"HLD":0,"ANP":1,"PTF":0,"ALTF":0,"cheaperFlightsDesktopDom":1,"ANU":0,"MFA":0,"MFD":0,"MFC":1,"INT":1,"PLK":1,"MFEA":0,"MFI":0,"LLS":0,"PDF":0,"AOA":0,"SRT":1,"MFMD":1,"BIRT":0,"PLS":1,"AOD":0,"MFP":0,"IFS":0,"flightPageLoadTracking":0,"NHP":0,"MFEI":0,"GSF":0,"AOI":0,"MFED":0,"msfn":0,"QFT":1,"MOB":0,"AOP":0,"BAA":0,"AGGRNEW":1,"BII":0,"INSTP":0,"ADDONM":0,"FAA":0,"MFTD":0,"BAN":0,"CANCT":0,"INSNEW":0,"GYOLO":0,"APD":0,"FAO":0,"marc":0,"FAT":0,"PET":0,"EMI":0,"BRB":0,"RNP":4}',
    'currency': 'inr',
    'x-user-rc': 'MUMBAI',
    'x-user-ip': '115.96.219.231',
    'domain': 'in',
    'sec-ch-ua-mobile': '?1',
    'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Mobile Safari/537.36',
    'region': 'in',
    'Accept': 'application/json',
    'x-user-cc': 'IN',
    'language': 'eng',
    'Origin': 'https://www.makemytrip.com',
    'Sec-Fetch-Site': 'same-site',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Dest': 'empty',
    'Referer': 'https://www.makemytrip.com/',
    'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8',
    'Cookie': '_abck=654C4FD8E2C711A801354537CC533ACC~-1~YAAQUN/aF1ULnrB6AQAAdQHRRQaLt2w9ZBolDoPp34gdom9eBnOLqdVapfrrIZYCytUvGbbnFqq5ut6E66d0NMrKKrf+FX3i1focAEeYdYWiOqB+HdPveF5f+HOJjWucCpKW/PklfBUm75xjMZfGzkV50toVjeOSZQm16t4GxfMz4JS6VGR/xLTdB6dTr8EGoT8p+7ZU0kneCXWoQ7FhilRNjTgU+4engfPObRRf62n3IWnhV0+DiWYymBlK6s3YBUOP5RVv2xkoIjMu7UCqhFNo3boBKwPBcoAD/4w1GYR9UjBtrMKULURnYd0IxW//3PtsDA0PzBOkdGpY0CqVF/xyu3q05f04bXEqFAsvEMXHKaSehQfGVl0edcZ15kcFKQ==~-1~-1~-1; bm_sz=B483238C650B2F179A48013EB55773C6~YAAQUN/aF1YLnrB6AQAAdQHRRQxTlcPukMdgxIsSvzFd0bpAHnnS5ZHXaH0ko+cMQe3F5BVxr15Pjbp/XExKN5w7W2v/8rZFAl2Jpc0XKx9QN/Kx3tIcvHA7DS7ru4Otc/KXKYt4HPU7PnLOQRWGo0ohZviqCOTafsv9hu5eIGDTO7Mp4QR3qQ/+EVDPzosrug2JLooQ+fdd9t7WxJmKygSGFT9EQ3Me/a+yTuMKSHvQHkVyc1rhOldG9NmrXaZ820S5XyOGVvx7ZDHT6umtYTvMKEp5hCij6B0i7qsS0Up0gLpXgw6Z~3355448~4535092'
  }

  response = requests.get(url, headers=headers)


  a = response.json()
  titles = a['cardList'][0]

  for title in titles:
    cv = title['journeyKeys'][0]
    price = title['fare']  

    rkey = title['rKey']  
    r = requests.get(f'https://flights-cb.makemytrip.com/api/search-dtl?rKey={rkey}&crId=dbeff0ae-79ef-43b8-a62f-ca6f051b161c&apiTimeStamp={ts}&region=in&currency=inr&language=eng', headers=headers)
    s = r.json()
    leg = s['journeyList'][0]['legList']
    for item in range(len(leg)):
      if len(leg) == 1:
        arr_city_1 = leg[item]['arrival']['city']
        arr_date_1 = leg[item]['arrival']['date']
        arr_time_1 = leg[item]['arrival']['time']
        arr_day = arr_date_1.split(',')[0]
        arr_date_1 = arr_date_1.split(',')[1]

        dep_city_1 = leg[item]['depart']['city']
        dep_date_1 = leg[item]['depart']['date']
        dep_time_1 = leg[item]['depart']['time']
        dep_day = dep_date_1.split(',')[0]
        dep_date_1 = dep_date_1.split(',')[1]

        dur_1 = leg[item]['duration']
        head = leg[0]['airlineHeading']
        Airline_name = head.split('b>')[1].split(' |')[0]
        Airline_code = head.split('l>')[1].split('</')[0]
        mydata = {
          'Airline': Airline_name,
          'Flt_no': Airline_code,
          'Dept date': dep_date_1,
          'Dept day': dep_day,
          'Dept time': dep_time_1,
          'Origin': dep_city_1,
          'Arr date': arr_date_1,
          'Arr day': arr_day,
          'Arr time': arr_time_1,
          'arr_city_1': arr_city_1,
          'Destination': dur_1,
          'Fare': price
        }
        
        data.append(mydata)
        df = pd.DataFrame(data)
        df.to_excel(f'{fro}-{to}-{day}{month}{year}mmt.xlsx',index=False,encoding='UTF-8')

def ixigo():
    

    driver =webdriver.Chrome(r'C:\Program Files\chromedriver.exe')
    driver.maximize_window()
    url = f'https://www.ixigo.com/search/result/flight?stops=0&from={fro}&to={to}&date={when_ixi}&returnDate=&adults=1&children=0&infants=0&class=e&source=Search%20Form'
    driver.get(url)
    print(driver.title)
    time.sleep(60)

    # no_stop = driver.find_element_by_xpath('//span[@class="checkbox-button u-pos-rel u-v-align-top u-ib selected"]')
    # no_stop.click()
    # time.sleep(3)

    #For flight numner
    global flt_no
    global air_name
    global dept_date
    global fare
    global duration
    global arr_city
    global arr_time
    global arr_day
    global arr_date
    global dept_city
    global dept_time
    global dept_day

    def dataa():
        a = driver.find_elements_by_xpath('//div[@class="u-text-ellipsis"]/div')
        
        
        for i in a:
            flt_no.append(i.text.split(',')[0])

        #For airline name

        b = driver.find_elements_by_xpath('//a[@class="flight-name"]/div')
        
        
        for i in b:
            air_name.append(i.text)

        #For dept date

        c = driver.find_elements_by_xpath('//div[@class="left-wing"]/div[@class="date"]')
        
        
        for i in c:
            dept_date.append(i.text.split(', ')[1])

        #for dept day
        cd = driver.find_elements_by_xpath('//div[@class="left-wing"]/div[@class="date"]')

        
        
        for i in cd:
            dept_day.append(i.text.split(',')[0])

        #For dept time

        d = driver.find_elements_by_xpath('//div[@class="left-wing"]/div[@class="time"]')
        
        for i in d:
            dept_time.append(i.text)
        #for detp city

        e = driver.find_elements_by_xpath('//div[@class="left-wing"]/div[@class="city u-text-ellipsis"]')
        
        for i in e:
            dept_city.append(i.text)

        #for arr date

        f = driver.find_elements_by_xpath('//div[@class="right-wing"]/div[@class="date"]')
        
        for i in f:
            arr_date.append(i.text)

        #for arr day
        fg = driver.find_elements_by_xpath('//div[@class="right-wing"]/div[@class="date"]')

        
        for i in fg:
            arr_day.append(i.text.split(',')[0])

        #for arr time

        g = driver.find_elements_by_xpath('//div[@class="right-wing"]/div[@class="time"]')
        
        for i in g:
            arr_time.append(i.text)

        #for arr city
        h = driver.find_elements_by_xpath('//div[@class="right-wing"]/div[@class="city u-text-ellipsis"]')
        
        for i in h:
            arr_city.append(i.text)
        #for duration

        j = driver.find_elements_by_xpath('//div[@class="c-timeline-wrapper horizontal"]/div[@class="label tl "]')
        
        for i in j:
            duration.append(i.text)
        #for fare

        k = driver.find_elements_by_xpath('//div[@class="price-section"]//span[@class=""]')
        
        for i in k:
            fare.append(i.text)

    flt_no = []
    air_name = []
    dept_date = []
    dept_day = []
    dept_time = []
    dept_city = []
    arr_date = []
    arr_day = []
    arr_time = []
    arr_city = []
    duration = []
    fare = []

    dataa()
    time.sleep(10)


    page = driver.find_elements_by_xpath('//span[@class="page-num"]')

    for i in page:
        i.click()
        dataa()
        time.sleep(10)


    #print(dept_date,'\n',dept_day,'\n',arr_date,'\n',arr_day)
    driver.quit()
    df = pd.DataFrame()

    df['Airline'] = air_name[0:]
    df['Flt_no'] = flt_no[0:]
    df['Dept date'] = dept_date[0:]
    df['Dept day'] = dept_day[0:]
    df['Dept time'] = dept_time[0:]
    df['Origin'] = dept_city[0:]
    df['Arr date'] = arr_date[0:]
    df['Arr day'] = arr_day[0:]
    df['Arr time'] = arr_time[0:]
    df['Destination'] = arr_city[0:]
    df['Duration'] = duration[0:]
    df['Fare'] = fare[0:]
    
    df.to_excel(f'{fro}-{to}-{day}{month}{year}ixigo.xlsx',index=False,encoding='UTF-8')

mmt()
ixigo()

df_mmt = pd.read_excel(f'{fro}-{to}-{day}{month}{year}mmt.xlsx')
df_ixi = pd.read_excel(f'{fro}-{to}-{day}{month}{year}ixigo.xlsx')

data = df_mmt.join(df_ixi,lsuffix='_mmt',rsuffix='_ixi')

xyz = data.to_excel(f'Data-{fro}-{to}-{day}{month}{year}.xlsx',index=False,encoding='UTF-8')


os.remove(f'{fro}-{to}-{day}{month}{year}mmt.xlsx')
os.remove(f'{fro}-{to}-{day}{month}{year}ixigo.xlsx')

data_1 = pd.read_excel(f'Data-{fro}-{to}-{day}{month}{year}.xlsx')

data_set = pd.DataFrame(data_1[['Flt_no_mmt','Fare_mmt','Fare_ixi']])
x = data_set['Flt_no_mmt']
y = data_set['Fare_mmt']
z = data_set['Fare_mmt']

axixx = np.arange(len(x))
plt.bar(axixx- 0.1, y, 0.20, label = 'Fare mmt')
plt.bar(axixx + 0.1, z, 0.20, label = 'Fare ixi')

plt.xticks(axixx, x)
plt.xlabel("Flights")
plt.ylabel("Fares")
plt.title("Fare comparision")
plt.legend()
plt.show()

