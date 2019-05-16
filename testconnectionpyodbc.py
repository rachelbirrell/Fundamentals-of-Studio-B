
import pyodbc


# PASS AN ODBC CONNECTION STRING TO THE CONNECT() FUNCTION TO RETURN 
# A CONNECTION, THEN YOU CAN ASK FOR A CURSOR

conn_str = (
	"DRIVER={PostgreSQL Unicode};"
	"DATABASE=studioB;"
	"UID=postgres;"
	"PWD=password;"
	"SERVER=localhost;"
	"PORT=5432;"
	)


# Specifying the ODBC driver, server name, database, etc. directly
cnxn = pyodbc.connect(conn_str)

print('connection successful')

# Driver naturally defaults to 255-byte maximum varchar size for writes
# which is very slow. Hence setting it to something bigger.
cnxn.maxwrite = 1024 * 1024 * 1024

# Decodes all the PostgreSQL text data and re-encodes it to UTF-8
cnxn.setdecoding(pyodbc.SQL_WCHAR, encoding='utf-8')
cnxn.setencoding(encoding='utf-8')

# enabling commit means that all work will be kept even if the connection
# object is closed
cnxn.commit()


################################################################################
# create table - CUSTOMER INFO

# cursor = cnxn.cursor()
# create_table = "CREATE TABLE Customer_Info(ref_id int, cust_name varchar);"
# cursor.execute(create_table)
# cnxn.commit()


################################################################################
# create table - MENU

menu_subtitles = input("Please enter the different categories in the menu, "
	"each seperate by a comma this will create a database for each of the "
	"categories.")

# menu subtitles in a string of words seperated by a comma, make this into a list
subtitles = menu_subtitles.split(",")

cursor = cnxn.cursor()
create_table = "CREATE TABLE Menu(ref_id int)"
cursor.execute(create_table)
cnxn.commit()


cursor = cnxn.cursor()
for i in range(len(subtitles)):
	subtitle = subtitles[i]
	"ALTER TABLE Menu ADD %s varchar" %subtitle
	cursor.execute(create_table)

cnxn.commit()


################################################################################
# if new customer and they would like to set up an account

# full_name = "Rachel_Birrell"

# cursor = cnxn.cursor()
# insert_customer = "INSERT INTO Customer_Info(ref_id, cust_name) VALUES(1, %s)" %full_name
# cursor.execute(insert_customer)
# cnxn.commit()

