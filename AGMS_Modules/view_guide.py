import streamlit as st
import pandas as pd
import mysql.connector
from streamlit_option_menu import option_menu
from PIL import Image
from pandas import option_context
from IPython.display import display
from streamlit_extras.switch_page_button import switch_page
import os
from datetime import datetime  # Updated import statement


def do_view_guide():
    conn = mysql.connector.connect(
    host='localhost', username='root', password='wasd', database='agms2')
    
    cur = conn.cursor()
    query="SELECT guide_id FROM guide"
    cur.execute(query)
    list1=cur.fetchall()
    list2=[i[0] for i in list1]
    list2.insert(0,0)
    
    s1 = st.selectbox("Enter Guide ID: ", list2)
    s2 = st.text_input("Enter Guide Name: ")

    if st.button("Search"):

        query = '''SELECT Guide_ID, Name, Phone_number, Rating FROM guide 
                WHERE guide_id=%s AND Name LIKE %s 
                ORDER BY rating DESC'''

        if s1 and s2:
            cur.execute(query, (s1, f"%{s2}%"))

        elif s1:
            query = '''SELECT Guide_ID, Name, Phone_number, Rating FROM guide 
                    WHERE guide_id=%s
                    ORDER BY rating DESC'''
            cur.execute(query, (s1,))

        elif s2:
            query = '''SELECT Guide_ID, Name, Phone_number, Rating FROM guide 
                    WHERE Name LIKE %s
                    ORDER BY rating DESC'''
            cur.execute(query, (f"%{s2}%",))

        elif s1==0:
            query = '''SELECT Guide_ID, Name, Phone_number, Rating FROM guide 
                    ORDER BY rating DESC'''
            cur.execute(query)
        

        list1 = cur.fetchall()
        df1 = pd.DataFrame(
            list1, columns=['Guide ID', 'Name', 'Phone Number', 'Rating'])
        st.header("View Guides")
        with option_context('display.max_colwidth', 400):
            st.write(df1)

        conn.close()