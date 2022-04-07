import uuid
from flask import Flask, render_template, request, redirect
import sqlite3 as sql
import pandas as pd
import os
import hashlib

app = Flask(__name__)

host = 'http://127.0.0.1:5000/'
connection = sql.connect('database.db')

@app.route('/', methods=['POST', 'GET'])
def index():
    stringVal = ""
    if request.method == 'POST':
        credentials = checkCredentials(request.form['Email'], request.form['Password'])
        if credentials:
            stringVal = "success"
            return redirect('/success')
        elif credentials == False:
            stringVal = "failure"
    return render_template('index.html')

@app.route('/success', methods = ['POST', 'GET'])
def loginSuccess():
    error = None
    if request.method == 'POST':
        redirect('/checkingInfo')

    return render_template('authenticated.html', error = error)

@app.route('/checkinginfo', methods = ['POST', 'GET'])
def checkingInfoView(emailAddress, password):
    cur = connection.cursor()
    cur.execute("Select name, emailID, age, gender, emailAddress, homeAddress, billingAddress, creditCard FROM Users WHERE "
                "u.ï»¿email = ? AND password = ?", (emailAddress, password,))
    return render_template('checking_info.html')

#check user input password with database password
def checkPasswords(userPassword, dbPassword):
    #password in db is not hashed
    #user entry not hashed
    #if success --> hash
    #password = userPassword
    #password2 = dbPassword

    #salt = uuid.uuid4().hex
    #hashed = hashlib.sha3_256(salt.encode() + password.encode()).hexdigest()
    #hashed2 = hashlib.sha3_256(salt.encode() + password2.encode()).hexdigest()

    #return (hashed == dbPassword)
    return (userPassword == dbPassword)

def checkCredentials(email, passwordUser):
    connection = sql.connect('database.db')
    cur = connection.cursor()
    cur.execute("Select * FROM Users")
    print(cur.fetchall())
    #cursor = connection.execute('Select password FROM Users u WHERE u.email = ?;', (email))
    cursor = connection.execute('Select password FROM Users u WHERE u.ï»¿email = ?;', (email,))
    singularPasswordDB = cursor.fetchone()
    # if email does not exist --> return False
    if(singularPasswordDB == None):
        return False #the password for an email (pre-hash)
    print(singularPasswordDB)
    return checkPasswords(passwordUser, singularPasswordDB[0])

#create load_address
def createDatabases():
    #a+ open for reading and writing, file created if does not exist
    #if does exist --> pass
    #if doesn't exist --> create
    with open('database.db', 'a+') as d:
        pass

    connection = sql.connect('database.db')
    cursor = connection.cursor()

    # create load_users
    connection.execute('CREATE TABLE IF NOT EXISTS Users(email TEXT, password TEXT, PRIMARY KEY(email));')


    # create zipcode_info
    connection.execute(
        'CREATE TABLE IF NOT EXISTS ZipcodeInfo(zipcode REAL, city text, state_id text, population text, density REAL, '
        'county_name text, timezone text, PRIMARY KEY(zipcode));')

    #create load_address
    cursor.execute('CREATE TABLE IF NOT EXISTS Address(address_id text, zipcode REAL,street_num REAL,street_name text,'
                    'PRIMARY KEY(address_id), FOREIGN KEY(zipcode) REFERENCES ZipcodeInfo(zipcode));')

    #create load buyers
    cursor.execute('CREATE TABLE IF NOT EXISTS Buyers(email text, first_name text, last_name text, gender text,'
                    'age REAL,home_address_id REAL, billing_address_id REAL, PRIMARY KEY(email),FOREIGN KEY(email) REFERENCES Users(email), '
                    'FOREIGN KEY(home_address_id) REFERENCES Address(address_id), FOREIGN KEY(billing_address_id) REFERENCES Address(address_id));')

    # create load_credit_cards
    connection.execute(
        'CREATE TABLE IF NOT EXISTS CreditCard(credit_card_num INTEGER, card_code text,expire_month text, expire_year text, '
        'card_type text, owner_email text, PRIMARY KEY(credit_card_num), FOREIGN KEY(owner_email) REFERENCES Buyers(email));')

    # create load_sellers
    connection.execute(
        'CREATE TABLE IF NOT EXISTS Sellers(email text, routing_number INTEGER, account_number text, balance REAL, '
        'PRIMARY KEY (email), '
        'FOREIGN KEY(email) REFERENCES Buyers(email));')

    #create local_vendor
    connection.execute(
        'CREATE TABLE IF NOT EXISTS Vendors(email text, business_name text, business_address_ID text, customer_service_number text, '
        'PRIMARY KEY(email), '
        'FOREIGN KEY(email) REFERENCES Sellers(email),'
        'FOREIGN KEY(business_address_ID) REFERENCES Address(address_id));')

    #create load categories
    cursor.execute('CREATE TABLE IF NOT EXISTS Categories(parent_category text, category_name text, PRIMARY KEY(category_name));')

    # create load_product_listing
    connection.execute(
        'CREATE TABLE IF NOT EXISTS Product_Listing(seller_email text, listing_ID REAL, category text, title text, '
        'product_name text, product_description text, price REAL, quantity REAL, PRIMARY KEY(seller_email, listing_id));')

    #create load_orders
    connection.execute('CREATE TABLE IF NOT EXISTS Orders(transaction_ID REAL, seller_email text, listing_ID REAL, buyer_email text, '
                        'date text, quantity REAL, payment REAL, PRIMARY KEY(transaction_id), '
                        'FOREIGN KEY(seller_email, listing_id) REFERENCES Product_Listings(seller_email, listing_id), '
                        'FOREIGN KEY(buyer_email) REFERENCES Buyers(email));')

    # create load_reviews
    connection.execute(
        'CREATE TABLE IF NOT EXISTS Reviews(Buyer_Email text,Seller_Email text,Listing_ID text,Review_Desc text, '
        'PRIMARY KEY(buyer_email, seller_email, listing_id), '
        'FOREIGN KEY(buyer_email) REFERENCES Buyers(email), '
        'FOREIGN KEY(seller_email, listing_id) REFERENCES Product_Listings(seller_email, listing_id));')

    #create load_ratings
    connection.execute('CREATE TABLE IF NOT EXISTS Ratings(Buyer_Email text, Seller_Email text, Date text, Rating INTEGER, Rating_Desc text, '
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
        #connection means getting connection
        #if_exists --> if table already exists, drop it and create new one
        #index = false refers to renaming the column
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



