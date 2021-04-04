import pandas as pd
from datetime import datetime
import random
import sqlalchemy as sq
import Storesim_table_creator as lib2

con = lib2.con
connection = con.raw_connection()
cursor = connection.cursor()
cursor2 = connection.cursor()
cursor0 = connection.cursor()
cursor_stationery = connection.cursor()
cursor_manager = connection.cursor()

column_names = ["Product_no", "Product_Name", "Price"]
cart_column_names = ["Product_no", "Product_Name", "Amount", "Price"]

def welcome():
    wel = ["Hello and welcome to the store simulation software!",
         "Hey there, welcome to the store simulation software!",
         "Welcome back to the store simulation software, How shall we be of service?"]
    print(random.choice(wel))


def manager_menu():
    print("\nWelcome to the Shop editor menu, Where you can change products or edit prices")
    print("\n-----Manager Menu-----"
          "\n1-View:View the catalogue of items"
          "\n2-Editproduct:Edit a products name or replace products with another one."
          "\n3-Editprice:Edit a product's price"
          "\n4-log out")
    manager_menu_choice = input("")
    if (manager_menu_choice == "1") or (manager_menu_choice.lower() == "view"):
        view = input("view Grocery or Stationery?")
        if view.lower() == "grocery":
            viewgrocery = pd.read_sql("select product_no ,product_name, price from grocery", con=con)
            print(viewgrocery.to_string(index=False))
            back = input("Type back to return to menu")
            if back.lower() == "back":
                manager_menu()
        elif view.lower() == "stationery":
            viewstationery = pd.read_sql("select product_no, product_name, price from stationery", con=con)
            print(viewstationery.to_string(index=False))
            back = input("Type back to return to menu")
            if back.lower() == "back":
                manager_menu()

        else:
            print("invalid option")
            manager_menu()

    elif (manager_menu_choice == "2") or (manager_menu_choice.lower() == "editproduct"):
        editproduct = input("Edit Grocery or Stationery?")
        if editproduct.lower() == "grocery":
            edit_name = str(input("Enter the name of the product that you want  to replace(case sensitive)"))
            new_name = str(input("Enter the new name of the product"))
            cursor_manager.execute("update grocery set product_name='"+new_name+"'where product_name='"+edit_name+"'")
            connection.commit()
            print(edit_name, "Successfully replaced with", new_name)
            manager_menu()

        elif editproduct.lower() == "stationery":
            edit_name = str(input("Enter the name of the product that you want  to replace(case sensitive)"))
            new_name = str(input("Enter the new name of the product"))
            cursor_manager.execute("update stationery set product_name='"+new_name+"'where product_name='"+edit_name+"'")
            connection.commit()
            print("Price of",edit_name, "successfully replaced with", new_name)
            manager_menu()

        else:
            print("invalid option")
            manager_menu()

    elif (manager_menu_choice == "3") or (manager_menu_choice.lower() == "editprice"):
        editproduct = input("Edit Grocery or Stationery?")
        if editproduct.lower() == "grocery":
            edit_no = str(input("Enter the product no. of the product which the price is to be replaced"))
            new_price = str(input("Enter the new price of the product"))
            cursor_manager.execute("update grocery set Price='" + new_price + "'where product_no='" + edit_no + "'")
            connection.commit()
            print("Price successfully replaced with", new_price)
            manager_menu()

        elif editproduct.lower() == "stationery":
            edit_no = str(input("Enter the name of the product which the price is to be replaced"))
            new_price = str(input("Enter the new price of the product"))
            cursor_manager.execute("update stationery set Price='" + new_price + "'where product_no='" + edit_no + "'")
            connection.commit()
            print("Price successfully replaced with", new_price)
            manager_menu()

        else:
            print("invalid option")
            manager_menu()

    elif (manager_menu_choice == "4") or (manager_menu_choice.lower() == "logout"):
        print("Logging out...")
        welcome()
        login()

    else:
        print("invalid option")
        manager_menu()


def manager():
    user_name=input("\nEnter your Admin provided user name:")
    password=input("\nEnter your Admin provided password")
    if (user_name.lower()=="root") and (password.lower()=="incorrect"):
        print("Successfully Logged in as Manager")
        manager_menu()

    else:
        retry = input("\nincorrect password or username. Type retry to try again or type back to go back")
        if retry.lower() == "retry":
            manager()
        elif retry.lower() == "back":
            login()


def nextpage():
    allrows = cursor.fetchmany(5)
    df1 = pd.DataFrame(allrows, columns=column_names)
    print(df1.to_string(index=False))


def nextpage_stationery():
    allrows = cursor_stationery.fetchmany(5)
    df1 = pd.DataFrame(allrows, columns=column_names)
    print(df1.to_string(index=False))

