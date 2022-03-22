from flask import Flask, render_template, request, redirect
import sqlite3 as sql
import pandas as pd
import os
import hashlib

app = Flask(__name__)

host = 'http://127.0.0.1:5000/'

salt = os.urandom(32)
password = 'example'

key =  hashlib.pbkdf2_hmac(
    'sha256', # The hash digest algorithm for HMAC
    password.encode('utf-8'), # Convert the password to bytes
    salt, # Provide the salt
    100000, # It is recommended to use at least 100,000 iterations of SHA-256
    dklen=128 #Get a 128 byte key
)

storage = salt + key

salt_storage = storage[:32]
key_storage = storage[:32]


@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        email = request.form['Email']
        password = request.form['Password']
        credentials = checkCredentials(email, password)
        if credentials:
            print('Successful Login')
        elif credentials == False:
            print('Failed to Login')
        return redirect('/')
    return render_template('index.html')

def checkCredentials(email, password):
    connection = sql.connect('database.db')
    cursor = connection.execute('Select * FROM Users u WHERE u.email = ? AND u.password = ?', (email, password, ))

    #credentials do not exist
    if cursor.fetchall() == 0:
        return False
    elif cursor.fetchall() == 1:
        return True

#create load_address
def createDatabases():
    with open('database.db', 'a+') as d:
        pass

    connection = sql.connect('database.db')
    cursor = connection.cursor()

    # create load_users
    connection.execute('CREATE TABLE IF NOT EXISTS Users(email text,password text, PRIMARY KEY(email));')

    # create zipcode_info
    connection.execute(
        'CREATE TABLE IF NOT EXISTS ZipcodeInfo(zipcode REAL, city varchar(20), state_id varchar(20), population varchar(20), density REAL, '
        'county_name varchar(20), timezone varchar(20), PRIMARY KEY(zipcode));')

    #create load_address
    cursor.execute('CREATE TABLE IF NOT EXISTS Address(address_id varchar(20), zipcode REAL,street_num REAL,street_name varchar(20),'
                    'PRIMARY KEY(address_ID), FOREIGN KEY(zipcode) REFERENCES Zipcode_Info(zipcode));')

    #create load buyers
    cursor.execute('CREATE TABLE IF NOT EXISTS Buyers(email varchar(20), first_name varchar(20), last_name varchar(20), gender varchar(20),'
                    'age REAL,home_address_id REAL, billing_address_id REAL, PRIMARY KEY(email),FOREIGN KEY(email) REFERENCES Users(email), '
                    'FOREIGN KEY(home_address_id) REFERENCES Address(address_id), FOREIGN KEY(billing_address_id) REFERENCES Address(address_id));')

    # create load_credit_cards
    connection.execute(
        'CREATE TABLE IF NOT EXISTS CreditCard(credit_card_num INTEGER, card_code varchar(20),expire_month varchar(20), expire_year varchar(20), '
        'card_type varchar(20), owner_email varchar(20), PRIMARY KEY(credit_card_num), FOREIGN KEY(owner_email) REFERENCES Buyers(email));')

    # create load_sellers
    connection.execute(
        'CREATE TABLE IF NOT EXISTS Sellers(email varchar(20), routing_number INTEGER, account_number varchar(20), balance REAL, '
        'PRIMARY KEY (email), '
        'FOREIGN KEY(email) REFERENCES Buyers(email));')

    #create local_vendor
    connection.execute(
        'CREATE TABLE IF NOT EXISTS Vendors(email varchar(20), business_name varchar(20), business_address_ID varchar(20), customer_service_number varchar(20), '
        'PRIMARY KEY(email), '
        'FOREIGN KEY(email) REFERENCES Sellers(email),'
        'FOREIGN KEY(business_address_ID) REFERENCES Address(address_id));')

    #create load categories
    cursor.execute('CREATE TABLE IF NOT EXISTS Categories(parent_category varchar(20), category_name varchar(20), PRIMARY KEY(category_name));')

    # create load_product_listing
    connection.execute(
        'CREATE TABLE IF NOT EXISTS Product_Listing(seller_email varchar(20), listing_ID REAL, category varchar(20), title varchar(30), '
        'product_name varchar(50), product_description varchar(40), price REAL, quantity REAL, PRIMARY KEY(seller_email, listing_id));')

    #create load_orders
    connection.execute('CREATE TABLE IF NOT EXISTS Orders(transaction_ID REAL, seller_email varchar(20), listing_ID REAL, buyer_email varchar(20), '
                        'date varchar(20), quantity REAL, payment REAL, PRIMARY KEY(transaction_id), '
                        'FOREIGN KEY(seller_email, listing_id) REFERENCES Product_Listings(seller_email, listing_id), '
                        'FOREIGN KEY(buyer_email) REFERENCES Buyers(email));')

    # create load_reviews
    connection.execute(
        'CREATE TABLE IF NOT EXISTS Reviews(Buyer_Email varchar(20),Seller_Email varchar(20),Listing_ID varchar(20),Review_Desc varchar(20), '
        'PRIMARY KEY(buyer_email, seller_email, listing_id), '
        'FOREIGN KEY(buyer_email) REFERENCES Buyers(email), '
        'FOREIGN KEY(seller_email, listing_id) REFERENCES Product_Listings(seller_email, listing_id));')

    #create load_ratings
    connection.execute('CREATE TABLE IF NOT EXISTS Ratings(Buyer_Email varchar(20), Seller_Email varchar(20), Date varchar(20), Rating INTEGER, Rating_Desc varchar(20), '
                'PRIMARY KEY(buyer_email, seller_email, date), '
                'FOREIGN KEY(buyer_email) REFERENCES Buyers(email), '
                'FOREIGN KEY(seller_email) REFERENCES Sellers(email));')

    connection.commit()
    #cursor.execute('Select * FROM Ratings')
    #print(cursor.fetchall())


