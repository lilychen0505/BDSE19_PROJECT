from bs4 import BeautifulSoup
import requests
import sys
sys.path.insert(0,'/usr/lib/chromium-browser/chromedriver')
import re
import random
import time
from selenium import webdriver
#import numpy as np
import pandas as pd

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
wd = webdriver.Chrome('chromedriver',chrome_options=chrome_options)

link_all = []
number = list(range(1,21))
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36'}
for i in range(1,165): #pages
  url = f'https://usedcar.u-car.com.tw/search.aspx?page={i}&keyword=&sorttype=0&sortby=3&during=0&make=0&pricerange=0&bodytype=0'
  wd.get(url)
  time.sleep(2)
  for j in number:
      for link in wd.find_elements_by_xpath(f'//*[@class="list_line"]/div/div[{j}]/a'):
          link_all.append(link.get_attribute('href'))

  print( i, ":  scraped successfully!")

def get_resource(url):
    while True:
        try:
            time.sleep(random.uniform(1, 3))
            r = requests.get(url, headers=headers)
            return r
        except:
            print("requests.get failed, so try again!")
            continue
        break

def parse_html(r):
    if r.status_code == requests.codes.ok:
        r.encoding = 'utf8'
        soup = BeautifulSoup(r.text, 'lxml')
    else:
        print("Http請求錯誤: "+url)
        soup = None
    return soup

df0 = []
df1 = []
df_id=pd.DataFrame(columns=['id'])
df_info=pd.DataFrame(columns=['car_brand', 'car_model', 'car_year', 'car_mileage', 'car_price', 'car_color', 'car_cylinderVolume', 'car_fuel', 'car_gear', 'car_title', 'car_photo', 'dealer_name'])

for i in link_all:
    r = get_resource(i)
    soup = parse_html(r)

    #id
    car_id1 = soup.find_all('div', class_='object_detail_info_2')
    car_id2 = BeautifulSoup(str(car_id1), 'html.parser')
    car_id3 = car_id2.find_all('a')
    car_id = str(car_id3)[32:64]
    #print(car_id)
    df0.append([car_id])
    df_id1 = pd.DataFrame(df0,columns=df_id.columns)

