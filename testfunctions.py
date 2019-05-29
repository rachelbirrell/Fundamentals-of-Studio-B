from databasefunctions import *

cnxn = connecting_to_postgresql()

# only run once
# create_customer_table(cnxn)

# only run once
# create_menu_table(cnxn)

Customer_Info = "Customer_Info"
name = "John"
photo = "B"

get_latest_ref_id(cnxn, Customer_Info)

create_new_customer(cnxn, Customer_Info, name, photo)

print_table(cnxn, Customer_Info)