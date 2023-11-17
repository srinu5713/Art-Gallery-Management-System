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


if 'isVisitor' not in st.session_state:
    st.session_state.isVisitor = False


if st.session_state.isVisitor:
    # st.header('Visitor Dashboard')

    username="Rahul"
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
    def do_ticket_book():
        connection = mysql.connector.connect(host='localhost', username='root', password='wasd', database='agms')
        try:
            if connection.is_connected():
                cur = connection.cursor(dictionary=True)
                try:
                    s1=st.date_input("Enter booking date: ")
                    s1 =s1.strftime('%Y-%m-%d')
                    nt=st.number_input('Enter the no of tickets: ',step=1)

                    if st.button("Book"):
                        query="SELECT COUNT(*) from ticket WHERE booking_date=%s"
                        cur.execute(query,(s1,))
                        list1=cur.fetchone()
                        if 200>=list1[0]+nt:
                            query1="SELECT MAX(ticket_id) from ticket"
                            query2="SELECT user_id FROM login WHERE username=%s"

                            cur.execute(query1)
                            list1=cur.fetchone()
                            max1=list1[0]

                            cur.execute(query2,(username,))
                            list2=cur.fetchone()
                            uid=list2[0]

                            for i in range(nt):
                                query1="INSERT INTO ticket(date_of_visit,booking_date,booking_user_id) VALUES (%s,%s,%s)" 
                                cur.execute(query1,(s1,datetime.date,uid)) 
                                connection.commit()

                            query1="SELECT booking_user_id,date_of_visit,booking_date,COUNT(*) AS No_of_tickets WHERE date_of_visit=%s AND user_id=%s GROUP BY booking_user_id"                           
                            cur.execute(query1,(s1,uid))
                            list1=cur.fetchall()

                            current_timestamp = datetime.now()
                            current_timestamp = current_timestamp.strftime("%Y-%m-%d %H:%M:%S")

                            query2="INSERT INTO visitor_transactions(booking_user_id,No_of_tickets,time) VALUES (%s,%s,%s)"
                            cur.execute(query2,(uid,list1[3],current_timestamp))

                            connection.close()

                        else:
                            st.write("No ticket available for the given booking date!!")

                    df1 = pd.DataFrame(list1, columns=['User ID', 'Tour Date', 'Ticket Booking date', 'No of Tickets'])
                    st.header("Ticket Booked details")
                    st.write(df1)

                except mysql.connector.Error as e:
                    st.error(f"Error: {e}")
                            
        except mysql.connector.Error as e:
            st.error(f"Error: {e}")

    def do_credentials():
        pass 

    def do_logs():
        pass

    def do_logout():
        pass

    def do_view_ticket():
        connection = mysql.connector.connect(host='localhost', username='root', password='wasd', database='agms')
        try:
            if connection.is_connected():
                cur = connection.cursor(dictionary=True)
                try:
                    query2="SELECT user_id FROM login WHERE username=%s"
                    cur.execute(query2,(username,))
                    list2=cur.fetchone()
                    uid=list2[0]

                    query1="SELECT * FROM visitor_transactions WHERE Booking_Visitor_ID=%s"
                    cur.execute(query1,(uid,))
                    list1=cur.fetchall()

                    connection.close()

                    df1 = pd.DataFrame(list1, columns=['Trans_ID', 'User ID', 'No of Tickets', 'Timestamp'])
                    st.header("Ticket Booked details")
                    st.write(df1)
                
                except mysql.connector.Error as e:
                    st.error(f"Error: {e}")
                            
        except mysql.connector.Error as e:
            st.error(f"Error: {e}")
                


  


    def do_guide_book():
        connection = mysql.connector.connect(host='localhost', username='root', password='wasd', database='agms')
        try:
            if connection.is_connected():
                cur = connection.cursor(dictionary=True)
                query="SELECT guide_id FROM guide"
                try:
                    cur.execute(query)
                    list1=cur.fetchall()
                    if list1:
                        option=st.selectbox("Select Guide ID to book: ",list1)
                        d1=st.date_input("Enter the Date: ")
                        s=st.selectbox("Enter your preferred Slot",("1 (9:30 AM to 10:30 AM)","2 (11:00 AM to 12:00 PM)","3 (1:30 PM to 2:30 PM)","4 (3:00 PM to 4:00 PM)","5 (4:30 PM to 5:30 PM)"))

                        if st.button("Book"):
                            query="SELECT COUNT(guide_id) from guided_tour WHERE tour_date=%s AND slot=%s"
                            cur.execute(query,(d1,s))
                            list1=cur.fetchone()
                            if 15>=list1[0]:
                                query1="INSERT INTO guided_tour(guide_id,tour_date,slot) VALUES (%s,%s,%s)"
                                try:
                                    cur.execute(query1,(option,d1,s[0]))
                                    st.write("Tour with Guide successfully !!")
                                    connection.commit()

                                except mysql.connector.Error as e:
                                    st.error(f"Error: {e}")
                            else:
                                st.write("No slot available for the given booking date!!")
                            
                        query2="SELECT gt.tour_id,gt.guide_id,g.Name,g.phone_number,gt.tour_date FROM guided_tour gt JOIN guide g WHERE booking_visitor_id=(SELECT visitor_id from login where username=%s)"
                        cur.execute(query2,username)
                        list1=cur.fetchall()

                        connection.close()

                        df1 = pd.DataFrame(list1, columns=['Tour ID', 'Guide ID', 'Guide Name', 'Phone Number', 'Tour Date'])
                        st.header("Guide Booking details")
                        st.write(df1)

                except mysql.connector.Error as e:
                    st.error(f"Error: {e}")
                            
        except mysql.connector.Error as e:
            st.error(f"Error: {e}")
                    
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

    styles = {
        "container": {"margin": "0px !important", "padding": "0!important", "align-items": "stretch", "background-color": "#03dffc"},
        "icon": {"color": "black", "font-size": "20px"},
        "nav-link": {"font-size": "20px", "text-align": "left", "margin": "0px", "--hover-color": "#fcd303"},
        "nav-link-selected": {"background-color": "#fcd303", "font-size": "20px", "font-weight": "normal", "color": "black", },
    }

    menu = {
        'title': 'User',
        'items': {
            'Home': {
                'action': None, 'item_icon': 'terminal-dash', 'submenu': {
                    'title': None,
                    'items': {
                        'View Tasks': {'action': do_view_tasks, 'item_icon': 'list-task', 'submenu': None},
                    },
                    'menu_icon': None,
                    'default_index': 0,
                    'with_view_panel': 'main',
                    'orientation': 'horizontal',
                    'styles': styles
                }
            },
            'Ticket Booking': {
                'action': None, 'item_icon': 'easel2', 'submenu': {
                    'title': None,
                    'items': {
                        'Ticket Booking': {'action': do_ticket_book, 'item_icon': 'key', 'submenu': None},
                        'View Booked Tickets': {'action': do_view_ticket, 'item_icon': 'journals', 'submenu': None},
                    },
                    'menu_icon': None,
                    'default_index': 0,
                    'with_view_panel': 'main',
                    'orientation': 'horizontal',
                    'styles': styles
                }
            },
            'Guide Booking': {
                'action': None, 'item_icon': 'easel2', 'submenu': {
                    'title': None,
                    'items': {
                        'Guide Booking': {'action': do_guide_book, 'item_icon': 'key', 'submenu': None},
                        'View Booked Guide': {'action': do_view_guide, 'item_icon': 'journals', 'submenu': None},
                    },
                    'menu_icon': None,
                    'default_index': 0,
                    'with_view_panel': 'main',
                    'orientation': 'horizontal',
                    'styles': styles
                }
            },
            'View Gallery': {
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
            'Review Artworks': {
                'action': None, 'item_icon': 'gear', 'submenu': {
                    'title': None,
                    'items': {
                        'View Reviews': {'action': do_credentials, 'item_icon': 'key', 'submenu': None},
                        'Share your experience': {'action': do_logs, 'item_icon': 'journals', 'submenu': None},
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