for i in link_all:
    r = get_resource(i)
    soup = parse_html(r)
    #car_brand
    car_brand1 = soup.find_all('p', class_='object_product_title')
    #car_brand2 = BeautifulSoup(str(car_brand1), 'html.parser')
    #car_brand3 = car_brand2.find_all('p')
    for car_brand2 in car_brand1 :
        car_brand2 = car_brand2.text.strip()
    car_brand = car_brand2.split( )[0]
    car_brand = car_brand.upper()
    #print(car_brand)

    #car_model
    car_model1 = soup.find_all('p', class_='object_product_title')
    car_model2 = BeautifulSoup(str(car_model1), 'html.parser')
    #car_model3 = car_model2.find_all('p')
    for car_model2 in car_model1 :
        car_model2 = car_model2.text.strip()
    car_model4 = car_model2.split( )[1:]
    car_model5 = " ".join(car_model4)
    car_model = car_model5.upper()
    #print(car_model)

    #car_year
    car_year1 = soup.find_all('p', class_='object_product_year')
    car_year2 = BeautifulSoup(str(car_year1), 'html.parser')
    for car_year2 in car_year1 :
        car_year = car_year2.text.strip()
        car_year = re.sub('出廠','',car_year)
    #print(car_year)

    #car_mileage
    car_mileage1 = soup.find_all('p', class_='gray_tab_info')
    car_mileage2 = BeautifulSoup(str(car_mileage1), 'html.parser')
    car_mileage3 = car_mileage2.find_all('p')[3]
    car_mileage = car_mileage3.text.strip()
    car_mileage = re.sub('公里','',car_mileage)
    #print(car_mileage)

    #car_price
    car_price1 = soup.find_all('p', class_='price')
    car_price2 = BeautifulSoup(str(car_price1), 'html.parser')
    for car_price2 in car_price1 :
        car_price = car_price2.text.strip()
    #print(car_price)

    #car_color
    car_color1 = soup.find_all('p', class_='gray_tab_info')
    car_color2 = BeautifulSoup(str(car_color1), 'html.parser')
    car_color3 = car_color2.find_all('p')[2]
    car_color = car_color3.text.strip()+'色'
    #print(car_color)
    
    #car_cylinderVolume
    car_cylinderVolume1 = soup.find_all('p', class_='object_product_cc')
    car_cylinderVolume2 = BeautifulSoup(str(car_cylinderVolume1), 'html.parser')
    for car_cylinderVolume2 in car_cylinderVolume1 :
        car_cylinderVolume = car_cylinderVolume2.text.strip()
        car_cylinderVolume = re.sub('c.c.','',car_cylinderVolume)
    #print(car_cylinderVolume)

    #car_fuel
    car_fuel1 = soup.find('p', class_='gray_tab_info')
    car_fuel2 = BeautifulSoup(str(car_fuel1), 'html.parser')
    car_fuel3 = car_fuel2.find_all('p')[0]
    car_fuel = car_fuel3.text.strip()
    #print(car_fuel)

    #car_gear
    car_gear1 = soup.find_all('p', class_='gray_tab_info')
    car_gear2 = BeautifulSoup(str(car_gear1), 'html.parser')
    car_gear3 = car_gear2.find_all('p')[1]
    car_gear = car_gear3.text.strip()
    #print(car_gear)
    
    #car_title
    car_title1 = soup.find_all('p', class_='object_product_info')
    car_title2 = BeautifulSoup(str(car_title1), 'html.parser')
    for car_title2 in car_title1 :
        car_title = car_title2.text.strip()
    #print(car_title)

    #car_photo
    car_photo1 = soup.find_all('div', class_='pic_b_area')
    car_photo2 = BeautifulSoup(str(car_photo1), 'html.parser')
    car_photo3 = car_photo2.find_all('a')
    car_photo = str(car_photo3)[83:-37]
    #print(car_photo)
    
    #dealer_name
    dealer_name1 = soup.find_all('p', class_='info')
    dealer_name2 = BeautifulSoup(str(dealer_name1), 'html.parser')
    dealer_name3 = dealer_name2.find_all('a')[0]
    dealer_name4 = []
    for dealer_name3 in dealer_name1 :
        dealer_name3 = dealer_name3.text.strip()
        dealer_name4.append(str(dealer_name3))
    dealer_name5 = dealer_name4[0]
    dealer_name6 = dealer_name5.split('(')
    dealer_name = dealer_name6[0]
    #print(dealer_name)

    df1.append([car_brand,car_model,car_year,car_mileage,car_price,car_color,car_cylinderVolume,car_fuel,car_gear,car_title,car_photo,dealer_name])
    df_info1 = pd.DataFrame(df1,columns=df_info.columns)
    
equipment_columns = ['ABS防鎖死煞車系統', 'CD音響', '真皮座椅', '衛星導航設備', '天窗', '影音系統', 'HID氣體放電頭燈', '恆溫空調',
                     'Keyless感應門鎖', '安全氣囊', '鋁合金輪圈', '停車雷達系統', '四輪傳動'] 

dfequipment = pd.DataFrame(columns=equipment_columns)

for i in link_all:
  dfequipment1 = pd.DataFrame([list([0]*len(equipment_columns))], columns=equipment_columns)
  r = get_resource(i)
  soup = parse_html(r)
  #equipment
  equipment1 = soup.find_all('div', class_='info_spec info_spec_n')
  equipment2 = soup.find_all('div', class_='info_spec_non info_spec_n')
  tmp = []
  for j in equipment1:
      tmp.append(j.text)
  for k in equipment2:
      tmp.append(k.text)   
      for z in equipment_columns:
          if z in tmp:
              dfequipment1[z] = '0'
          else:
              dfequipment1[z] = '1'
  dfequipment = dfequipment.append(dfequipment1, ignore_index=True)
      
df_temp = pd.concat([df_id1,df_info1,dfequipment],axis=1)

df_temp.to_csv('Ucar_all.csv', encoding='utf_8_sig')