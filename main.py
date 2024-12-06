import streamlit as st
import pandas as pd 
from PIL import Image
import random
import mysql.connector  
import io

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="PharmacyDB"   
)

if conn.is_connected():
    print("Success")

c = conn.cursor()


def customer_add_data(phone, firstName, lastName, city, password):
    c.execute("INSERT INTO Customers (Phone, FirstName, LastName, City, Password) VALUES (%s, %s, %s, %s, %s)",
                  (phone, firstName, lastName, city, password))
    conn.commit()

def customer_view_all_data():
    c.execute('SELECT * FROM Customers')
    customer_data = c.fetchall()
    return customer_data

def customer_delete(phone):
    c.execute(''' DELETE FROM Customers WHERE Phone = %s''', (phone,))
    conn.commit()

def drug_update(Dqty, Did):
    c.execute(''' UPDATE Drugs SET Qty = %s WHERE ID = %s''', (Dqty,Did))
    conn.commit()

def drug_delete(Did):
    c.execute(''' DELETE FROM Drugs WHERE ID = %s''', (Did,))
    conn.commit()

def drug_add_data(Did, Dname, Dexpdate, Duse, Dqty, DPrice):
    c.execute('''INSERT INTO Drugs (ID, ExpDate, Qty, Price, D_Use) VALUES(%s,%s,%s,%s, %s)''', (Did, Dexpdate, Dqty, DPrice, Duse))
    c.execute('''INSERT INTO DrugNames (ID, Name) VALUES(%s,%s)''', (Did, Dname))
    conn.commit()

def drug_view_all_data():
    c.execute('SELECT * FROM DrugNames NATURAL JOIN Drugs')
    drug_data = c.fetchall()
    return drug_data

def order_delete(Oid):
    c.execute(''' DELETE FROM Orders WHERE O_ID = %s''', (Oid,))

def order_add_data(phoneNumber,O_Items,O_Qty,O_id):
    c.execute('''INSERT INTO Orders (O_ID, PhoneNumber) VALUES(%s,%s)''',
              (O_id, phoneNumber))
    O_Qty = O_Qty[0:len(O_Qty)-1]
    O_Items = O_Items[0:len(O_Items)-1]
    qtyList = O_Qty.split(",")
    itemsList = O_Items.split(",")
    for i in range(len(qtyList)):
        c.execute("INSERT INTO OrderItems (O_ID, Item_Name, Item_Qty) VALUES(%s, %s, %s)", (O_id, itemsList[i], qtyList[i]))
    conn.commit()

def order_view_data(phone):
    c.execute('SELECT O_ID, Item_Name, Item_Qty  FROM Orders NATURAL JOIN OrderItems Where PhoneNumber = %s',(phone,))
    order_data = c.fetchall()
    return order_data

def order_view_all_data():
    c.execute('SELECT O_ID, FirstName, LastName, Phone, City, Item_Name, Item_Qty FROM Orders NATURAL JOIN OrderItems NATURAL JOIN Customers WHERE Customers.Phone = Orders.PhoneNumber')
    order_all_data = c.fetchall()
    return order_all_data

def admin():
    st.title("Your Pharmacy Dashboard")
    menu = ["Drugs", "Customers", "Orders", "About"]
    choice = st.sidebar.selectbox("Menu", menu)

    if choice == "Drugs":
        menu = ["Add", "View", "Update", "Delete"]
        choice = st.sidebar.selectbox("Menu", menu)
        if choice == "Add":
            st.subheader("Add Drugs")
            col1, col2 = st.columns(2)
            with col1:
                drug_name = st.text_area("Enter the Drug Name")
                drug_expiry = st.date_input("Expiry Date of Drug (YYYY-MM-DD)")
                drug_mainuse = st.text_area("When to Use")
                uploaded_file = st.file_uploader("Choose an image...", type=["png", "jpg", "jpeg"])
            with col2:
                drug_quantity = st.text_area("Enter the quantity")
                drug_price = st.text_area("Enter the price")
                drug_id = st.text_area("Enter the Drug id (example: 1)")
            if st.button("Add Drug"):
                if uploaded_file is not None:
                    image_data = uploaded_file.read()
                    drug_add_data(drug_id, drug_name, drug_expiry, drug_mainuse, drug_quantity, drug_price)
                    c.execute("INSERT INTO Images (ID, Image) VALUES (%s, %s)", (drug_id, image_data,))
                    st.success("Successfully Added Data")
                    conn.commit()

        if choice == "View":
            st.subheader("Drug Details")
            drug_result = drug_view_all_data()
            print(drug_result)
            with st.expander("View All Drug Data"):
                drug_clean_df = pd.DataFrame(drug_result, columns=["ID", "Name", "Expiry Date", "Quantity", "Price", "Use"])
                st.dataframe(drug_clean_df)

        if choice == 'Update':
            st.subheader("Update Drug Details")
            d_id = st.text_area("Drug ID")
            d_qty = st.text_area("Enter the new Quantity")
            if st.button(label='Update'):
                if(int(d_qty) >= 0):
                    drug_update(int(d_qty),int(d_id))
                    st.success("Updated Quantity Successfully!")
                else:
                    st.error("Please enter a positive value")


        if choice == 'Delete':
            st.subheader("Delete Drugs")
            did = st.text_area("Enter drug ID:")
            if st.button(label="Delete"):
                drug_delete(int(did))
                st.success("Deleted successfully!")

    elif choice == "Customers":
        menu = ["View", "Delete"]
        choice = st.sidebar.selectbox("Menu", menu)
        if choice == "View":
            st.subheader("Customer Details")
            cust_result = customer_view_all_data()
            with st.expander("View All Customer Data"):
                cust_clean_df = pd.DataFrame(cust_result, columns=["Phone Number", "First Name", "Last Name", "City" , "Password"])
                st.dataframe(cust_clean_df)

        if choice == 'Delete':
            st.subheader("Delete Customer")
            cust_ph = st.text_area("Enter the phone number of the customer to be deleted:")
            if st.button(label="Delete"):
                customer_delete(cust_ph)
                st.success("Deleted Customer successfully!")

    elif choice == "Orders":
        menu = ["View"]
        choice = st.sidebar.selectbox("Menu", menu)
        if choice == "View":
            st.subheader("Order Details")
            order_result = order_view_all_data()
            with st.expander("View All Order Data"):
                order_clean_df = pd.DataFrame(order_result, columns=["Order ID", "First Name", "Last Name", "Phone Number", "City", "Item Name","Item Quantity"])
                st.dataframe(order_clean_df)

    elif choice == "About":
        st.subheader("DBMS Project: Pharmacy Management System")
        st.subheader("Umesh Kashyap (2023UCS1693)")
        st.subheader("Yash Aggarwal (2023UCS1698)")
        st.subheader("Divyansh Ahuja (2023UCS1677)")

