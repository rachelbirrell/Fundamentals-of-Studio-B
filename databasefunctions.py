

from datetime import datetime
from PIL import Image

import pyodbc, base64, io, random 




################################################################################
# Connect to the PostgreSQL database

def connecting_to_postgresql(name, pwd, port):

	conn_str = (
	"DRIVER={PostgreSQL Unicode};"
	"DATABASE=" + name + ";"
	"UID=postgres;"
	"PWD=" + pwd + ";"
	"SERVER=localhost;"
	"PORT=" + str(port) + ";"
	)

	cnxn = pyodbc.connect(conn_str)

	cnxn.maxwrite = 1024 * 1024 * 1024
	cnxn.setdecoding(pyodbc.SQL_WCHAR, encoding='utf-8')
	cnxn.setencoding(encoding='utf-8')

	cnxn.commit()

	return cnxn


################################################################################
# create table - CUSTOMER INFO - RUN ONCE

def create_customer_table(cnxn):

	cursor = cnxn.cursor()
	cursor.execute("""
		CREATE TABLE Customer_Info(ref_id serial, cust_name varchar, \
		photo varchar, previous_order1 varchar, previous_order2 varchar, \
		previous_order3 varchar, date_last_visit date);
		""")
	cnxn.commit()


################################################################################
# create table - MENU - RUN ONCE

def create_menu_table(cnxn):

	cursor = cnxn.cursor()
	cursor.execute("""
		CREATE TABLE Menu(food_item varchar, \
		item_cost int, item_type varchar);
		""")
	cnxn.commit()


################################################################################
# add items to menu

def add_items_to_menu(cnxn):

	food_items = ["coffee", "hot chocolate", "milkshake", "burger", "pizza",
		"burrito", "ice cream", "brownie", "pancakes"]
	food_prices = [4, 3, 5, 10, 15, 8, 5, 4, 10]
	food_category = ["drink", "drink", "drink", "food", "food", "food",
		"dessert", "dessert", "dessert"]

	cursor = cnxn.cursor()

	for i in range(len(food_items)):
		cursor.execute("""
			INSERT INTO Menu(food_item, item_cost, item_type) \
			VALUES (?, ?, ?)
			""", food_items[i], food_prices[i], food_category[i])

	cnxn.commit()


################################################################################
# get the latest (maximum) ref_num and return it

# def get_latest_ref_id(cnxn, database_table):

# 	cursor = cnxn.cursor()

# 	if database_table == "Customer_Info":
# 		cursor.execute("""
# 			SELECT MAX(ref_id)
# 			FROM Customer_Info
# 			""")
# 		ref_num = cursor.fetchone()
# 		return int(ref_num[0])

# 	elif database_table == "Menu":
# 		cursor.execute("""
# 			SELECT MAX(ref_id)
# 			FROM Menu
# 			""")
# 		ref_num = cursor.fetchone()
# 		return int(ref_num[0])

# 	else:
# 		print("There is no database with this name.")

# 	cnxn.commit()


################################################################################
# if face recognition doesn't work, create new customer

def create_new_customer(cnxn, name, path_to_file, order_list):

	# ref_num = get_latest_ref_id(cnxn, database) + 1
	date = datetime.today().strftime('%Y-%m-%d')

	comma = ","
	order_string = comma.join(order_list)

	file = open(path_to_file, 'rb')
	img_content = file.read()
	img_to_b64 = base64.b64encode(bytes(img_content))
	file.close()

	cursor = cnxn.cursor()
	cursor.execute(""" 
		INSERT INTO Customer_Info(cust_name, photo, previous_order1, date_last_visit)
		VALUES (?, ?, ?, ?)
		""", (name, img_to_b64, order_string, date))

	cnxn.commit()


################################################################################
# Print the table from the database