def purchase():
    print("\nHere is a preview of your cart:")
    cart_data = pd.read_sql("select product_no, product_name, amount, price, sum(amount*price) as total from cart group by product_name", con=con)
    print(cart_data.to_string(index=False))
    confirm = input("\nIf you want to continue, type continue or type cancel to return back")
    if confirm == "continue":
        customer_name = input("Enter your name")
        total_amt_df = pd.read_sql("select amount * price as total from cart", con=con)
        total_amt = total_amt_df['total'].sum()
        cgst = (total_amt*9/100)
        sgst = (total_amt*9/100)
        net_amt = total_amt+cgst+sgst
        print("Calculating amount to be paid.")
        print("\nBase amount:", total_amt)
        print("Tax amount:", (cgst+sgst))
        print("Net amount to be paid:", net_amt)

        def payment():
            paid = int(input("Enter amount to be paid"))
            if paid == net_amt:
                if_receipt = input("Thank you for your purchase. Type 'Receipt' to view a digital copy of your receipt")
                balance = 0
                unpaid = 0
                if if_receipt.lower() == "receipt":
                    print("_____________________________________________________________________________________")
                    print("                                    Retail Invoice                                   ")
                    now = datetime.now()
                    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
                    print("\nDate and Time of transaction", dt_string)
                    print("\nInvoice Number:", random.randint(10000, 99999))
                    print("\nCustomer Name:", customer_name)
                    receipt_preview = pd.read_sql(
                        "select Product_name,Amount,Price,sum(Amount*Price) as Total from cart group by Product_name",
                        con=con)
                    print(receipt_preview.to_string(index=False))
                    print("Base Amount:", total_amt)
                    print("Tax Amount(18% GST):", cgst + sgst)
                    print("\n\nAmount Paid by user:", paid)
                    print("Amount to be refunded:", balance)
                    print("Amount outstanding:", unpaid)
                    print("\n\nThank you for shopping with the Store simulation software.")
                    print("_____________________________________________________________________________________")
                    final_choice = str(input("Type 'return' to go back to login screen or press any key to exit program"))
                    if final_choice.lower() == "return":
                        welcome()
                        login()
                else:
                    exit()

            elif paid < (net_amt / 2):
                print("You must pay at least 50% of Net amount to avail credit facility")
                payment()

            elif paid > net_amt:
                if_receipt = input("Thank you for your purchase. Your balance will be returned. Type 'Receipt' to view a digital copy of your receipt")
                balance = paid-net_amt
                unpaid = 0
                if if_receipt.lower() == "receipt":
                    print("_____________________________________________________________________________________")
                    print("                                    Retail Invoice                                   ")
                    now = datetime.now()
                    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
                    print("\nDate and Time of transaction", dt_string)
                    print("\nInvoice Number:", random.randint(10000, 99999))
                    print("\nCustomer Name:", customer_name)
                    receipt_preview = pd.read_sql(
                        "select Product_name,Amount,Price,sum(Amount*Price) as Total from cart group by Product_name",
                        con=con)
                    print(receipt_preview.to_string(index=False))
                    print("Base Amount:", total_amt)
                    print("Tax Amount(18% GST):", cgst + sgst)
                    print("\n\nAmount Paid by user:", paid)
                    print("Amount to be refunded:", balance)
                    print("Amount outstanding:", unpaid)
                    print("_____________________________________________________________________________________")
                else:
                    exit()

            elif (paid >= (net_amt / 2)) and (paid < net_amt):
                if_receipt = input("Thank you for your purchase. The remaining amount will have to be paid at a later date. Type 'Receipt' to view a digital copy of your receipt")
                unpaid = net_amt-paid
                balance=0
                if if_receipt.lower() == "receipt":
                    print("_____________________________________________________________________________________")
                    print("                                    Retail Invoice                                   ")
                    now = datetime.now()
                    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
                    print("\nDate and Time of transaction", dt_string)
                    print("\nInvoice Number:", random.randint(10000, 99999))
                    print("\nCustomer Name:", customer_name)
                    receipt_preview = pd.read_sql(
                        "select Product_name,Amount,Price,sum(Amount*Price) as Total from cart group by Product_name",
                        con=con)
                    print(receipt_preview.to_string(index=False))
                    print("Base Amount:", total_amt)
                    print("Tax Amount(18% GST):", cgst+sgst)
                    print("\n\nAmount Paid by user:", paid)
                    print("Amount to be refunded:", balance)
                    print("Amount outstanding:", unpaid)
                    print("_____________________________________________________________________________________")
                else:
                    exit()
        payment()


