import requests
import numpy as np
import pandas as pd
from pprint import pprint
from bs4 import BeautifulSoup
import time
import sys
import re


class exc(Exception):
    def __init__(self, i):
        self.i = i

    def __str__(self):
        return f'自定義例外:{self.i}'


def get_api(url, headers):
    num_retry = 0  # 設定初始重試次數
    max_retry = 3  # 最大重試次數03次
    try:
        while num_retry <= max_retry:
            r = requests.get(url, headers=headers)
            if r.status_code == requests.codes.ok:  # 是否成功請求網頁
                print('request success: %s' % url)
                return r
            else:
                time.sleep(3)
                if num_retry == max_retry:  # 當重試三次後丟出錯誤
                    raise exc
                print('retrying request')
                num_retry += 1
    except exc:
        # 超過請求次數印出 http request eror 並將錯誤丟出function外
        print('http request error: %s' % url)
        raise
    except:
        # 出現意料之外的錯誤時印出錯誤並將錯誤丟出function外
        print('Unexcepted error: %s' % url, sys.exc_info())
        raise


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
        raise exc('parse_error')  # 當beautifulsoup解析失敗為Nonetype時，將錯誤丟出function外



def equipment_crawl(soup, i):
    try:
        dfequ = None
        dfequ = pd.DataFrame(np.zeros(shape=(1, 20), dtype=int), columns=['胎壓偵測', '動態穩定系統', '防盜系統', 'keyless免鑰系統', '循跡系統', '中控鎖', '剎車輔助系統', '兒童安全椅固定裝置', 'ABS防鎖死',
                                                                          '安全氣囊', '定速系統', 'LED頭燈', '倒車顯影系統', '衛星導航', '多功能方向盤', '倒車雷達', '恆溫空調', '自動停車系統', '電動天窗', '真皮/皮革座椅'])

        carequ = soup.find('div', id='car-equip')
        equip = carequ.find_all('li')
        for x in equip:
            e = x.text.strip()
            h = x.get('class')
            if 'has' in h:
                if e in dfequ:
                    dfequ[e] = 1
    except:
        print('get-equipment error', sys.exc_info(), i)
        pass
    return dfequ


def verified_crawl(soup, i):

    try:
        verified_info = soup.find('div', class_='vihicle-data').find_all('li')

        ver = verified_info[1].find(class_='title').text.strip()

        if ver == '暫未驗證':
            return 0
        else:
            return 1
    except AttributeError:
        try:
            print(f'Change to get-8891-verification Car_id: {i}')
            ver = soup.find('span', class_='tip-triangle')
            if ver:
                return 1
            else:
                raise exc('get-8891-verification error')
        except exc:
            print(Exception)
            print('get8891-verification error: \n', sys.exc_info())
            print(i)
            return None
    except:
        print('Unexcepted get-verification error: \n', sys.exc_info())
        print(i)
        return None


headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36 Edg/88.0.705.68'}

# df1=pd.DataFrame(columns=['id','m_id','auto_brand_en','auto_brand_id','auto_gas_size','auto_make_date','auto_mileage_num','auto_price','auto_price_tag',
#                            'auto_price_type','auto_title_all','item_post_date','item_renew_date','is_new','item_show_num','photo','photoList','rank'])

# for i in range(1,989):

#     url = f'https://auto.8891.com.tw/usedauto-newSearch.html?page={i}&limit=40'
#     try:
#         r = get_html(url,headers)
#     except:
#         print('get-HTML error： %s' % url, sys.exc_info()) # 接住錯誤確保翻頁迴圈持續運作
#         continue
#     try:
#         data = r.json()
#         df1 = df1.append(pd.json_normalize(data['data']['data']))
# #         df1.to_csv('car_8891.csv', mode='a',header=0,encoding='utf-8-sig')
#     except:
#         print(f'Dataframe processing error: '+url, sys.exc_info())
#         continue


# df1.to_csv('car_8891_first.csv', mode='w',encoding='utf-8-sig')
df1 = pd.read_csv('car_8891_first.csv', index_col=0)

base_url = 'https://auto.8891.com.tw/oapi/shop/shopInfo/'

df_final = pd.DataFrame(columns=['id', 'car_color', 'car_driveMode', 'car_fuel', 'car_door', 'car_seat',
                                 'car_license', 'verified', 'dealer_name', 'seller_role',
                                 'dealer_address', '胎壓偵測', '動態穩定系統', '防盜系統', 'keyless免鑰系統', '循跡系統',
                                 '中控鎖', '剎車輔助系統', '兒童安全椅固定裝置', 'ABS防鎖死', '安全氣囊', '定速系統', 'LED頭燈',
                                 '倒車顯影系統', '衛星導航', '多功能方向盤', '倒車雷達', '恆溫空調', '自動停車系統', '電動天窗',
                                 '真皮/皮革座椅'])

