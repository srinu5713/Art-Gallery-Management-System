import streamlit as st
import mysql.connector
from streamlit_extras.switch_page_button import switch_page


st.header("Registration")

username = st.text_input("Username:")
Name = st.text_input("Name:")
Email = st.text_input("Email ID:")
Ph_no = st.text_input("Phone Number :")
password = st.text_input("Password:", type="password")
type = 'Visitor'

if st.button("Register"):

    # Check for null values in the fields
    if not username or not password or not Name or not Ph_no:
        st.warning("Please fill the required fields!!")

    else :
        connection = mysql.connector.connect(host='localhost', username='root', password='wasd', database='agms2')
        try:
            if connection.is_connected():
                cursor = connection.cursor(dictionary=True)
                try:
                    if Email:
                        cursor.execute("INSERT INTO Login (Username, Password, Type, Name, email_id, phone_number) VALUES (%s, %s, %s, %s, %s, %s)", (username, password, type, Name, Email, Ph_no))
                    else:
                        cursor.execute("INSERT INTO Login (Username, Password, Type, Name,email_id, phone_number) VALUES (%s, %s, %s, %s, %s,%s, %s)", (username, password, type, Name,'Not Specified',Ph_no))
                    connection.commit()
                    st.success("Registered Successfully !!")
                    switch_page('Login')

                except mysql.connector.Error as e:
                    st.error(f"Error inserting data: {e}")


                cursor.close()
                connection.close()
        
        except Exception as e:
            st.warning(e)
                        
        finally:
            print("Register")