def grocery_store():
    print("\nWelcome to the Grocery section. Here you will find food items and other edible products.\nPlease make a choice from the menu below by typing corresponding number\n1-View catalogue of available groceries\n2-go back to previous page")
    gchoice = input("Make a choice:")
    if gchoice=="1":
        cursor.execute("select Product_no, Product_name, Price from grocery")
        n = 1
        nextpage()
        while True:
            print("Currently viewing page:", n, "of 5")
            if_purchased = input("\nNext-view next 5 items\nBuy-to add a product to your cart\nCart-to view the contents of your cart\nPurchase-To purchase everything from your cart\nBack-to return to previous menu")
            if if_purchased.lower() == "buy":
                item_purchased = input("Enter the product no. of item you want to purchase")
                amount_purchased = input("How many of that item would you like?")
                cursor2.execute("select * from grocery")
                cursor2.execute("insert into cart select * from grocery where Product_No='" + item_purchased + "'")
                cursor2.execute("update cart set Amount='"+amount_purchased+"'where Product_No='" + item_purchased + "'")
                connection.commit()
                cursor2.execute("select product_name from cart where Product_No='" + item_purchased + "'")
                item = cursor2.fetchone()
                print("\n", amount_purchased, item, "added to cart!\n")

            elif (if_purchased.lower()=="next") and (n<5):
                n=n+1
                nextpage()

            elif n==5:
                cursor.execute("select Product_no,Product_name,Price from grocery")
                n = 1
                nextpage()

            elif if_purchased.lower() == "cart":
                cart_data=pd.read_sql_table("cart", con)
                print(cart_data.to_string(index=False))

            elif if_purchased.lower() == "back":
                customer()

            elif if_purchased.lower() == "purchase":
                purchase()
                break

            else:
                print("\ninvalid option. Please try again")

    elif gchoice=="2":
        customer()

    else:
        customer()


def stationery_store():
    print("\nWelcome to the Stationery section. Here you will find items for home use and other useful products.\nPlease make a choice from the menu below by typing corresponding number\n1-View catalogue of available groceries\n2-go back to previous page")
    gchoice2=input("Make a choice:")
    if gchoice2=="1":
        cursor.execute("select Product_no,Product_name,Price from stationery")
        n=1
        nextpage()
        while True:
            print("\nCurrently viewing page:", n, "of 5")
            print("---Menu---")
            if_purchased = input("\nNext-view next 5 items\nBuy-to add a product to your cart\nCart-to view the contents of your cart\nPurchase-To purchase everything from your cart\nBack-to return to previous menu")
            if if_purchased.lower() == "buy":
                item_purchased = input("Enter the product no. of item you want to purchase")
                amount_purchased = input("How many of that item would you like?")
                cursor_stationery.execute("select * from stationery")
                cursor_stationery.execute("insert into cart select * from stationery where Product_No='" + item_purchased + "'")
                cursor_stationery.execute("update cart set Amount='"+amount_purchased+"'where Product_No='" + item_purchased + "'")
                connection.commit()
                cursor_stationery.execute("select product_name from cart where Product_No='" + item_purchased + "'")
                item = cursor_stationery.fetchone()
                print(amount_purchased, item, "added to cart!")

            elif (if_purchased.lower()=="next") and (n<5):
                n=n+1
                nextpage()

            elif n==5:
                cursor.execute("select Product_no,Product_name,Price from stationery")
                n = 1
                nextpage()

            elif if_purchased.lower() == "cart":
                cart_data=pd.read_sql_table("cart", con)
                print(cart_data.to_string(index=False))

            elif if_purchased.lower() == "back":
                customer()

            elif if_purchased.lower() == "purchase":
                purchase()
                break
            else:
                print("\nInvalid option. Please try again")

    elif gchoice2=="2":
        customer()

    else:
        print("Invalid option. Please try again")
        stationery_store()


def customer():
    print("\nThis is the Store simulation software. Designed to emulate an online shopping environment.")
    store_choice=str(input("\nThe store has a choice of two sections to shop from. Please make a choice depending upon your preference.\n1-Grocery\n2-Stationery\n3-return to menu"))
    if (store_choice.lower()=="grocery") or (store_choice=="1"):
        grocery_store()
    elif (store_choice.lower()=="stationery") or (store_choice=="2"):
        stationery_store()
    elif store_choice.lower()=="3":
        login()
    else:
        print("\ninvalid option, Please try again")
        customer()


def login():
    log=input("\nWould you like to login as Manager or Customer? Or type 'exit' to log off")
    if log.lower()=="manager":
        user_name=input("\nEnter your Admin provided user name:")
        password=input("\nEnter your Admin provided password")
        if (user_name.lower()=="root") and (password.lower()=="root"):
            print("Successfully Logged in as Manager")
            manager_menu()
        else:
            retry = input("\nincorrect password or username. Type retry to try again or type back to go back")
            if retry.lower() == "retry":
                manager()
            elif retry.lower() == "back":
                login()

    elif log.lower()=="customer":
        print("\nSuccessfully Logged in as customer")
        customer()

    elif log.lower()=="exit":
        print("\nThank your for using the store simulation software. Please visit us again soon!")
        exit()

    else:
        print("\ninvalid option, please try again")
        login()