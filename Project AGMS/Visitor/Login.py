import streamlit as st
import pandas as pd
import mysql.connector
import datetime
from streamlit_option_menu import option_menu
from PIL import Image
from streamlit_extras.switch_page_button import switch_page

st.session_state.isAdmin = 0
st.session_state.isVisitor=0
st.session_state.username=''

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
                if user['type'] == 'Visitor':
                    st.session_state.username=username
                    st.success("Login successful! Redirecting to Visitor dashboard...")
                    st.session_state.isVisitor = 1
                    print(st.session_state.isVisitor)
                    switch_page('Visitor')

                else:
                    st.warning("User not registered !!")
                    
            else:
                st.error("Incorrect credentials. Please try again.")
    except Exception as e:
        st.error(f"Error: {e}")
        
    finally:
        connection.close()

# Logout button
if st.button("Register"):
    # Clear the user_id and switch back to the login page
    st.session_state.user_id = None
    switch_page("Register")

