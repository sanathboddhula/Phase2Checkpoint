import mysql.connector

def get_data(query):
    cnx = mysql.connector.connect(user='root', password = 'admin',
                                  host = 'localhost', database = 'RelSchema')
    cursor = cnx.cursor()
    cursor.execute(query)
    result = list()
    for row in cursor:
        result.append(row)
    cnx.close()
    return result


from flask import Flask, render_template, request
import sqlite3 as sql

app = Flask(__name__)

host = 'http://127.0.0.1:5000/'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/name', methods=['POST', 'GET'])
def name():
    error = None
    if request.method == 'POST':
        result = valid_name(request.form['FirstName'], request.form['LastName'])
        if result:
            return render_template('input.html', error=error, result=result)
        else:
            error = 'invalid input name'
    return render_template('input.html', error=error)


def load_buyers(email,first_name,last_name,gender,age,home_address_id,billing_address_id):
    connection = sql.connect('database.db')
    cursor = connection.cursor()
    connection.execute('CREATE TABLE IF NOT EXISTS users(email TEXT,first_name TEXT,last_name TEXT,gender TEXT,age INT,home_address_id INT,'
                       'billing_address_id INT);')
    for(email, first_name, last_name, gender, age, home_address_id, billing_address_id) in cursor:
        connection.execute('INSERT INTO users (email TEXT,first_name TEXT,last_name TEXT,gender TEXT,age INT,home_address_id INT,'
        'billing_address_id INT) VALUES (?, ?, ?, ?, ?, ?, ?);', (email, first_name, last_name, gender, age, home_address_id, billing_address_id))
    connection.commit()
    cursor2 = connection.execute('SELECT * FROM users;')
    return cursor2.fetchall()

def load_categories(parent_category, category_name):
    connection = sql.connect('database.db')
    cursor = connection.cursor()
    connection.execute('CREATE TABLE IF NOT EXISTS users(parent_category TEXT, category_name TEXT);')
    for(parent_category, category_name) in cursor:
        connection.execute('INSERT INTO users (parent_category TEXT, category_name TEXT) VALUES (?, ?);',
                           (parent_category, category_name))
    connection.commit()
    cursor2 = connection.execute('SELECT * FROM users;')
    return cursor2.fetchall()

def load_categories(credit_card_num,card_code,expire_month,expire_year,card_type, owner_email):
    connection = sql.connect('database.db')
    cursor = connection.cursor()
    connection.execute('CREATE TABLE IF NOT EXISTS users(credit_card_num INTEGER, card_code TEXT,expire_month TEXT, expire_year TEXT, '
                       'card_type TEXT, owner_email TEXT);')
    for(credit_card_num,card_code,expire_month,expire_year,card_type, owner_email) in cursor:
        connection.execute('INSERT INTO users (credit_card_num INTEGER, card_code TEXT,expire_month TEXT, expire_year TEXT, '
        'card_type TEXT, owner_email TEXT) VALUES (?, ?, ?, ?, ?, ?);',
        (credit_card_num,card_code,expire_month,expire_year,card_type, owner_email))
    connection.commit()
    cursor2 = connection.execute('SELECT * FROM users;')
    return cursor2.fetchall()

def local_vendors(email, business_name, business_address_ID, customer_service_number):
    connection = sql.connect('database.db')
    cursor = connection.cursor()
    connection.execute('CREATE TABLE IF NOT EXISTS users(email TEXT, business_name TEXT, business_address_ID TEXT, customer_service_number TEXT);')
    for(email, business_name, business_address_ID, customer_service_number) in cursor:
        connection.execute('INSERT INTO users (email TEXT, business_name TEXT, business_address_ID TEXT, customer_service_number TEXT) '
                           'VALUES (?, ?, ?, ?);',
        (email, business_name, business_address_ID, customer_service_number))
    connection.commit()
    cursor2 = connection.execute('SELECT * FROM users;')
    return cursor2.fetchall()

def local_vendors(transaction_ID, seller_email, listing_ID, buyer_email, date, quantity, payment):
    connection = sql.connect('database.db')
    cursor = connection.cursor()
    connection.execute('CREATE TABLE IF NOT EXISTS users(email TEXT, business_name TEXT, business_address_ID TEXT, customer_service_number TEXT);')
    for(email, business_name, business_address_ID, customer_service_number) in cursor:
        connection.execute('INSERT INTO users (email TEXT, business_name TEXT, business_address_ID TEXT, customer_service_number TEXT) '
                           'VALUES (?, ?, ?, ?);',
        (email, business_name, business_address_ID, customer_service_number))
    connection.commit()
    cursor2 = connection.execute('SELECT * FROM users;')
    return cursor2.fetchall()

def orders(transaction_ID, seller_email, listing_ID, buyer_email, date, quantity, payment):
    connection = sql.connect('database.db')
    cursor = connection.cursor()
    connection.execute('CREATE TABLE IF NOT EXISTS users(email TEXT, business_name TEXT, business_address_ID TEXT, customer_service_number TEXT);')
    for(email, business_name, business_address_ID, customer_service_number) in cursor:
        connection.execute('INSERT INTO users (email TEXT, business_name TEXT, business_address_ID TEXT, customer_service_number TEXT) '
                           'VALUES (?, ?, ?, ?);',
        (email, business_name, business_address_ID, customer_service_number))
    connection.commit()
    cursor2 = connection.execute('SELECT * FROM users;')
    return cursor2.fetchall()

def orders(seller_email, listing_ID, category, title, product_name, product_description, price, quantity):
    connection = sql.connect('database.db')
    cursor = connection.cursor()
    connection.execute('CREATE TABLE IF NOT EXISTS users(email TEXT, business_name TEXT, business_address_ID TEXT, customer_service_number TEXT);')
    for(email, business_name, business_address_ID, customer_service_number) in cursor:
        connection.execute('INSERT INTO users (email TEXT, business_name TEXT, business_address_ID TEXT, customer_service_number TEXT) '
                           'VALUES (?, ?, ?, ?);',
        (email, business_name, business_address_ID, customer_service_number))
    connection.commit()
    cursor2 = connection.execute('SELECT * FROM users;')
    return cursor2.fetchall()

if __name__ == "__main__":
    app.run()


