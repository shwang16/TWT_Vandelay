import mysql.connector
from mysql.connector import errorcode

# start connection
try:
    cnn = mysql.connector.connect(
    user = 'root',
    password = 'prplSQL16!',
    host = '127.0.0.1',
    database = 'flaskapp')
    print('It works!')
except mysql.connector.Error as e:
    if e.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print('Something is wrong with username or password')
    elif e.errno == errorcode.ER_BAD_DB_ERROR:
        print('Database does not exist')
    else:
        print(e)
