CREATE TABLE Users(email varchar(20), password char(20), PRIMARY KEY(email));

CREATE TABLE Buyers(email varchar(20), first_name varchar(20), last_name varchar(20), gender char(5), age integer, home_address_id integer, billing_address_id integer,
PRIMARY KEY(email), FOREIGN KEY(email) REFERENCES Users(email), FOREIGN KEY(home_address_id) REFERENCES Address(address_id), FOREIGN KEY(billing_address_id) REFERENCES Address(address_id));

CREATE TABLE Credit_Cards(credit_card_num integer, card_code varchar(20), expire_month varchar(3), expire_year integer, card_type varchar(20), owner_email char(20), PRIMARY KEY(credit_card_num),
FOREIGN KEY(owner_email) REFERENCES Buyers(email));

CREATE TABLE Address(address_ID integer, zipcode integer, street_num integer, street_name varchar(20), PRIMARY KEY(address_ID), FOREIGN KEY(zipcode) REFERENCES Zipcode_Info(zipcode));

CREATE TABLE Zipcode_Info(zipcode integer, city varchar(30), state_id integer, population integer, density integer, county_name varchar(30), timezone varchar(10), PRIMARY KEY(zipcode));

CREATE TABLE Sellers(email varchar(20), routing_number integer, account_number integer, balance decimal, PRIMARY KEY (email), FOREIGN KEY(email) REFERENCES Buyers(email));

CREATE TABLE Local_Vendors(email varchar(20), business_name varchar(20), business_address_id integer, customer_service_number varchar(20), PRIMARY KEY(email), FOREIGN KEY(email) REFERENCES Sellers(email),
FOREIGN KEY(business_address_ID) REFERENCES Address(address_id));

CREATE TABLE Categories(parent_category varchar(10), category_name varchar(15), PRIMARY KEY(category_name));

CREATE TABLE Product_Listings(seller_email varchar(20), listing_id integer, category varchar(20), title varchar(10), product_name varchar(15), product_description varchar(50), price decimal,
quantity integer, PRIMARY KEY(seller_email, listing_id));
#FOREIGN KEY(seller_email) REFERENCES Sellers(email), FOREIGN KEY(category) REFERENCES Categories(category_name)

CREATE TABLE Orders(transaction_id integer, seller_email varchar(20), listing_id integer, buyer_email varchar(20), date varchar(20), quantity integer, payment decimal, PRIMARY KEY(transaction_id),
FOREIGN KEY(seller_email) REFERENCES Product_Listings(seller_email), FOREIGN KEY(listing_id) REFERENCES Product_Listings(seller_email), FOREIGN KEY(buyer_email) REFERENCES Buyers(email));

CREATE TABLE Reviews(buyer_email varchar(20), seller_email varchar(20), listing_id integer, review_desc varchar(50), PRIMARY KEY(buyer_email, seller_email, listing_id),
FOREIGN KEY(buyer_email) REFERENCES Buyers(email), FOREIGN KEY(seller_email, listing_id) REFERENCES Product_Listings(seller_email, listing_id));

CREATE TABLE Rating(buyer_email varchar(20), seller_email varchar(20), date varchar(20), rating varchar(20), rating_desc varchar(50), PRIMARY KEY(buyer_email, seller_email, date),
FOREIGN KEY(buyer_email) REFERENCES Buyers(email), FOREIGN KEY(seller_email) REFERENCES Sellers(email));


Order:
Users
Zipcode_Info
Address
Buyers
Credit_Cardss
sellers
local
categorits
product listing_id
orders
reviews
rating
