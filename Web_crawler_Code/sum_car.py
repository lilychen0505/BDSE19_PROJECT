import requests
from bs4 import BeautifulSoup
import numpy as np
import pandas as pd
import sys
import re
import time


class exc(Exception):
    def __init__(self, i):
        self.i = i

    def __str__(self):
        return f'自定義例外:{self.i}'


def get_html(url, headers):
    num_retry = 0  # 設定初始重試次數
    max_retry = 3  # 最大重試次數3次
    try:
        while num_retry <= max_retry:
            r = requests.get(url, headers=headers)
            if r.status_code == requests.codes.ok:  # 是否成功請求網頁
                print('request success: %s' % url)
                return r
            else:
                time.sleep(3)
                if num_retry == max_retry:  # 當重試三次後丟出錯誤
                    raise exc(url)
                print('retrying request')
                num_retry += 1
    except exc:
        print(exc)
        # 超過請求次數印出 http request eror 並將錯誤丟出function外
        print('http request error: %s' % url)
        raise
    except:
        # 出現意料之外的錯誤時印出錯誤並將錯誤丟出function外
        print('Unexcepted error: %s' % url, sys.exc_info())
        raise


def parse_html(r):
    soup = BeautifulSoup(r.text, 'lxml')
    if soup != None:
        print('parsing success')  # 印出成功解析網頁名
        return soup
    else:
        # 當beautifulsoup解析失敗為Nonetype時，將錯誤丟出function外
        raise Exception('parse_error')


def equipment_crawl(soup):

    list1 = []

    equ1 = soup1.find(class_='buyCarDetailContentSpec').find_all('li')

    for x in equ1:
        list1.append(x.text.strip())

    list2 = list1[:-6]

    arr = np.array(list2)

    dfequ = pd.DataFrame(
        np.zeros(shape=(1, len(list2)), dtype=int), columns=arr)
    for y in equ1[:-6]:
        try:
            e = y.text.strip()
            class_type = None
            class_type = y.get('class')[0]
            if class_type == 'specChecked':
                dfequ[e] = 1
        except IndexError:
            continue

    return dfequ


def dealer_address_crawl(soup):
    try:
        dealer_info = soup1.find(
            'div', class_='buyCarDetailContentDealerContact').find_all('p')
        dealer_address = None
        for p in dealer_info:
            address = re.search('地址', p.text)
            if address:
                dealer_address = p.text.split('：')[1].strip()
                return dealer_address
    except:
        print('dealer_address parse error')
        return None


def verified_crawl(soup):
    carVerified = soup1.find(
        'div', class_='buyCarDetailTitleTextBadge').find_all('li')

    dfver = pd.DataFrame(np.zeros(shape=(1, 5), dtype=int), columns=[
                         '三大保證', '非計程車', '四大保固', '里程保證', 'YES認證'])

    for x in carVerified:
        v = x.text.strip()
        class_type = None

        try:
            class_type = x.get('class')[1]
            if class_type == 'carConditionActive':
                dfver[v] = 1
        except IndexError:
            continue

    return dfver


df1 = pd.DataFrame(columns=['id', 'car_brand', 'car_model', 'car_address', 'car_title', 'dealer_name'])

for page in range(1, 4):

    sum_url = f'https://www.sum.com.tw/carsearchlist.php?v=3&ctp_prt=&price1=0&price2=220&yearrange=&cararea=&carregion=&cartype=&carcolor=&brand=&model=&year1=&year2=&doors=&q=&show_type=&carrecommend=&comp_goldstore=&discount=&cc1=&cc2=&protection=&carvr=&page=&sort=&sortpage1=&gclid=&priceRange1=&priceRange2=&wd=&_de=0.5690229095899482&page={page}'

    headers = {
        'Host': 'www.sum.com.tw',
        'Connection': 'keep-alive',
        'Accept': 'text/plain, */*; q=0.01',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.106 Safari/537.36',
        'Cookie': 'PHPSESSID=qn203skntjuv8bkevorgrhg5g7; _gcl_au=1.1.1197458183.1624031200; _ga=GA1.3.849228594.1624031200; __auc=38660c2a17a1fcd839cb333ad40; _hjTLDTest=1; _hjid=13961593-1974-490c-8e9b-f0726e39cde0; _fbp=fb.2.1624031200855.1701953032; _gid=GA1.3.966926215.1624256678; _TUCI_T=sessionNumber+18799&pageView+18799; Tagtoo_pta=pta_03+_&lta+_tm^3Ad1056_; __asc=c83520af17a2d7bcacaaa8c8958; _TUCS=1; _TUCI=sessionNumber+2498&ECId+155&hostname+www.sum.com.tw&pageView+7493',
    }
    try:
        soup = parse_html(get_html(sum_url, headers=headers))
    except:
        print('HTTP_error')
        print(sys.exc_info())
        continue

    seo_list = soup.find_all('li', class_='seo_list')
    list1 = []

    for li in seo_list:

        idnum = li.get('data-seo_name')

        car_info = li.find('h3').a.text.split('｜')

        car_brand = car_info[0].split(' ', 1)[0]

        car_model = car_info[0].split(' ', 1)[1]

        car_address = li.find('ul').find_next_sibling().find('li').text

        car_title = li.find('div', class_='carCondition').h3.text.strip()

        car_dealer = li.find('ul').find_next_sibling().find(
            'li').find_next_sibling().text

        df1 = df1.append({'id': idnum, 'car_brand': car_brand, 'car_model': car_model,
                          'car_address': car_address, 'car_title': car_title, 'dealer_name': car_dealer}, ignore_index=True)

