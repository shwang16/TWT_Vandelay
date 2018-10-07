from flask import Flask, render_template, request, redirect, url_for
app = Flask(__name__)

import pymysql
import requests

#connect to database
conn = pymysql.connect(user = 'root', password = 'prplSQL16!', host='127.0.0.1', db = 'flaskapp')

#create tables in sql db

# cursor = conn.cursor()
# create_cars = "CREATE TABLE cars( id INT NOT NULL AUTO_INCREMENT,
#     import_country VARCHAR(50) NOT NULL,
#     model VARCHAR(25),
#     make VARCHAR(25),
#     sold_by VARCHAR(30) NOT NULL,
#     sale_price INT NOT NULL,
#     PRIMARY KEY (id),
#     UNIQUE (import_country, model, make, sold_by, sale_price))"
# create_countries = "CREATE TABLE countries(
#     id INT NOT NULL AUTO_INCREMENT,
#     name VARCHAR(50) NOT NULL,
#     num INT NOT NULL,
#     profit INT NOT NULL,
#     average INT NOT NULL,
#     PRIMARY KEY (id),
#     UNIQUE (name))"
# cursor.execute(create_cars);
# cursor.execute(create_countries);
# cursor.close()

#define locations list
locs = [];
#home page
@app.route('/', methods = ['GET', 'POST'])
def home():
    #get data from api
    r = requests.get('https://my.api.mockaroo.com/swang.json?key=e6ac1da0')
    list = r.json();

    #synthesize each data point
    for d in list:
        make = None
        mod = None
        country = d["import_country"]
        soldby = d["sold_by"]
        saleprice = d["sale_price"]
        for key in d:
            if key == "model":
                mod = d['model']
            if key == "make":
                make = d['make']

        #update db
        cursor = conn.cursor()
        add_data = "INSERT INTO cars(import_country, model, make, sold_by, sale_price) VALUES (%s, %s, %s, %s, %s)"
        cursor.execute( add_data , (country, mod, make, soldby, saleprice))
        conn.commit()
        cursor.close()

        #add country TO DB
        cursor = conn.cursor()
        check_ctry = "SELECT * FROM countries WHERE name = %s"
        cursor.execute( check_ctry, country)
        row = cursor.fetchone()
        cursor.close()
        if row == None:
            #add record
            cursor = conn.cursor()
            line = "INSERT INTO countries(name, num, profit, average) VALUES (%s, %s, %s, %s)"
            cursor.execute(line, (country, 1, saleprice, saleprice))
            conn.commit()
            cursor.close()
        else:
            #update current record
            newnum = row[2] + 1
            newsale = row[3] + saleprice
            newavg = newsale / newnum
            cursor = conn.cursor()
            update = "UPDATE countries SET num = %s, profit = %s, average = %s WHERE name = %s"
            cursor.execute(update, (newnum, newsale, newavg, country))
            conn.commit()
            cursor.close()

    #add to countries list
    cursor = conn.cursor()
    add_list = "SELECT * FROM countries"
    cursor.execute(add_list)
    result = cursor.fetchall()
    cursor.close()
    for r in result:
        locs.append(r[1])

    #filter form
    if request.method == 'POST':
        detail = request.form
        if 'one' in detail:
            pl = detail['cty']
            return redirect(url_for('specify_country', place=pl))
        elif 'two' in detail:
            f_ma = detail['mk']
            return redirect(url_for('show_make', value=f_ma))
        elif 'three' in detail:
            ra = detail['priceR']
            return redirect(url_for('price_range', range=ra))

    return render_template('display.html', list = locs)

#endpoint for filter by country
@app.route('/country/<place>')
def specify_country(place):

    #query countries table
    query = "SELECT * FROM countries WHERE name = %s"
    cursor = conn.cursor()
    cursor.execute(query, place)
    thing = cursor.fetchone()
    cursor.close()

    #query cars table
    query = "SELECT * FROM cars WHERE import_country = %s ORDER BY make, model"
    cursor = conn.cursor()
    cursor.execute(query, place)
    details = cursor.fetchall()
    cursor.close()

    return render_template('country.html', data = details, specs=thing)

#filter by make
@app.route('/make/<value>')
def show_make(value):

    #query cars table
    query = "SELECT * FROM cars WHERE make= %s ORDER BY import_country, model"
    cursor = conn.cursor()
    cursor.execute(query, value)
    details = cursor.fetchall()
    cursor.close()

    return render_template('make.html', data = details, thing = value, length = len(details))

#filter by price range
@app.route('/pr/<range>')
def price_range(range):
    #query cars table
    if range == "less":
        query = "SELECT * FROM cars WHERE sale_price <= %s ORDER BY sale_price, import_country, make, model"
    else:
        query = "SELECT * FROM cars WHERE sale_price > %s ORDER BY sale_price, import_country, make, model"

    cursor = conn.cursor()
    cursor.execute(query, 15000)
    details = cursor.fetchall()
    cursor.close()

    map = {};
    for t in details:
        cy = t[1]
        if cy in map.keys():
            map[cy] += 1
        else:
            map[cy] = 1

    return render_template('table.html', data = details, map = map)

#display data on each country relating to price
@app.route('/summary')
def summary():
    q = "SELECT * FROM countries"
    cursor = conn.cursor()
    cursor.execute(q)
    table = cursor.fetchall()
    cursor.close()
    return render_template('summary.html', table=table)


if __name__ == "__main__":
    app.run()
