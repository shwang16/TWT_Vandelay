import requests
import pymysql

conn = pymysql.connect(user = 'root', password = 'prplSQL16!', host='127.0.0.1', db = 'flaskapp')
cursor = conn.cursor()
country = "China"
#add country
check_ctry = "SELECT * FROM countries WHERE name = %s"
cursor.execute( check_ctry, country)
row = cursor.fetchone()
print(row)

newnum = row[2] + 1
newsale = row[3] + 123
cursor.execute("UPDATE countries SET num = %s, profit = %s WHERE name = %s", (newnum, newsale, country))
conn.commit()
