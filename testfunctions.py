from databasefunctions import *

database_name = "StudioTest"
password = "password"
port = 5432


cnxn = connecting_to_postgresql(database_name, password, port)


#print(get_latest_previous_order_num(cnxn, "Rachel"))

# retrieve_images(cnxn)




#Customer_Info = "Customer_Info"
#name = "John"
#photo = "B"
#filename = "john_profile.jpg"

#get_latest_ref_id(cnxn, Customer_Info)

# create_new_customer(cnxn, "Elon Musk", "elonphoto.png", 
# 	["milkshake", "pizza", "pancakes"])

# create_new_customer(cnxn, "Rachel Birrell", "rachelphoto.jpg", 
# 	["coffee", "burger", "pancakes"])



#add_customer_image(filename)

#delete_data(cnxn)

#print_table(cnxn, "Customer_Info")

# add_image(cnxn, 'Nick', 'john_profile.jpg')

retrieve_images(cnxn)

# read_cust_image(cnxn, 'Ray')

#verify_image(cnxn, 'john_profile.jpg')
#