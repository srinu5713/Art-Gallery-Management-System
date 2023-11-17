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


def do_credentials():
    connection = mysql.connector.connect(host='localhost', username='root', password='wasd', database='agms2')
    cursor = connection.cursor()

    cursor.execute('SELECT DISTINCT Artwork_ID FROM review')
    artwork_ids = [str(row[0]) for row in cursor.fetchall()]
    # Dropdown to select artwork ID
    selected_artwork_id = st.selectbox("Select the artwork ID to review:", artwork_ids)

    # Button to submit the review
    if st.button("Show Reviews"):
        try:                
            review_query = "SELECT * FROM REVIEW WHERE Artwork_ID=%s ORDER BY rating DESC"
            cursor.execute(review_query, (selected_artwork_id, ))
            reviews = cursor.fetchall()

            if reviews:
                columns = [desc[0] for desc in cursor.description]
                df_reviews = pd.DataFrame(reviews, columns=columns)
                st.write(df_reviews)
            else:
                st.write("No reviews found for the selected artwork.")

        except mysql.connector.Error as e:
            st.error(f"Error: {e}")

        finally:
            connection.close()
     