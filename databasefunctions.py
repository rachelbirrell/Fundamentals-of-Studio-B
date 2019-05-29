
import pyodbc
from datetime import datetime


################################################################################
# Connect to the PostgreSQL database

def connecting_to_postgresql():

	conn_str = (
	"DRIVER={PostgreSQL Unicode};"
	"DATABASE=studioB;"
	"UID=postgres;"
	"PWD=password;"
	"SERVER=localhost;"
	"PORT=5432;"
	)

	cnxn = pyodbc.connect(conn_str)

	cnxn.maxwrite = 1024 * 1024 * 1024
	cnxn.setdecoding(pyodbc.SQL_WCHAR, encoding='utf-8')
	cnxn.setencoding(encoding='utf-8')

	cnxn.commit()

	return cnxn


################################################################################
# create table - CUSTOMER INFO

def create_customer_table(cnxn):

	cursor = cnxn.cursor()
	cursor.execute("""
		CREATE TABLE Customer_Info(ref_id int, cust_name varchar, \
		photo bytea, previous_order1 varchar, previous_order2 varchar, \
		previous_order3 varchar, date_last_visit date);
		""")
	cnxn.commit()

	return None


################################################################################
# create table - MENU

def create_menu_table(cnxn):

	cursor = cnxn.cursor()
	cursor.execute("""
		CREATE TABLE Menu(ref_id int, food_item varchar, \
		item_cost int, item_type varchar);
		""")
	cnxn.commit()

	return None


################################################################################
# get the latest (maximum) ref_num and return it

def get_latest_ref_id(cnxn, database_table):

	cursor = cnxn.cursor()

	if database_table == "Customer_Info":
		cursor.execute("""
			SELECT MAX(ref_id)
			FROM Customer_Info
			""")
		ref_num = cursor.fetchone()
		return int(ref_num[0])

	elif database_table == "Menu":
		cursor.execute("""
			SELECT MAX(ref_id)
			FROM Menu
			""")
		ref_num = cursor.fetchone()
		return int(ref_num[0])

	else:
		print("There is no database with this name.")
		return None

	cnxn.commit()


################################################################################
# if face recognition doesn't work, create new customer

def create_new_customer(cnxn, database, name, photo):

	ref_num = get_latest_ref_id(cnxn, database) + 1
	date = datetime.today().strftime('%Y-%m-%d')

	cursor = cnxn.cursor()
	cursor.execute(""" 
		INSERT INTO Customer_Info(ref_id, cust_name, photo, date_last_visit)
		VALUES (?, ?, ?, ?)
		""", (ref_num, name, photo, date))

	cnxn.commit()

	return None


################################################################################
# Print the table from the database

def print_table(cnxn, database_table):

	print("This is the data contained within the Customer Info table:")

	cursor = cnxn.cursor()

	if database_table == "Customer_Info":
		cursor.execute("""
			SELECT *
			FROM Customer_Info
			""")
		rows = cursor.fetchall()

	elif database_table == "Menu":
		cursor.execute("""
			SELECT *
			FROM Menu
			""")
		rows = cursor.fetchall()

	else:
		print("There is no database with this name.")

	
	for row in rows:
		print(row.ref_id, row.cust_name, row.photo)

	cnxn.commit()

	return None

################################################################################