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


def do_ticket_book(username):
    connection = mysql.connector.connect(
        host='localhost', username='root', password='wasd', database='agms2')
    
    try:
        if connection.is_connected():
            cur = connection.cursor(dictionary=True)
            
            try:
                s1 = st.date_input("Enter booking date: ")
                s1 = s1.strftime('%Y-%m-%d')
                
                # Check if the selected date is greater than or equal to the current date
                if s1 >= datetime.now().strftime('%Y-%m-%d'):
                    nt = st.number_input('Enter the no of tickets: ', step=1, min_value=1)

                    if st.button("Book"):
                        try:
                            query = "SELECT COUNT(*) from ticket WHERE date_of_visit=%s"
                            cur.execute(query, (s1,))
                            result_tickets = cur.fetchone()
                            available_tickets = 200 - result_tickets['COUNT(*)']

                            if available_tickets >= nt:
                                query2 = "SELECT user_id FROM login WHERE username=%s"
                                cur.execute(query2, (username,))
                                result_user = cur.fetchone()

                                if result_user:
                                    uid = result_user['user_id']

                                    for i in range(nt):
                                        query1 = "INSERT INTO ticket(date_of_visit,booking_date,booking_user_id) VALUES (%s,%s,%s)"
                                        cur.execute(
                                            query1, (s1, datetime.now(), uid))
                                        connection.commit()

                                    query3 = '''SELECT booking_user_id, date_of_visit, booking_date, COUNT(*) AS No_of_tickets
                                                FROM ticket
                                                WHERE date_of_visit=%s AND booking_user_id=%s
                                                GROUP BY booking_user_id, date_of_visit, booking_date'''

                                    st.success("Ticket Booked Successfully")
                                    cur.execute(query3, (s1, uid))
                                    result_tickets_user = cur.fetchall()

                                    st.table(result_tickets_user)

                                    current_timestamp = datetime.now()
                                    current_timestamp = current_timestamp.strftime("%Y-%m-%d %H:%M:%S")

                                    query4 = "INSERT INTO visitor_transactions(booking_user_id, No_of_tickets, time) VALUES (%s,%s,%s)"
                                    cur.execute(
                                        query4, (uid, result_tickets_user[0]['No_of_tickets'], current_timestamp))
                                    connection.commit()

                                else:
                                    st.write("User not found.")

                            else:
                                st.write("No tickets available for the given booking date!!")

                        except mysql.connector.Error as e:
                            st.error(f"Error: {e}")
                else:
                    st.write("Please select a date greater than or equal to the current date.")

            except mysql.connector.Error as e:
                st.error(f"Error: {e}")

    except mysql.connector.Error as e:
        st.error(f"Error: {e}")

    except mysql.connector.Error as e:
        st.error(f"Error: {e}")
