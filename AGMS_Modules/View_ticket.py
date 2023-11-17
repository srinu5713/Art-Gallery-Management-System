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


def do_view_ticket(username):
    connection = mysql.connector.connect(host='localhost', username='root', password='wasd', database='agms2')
    try:
        if connection.is_connected():
            cur = connection.cursor(dictionary=True)
            try:
                query2="SELECT user_id FROM login WHERE username=%s"
                cur.execute(query2,(username,))
                list2=cur.fetchone()
                uid=list2['user_id']

                query1="SELECT * FROM visitor_transactions WHERE booking_user_id=%s ORDER BY Time DESC"
                cur.execute(query1,(uid,))
                list1 = cur.fetchall()

                connection.close()

                if list1:
                    df1 = pd.DataFrame(list1, columns=['Trans_ID', 'Booking_User_ID', 'No_of_Tickets', 'Time'])
                    st.header("Ticket Booking Transactions")
                    st.table(df1)
                else:
                    st.warning("No ticket booking details found for the user.")

                # df1 = pd.DataFrame(list1, columns=['Trans_ID', 'User ID', 'No of Tickets', 'Timestamp'])
                # st.header("Ticket Booked details")
                # st.write(df1)
            
            except mysql.connector.Error as e:
                st.error(f"Error: {e}")
                        
    except mysql.connector.Error as e:
        st.error(f"Error: {e}")

