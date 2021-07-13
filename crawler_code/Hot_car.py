from pandas.io.formats import style
from selenium import webdriver
from bs4 import BeautifulSoup
import numpy as np
import pandas as pd
import time
import sys
import logging

logging.basicConfig(
    filename='crawl_HOT.log',
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)


def parse_html(pagesource):
    soup = BeautifulSoup(pagesource, 'lxml')
    if soup != None:
        print('parsing success')  # 印出成功解析網頁名
        return soup
    else:
        # 當beautifulsoup解析失敗為Nonetype時，將錯誤丟出function外
        raise Exception('parse_error')


if __name__ == "__main__":
    logger = logging.getLogger(__name__)

    df1 = pd.read_csv('./HOT_car/hot_first.csv', index_col=0, encoding='utf-8')
    df_final = pd.DataFrame(columns=['TSEQNO', 'car_driveMode', 'dealer_address', 'car_photo', '安全氣囊', 'ABS', '定速',
                                     '倒車影像', '倒車雷達', '衛星導航', '胎壓偵測', '霧燈', 'ESP', '車道偏移系統',
                                     '車側盲點偵測系統', '鋁圈', '電動後視鏡', 'HID頭燈', '天窗', '電動尾門',
                                     '電動滑門', '全景天窗', '皮椅', '恆溫空調', 'PUSH START', 'ISOFIX', 'CD', 'VCD',
                                     'DVD', '液晶螢幕', '電動座椅', '方向盤換檔撥片'])

    for idnum in df1['TSEQNO'][:5]:

        logger.info(f'start crawling new page: {idnum}')

        url_idnum = None
        url_idnum = f'https://www.hotcar.com.tw/CWA/CWA060.html?TSEQNO={idnum}'

        try:
            driver = webdriver.Chrome('./chromedriver')
            driver.get(url_idnum)
        except:
            logger.warning(f'driver_getURL error: {idnum}')
            logger.warning(sys.exc_info)
            continue

        driver.maximize_window()
        time.sleep(3)

        try:
            soup = None
            soup = BeautifulSoup(driver.page_source, 'lxml')
        except:
            logger.warning(f'parse_html error: {idnum}')
            logger.warning(sys.exc_info)
            continue

        try:
            car_driveMode = None
            car_driveMode = soup.find(class_='tablein').find_next_sibling().find(
                class_='text').text.strip()

        except:
            logger.warning(f'car_driveMode parsing error {idnum}')
            logger.warning(sys.exc_info)
            pass

        try:
            dealer_address = None
            dealer_address = soup.find(class_='table web').find(
                class_='text').text.strip()

        except:
            logger.warning(f'dealer_address parsing error {idnum}')
            logger.warning(sys.exc_info)
            pass

        try:
            car_photo = None
            car_photo = soup.find(
                'img', class_='rsImg rsMainSlideImage').get('src').strip()

        except:
            logger.warning(f'car_photo parsing error {idnum}')
            logger.warning(sys.exc_info)
            pass

        dfinfo = None
        dfinfo = pd.DataFrame(
            columns=['TSEQNO', 'car_driveMode', 'dealer_address', 'car_photo'])
        dfinfo = dfinfo.append({'TSEQNO': idnum, 'car_driveMode': car_driveMode,
                                'dealer_address': dealer_address, 'car_photo': car_photo}, ignore_index=True)

        dfequ = pd.DataFrame(np.zeros(shape=(1, 28), dtype=int), columns=['安全氣囊', 'ABS', '定速',
                                                                          '倒車影像', '倒車雷達', '衛星導航', '胎壓偵測', '霧燈', 'ESP', '車道偏移系統',
                                                                          '車側盲點偵測系統', '鋁圈', '電動後視鏡', 'HID頭燈', '天窗', '電動尾門',
                                                                          '電動滑門', '全景天窗', '皮椅', '恆溫空調', 'PUSH START', 'ISOFIX', 'CD', 'VCD',
                                                                          'DVD', '液晶螢幕', '電動座椅', '方向盤換檔撥片'])
        try:
            component = None
            component = soup.find('div', id='components').find_all('li')
            for i in component:
                style_type = i.get('style')
                equ = i.text.strip()
                if style_type == 'display: none;':
                    dfequ[equ] = 0
                else:
                    dfequ[equ] = 1
        except:
            logger.warning(f'equipment parsing error {idnum}')
            logger.warning(sys.exc_info)
            pass

        df_temp = None
        df_temp = pd.concat([dfinfo, dfequ], axis=1)
        df_final = df_final.append(df_temp)
        driver.close()

    df_complete = df1.merge(df_final, on='TSEQNO')

    df_complete.to_csv('hot_car_crawl.csv', encoding='utf-8-sig')

    logger.info('Complete!')
