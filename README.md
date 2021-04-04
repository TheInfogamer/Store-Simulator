# Store-Simulator
A Python-MySQL command console based Store simulator to satisfy all your virtual shopping needs

This is a program designed to emulate The shopping experience.
The simulator runs by having the user input simple words/numbers into the command console

# Features

2 sides to the program.
A 'customer' side for main shopping purposes. No login required
A 'Manager' side for updating and maintaining backend MySQL tables through passing queries. Password protected

Customer has the choice of shopping from 2 sections(for now)- Grocery or stationery
Shopping catalogue is a 'book-style' catalogue with 5 items per 'page' and can be cycled through to show all purchaseable items
Cart system where all items selected will get placed in a cart for buying all at once at checkout
Optional Receipt on checkout with all taxes calculated.
Semi-credit system where you can pay atleast half of the total amount and rest is bought by credit.(paying back credit not implemented yet)

Manager can manage grocery/stationery products and prices and can delete products(wip)

# Prerequisite Python modules:
1) pandas
2) SQLAlchemy
3) numpy
4) PyMySql
5) python-dateutil
6) mysql-connector
7) cryptography

You will also need to have MySQL installed.

# Instructions to run the simulator
1) Open mysql and type this command:
create database storesim;
2) within the folder itself, right click on Storesim_table_creator.py and select edit with IDLE/ Your preferred IDE
3) in the 6th line replace 'user' with your MySQL username and 'password' with your MySQL password.
4) Now run the storesim_table_creator.py After it runs successfully, close it.
5) within the folder itself, right click on storesim.py and edit with IDLE/ Your preferred IDE and run it.
6) Congrats, It should now be launching
