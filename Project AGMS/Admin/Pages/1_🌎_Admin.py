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
 

# conn = mysql.connector.connect(host='localhost',username='root',password='wasd',database='onlinebookstore')
# cur = conn.cursor()


st.set_page_config(page_title='Admin Dashboard', layout='wide')

if 'isAdmin' not in st.session_state:
    st.session_state.isAdmin = False

if st.session_state.isAdmin:

    UPLOAD_FOLDER = 'C:/Users/HP/Documents/Academic Stuff/5th SEM/SE/Project AGMS/'
    # dict1={1:"483px-Mona_Lisa,_by_Leonardo_da_Vinci,_from_C2RMF_retouched.jpg",2:"the starry night.jpg",3:"thinker.jpg",4:"Saurashtra.jpg",5:"Indian Heritage.jpg"}
    # print(dict1)

    # # URL of your custom background image
    # background_image_url = "F:/PES/B_Tech (Sem_5)/Software Engineering/Mini Project/art_gallery_img.webp"

    # # Add background image and styling to the entire app
    # st.markdown(
    #     f"""
    #     <style>
    #         .reportview-container {{
    #             background: url("{background_image_url}") no-repeat center center fixed;
    #             background-size: cover;
    #         }}
    #     </style>
    #     """,
    #     unsafe_allow_html=True,
    # )

    # def do_upload_tasks():
    #     st.markdown('### Upload task file')


    def do_view_tasks():
        st.markdown('### Taxing tasks')

        selected_date = st.date_input("Select a date:", max_value=None)
        cur_date=datetime.date.today()
        if selected_date<=cur_date:
            if st.button('Show Stats'):
                conn = mysql.connector.connect(host='localhost', username='root', password='wasd', database='agms')
                cur = conn.cursor()

                visitors_query = "SELECT COUNT(DISTINCT v.Visitor_ID) as num_visitors FROM visitor v JOIN ticket t ON v.Ticket_ID = t.Ticket_ID WHERE t.date_of_visit = %s"
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



    def do_manage_tasks():
        st.markdown('### Dashboard')
        st.checkbox('Task1', False)
        st.checkbox('Task2', True)
        st.checkbox('Task3', False)
        c1, c2, c3, _ = st.columns([1, 1, 1, 7])
        c1.button('Update tasks')
        c2.button('Add new task...')
        c3.button('Delete selected tasks')

    def do_credentials():
        st.markdown('### Viewing Logs and Understanding Log Structure')
        st.markdown('''Step 1: Accessing the Log System

    As a new admin, you log in to the Art Gallery Management System's admin panel. Navigate to the "Log Transaction" section, where you can access the centralized logging system.

    Step 2: Logging System Overview

    Upon entering the "Logs" section, you are presented with an overview dashboard displaying key metrics, such as the total number of logs, error rates, and recent activities. This provides a quick snapshot of the system's health.

    Step 3: Log Structure Exploration

    Click on the "View Logs" or a similar option to dive into the log entries. Here, you encounter log entries with various columns, including:

    Timestamp: Indicates when the event occurred.
                    
    Log Level: Specifies the severity (INFO, DEBUG, WARN, ERROR).
                    
    User: Identifies the user associated with the log entry.
                    
    Action: Describes the specific action or event.
                    
    Additional Context: Displays any relevant contextual information, such as the artwork involved or the gallery section affected.
                    
    Step 4: Filtering Logs

    Utilize the filtering options to narrow down logs based on specific criteria. For instance, filter logs to show only errors or warnings, focusing on potential issues that require attention.''')

    def do_logs():
        s1 = st.date_input("Enter the date:")
        if st.button("Search"):
            conn = mysql.connector.connect(
                host='localhost', username='root', password='wasd', database='agms')
            cur = conn.cursor()

            query1 = 'SELECT CURRENT_DATE()'
            cur.execute(query1)
            list1 = cur.fetchone()
            if s1 <= list1[0]:
                query = "SELECT vl.log_id,vt.tag_id,vl.visitor_id,vl.entry_time,vl.exit_time FROM visitor_log vl JOIN visitor_tag vt ON vl.visitor_id=vt.visitor_id WHERE vt.assigned_date=%s"
                cur.execute(query, (s1,))
                list1 = cur.fetchall()
                df1 = pd.DataFrame(
                    list1, columns=['Log ID', 'Tag ID', 'Visitor ID', 'Entry time', 'Exit time'])
                st.header("Log Transactions")
                st.write(df1)

            else:
                st.error("Enter valid date!")

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
                host='localhost', username='root', password='wasd', database='agms')
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

        # col1, mid, col2 = st.beta_columns([1,1,20])
        # with col1:
        #     st.image(original, width=60)
        # with col2:
        #     st.write('A Name')

    def allowed_file(filename):
        # Check if the file extension is allowed
        allowed_extensions = {'png', 'jpg', 'jpeg', 'gif'}
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions

    def do_add_del_art():
        option = st.selectbox('Select the operation:',
                              ('Add Artwork', 'Delete Artwork'))

        if option == 'Add Artwork':
            s2 = st.text_input("Title: ")
            s3 = st.text_input("Artist: ")
            s4 = st.text_area("Description: ")
            s5 = st.date_input("Publish Date:")
            s6 = st.selectbox('Select Type of Artwork:', ('Painting',
                              'Sculpture', 'Illustration', 'Figurine', 'Photograph'))
            uploaded_file = st.file_uploader("Choose an image...", type=[
                                             "jpg", "jpeg", "png", "gif"])

            if st.button("Add"):
                if s2 and s3 and s4 and s5 and s6 and uploaded_file:
                    # Save the uploaded image to the specified path
                    if allowed_file(uploaded_file.name):
                        img_path = os.path.join(
                            UPLOAD_FOLDER, uploaded_file.name)
                        with open(img_path, 'wb') as f:
                            f.write(uploaded_file.getvalue())

                        # Insert data into the database
                        conn = mysql.connector.connect(
                            host='localhost', username='root', password='wasd', database='agms')
                        cur = conn.cursor()

                        query = "INSERT INTO Artwork(Title, Artist, description, published_date, type, img_loc) VALUES(%s, %s, %s, %s, %s, %s)"
                        try:
                            cur.execute(query, (s2, s3, s4, s5, s6, img_path))
                            conn.commit()

                            st.write("Inserted Artwork successfully")

                        except Exception as e:
                            st.error(f"Error: {e}")

                        finally:
                            conn.close()

                    else:
                        st.error(
                            'Invalid file format. Please upload a valid image file.')

                else:
                    st.error("Please enter all the details to add...")

        elif option == 'Delete Artwork':
            try:
                s1 = st.number_input("Artwork ID: ", step=1, value=1)
                if st.button("Delete"):
                    if s1:
                        conn = mysql.connector.connect(
                            host='localhost', username='root', password='wasd', database='agms')
                        cur = conn.cursor()

                        query = "DELETE FROM Artwork WHERE Artwork_ID=%s"
                        cur.execute(query, (s1,))
                        st.write("Deleted Artwork successfully")
                    else:
                        st.error("Please enter artwork id to delete...")

            except mysql.connector.Error as e:
                st.error("Please Enter valid value")

    def do_view_guide():
        s1 = st.number_input("Enter Guide ID: ", step=1, value=1)
        s2 = st.text_input("Enter Guide Name: ")

        if st.button("Search"):
            conn = mysql.connector.connect(
                host='localhost', username='root', password='wasd', database='agms')
            cur = conn.cursor()

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

            else:
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

    def do_add_del_guide():
        s1 = st.number_input("Enter Guide ID: ", step=1, value=1)

        if st.button("Search"):
            if s1:
                conn = mysql.connector.connect(
                    host='localhost', username='root', password='wasd', database='agms')
                cur = conn.cursor()

                query = '''DELETE FROM guide WHERE Guide_ID = %s'''
                cur.execute(query, (s1,))
                list1 = cur.fetchall()
                df1 = pd.DataFrame(
                    list1, columns=['Guide ID', 'Name', 'Phone Number', 'Rating'])
                st.header("View Guides")
                st.write(df1)

            else:
                st.error("Please enter the guide ID...")

            conn.close()

    def do_ticket_book():
        s1 = st.date_input("From Booking Date: ")
        formatted_start_date = s1.strftime('%Y-%m-%d')
        s2 = st.date_input("To Booking date: ")
        formatted_start_date = s2.strftime('%Y-%m-%d')

        x = st.button("Search")

        if x:
            if s1 and s2 and s2 >= s1:
                conn = mysql.connector.connect(
                    host='localhost', username='root', password='wasd', database='agms')
                cur = conn.cursor()

                query = '''
                SELECT v.trans_ID, v.booking_visitor_id, v.no_of_tickets, t.date_of_visit, v.time, 100 * v.no_of_tickets AS amount 
                FROM visitor_transactions v 
                JOIN ticket t ON v.booking_visitor_id = t.Visitor_ID
                WHERE DATE(v.time) BETWEEN %s AND %s
                '''
                query1 = 'SELECT CURRENT_DATE()'
                cur.execute(query1)
                list1 = cur.fetchone()
                if s2 <= list1[0]:
                    cur.execute(query, (s1, s2))
                    list1 = cur.fetchall()
                    df1 = pd.DataFrame(list1, columns=[
                                       'Transaction ID', 'Visitor ID', 'No of tickets', 'Date of visit', 'Booked Date', 'Amount'])
                    st.header("Ticket Booking Transaction")
                    st.write(df1)
                else:
                    st.error("No Transactions yet")
                conn.close()
            else:
                st.error("Enter valid From to dates")

            # elif s1:
            #     conn = mysql.connector.connect(host='localhost',username='root',password='wasd',database='agms')
            #     cur = conn.cursor()

            #     query='''SELECT v.trans_ID,v.booking_visitor_id, v.no_of_tickets, t.date_of_visit, v.time, 100*(v.no_of_tickets) AS amount
            #     FROM visitor_transactions v JOIN ticket t ON v.booking_visitor_id = t.Visitor_ID WHERE date(v.time)>%s'''
            #     cur.execute(query,(s1,))
            #     list1=cur.fetchall()
            #     df1=pd.DataFrame(list1,columns=['Transaction ID','Visitor ID','No of tickets','Date of visit','Booked Date','Amount'])
            #     st.header("Ticket Booking Transaction")
            #     st.write(df1)

            # elif s2:
            #     conn = mysql.connector.connect(host='localhost',username='root',password='wasd',database='agms')
            #     cur = conn.cursor()

            #     query='''SELECT v.trans_ID,v.booking_visitor_id, v.no_of_tickets, t.date_of_visit, v.time, 100*(v.no_of_tickets) AS amount
            #     FROM visitor_transactions v JOIN ticket t ON v.booking_visitor_id = t.Visitor_ID WHERE date(v.time)<%s'''
            #     cur.execute(query,(s2,))
            #     list1=cur.fetchall()
            #     df1=pd.DataFrame(list1,columns=['Transaction ID','Visitor ID','No of tickets','Date of visit','Booked Date','Amount'])
            #     st.header("Ticket Booking Transaction")
            #     st.write(df1)

            # else:
            #     conn = mysql.connector.connect(host='localhost',username='root',password='wasd',database='agms')
            #     cur = conn.cursor()

            #     query='''SELECT v.trans_ID,v.booking_visitor_id, v.no_of_tickets, t.date_of_visit, v.time, 100*(v.no_of_tickets) AS amount
            #     FROM visitor_transactions v JOIN ticket t ON v.booking_visitor_id = t.Visitor_ID'''
            #     cur.execute(query)
            #     list1=cur.fetchall()
            #     df1=pd.DataFrame(list1,columns=['Transaction ID','Visitor ID','No of tickets','Date of visit','Booked Date','Amount'])
            #     st.header("Ticket Booking Transaction")
            #     st.write(df1)

    def do_guide_book():
        search_criteria = st.radio("Select Search Criteria:", [
                                   "Guide ID", "Tour Date"])

        if search_criteria == 'Guide ID':
            s1 = st.number_input("Guide_ID: ", step=1, value=1)
            s2 = None

        elif search_criteria == 'Tour Date':
            s1 = None
            s2 = st.date_input("Tour_date: ")
            formatted_start_date = s2.strftime('%Y-%m-%d')

        x = st.button("Search")

        if x:
            if s1:
                conn = mysql.connector.connect(
                    host='localhost', username='root', password='wasd', database='agms')
                cur = conn.cursor()

                query = '''SELECT guide_id,tour_id, tour_date FROM guided_tour WHERE guide_id=%s'''
                cur.execute(query, (s1,))
                list1 = cur.fetchall()
                df1 = pd.DataFrame(
                    list1, columns=['Guide ID', 'Tour ID', 'Tour Date'])
                st.header("Guide Booking Transaction")
                st.write(df1)

            elif s2:
                conn = mysql.connector.connect(
                    host='localhost', username='root', password='wasd', database='agms')
                cur = conn.cursor()

                query1 = 'SELECT CURRENT_DATE()'
                cur.execute(query1)
                list1 = cur.fetchone()
                if s2 <= list1[0]:
                    query = '''SELECT guide_id,tour_id, tour_date FROM guided_tour WHERE tour_date=%s'''
                    cur.execute(query, (s2,))
                    list1 = cur.fetchall()
                    df1 = pd.DataFrame(
                        list1, columns=['Guide ID', 'Tour ID', 'Tour Date'])
                    st.header("Guide Booking Transaction")
                    st.write(df1)
                else:
                    st.error("You have entered beyond current date...")

            conn.close()

    def do_latest_rev():
        option = st.selectbox("Ratings", ('5', '4', '3', '2', '1'))
        if st.button("Search"):
            conn = mysql.connector.connect(
                host='localhost', username='root', password='wasd', database='agms')
            cur = conn.cursor()

            query = '''SELECT artwork_id,visitor_id,rating,comment FROM review WHERE rating=%s AND review_date> (SELECT DATE_SUB(CURRENT_DATE(), INTERVAL 30 DAY)) ORDER BY review_date DESC'''
            cur.execute(query, (option,))
            list1 = cur.fetchall()

            df1 = pd.DataFrame(
                list1, columns=['Artwork ID', 'Visitor ID', 'Ratings', 'Review'])
            st.header("Latest Reviews")

            st.write(df1)

    def do_past_rev():
        option = st.selectbox("Ratings", ('5', '4', '3', '2', '1'))
        if st.button("Search"):
            conn = mysql.connector.connect(
                host='localhost', username='root', password='wasd', database='agms')
            cur = conn.cursor()

            query = '''SELECT artwork_id, visitor_id, rating, comment 
                    FROM review 
                    WHERE rating = %s AND review_date < (SELECT DATE_SUB(CURRENT_DATE(), INTERVAL 30 DAY)) 
                    ORDER BY review_date DESC'''

            cur.execute(query, (option,))
            list1 = cur.fetchall()
            df1 = pd.DataFrame(
                list1, columns=['Artwork ID', 'Visitor ID', 'Ratings', 'Review'])
            st.header("Past Reviews")

            st.write(df1)

    def do_logout():
        st.markdown("### Logout")
        st.warning('Are you sure, you want to logout?', icon="⚠️")
        if st.button("Yes", key="logout_yes_button"):
            st.markdown("###Logout successfully")
            switch_page('login')

        elif st.button("No", key="logout_no_button"):
            st.markdown("### Continue")

    styles = {
        "container": {"margin": "0px !important", "padding": "0!important", "align-items": "stretch", "background-color": "#03dffc"},
        "icon": {"color": "black", "font-size": "20px"},
        "nav-link": {"font-size": "20px", "text-align": "left", "margin": "0px", "--hover-color": "#fcd303"},
        "nav-link-selected": {"background-color": "#fcd303", "font-size": "20px", "font-weight": "normal", "color": "black", },
    }

    menu = {
        'title': 'Admin',
        'items': {
            'Dashboard': {
                'action': None, 'item_icon': 'terminal-dash', 'submenu': {
                    'title': None,
                    'items': {
                        'View Tasks': {'action': do_view_tasks, 'item_icon': 'list-task', 'submenu': None},
                        # 'Manage Tasks': {'action': do_manage_tasks, 'item_icon': 'list-check', 'submenu': None},
                        # 'Upload Tasks': {'action': do_upload_tasks, 'item_icon': 'cloud-upload-fill', 'submenu': None},
                    },
                    'menu_icon': None,
                    'default_index': 0,
                    'with_view_panel': 'main',
                    'orientation': 'horizontal',
                    'styles': styles
                }
            },
            'Artwork': {
                'action': None, 'item_icon': 'easel2', 'submenu': {
                    'title': None,
                    'items': {
                        'View artworks': {'action': do_view_artw, 'item_icon': 'key', 'submenu': None},
                        'Add or Delete artwork': {'action': do_add_del_art, 'item_icon': 'journals', 'submenu': None},
                    },
                    'menu_icon': None,
                    'default_index': 0,
                    'with_view_panel': 'main',
                    'orientation': 'horizontal',
                    'styles': styles
                }
            },
            'Guide': {
                'action': None, 'item_icon': 'easel2', 'submenu': {
                    'title': None,
                    'items': {
                        'View Guides': {'action': do_view_guide, 'item_icon': 'key', 'submenu': None},
                        'Add or Delete Guides': {'action': do_add_del_guide, 'item_icon': 'journals', 'submenu': None},
                    },
                    'menu_icon': None,
                    'default_index': 0,
                    'with_view_panel': 'main',
                    'orientation': 'horizontal',
                    'styles': styles
                }
            },
            'Booking Details': {
                'action': None, 'item_icon': 'ticket-perforated', 'submenu': {
                    'title': None,
                    'items': {
                        'Ticket Booking': {'action': do_ticket_book, 'item_icon': 'key', 'submenu': None},
                        'Guide Booking ': {'action': do_guide_book, 'item_icon': 'journals', 'submenu': None},
                    },
                    'menu_icon': None,
                    'default_index': 0,
                    'with_view_panel': 'main',
                    'orientation': 'horizontal',
                    'styles': styles
                }
            },
            'Log Transaction': {
                'action': None, 'item_icon': 'gear', 'submenu': {
                    'title': None,
                    'items': {
                        'Precursor for Log Management': {'action': do_credentials, 'item_icon': 'key', 'submenu': None},
                        'View Logs': {'action': do_logs, 'item_icon': 'journals', 'submenu': None},
                    },
                    'menu_icon': None,
                    'default_index': 0,
                    'with_view_panel': 'main',
                    'orientation': 'horizontal',
                    'styles': styles
                }
            },
            'Reviews': {
                'action': None, 'item_icon': 'chat-right-text', 'submenu': {
                    'title': None,
                    'items': {
                        'Latest Reviews': {'action': do_latest_rev, 'item_icon': 'key', 'submenu': None},
                        'Past Reviews': {'action': do_past_rev, 'item_icon': 'journals', 'submenu': None},
                    },
                    'menu_icon': None,
                    'default_index': 0,
                    'with_view_panel': 'main',
                    'orientation': 'horizontal',
                    'styles': styles
                }
            },
            'Logout': {
                'action': None, 'item_icon': 'box-arrow-left', 'submenu': {
                    'title': None,
                    'items': {
                        'Logout': {'action': do_logout, 'item_icon': 'key', 'submenu': None},
                    },
                    'menu_icon': None,
                    'default_index': 0,
                    'with_view_panel': 'main',
                    'orientation': 'horizontal',
                    'styles': styles
                }
            }


        },
        'menu_icon': 'person-fill-check',
        'default_index': 0,
        'with_view_panel': 'sidebar',
        'orientation': 'vertical',
        'styles': styles
    }

    def show_menu(menu):
        def _get_options(menu):
            options = list(menu['items'].keys())
            return options

        def _get_icons(menu):
            icons = [v['item_icon'] for _k, v in menu['items'].items()]
            return icons

        kwargs = {
            'menu_title': menu['title'],
            'options': _get_options(menu),
            'icons': _get_icons(menu),
            'menu_icon': menu['menu_icon'],
            'default_index': menu['default_index'],
            'orientation': menu['orientation'],
            'styles': menu['styles']
        }

        with_view_panel = menu['with_view_panel']
        if with_view_panel == 'sidebar':
            with st.sidebar:
                menu_selection = option_menu(**kwargs)
        elif with_view_panel == 'main':
            menu_selection = option_menu(**kwargs)
        else:
            raise ValueError(
                f"Unknown view panel value: {with_view_panel}. Must be 'sidebar' or 'main'.")

        if menu['items'][menu_selection]['submenu']:
            show_menu(menu['items'][menu_selection]['submenu'])

        if menu['items'][menu_selection]['action']:
            menu['items'][menu_selection]['action']()

    show_menu(menu)

else:
    st.write("Please Login First !!")
