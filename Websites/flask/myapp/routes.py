from flask.helpers import url_for
from myapp import app
from flask import render_template, request, redirect
from myapp.model import predict, data_collect, result_compute
from myapp.mysql_model import create_url
from myapp.init_conn import connection
import math


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/predictPrice', methods=['GET', 'POST'])
def predictPrice():
    car_brand = ['Toyota', 'Ford', 'Nissan', 'Mercedes-Benz', 'BMW', 'Mitsubishi', 'Suzuki', 'Honda', 'Mazda', 'Hyundai', 'Luxgen', 'Subaru', 'Lexus', 'Kia', 'VW', 'Landrover', 'Skoda',
                 'Mini', 'Volvo', 'Audi', 'Smart', 'Peugeot', 'Porsche', 'Citroen', 'Infiniti', 'Jaguar', 'Isuzu', 'Lamborghini', 'Ferrari', 'Alfa Romeo', 'Chevrolet', 'Dodge', 'Maserati', 'Opel', 'Saab',
                 'Fiat','Jeep','Bentley','Mclaren','Chrysler','Tesla','Buick','Cmc','Renault','Hummer','Scion','Rolls-Royce','Acura','Cadillac','Iveco','Formosa','Aston Martin']
    exec_info = None

    if request.method == 'POST':
        try:
            form = request.form
            form = dict(form)
            input = data_collect(form)
            result = predict(input)
            result = result_compute(result)
        except:
            exec_info = '預測時出現錯誤請重新輸入'
            return render_template('predictPrice_form.html', car_brand=car_brand, exec_info=exec_info)
        # sqlprice = f'SELECT * FROM car_list WHERE carPrice>={result["set1"]} and carPrice<={result["set2"]} LIMIT 9'
        # cursor1 = connection.cursor()
        # cursor1.execute(sqlprice)
        # price_range_car = cursor1.fetchall()
        return render_template('predictPrice_result.html', form=form, car_brand=car_brand, result=result)

    return render_template('predictPrice_form.html', car_brand=car_brand, exec_info=exec_info)


@app.route('/loan')
def loan():
    price = request.args.get('price', type=float)
    return render_template('loan.html', price=price)


@app.route('/bestCarForm',  methods=['GET', 'POST'])
def bestCarForm():
    exec_info = None
    if request.method == 'POST':
        try:
            form = dict(request.form)
            cbrand = form['brand']
            cyear = form['cyear']
            ckm = form['km']
            return redirect(url_for('bestCarResult', brand=cbrand, year=cyear, mileage=ckm))
        except:
            exec_info = '資料出現錯誤請重新選擇'
            return render_template('bestCar_form.html',exec_info=exec_info)
    return render_template('bestCar_form.html', exec_info=exec_info)


@app.route('/bestCarResult')
def bestCarResult():

    page = request.args.get('page', 1, type=int)  # init page=1
    cbrand = request.args.get('brand', None)
    cyear = request.args.get('year', None)
    ckm = request.args.get('mileage', None)

    # Normal: TOYOTA, FORD, HONDA, NISSAN, MITSUBISHI, MAZADA, LUXGEN, HYUNDAI, KIA, SUZUKI
    # Advanced: SKODA, SUBARU, VOLKSWAGEN, PEUGEOT, CITROEN, RENAULT, OPEL,
    # Luxury: LEXUS, INFINITI, JAGUAR, TESLA, VOLVO, BENZ, BMW, AUDI, PORSCHE, MASERATI, MCLAREN, FERRARI, LAMBORGHINI

    brandsql = None
    if cbrand == 'normal':
        brandsql = 'carBrand="TOYOTA" or carBrand="FORD" or carBrand="HONDA" or carBrand="NISSAN" or carBrand="MITSUBISHI" or carBrand="MAZADA" or carBrand="LUXGEN" or carBrand="HYUNDAI" or carBrand="KIA"'
    if cbrand == 'advanced':
        brandsql = 'carBrand="SKODA" or carBrand="SUZUKI" or carBrand="SUBARU" or carBrand="VOLKSWAGEN" or carBrand="PEUGEOT" or carBrand="CITROEN" or carBrand="RENAULT" or carBrand="OPEL"'
    if cbrand == 'luxury':
        brandsql = 'carBrand="LEXUS" or carBrand="INFINITI" or carBrand="JAGUAR" or carBrand="TESLA" or carBrand="VOLVO" or carBrand="BENZ" or carBrand="BMW" or carBrand="AUDI" or carBrand="PORSCHE" or carBrand="MASERATI" or carBrand="MCLAREN" or carBrand="FERRARI" or carBrand="LAMBORGHINI"'

    yearsql = None
    if cyear == '5':
        yearsql = 'carYear >= 2016'
    if cyear == '510':
        yearsql = 'carYear >= 2011 and carYear <= 2016'
    if cyear == '10':
        yearsql = 'carYear <= 2011'

    kmsql = None
    if ckm == '3':
        kmsql = 'carMileage <= 30000'
    if ckm == '310':
        kmsql = 'carMileage >= 30000 and carMileage <= 100000'
    if ckm == '10':
        kmsql = 'carMileage >= 100000'

    cr = connection.cursor()    # init cursor
    sqlitems = f'SELECT COUNT(*) AS items FROM car_list WHERE ({brandsql}) and ({yearsql}) and ({kmsql})'

    cr.execute(sqlitems)        # execute sql query
    rows = cr.fetchone()        # get sql result
    items = rows['items']       # to get total items
    total_pages = math.ceil(items/9)   # get total pages
    limit = 9                   # limited 9 items in one page

    if page < total_pages:      # user's page < totalpages then offset -> user's page
        offset = page*limit - limit
    else:
        # user's page >= totalpages then offest -> total page
        offset = total_pages*limit - limit

    cur = connection.cursor()   # init cursor
    # from offset value to query 9 items
    sqltest = f'SELECT * FROM car_list WHERE ({brandsql}) and ({yearsql}) and ({kmsql}) ORDER BY carYear DESC LIMIT {limit} OFFSET {offset}'
    cur.execute(sqltest)        # execute sql query
    result = cur.fetchall()     # get sql result

    for r in result:
        r['car_url'] = create_url(r)    # create car link from defined function

    return render_template('bestCar_result.html', result=result, page=page, totalpages=total_pages, items=items, brand=cbrand, year=cyear, mileage=ckm)
