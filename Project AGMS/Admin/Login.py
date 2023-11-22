import streamlit as st
import pandas as pd
import mysql.connector
import datetime
from streamlit_option_menu import option_menu
from PIL import Image
from streamlit_extras.switch_page_button import switch_page

st.session_state.isAdmin = 0
st.session_state.isVisitor=0


st.header("Login")

username = st.text_input("Username:")
password = st.text_input("Password:", type="password")

# Login button
if st.button("Login"):
    connection=mysql.connector.connect(host='localhost',username='root',password='wasd',database='agms')
    try:
        if connection:
            cursor = connection.cursor(dictionary=True)
            cursor.execute("SELECT * FROM login WHERE username = %s", (username,))
            user = cursor.fetchone()
            if user and user['password'] == password:
                if user['type'] == 'Admin':
                    st.success("Login successful! Redirecting to Admin dashboard...")
                    st.session_state.isAdmin = 1
                    print(st.session_state.isAdmin)
                    switch_page('Admin')

                else:
                    st.error("Permission Denied !!")
                    
            else:
                st.error("Incorrect credentials. Please try again.")
    except Exception as e:
        st.error(f"Error: {e}")
        
    finally:
        connection.close()