def print_table(cnxn, database_table):

	cursor = cnxn.cursor()

	if database_table == "Customer_Info":
		print("This is the data contained within the Customer Info table:")

		cursor.execute("""
			SELECT *
			FROM Customer_Info
			""")
		rows = cursor.fetchall()

		for row in rows:
			print(row.ref_id, row.cust_name, row.photo, row.previous_order1,
				row.previous_order2, row.previous_order3, row.date_last_visit)


	elif database_table == "Menu":
		print("This is the data contained within the Menu table:")

		cursor.execute("""
			SELECT *
			FROM Menu
			""")
		rows = cursor.fetchall()

		for row in rows:
			print(row.food_item, row.item_cost, row.item_type)


	else:
		print("There is no database with this name.")

	cnxn.commit()


################################################################################
# Inserting an image - inserts the image without a bracket 

def add_image(cnxn, name, path_to_file):

	file = open(path_to_file, 'rb')
	img_content = file.read()
	img_to_b64 = base64.b64encode(bytes(img_content))
	file.close()

	cursor = cnxn.cursor()
	cursor.execute("""
			INSERT INTO Customer_Info(cust_name, photo)
			VALUES (?, ?)
			""", (name, img_to_b64))		
	cnxn.commit()


################################################################################
# Reading an image - fetches the customers image (returns it to us in bytea)

def retrieve_images(cnxn):

	cursor = cnxn.cursor()

	cursor.execute("""
			SELECT ref_id, photo
			FROM Customer_Info 
			""")
	rows = cursor.fetchall()

	for row in rows:
		database_img = base64.b64decode(row.photo)
		outfile = '%s.jpg' %("photo" + str(row.ref_id))
		f = open(outfile, 'wb')
		f.write(database_img)
		f.close

	cnxn.commit()



################################################################################
# PostgreSQL delete Data

def delete_data(cnxn):

	cursor = cnxn.cursor()
	cursor.execute("""
			DELETE FROM Customer_Info
			""")		
	cnxn.commit()



################################################################################
# Get the latest (maximum) previous order number return it, it will return 
# a number when the colum is empty. Hence we can use this column to store 
# the next order. 

def get_latest_previous_order_num(cnxn, name):

	cursor = cnxn.cursor()

	cursor.execute("""
		SELECT (cust_name, previous_order1, previous_order2, previous_order3)
		FROM Customer_Info
		""")
	rows = cursor.fetchall()

	for row in rows:
		if row.cust_name == name:
			if row.previous_order1 == "":
				return 1
			elif row.previous_order2 == "":
				return 2
			elif row.previous_order3 == "":
				return 3

	cnxn.commit()


################################################################################
# Store previous order
# Write function to store order, input order as a list of the items, store in 
# database as a string seperating each value with a comma. 


def store_order(cnxn, name, order_list):

	order_num = get_latest_previous_order_num(cnxn, name)

	comma = ","
	order_string = comma.join(order_list)

	cursor = cnxn.cursor()

	if order_num == 1:
		cursor.execute("""
				INSERT INTO Customer_Info(cust_name, previous_order1)
				VALUES (?, ?) 
				""", (name, order_string))

	elif order_num == 2:
		cursor.execute("""
				INSERT INTO Customer_Info(cust_name, previous_order2)
				VALUES (?, ?) 
				""", (name, order_string))	

	elif order_num == 3:
		cursor.execute("""
				INSERT INTO Customer_Info(cust_name, previous_order3)
				VALUES (?, ?) 
				""", (name, order_string))	

	cnxn.commit()


################################################################################
# Retrieve previous order
# Write function to retrieve all of the previous orders, if applicable. The 
# orders are stored as a string separated by commas, need to read each string 
# and separate and return as list.  

def retrieve_orders(cnxn, name):

	previous_order1 = ""
	previous_order2 = ""
	previous_order3 = ""

	cursor = cnxn.cursor()
	cursor.execute("""
			SELECT (cust_name, previous_order1, previous_order2, previous_order3) 
			FROM Customer_Info 
			""")
	rows = cursor.fetchall()

	for row in rows:
		if row.cust_name == name:
			previous_order1 = row.previous_order1.split(",")
			previous_order2 = row.previous_order2.split(",")
			previous_order3 = row.previous_order3.split(",")

	cnxn.commit()