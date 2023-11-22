import streamlit as st
import pandas as pd
import mysql.connector
from streamlit_option_menu import option_menu
from PIL import Image
from pandas import option_context
from IPython.display import display
from streamlit_extras.switch_page_button import switch_page
import os
import datetime

def do_view_tasks():
    st.markdown('Overview')

    selected_date = st.date_input("Select a date:", max_value=None)
    cur_date = datetime.date.today()
    if selected_date<=cur_date:
        if st.button('Show Stats'):
            conn = mysql.connector.connect(host='localhost', username='root', password='wasd', database='agms2')
            cur = conn.cursor()

            visitors_query = "SELECT COUNT(DISTINCT Ticket_ID) as num_visitors FROM  ticket  WHERE date_of_visit = %s"
            artworks_query = "SELECT COUNT(*) FROM artwork"
            comments_query = "SELECT COUNT(*) FROM review WHERE DATE(review_date) = %s"
            guides_query = "SELECT COUNT(*) FROM guide"
            tickets_query = "SELECT SUM(No_of_Tickets) FROM visitor_transactions WHERE DATE(Time) = %s"

            try:
                cur.execute(visitors_query, (selected_date,))
                result = cur.fetchone()
                num_visitors = int(result[0]) if result and result[0] is not None else 0

                cur.execute(artworks_query)
                result = cur.fetchone()
                num_artworks = int(result[0]) if result and result[0] is not None else 0

                cur.execute(comments_query, (selected_date,))
                result = cur.fetchone()
                num_comments = int(result[0]) if result and result[0] is not None else 0

                cur.execute(guides_query)
                result = cur.fetchone()
                num_guides = int(result[0]) if result and result[0] is not None else 0

                cur.execute(tickets_query, (selected_date,))
                result = cur.fetchone()
                no_of_tickets = int(result[0]) if result and result[0] is not None else 0

                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Visitors", num_visitors, delta="Daily", help="Number of visitors")
                with col2:
                    st.metric("Paintings in Gallery", num_artworks, delta="Daily", help="Number of paintings")
                with col3:
                    st.metric("Comments", num_comments, delta="Daily", help="Number of comments")

                col4, col5 = st.columns(2)
                with col4:
                    st.metric("Guides", num_guides, delta="Daily", help="Number of guides")
                with col5:
                    st.metric("No of Tickets Sold", no_of_tickets, delta="Daily", help="Amount earned")

            except Exception as e:
                st.error(f"An error occurred: {e}")

            finally:
                conn.close()
    else:
        st.warning('Select a valid date!!!')