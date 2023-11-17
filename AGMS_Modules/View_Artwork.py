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


def do_view_artw():
    st.markdown("### View Artworks")

    search_option = st.radio(
        "Search by:", ["All", "Published Year", "Type", "Both"])

    if search_option == "Published Year":
        years = range(2023, 1969,-1)  # Change the range based on your data
        yr = st.selectbox("Select Published Year:",
                            years, index=len(years)-1)

    elif search_option == "Type":
        option = st.selectbox('Select Type of Artwork:', ('Painting',
                                'Sculpture', 'Illustration', 'Figurine', 'Photograph'))

    elif search_option == "Both":
        years = range(1970, 2024)  # Change the range based on your data
        yr = st.selectbox("Select Published Year:",
                            years, index=len(years)-1)
        option = st.selectbox('Select Type of Artwork:', ('Painting',
                                'Sculpture', 'Illustration', 'Figurine', 'Photograph'))

    if st.button('Search'):
        col1, col2 = st.columns(2)

        conn = mysql.connector.connect(
            host='localhost', username='root', password='wasd', database='agms2')
        cur = conn.cursor()

        if search_option == "All":

            query = "SELECT * FROM Artwork"
            cur.execute(query)
            list1 = cur.fetchall()

            for i in range(len(list1)):
                if i % 2 != 0:
                    original = Image.open(list1[i][6])
                    col1.header("Image "+str(i))
                    col1.image(original, use_column_width=True)
                    col1.markdown(f'''`
                            1. Artwork ID: {list1[i][0]}
                            2. Title: {list1[i][1]}
                            3. Artist Name: {list1[i][2]}
                            4. Description: {list1[i][3]}
                            5. Published Year: {list1[i][4]}
                            6. Type: {list1[i][5]}
                            ''')
                else:
                    original1 = Image.open(list1[i][6])
                    col2.header("Image "+str(i))
                    col2.image(original1, use_column_width=True)
                    col2.markdown(f'''
                            1. Artwork ID: {list1[i][0]}
                            2. Title: {list1[i][1]}
                            3. Artist Name: {list1[i][2]}
                            4. Description: {list1[i][3]}
                            5. Published Year: {list1[i][4]}
                            6. Type: {list1[i][5]}
                            ''')

            return

        elif search_option == "Published Year":
            query = "SELECT * FROM Artwork WHERE published_date LIKE %s"
            # print("BEFORE TRY ")
            try:
                cur.execute(query, (f"%{yr}%",))
                list1 = cur.fetchall()
                if list1:
                    for i in range(len(list1)):
                        # print(f"artwork ID and url: {dict1}")
                        if i % 2 == 0:
                            original = Image.open(list1[i][6])
                            col1.header("Image "+str(i))
                            col1.image(original, use_column_width=True)
                            col1.markdown(f'''
                                1. Artwork ID: {list1[i][0]}
                                2. Title: {list1[i][1]}
                                3. Artist Name: {list1[i][2]}
                                4. Description: {list1[i][3]}
                                5. Published Year: {list1[i][4]}
                                6. Type: {list1[i][5]}
                                ''')
                        else:
                            original1 = Image.open(list1[i][6])
                            col2.header("Image "+str(i))
                            col2.image(original1, use_column_width=True)
                            col2.markdown(f'''
                                1. Artwork ID: {list1[i][0]}
                                2. Title: {list1[i][1]}
                                3. Artist Name: {list1[i][2]}
                                4. Description: {list1[i][3]}
                                5. Published Year: {list1[i][4]}
                                6. Type: {list1[i][5]}
                                ''')

                    return
                else:
                    st.write('No Artworks Published that year')
            except:
                st.warning("No Artwork published in this year")

        elif search_option == "Type":
            query = "SELECT * FROM Artwork WHERE type=%s"
            try:
                cur.execute(query, (option,))
                list1 = cur.fetchall()

                for i in range(len(list1)):
                    # print(f"artwork ID and url: {dict1}")
                    if i % 2 == 0:
                        original = Image.open(list1[i][6])
                        col1.header("Image "+str(i))
                        col1.image(original, use_column_width=True)
                        col1.markdown(f'''
                            1. Artwork ID: {list1[i][0]}
                            2. Title: {list1[i][1]}
                            3. Artist Name: {list1[i][2]}
                            4. Description: {list1[i][3]}
                            5. Published Year: {list1[i][4]}
                            6. Type: {list1[i][5]}
                            ''')
                    else:
                        original1 = Image.open(list1[i][6])
                        col2.header("Image "+str(i))
                        col2.image(original1, use_column_width=True)
                        col2.markdown(f'''
                            1. Artwork ID: {list1[i][0]}
                            2. Title: {list1[i][1]}
                            3. Artist Name: {list1[i][2]}
                            4. Description: {list1[i][3]}
                            5. Published Year: {list1[i][4]}
                            6. Type: {list1[i][5]}
                            ''')

                return
            except:
                st.warning("No Artwork of this Type published")

        elif search_option == "Both":
            query = "SELECT * FROM Artwork WHERE published_date LIKE %s and type=%s"
            try:
                cur.execute(query, (f"%{yr}%", option))
                list1 = cur.fetchall()

                for i in range(len(list1)):
                    if i % 2 == 0:
                        original = Image.open(list1[i][6])
                        col1.header("Image "+str(i))
                        col1.image(original, use_column_width=True)
                        col1.markdown(f'''
                            1. Artwork ID: {list1[i][0]}
                            2. Title: {list1[i][1]}
                            3. Artist Name: {list1[i][2]}
                            4. Description: {list1[i][3]}
                            5. Published Year: {list1[i][4]}
                            6. Type: {list1[i][5]}
                            ''')
                    else:
                        original1 = Image.open(list1[i][6])
                        col2.header("Image "+str(i))
                        col2.image(original1, use_column_width=True)
                        col2.markdown(f'''
                            1. Artwork ID: {list1[i][0]}
                            2. Title: {list1[i][1]}
                            3. Artist Name: {list1[i][2]}
                            4. Description: {list1[i][3]}
                            5. Published Year: {list1[i][4]}
                            6. Type: {list1[i][5]}
                            ''')
                return
            except:
                st.warning(
                    "No Artwork of this Type published in this year")