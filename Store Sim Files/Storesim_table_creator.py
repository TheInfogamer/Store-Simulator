import sqlalchemy as sq
import pandas as pd
# ATTENTION
# in the next line please replace 'user' with your sql username and 'password' with your sql password.
# for example if you're username is 'admin' and password is '123' it will look like this:con = sq.create_engine("mysql+pymysql://admin:123@localhost/storesim")
con = sq.create_engine("mysql+pymysql://root:root@localhost/storesim")




connection = con.raw_connection()
cursor0 = connection.cursor()

column_names = ["Product_no","Product_Name","Price"]
cart_column_names = ["Product_no","Product_Name","Amount","Price"]
grocery = pd.read_csv("Grocery.csv")
df1 = pd.DataFrame(grocery)
df1.to_sql(name = 'grocery', con = con,if_exists = 'replace',index = False)

stationery=pd.read_csv("Stationery.csv")
df4=pd.DataFrame(stationery)
df4.to_sql(name='stationery',con=con,if_exists='replace',index=False)

df2={"Product_No":[],"Product_Name":[],"Amount":[],"Price":[]}
cart=pd.DataFrame(df2)
cart.to_sql(name='cart',con=con,if_exists='replace',index=False)
cursor0.execute("alter table cart modify Product_No bigint")
cursor0.execute("alter table cart modify Product_Name text")
cursor0.execute("alter table cart modify Amount bigint")
cursor0.execute("alter table cart modify Price bigint")
