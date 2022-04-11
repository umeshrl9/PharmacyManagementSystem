import streamlit as st
import pandas as pd
#from drug_db import *

## SQL DATABASE CODE
import sqlite3


conn = sqlite3.connect("drug_data.db",check_same_thread=False)
c = conn.cursor()

def cust_create_table():
    c.execute('''CREATE TABLE IF NOT EXISTS Customers(
                    C_Name VARCHAR(50) NOT NULL,
                    C_Email VARCHAR(50) NOT NULL, 
                    C_Area VARCHAR(50) NOT NULL,
                    C_Number VARCHAR(50) NOT NULL, 
                    C_id VARCHAR(10) PRIMARY KEY NOT NULL)
                    ''')
    print('Customer Table create Successfully')

def customer_add_data(Cname, Cemail, Carea,Cnumber, Cid):
    c.execute('''INSERT INTO Customers (C_Name, C_Email, C_Area, C_Number, C_id) VALUES(?,?,?,?,?)''', (Cname, Cemail, Carea,Cnumber, Cid))
    conn.commit()

def customer_view_all_data():
    c.execute('SELECT * FROM Customers')
    customer_data = c.fetchall()
    return customer_data

def drug_create_table():
    c.execute('''CREATE TABLE IF NOT EXISTS Drugs(
                D_Name VARCHAR(50) NOT NULL,
                D_ExpDate DATE NOT NULL, 
                D_Use VARCHAR(50) NOT NULL,
                D_Qty INT NOT NULL, 
                D_id INT PRIMARY KEY NOT NULL)
                ''')
    print('DRUG Table create Successfully')

def drug_add_data(Dname, Dexpdate, Duse, Dqty, Did):
    c.execute('''INSERT INTO Drugs (D_Name, D_Expdate, D_Use, D_Qty, D_id) VALUES(?,?,?,?,?)''', (Dname, Dexpdate, Duse, Dqty, Did))
    conn.commit()

def drug_view_all_data():
    c.execute('SELECT * FROM Drugs')
    drug_data = c.fetchall()
    return drug_data







#__________________________________________________________________________________







def main():
    st.title("Pharmacy Database Dashboard")
    menu = ["Drugs", "Customers", "Seller", "Inventory", "About"]
    choice = st.sidebar.selectbox("Menu", menu)

    ## Creating Tables
    drug_create_table()
    cust_create_table()

    ## DRUGS
    if choice == "Drugs":

        menu = ["Add", "View", "Update", "Delete"]
        choice = st.sidebar.selectbox("Menu", menu)
        if choice == "Add":

            st.subheader("Add Drugs")

            col1, col2 = st.columns(2)

            with col1:
                drug_name = st.text_area("Enter the Drug Name")
                drug_expiry = st.date_input("Expiry Date of Drug (DD-MM-YY)")
                drug_mainuse = st.text_area("When to Use")
            with col2:
                drug_quantity = st.text_area("Enter the quantity")
                drug_id = st.text_area("Enter the Drug id (example:#D1)")

            if st.button("Add Drug"):
                drug_add_data(drug_name,drug_expiry,drug_mainuse,drug_quantity,drug_id)
                st.success("Successfully Added Data")
        if choice == "View":
            st.subheader("Drug Details")
            drug_result = drug_view_all_data()
            #st.write(drug_result)
            with st.expander("View All Drug Data"):
                drug_clean_df = pd.DataFrame(drug_result, columns=["Name", "Expiry Date", "Use", "Quantity", "ID"])
                st.dataframe(drug_clean_df)
            with st.expander("View Drug Quantity"):
                drug_name_quantity_df = drug_clean_df[['Name','Quantity']]
                #drug_name_quantity_df = drug_name_quantity_df.reset_index()
                st.dataframe(drug_name_quantity_df)


    ## CUSTOMERS
    elif choice == "Customers":

        menu = ["Add", "View", "Update", "Delete"]
        choice = st.sidebar.selectbox("Menu", menu)
        if choice == "Add":
            # drug_create_table()
            st.subheader("Add Customer")

            col1, col2 = st.columns(2)

            with col1:
                cust_name = st.text_area("Enter the Customer Name")
                cust_email = st.text_area("Enter Customer Email ID")
                cust_area = st.text_area("Enter the Area of Customer")
            with col2:
                cust_number = st.text_area("Enter the number")
                cust_id = st.text_area("Enter the Customer id (example:#C1)")

            if st.button("Add Customer"):
                customer_add_data(cust_name,cust_email,cust_area,cust_number,cust_id)
                st.success("Successfully Added Data")
        if choice == "View":
            st.subheader("Customer Details")
            cust_result = customer_view_all_data()
            #st.write(cust_result)
            with st.expander("View All Customer Data"):
                cust_clean_df = pd.DataFrame(cust_result, columns=["Name", "Email ID", "Area", "Number", "ID"])
                st.dataframe(cust_clean_df)

    elif choice == 'Update Drugs':
        st.subheader("Update Drug Details")
    elif choice == 'Delete Drugs':
        st.subheader("Delete Drugs")



if __name__ == '__main__':
	main()