df1.to_csv('sum_car_first.csv', encoding = 'utf-8-sig')

df_xxx = pd.DataFrame()

for id_nu in df1['id']:
    url_in = f'https://www.sum.com.tw/carinfo-{id_nu}.php'
    print('-----------------------------start parsing new page---------------------------------')
    headers = {
        'Host': 'www.sum.com.tw',
        'Connection': 'keep-alive',
        'Accept': 'text/plain, */*; q=0.01',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.106 Safari/537.36',
        'Cookie': 'PHPSESSID=qn203skntjuv8bkevorgrhg5g7; _gcl_au=1.1.1197458183.1624031200; _ga=GA1.3.849228594.1624031200; __auc=38660c2a17a1fcd839cb333ad40; _hjTLDTest=1; _hjid=13961593-1974-490c-8e9b-f0726e39cde0; _fbp=fb.2.1624031200855.1701953032; _gid=GA1.3.966926215.1624256678; _TUCI_T=sessionNumber+18799&pageView+18799; Tagtoo_pta=pta_03+_&lta+_tm^3Ad1056_; __asc=c83520af17a2d7bcacaaa8c8958; _TUCS=1; _TUCI=sessionNumber+2498&ECId+155&hostname+www.sum.com.tw&pageView+7493',
    }

    try:
        soup1 = parse_html(get_html(url_in, headers=headers))
    except:
        print('HTTP_error')
        print(sys.exc_info())
        continue
    try:
        carPrice = soup1.find('div', class_='buyCarDetailTitleTextPrice')
        car_price = carPrice.find('b').text
    except:
        print(f'car_price parsing error:{id_nu}')
        car_price =  None
        pass

    dfver = verified_crawl(soup1)

    carDetail = soup1.find('div', class_='buyCarDetailTitleTextContent')

    photo_url = soup1.find('div', class_='buyCarDetailTitleImg').text

    info = carDetail.div.find_next_siblings()

    info_list = []
    
    try:
        for sp in info:
            info_list.append(sp.span.text.strip())
    except:
        pass

    dealer_address = dealer_address_crawl(soup1)

    dfequ = equipment_crawl(soup1)

    car_year = info_list[0]

    car_cylinderVolumn = info_list[1]

    car_color = info_list[2]

    car_gearType = info_list[3]

    car_driveMode = info_list[4]

    car_fuel = info_list[5]

    car_mileage = info_list[6]

    car_door = info_list[7]

    car_seat = info_list[8]

    df2 = pd.DataFrame(columns=['id', 'car_mileage', 'car_year', 'car_price', 'car_cylinderVolumn', 'car_color', 'car_gearType',
                                'car_dirveMode', 'car_fuel', 'car_door', 'car_seat', 'dealer_address'])
    
    df2 = df2.append({'id': id_nu, 'car_mileage': car_mileage, 'car_year': car_year, 'car_price': car_price,
                      'car_cylinderVolumn': car_cylinderVolumn, 'car_color': car_color, 'car_gearType': car_gearType,
                      'car_dirveMode': car_driveMode, 'car_fuel': car_fuel, 'car_door': car_door, 'car_seat': car_seat, 'dealer_address': dealer_address}, ignore_index=True)

    df_temp = pd.concat([df2, dfequ, dfver], axis=1)
    
    df_xxx = df_xxx.append(df_temp)

df_final = df1.merge(df_xxx, on='id')

df_final.to_csv('Sum_car_0707.csv', encoding='utf-8-sig')

