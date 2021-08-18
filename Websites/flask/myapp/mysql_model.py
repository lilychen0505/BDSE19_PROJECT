def create_url(result):
    if result['source'] == '8891':
        car_url = f"https://auto.8891.com.tw/usedauto-infos-{result['carID']}.html"
    if result['source'] == 'HOT':
        car_url = f"https://www.hotcar.com.tw/CWA/CWA060.html?TSEQNO={result['carID']}"
    if result['source'] == 'SUM':
        car_url = f"https://www.sum.com.tw/carinfo-{result['carID']}.php"
    if result['source'] == 'abc':
        car_url = f"https://www.abccar.com.tw/car/{result['carID']}?"
    if result['source'] == 'isave':
        car_url = f"https://www.isave.com.tw/car.aspx?cid={result['carID']}"
    if result['source'] == 'usedcar':
        car_url = f"https://used.carnews.com/UsedCar/Details/{result['carID']}"
    if result['source'] == 'ucar':
        car_url = f"https://usedcar.u-car.com.tw/objectdetail.aspx?usedcarid={result['carID']}"
    if result['source'] == 'yahoo':
        car_url = f"https://tw.usedcar.yahoo.com/item/detail/{result['carID']}"
    return car_url