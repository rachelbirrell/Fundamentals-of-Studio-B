## This file contains all of the required code to set up a new database on the 
## system. 

import databasefunctions as dbf

database_name = "StudioTest"
password = "password"
port = 5432


cnxn = dbf.connecting_to_postgresql(database_name, password, port)
dbf.create_customer_table(cnxn)
dbf.create_menu_table(cnxn)
dbf.add_items_to_menu(cnxn)

dbf.print_table(cnxn, "Customer_Info")
dbf.print_table(cnxn, "Menu")