for i, m in zip(df1['id'], df1['m_id']):

    print('--------------------------------------------------start new Car_page parsing ----------------------------------------------')
    
    # 取得商品頁面資訊
    url_info = f'https://auto.8891.com.tw/usedauto-infos-{i}.html'
    
    try:
        soup = parse_html(get_html(url_info, headers))
    except:
        print('get-url error： %s\n' % url_info, sys.exc_info())
        continue
    
    # 獲取地址
    try:
        dealer_address = None
        dealer_address = soup.find(
            'div', class_='car-contact').find('a', class_='car-pos').text.strip()

    except:
        print('get-dealer_address error: '+url_info+'\n', sys.exc_info())
        pass
    
    # 獲取車商id

    try:
        gethref = None
        sid = None
        gethref = soup.find(
            'div', class_='car-contact').find('a', class_='car-pos').get('href')
        testre = re.search('[0-9]{3,5}.html', gethref)
        sid = testre[0].split('.')[0]
    except:
        print('get-sid error: '+url_info+'\n', sys.exc_info())  # 如果沒有車商id 則pass
        pass

    headers = {
        'authority': 'auto.8891.com.tw',
        'accept': 'application/json, text/javascript, */*; q=0.01',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36',
        'referer': f'https://auto.8891.com.tw/usedauto-infos-{i}.html',
        'accept-language': 'zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7,zh-CN;q=0.6',
        'cookie': '__ab=b; _gcl_au=1.1.1197516456.1623856972; __gads=ID=eb1d3aa39b7b3281:T=1623856972:S=ALNI_Mbi88iGOVW1RSC9YpvmrDWaRXwV9g; _hjid=8f6beed8-1df7-46e9-b1ae-f27f57093626; uuid=39974315-0ae6-49c3-b425-f14b4d9874d6; _ga=GA1.4.1383164813.1623856973; _fbp=fb.2.1624072959016.1508856945; g=mobile; PHPSESSID=2hdh01fjj59huc33gv8qlnirp4; webp=1; newcar_version=online; _gid=GA1.3.1805357577.1625150977; _hjTLDTest=1; _=1; _gid=GA1.4.1805357577.1625150977; globalPopupAd=2; utp=U1625302232; uvt=eyJ0cyI6eyJVIjoxMzY4OTk4LjA4MTk3NjcsIk4iOjk5NzQxLjg0ODgwNTQyOH0sIm50IjoxNjI1MzI1NzE4Ljg5MTUsIm5wIjoiVSJ9; _ga=GA1.3.1383164813.1623856973; auto-video-hint=1; _ga_4YCT4M05RT=GS1.1.1625328654.30.0.1625328654.60; user_session=1',
    }

    params = (
        ('sid', f'{sid}'),
    )
    # 嘗試獲取車商id資訊
    try:
        r = None
        r = requests.get(base_url, headers=headers, params=params)
        seller_role = r.json()['data']['shop_name']
        dealer_name = r.json()['data']['shop_name']
    
    # 如果出現 Key error 則嘗試抓取會員id
    except KeyError:
        try:
            print(f'Change to memberID: {m}, car_id: {i}')
            seller_role = None
            dealer_name = None
            if r.json()['status'] == 400:
                params = (('mid', f'{m}'),)
                r = requests.get(base_url, headers=headers, params=params)
                seller_role = r.json()['data']['is_role']
                dealer_name = r.json()['data']['shop_name']
            else:
                raise exc('dealer_name parse error')
        except exc:
            print(f'dealer_name parse error \nid:{i} m_id:{m}')
            pass
        except:
            print(f'dealer_name parse error \nid:{i} m_id:{m}')
            pass
    except:
        print('Unexcepted error:\n', sys.exc_info(), f'\nid:{i} m_id:{m}')
        continue

    # 開始從商品頁抓取資料

    dfequ = None
    dfequ = equipment_crawl(soup, i)

    verified = None
    verified = verified_crawl(soup, i)

    try:
        car_license = None
        car_color = None
        car_fuel = None
        car_door = None
        car_seat = None
        car_driveMode = None

        car_info = soup.find('ul', class_='car-info clearfix')
        span = car_info.find_all('span')
        list1 = []
        for y in span:
            list1.append(y.text.strip())

        car_license = list1[3]
        car_color = list1[4]
        car_fuel = list1[8]
        car_door = list1[6].split('門')[0]+'門'
        car_seat = list1[6].split('門')[1]
        car_driveMode = list1[10]
    except:
        print('get-car_info error: '+url_info+'\n', sys.exc_info())
        pass
    
    # 處理Dataframe
    try:
        df2 = None
        df2 = pd.DataFrame(columns=['id', 'car_color', 'car_driveMode', 'car_fuel', 'car_door',
                           'car_seat', 'car_license', 'verified', 'dealer_name', 'seller_role', 'dealer_address'])
        df2 = df2.append({'id': i, 'car_color': car_color, 'car_driveMode': car_driveMode, 'car_fuel': car_fuel,
                          'car_door': car_door, 'car_seat': car_seat, 'car_license': car_license, 'verified': verified,
                          'dealer_name': dealer_name, 'seller_role': seller_role, 'dealer_address': dealer_address}, ignore_index=True)
        df_temp = None
        df_temp = pd.concat([df2, dfequ], axis=1)
        df_final = df_final.append(df_temp)

    except:
        print('Dataframe process error: \n', sys.exc_info())
        print(url_info)
        continue

df_xxx = df1.merge(df_final, on='id') # 與開頭抓取 json merge
df_xxx.to_csv('8891_0705.csv', mode='w', encoding='utf-8-sig') 
print('8891 complete')