def load_data():
    connection = sql.connect('database.db')
    cursor = connection.cursor()

    with open('Users.csv', 'r') as tbl:
        val = pd.read_csv(tbl)
        val.to_sql('Users', connection, if_exists="replace", index = False)

    with open('Zipcode_Info.csv', 'r') as tbl:
        val = pd.read_csv(tbl)
        val.to_sql('Zipcode_Info', connection, if_exists="replace", index=False)

    with open('Address.csv', 'r') as tbl:
        val = pd.read_csv(tbl)
        val.to_sql('Address', connection, if_exists="replace", index = False)

    with open('Buyers.csv', 'r') as tbl:
        val = pd.read_csv(tbl)
        val.to_sql('Buyers', connection, if_exists="replace", index = False)

    with open('Credit_Cards.csv', 'r') as tbl:
        val = pd.read_csv(tbl)
        val.to_sql('Credit_Cards', connection, if_exists="replace", index = False)

    with open('Sellers.csv', 'r') as tbl:
        val = pd.read_csv(tbl)
        val.to_sql('Sellers', connection, if_exists="replace", index = False)

    with open('Local_Vendors.csv', 'r') as tbl:
        val = pd.read_csv(tbl)
        val.to_sql('Local_Vendors', connection, if_exists="replace", index = False)

    with open('Categories.csv', 'r') as tbl:
        val = pd.read_csv(tbl)
        val.to_sql('Categories', connection, if_exists="replace", index = False)

    with open('Product_Listing.csv', 'r') as tbl:
        val = pd.read_csv(tbl)
        val.to_sql('Product_Listing', connection, if_exists="replace", index = False)

    with open('Orders.csv', 'r') as tbl:
        val = pd.read_csv(tbl)
        val.to_sql('Orders', connection, if_exists="replace", index = False)

    with open('Reviews.csv', 'r') as tbl:
        val = pd.read_csv(tbl)
        val.to_sql('Reviews', connection, if_exists="replace", index = False)

    with open('Ratings.csv', 'r') as tbl:
        val = pd.read_csv(tbl)
        val.to_sql('Ratings', connection, if_exists="replace", index=False)

    connection.commit()

