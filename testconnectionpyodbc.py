
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


# Create a cursor from the connection
cursor = cnxn.cursor()