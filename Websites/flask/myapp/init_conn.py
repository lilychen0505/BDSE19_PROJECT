import pymysql
connection = pymysql.connect(host='mysql', user='daniel',password='daniel03',
                             charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor, database='carsgo')