def getauthenicate(phone, password):
    c.execute('SELECT Password FROM Customers WHERE Phone = %s', (phone,))
    cust_password = c.fetchall()
    if(len(cust_password) == 0):
        return False
    if cust_password[0][0] == password:
        return True
    else:
        return False

def customer(phone, password):
    if getauthenicate(phone, password):
        st.title("Welcome to Pharmacy Store")

        st.subheader("Your Order Details")
        order_result = order_view_data(phone)
        with st.expander("View All Order Data"):
            order_clean_df = pd.DataFrame(order_result, columns=["ID", "Items", "Qty"])
            st.dataframe(order_clean_df)

        drug_result = drug_view_all_data()
        print(drug_result)
        O_List = []

        for i in range(len(drug_result)):
            st.subheader("Drug: "+ str(drug_result[i][1]))
            c.execute("SELECT image FROM images WHERE id=%s", (drug_result[i][0],))  
            result = c.fetchone()
            st.image(Image.open(io.BytesIO(result[0])), caption="Price Rs." + str(drug_result[i][4]), width=150)
            medSlider = st.slider(label="Quantity",min_value=0, max_value=100, key = (10*(i**2) + 1000))
            O_List.append(int(medSlider))

            st.info("When to USE: " + str(drug_result[i][5]))

        if st.button(label="Buy now"):
            O_Qty = ""
            O_Items = ""
            flag = 1
            for i in range(len(drug_result)):
                if(O_List[i] > 0):
                    c.execute('SELECT Qty FROM Drugs WHERE ID = %s', (drug_result[i][0],))
                    current_qty = c.fetchone()[0]
                    if(current_qty < O_List[i]):
                        O_List = []
                        flag = 0
                        st.error("Not enough stock")
                        break
                    O_Qty += (str(O_List[i]) + str(','))
                    O_Items += (drug_result[i][1] + ",")

            if(flag == 1 and set(O_List) != {0}):
                O_id = "#O" + str(random.randint(0,1000000))
                order_add_data(phone, O_Items, O_Qty, O_id)
                for i in range(len(O_List)):
                    if O_List[i] > 0:
                        c.execute('SELECT Qty FROM Drugs WHERE ID = %s', (drug_result[i][0],))
                        current_qty = c.fetchone()[0]
                        print(current_qty)
                        new_qty = current_qty - O_List[i]
                        print(new_qty)


                # Update the database with the new quantity
                        c.execute('''UPDATE Drugs SET Qty = %s WHERE ID = %s''', (new_qty, drug_result[i][0],))
                conn.commit()

                st.success("Order placed successfully! Please refresh the page")
                # c.execute(''' UPDATE Drugs SET C_Number = %s WHERE C_ID = %s''', (Cnumber,Cid))
            
            if(set(O_List) == {0}):
                st.error("Please enter some items before placing an order")
    else:
        st.error("Wrong credentials")
            

if __name__ == '__main__':
    menu = ["Login", "SignUp","Admin"]
    choice = st.sidebar.selectbox("Menu", menu)
    if choice == "Login":
        username = st.sidebar.text_input("Registered Phone Number:")
        password = st.sidebar.text_input("Password", type='password')
        if st.sidebar.checkbox(label="Login"):
            customer(username, password)

    elif choice == "SignUp":
        st.subheader("Create New Account")
        cust_fname = st.text_input("First Name")
        cust_lname = st.text_input("Last Name")
        cust_password = st.text_input("Password", type='password', key=1000)
        cust_password1 = st.text_input("Confirm Password", type='password', key=1001)
        col1, col2 = st.columns(2)

        with col1:
            cust_area = st.text_area("City")
        with col2:
            cust_number = st.text_area("Phone Number")

        if st.button("Signup"):
            if (cust_password == cust_password1):
                customer_add_data(cust_number, cust_fname, cust_lname, cust_area, cust_password,)
                st.success("Account Created!")
                st.info("Go to Login Menu to login")
            else:
                st.warning('Password dont match')
    elif choice == "Admin":
        username = st.sidebar.text_input("User Name")
        password = st.sidebar.text_input("Password", type='password')
        if st.sidebar.checkbox(label="Login"):
            if username == 'admin' and password == 'admin':
                admin()
            else:
                st.error("Wrong credentials")