createDatabases()
load_data()

if __name__ == "__main__":
    app.run()



'''
def load_address(address_id,zipcode,street_num,street_name):
    connection = sql.connect('database.db')
    cursor = connection.cursor()
    connection.execute('CREATE TABLE IF NOT EXISTS Address(address_id varchar(20), zipcode REAL,street_num REAL,street_name varchar(20),'
                       'PRIMARY KEY(address_ID), FOREIGN KEY(zipcode) REFERENCES Zipcode_Info(zipcode));')
    for(address_id,zipcode,street_num,street_name) in cursor:
        connection.execute('INSERT INTO Address (email varchar(20), first_name varchar(20), last_name varchar(20), gender varchar(20),'
                       'age REAL,home_address_id REAL, billing_address_id REAL) VALUES (?, ?, ?, ?, ?, ?, ?);',
                           (address_id,zipcode,street_num,street_name))
    connection.commit()
    cursor2 = connection.execute('SELECT * FROM users;')
    #return cursor2.fetchall()


def load_buyers(email,first_name,last_name,gender,age,home_address_id,billing_address_id):
    connection = sql.connect('database.db')
    cursor = connection.cursor()
    connection.execute('CREATE TABLE IF NOT EXISTS Buyers(email varchar(20), first_name varchar(20), last_name varchar(20), gender varchar(20),'
                       'age REAL,home_address_id REAL, billing_address_id REAL, PRIMARY KEY(email),FOREIGN KEY(email) REFERENCES Users(email), '
                       'FOREIGN KEY(home_address_id) REFERENCES Address(address_id),FOREIGN KEY(billing_address_id) REFERENCES Address(address_id)));')
    for(email,first_name,last_name,gender,age,home_address_id,billing_address_id) in cursor:
        connection.execute('INSERT INTO Buyers (email varchar(20), first_name varchar(20), last_name varchar(20), gender varchar(20),'
                       'age REAL,home_address_id REAL, billing_address_id REAL) VALUES (?, ?, ?, ?, ?, ?, ?);',
                           (email,first_name,last_name,gender,age,home_address_id,billing_address_id))
    connection.commit()
    cursor2 = connection.execute('SELECT * FROM users;')
    #return cursor2.fetchall()

def load_categories(parent_category, category_name):
    connection = sql.connect('database.db')
    cursor = connection.cursor()
    connection.execute('CREATE TABLE IF NOT EXISTS Categories(parent_category varchar(20), category_name varchar(20), PRIMARY KEY(category_name));')
    for(parent_category, category_name) in cursor:
        connection.execute('INSERT INTO Categories (parent_category TEXT, category_name TEXT) VALUES (?, ?);',
                           (parent_category, category_name))
    connection.commit()
    cursor2 = connection.execute('SELECT * FROM users;')
    #return cursor2.fetchall()

def load_credit_card(credit_card_num,card_code,expire_month,expire_year,card_type, owner_email):
    connection = sql.connect('database.db')
    cursor = connection.cursor()
    connection.execute('CREATE TABLE IF NOT EXISTS CreditCard(credit_card_num INTEGER, card_code varchar(20),expire_month varchar(20), expire_year varchar(20), '
                       'card_type varchar(20), owner_email varchar(20), PRIMARY KEY(credit_card_num), FOREIGN KEY(owner_email) REFERENCES Buyers(email));')
    for(credit_card_num,card_code,expire_month,expire_year,card_type, owner_email) in cursor:
        connection.execute('INSERT INTO CreditCard (credit_card_num INTEGER, card_code TEXT,expire_month TEXT, expire_year TEXT, '
        'card_type TEXT, owner_email TEXT) VALUES (?, ?, ?, ?, ?, ?);',
        (credit_card_num,card_code,expire_month,expire_year,card_type, owner_email))
    connection.commit()
    cursor2 = connection.execute('SELECT * FROM users;')
    #return cursor2.fetchall()

def local_vendors(email, business_name, business_address_ID, customer_service_number):
    connection = sql.connect('database.db')
    cursor = connection.cursor()
    connection.execute('CREATE TABLE IF NOT EXISTS Vendors(email varchar(20), business_name varchar(20), business_address_ID varchar(20), customer_service_number varchar(20), '
                       'PRIMARY KEY(email), '
                       'FOREIGN KEY(email) REFERENCES Sellers(email),'
                       'FOREIGN KEY(business_address_ID) REFERENCES Address(address_id));')
    for(email, business_name, business_address_ID, customer_service_number) in cursor:
        connection.execute('INSERT INTO Vendors (email varchar(20), business_name varchar(20), business_address_ID varchar(20), customer_service_number varchar(20)) '
                           'VALUES (?, ?, ?, ?);',
        (email, business_name, business_address_ID, customer_service_number))
    connection.commit()
    cursor2 = connection.execute('SELECT * FROM users;')
    #return cursor2.fetchall()

def load_orders(transaction_ID, seller_email, listing_ID, buyer_email, date, quantity, payment):
    connection = sql.connect('database.db')
    cursor = connection.cursor()
    connection.execute('CREATE TABLE IF NOT EXISTS Orders(transaction_ID REAL, seller_email varchar(20), listing_ID REAL, buyer_email varchar(20), '
                       'date varchar(20), quantity REAL, payment REAL, PRIMARY KEY(transaction_id), '
                       'FOREIGN KEY(seller_email, listing_id) REFERENCES Product_Listings(seller_email, listing_id), '
                       'FOREIGN KEY(buyer_email) REFERENCES Buyers(email)););')
    for(transaction_ID, seller_email, listing_ID, buyer_email, date, quantity, payment) in cursor:
        connection.execute('INSERT INTO Orders (transaction_ID REAL, seller_email varchar(20), listing_ID REAL, buyer_email varchar(20), '
                       'date varchar(20), quantity REAL, payment REAL) '
                           'VALUES (?, ?, ?, ?, ?, ?, ?);',
        (transaction_ID, seller_email, listing_ID, buyer_email, date, quantity, payment))
    connection.commit()
    cursor2 = connection.execute('SELECT * FROM users;')
    #return cursor2.fetchall()

def load_product_listing(seller_email, listing_ID, category, title, product_name, product_description, price, quantity):
    connection = sql.connect('database.db')
    cursor = connection.cursor()
    connection.execute('CREATE TABLE IF NOT EXISTS Product_Listing(seller_email varchar(20), listing_ID REAL, category varchar(20), title varchar(30), '
                       'product_name varchar(50), product_description varchar(40), price REAL, quantity REAL, PRIMARY KEY(seller_email, listing_id));')
    for(seller_email, listing_ID, category, title, product_name, product_description, price, quantity) in cursor:
        connection.execute('INSERT INTO Product_Listing (seller_email varchar(20), listing_ID REAL, category varchar(20), title varchar(30), '
                       'product_name varchar(50), product_description varchar(40), price REAL, quantity REAL)) '
                           'VALUES (?, ?, ?, ?, ?, ?, ?, ?);',
        (seller_email, listing_ID, category, title, product_name, product_description, price, quantity))
    connection.commit()
    cursor2 = connection.execute('SELECT * FROM users;')
    #return cursor2.fetchall()

def load_ratings(Buyer_Email , Seller_Email, Date, Rating, Rating_Desc):
    connection = sql.connect('database.db')
    cursor = connection.cursor()
    connection.execute('CREATE TABLE IF NOT EXISTS Ratings(Buyer_Email varchar(20), Seller_Email varchar(20), Date varchar(20), Rating INTEGER, Rating_Desc varchar(20), '
                       'PRIMARY KEY(buyer_email, seller_email, date), '
                       'FOREIGN KEY(buyer_email) REFERENCES Buyers(email), '
                       'FOREIGN KEY(seller_email) REFERENCES Sellers(email));')
    for(Buyer_Email , Seller_Email, Date, Rating, Rating_Desc) in cursor:
        connection.execute('INSERT INTO Ratings (Buyer_Email varchar(20), Seller_Email varchar(20), Date varchar(20), Rating INTEGER, '
                           'Rating_Desc varchar(20)) VALUES (?, ?, ?, ?, ?, ?);',
        (Buyer_Email , Seller_Email, Date, Rating, Rating_Desc))
    connection.commit()
    cursor2 = connection.execute('SELECT * FROM users;')
    #return cursor2.fetchall()

def load_reviews(Buyer_Email,Seller_Email,Listing_ID,Review_Desc):
    connection = sql.connect('database.db')
    cursor = connection.cursor()
    connection.execute('CREATE TABLE IF NOT EXISTS Reviews(Buyer_Email varchar(20),Seller_Email varchar(20),Listing_ID varchar(20),Review_Desc varchar(20), '
                       'PRIMARY KEY(buyer_email, seller_email, listing_id), '
                       'FOREIGN KEY(buyer_email) REFERENCES Buyers(email), '
                       'FOREIGN KEY(seller_email, listing_id) REFERENCES Product_Listings(seller_email, listing_id));')
    for(Buyer_Email,Seller_Email,Listing_ID,Review_Desc) in cursor:
        connection.execute('INSERT INTO Reviews (Buyer_Email varchar(20),Seller_Email varchar(20),Listing_ID varchar(20),Review_Desc varchar(20)) '
                           'VALUES (?, ?, ?, ?);',
        (Buyer_Email,Seller_Email,Listing_ID,Review_Desc))
    connection.commit()
    cursor2 = connection.execute('SELECT * FROM users;')
    #return cursor2.fetchall()

def load_sellers(email,routing_number,account_number,balance):
    connection = sql.connect('database.db')
    cursor = connection.cursor()
    connection.execute('CREATE TABLE IF NOT EXISTS Sellers(email varchar(20), routing_number INTEGER, account_number varchar(20), balance REAL, '
                       'PRIMARY KEY (email), '
                       'FOREIGN KEY(email) REFERENCES Buyers(email));')
    for(email,routing_number,account_number,balance) in cursor:
        connection.execute('INSERT INTO Sellers (email varchar(20),routing_number INTEGER, account_number varchar(20), balance REAL)'
                           'VALUES (?, ?, ?, ?);', (email,routing_number,account_number,balance))
    connection.commit()
    cursor2 = connection.execute('SELECT * FROM users;')
    #return cursor2.fetchall()

def load_users(email, password):
    connection = sql.connect('database.db')
    cursor = connection.cursor()
    connection.execute('CREATE TABLE IF NOT EXISTS Users(email varchar(20),password varchar(20), PRIMARY KEY(email);')
    for(email,password) in cursor:
        connection.execute('INSERT INTO Users (email varchar(20),password varchar(20))'
                           'VALUES (?, ?);',
        (email, password))
    connection.commit()
    cursor2 = connection.execute('SELECT * FROM users;')
    #return cursor2.fetchall()

def load_zipcodeInfo(zipcode, city, state_id, population, density, county_name, timezone):
    connection = sql.connect('database.db')
    cursor = connection.cursor()
    connection.execute('CREATE TABLE IF NOT EXISTS ZipcodeInfo(zipcode REAL, city varchar(20), state_id varchar(20), population varchar(20), density REAL, '
                       'county_name varchar(20), timezone varchar(20), PRIMARY KEY(zipcode);')
    for(zipcode,city,state_id,population,density,county_name,timezone) in cursor:
        connection.execute('INSERT INTO ZipcodeInfo (zipcode REAL, city varchar(20), state_id varchar(20), population varchar(20), density REAL, '
                           'county_name varchar(20), timezone varchar(20))'
                           'VALUES (?, ?, ?, ?, ?, ?, ?);',
        (zipcode,city,state_id,population,density,county_name,timezone))
    connection.commit()
    cursor2 = connection.execute('SELECT * FROM users;')
    #return cursor2.fetchall()
'''



