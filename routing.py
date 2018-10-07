from flask import Flask, render_template, request, redirect, url_for
app = Flask(__name__)

import pymysql
import requests

#connect to database
conn = pymysql.connect(user = 'root', password = 'prplSQL16!', host='127.0.0.1', db = 'flaskapp')

#list of countries
locs = []

@app.route('/', methods = ['GET', 'POST'])
def home():
    r = requests.get('https://my.api.mockaroo.com/swang.json?key=e6ac1da0')
    list = r.json();

    for d in list:
        #set variable values
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
            cursor.execute("INSERT INTO countries(name, num, profit) VALUES (%s, %s, %s)", (country, 1, saleprice))
            conn.commit()
            cursor.close()
        else:
            #update current record
            newnum = row[2] + 1
            newsale = row[3] + saleprice
            cursor = conn.cursor()
            cursor.execute("UPDATE countries SET num = %s, profit = %s WHERE name = %s", (newnum, newsale, country))
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

    if request.method == 'POST':
        detail = request.form
        place = detail['cty']
        return redirect(url_for('specify_country', place=place))

    return render_template('display.html', list = locs)

@app.route('/<place>')
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

    return render_template('data.html', data = details, specs=thing)

if __name__ == "__main__":
    app.run()
