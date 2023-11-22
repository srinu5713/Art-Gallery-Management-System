import streamlit as st
import pandas as pd
import mysql.connector
from streamlit_option_menu import option_menu
from PIL import Image
from pandas import option_context
from IPython.display import display
from streamlit_extras.switch_page_button import switch_page
import os
from datetime import datetime



def do_guide_book(username):
    connection = mysql.connector.connect(host='localhost', username='root', password='wasd', database='agms2')
    try:
        if connection.is_connected():
            cur = connection.cursor(dictionary=True)
            query="SELECT guide_id FROM guide"
            try:
                cur.execute(query)
                list1=cur.fetchall()
                list2=[i['guide_id'] for i in list1]

                #print(list2)
                if list2:
                    option=st.selectbox("Select Guide ID to book: ",list2)
                    d1=st.date_input("Enter the Date: ")
                    s=st.selectbox("Enter your preferred Slot",("1 (9:30 AM to 10:30 AM)","2 (11:00 AM to 12:00 PM)","3 (1:30 PM to 2:30 PM)","4 (3:00 PM to 4:00 PM)","5 (4:30 PM to 5:30 PM)"))
                    current_date = datetime.now().date()

                    query2 = "SELECT user_id FROM login WHERE username=%s"
                    cur.execute(query2, (username,))
                    result_user = cur.fetchone()
                    uid = result_user['user_id']

                    if d1>=current_date:
                        q="SELECT 1 FROM ticket WHERE booking_user_id = %s and date_of_visit=%s"
                        cur.execute(q,(uid,d1))
                        x=cur.fetchall()
                        print(f"Check: {x}")
                        if st.button("Book"):
                            if x:
                                query="SELECT COUNT(guide_id) AS count from guided_tour WHERE tour_date=%s AND slot=%s AND Guide_id=%s GROUP BY tour_date,slot,Guide_id"
                                cur.execute(query,(d1,s,option))
                                list1=cur.fetchone() 
                                if list1:   
                                    ng=list1['count']
                                else:
                                    ng=0

                                if 15>=ng:
                                    query2 = "SELECT user_id FROM login WHERE username=%s"
                                    cur.execute(query2, (username,))
                                    result_user = cur.fetchone()

                                    query1="INSERT INTO guided_tour(guide_id,tour_date,booking_user_id,slot) VALUES (%s,%s,%s,%s)"
                                    try:
                                        cur.execute(query1,(option,d1,result_user['user_id'],s[0]))
                                        st.write("Tour with Guide successfully !!")
                                        connection.commit()

                                    except mysql.connector.Error as e:
                                        st.error(f"Error: {e}")
                                else:
                                    st.write("No slot available for the given booking date!!")
                                
                            
                                query2='''SELECT gt.tour_id,gt.guide_id,g.Name,g.phone_number,gt.tour_date 
                                FROM guided_tour gt JOIN guide g ON gt.Guide_id=g.Guide_id 
                                WHERE booking_user_id=(SELECT user_id from login where username=%s) AND g.Guide_id=%s'''
                                cur.execute(query2,(username,option))
                                list4=cur.fetchall()
                                print(list4)
                                connection.close()

                                st.table(list4)

                            else: 
                                st.warning("Please book the ticket(s) before booking Guide...")
                
                    else:
                        st.warning("select correct date")

                            
            except mysql.connector.Error as e:
                st.error(f"Error: {e}")
                        
    except mysql.connector.Error as e:
        st.error(f"Error: {e}")