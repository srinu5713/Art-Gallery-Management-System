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

def do_logs(username):
    connection = mysql.connector.connect(host='localhost', username='root', password='wasd', database='agms2')
    cursor = connection.cursor()

    cursor.execute('SELECT DISTINCT Artwork_ID FROM review')
    artwork_ids = [str(row[0]) for row in cursor.fetchall()]
    # Dropdown to select artwork ID
    selected_artwork_id = st.selectbox("Select the artwork ID to review:", artwork_ids)

    # Input for review comment
    review_comment = st.text_input("Review Comment:")

    # Input for rating
    rating = st.number_input("Rating: ", min_value=0.0, max_value=5.0, step=0.5)

    # Button to submit the review
    if st.button("Submit Review"):
        review_date = datetime.now().strftime("%Y-%m-%d")  
        try:                
            insert_query = "INSERT INTO review (Artwork_ID, username, rating, comment, Review_date) VALUES (%s, %s, %s, %s, %s)"
            cursor.execute(insert_query, (selected_artwork_id, username, rating, review_comment, review_date))
            
            connection.commit()
            st.success("Review submitted successfully!")

        except mysql.connector.Error as e:
            st.error(f"Error: {e}")

        finally:
            connection.close()