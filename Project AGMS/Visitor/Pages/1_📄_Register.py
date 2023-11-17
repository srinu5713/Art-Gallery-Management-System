import streamlit as st
import mysql.connector
import pywhatkit
from datetime import datetime, timedelta
import random
import time

st.header("Registration")

# Initialize Session State
if 'otp_verification_ongoing' not in st.session_state:
    st.session_state.otp_verification_ongoing = False

username = st.text_input("Username:")
Name = st.text_input("Name:")
Email = st.text_input("Email ID:")
Ph_no = st.text_input("Phone Number with WhatsApp:")
password = st.text_input("Password:", type="password")
type = 'Visitor'

if st.button("Register"):

    # Check for null values in the fields
    if not username or not password or not Name or not Ph_no:
        st.warning("Please fill the required fields!!")

    elif not st.session_state.otp_verification_ongoing:
        connection = mysql.connector.connect(host='localhost', username='root', password='wasd', database='agms')
        try:
            if connection.is_connected():
                cursor = connection.cursor(dictionary=True)

                # Generate OTP
                otp = str(random.randrange(100000, 1000000))
                print(f"OTP sent to {Name} is: {otp}")
                st.write("OTP is sent to your Whatsapp number")
                # Send OTP via WhatsApp
                try:
                    current_time = datetime.now()
                    scheduled_time = current_time+timedelta(minutes=2)

                    hour = scheduled_time.hour
                    minute = scheduled_time.minute

                    # Replace the phone number with the desired one
                    phone_number = f"+91{Ph_no}"

                    message1 = f'''Hello {Name}, Welcome to AGMS !! OTP to log in to AGMS account is {otp}. Please don't share your OTP with anyone. -AGMS '''

                    pywhatkit.sendwhatmsg(phone_number, message1, hour, minute)
                    print("Successfully Sent!")

                    # User enters OTP
                    enter_otp = st.text_input("Enter the OTP sent to your Whatsapp Number:")
                    if st.button("Submit"):
                        st.session_state.otp_verification_ongoing = True
                        st.write("Verifying OTP")
                        if enter_otp == otp:
                            st.write("OTP Verified...")
                            try:
                                cursor.execute("INSERT INTO Login (Username, Password, Type) VALUES (%s, %s, %s)", (username, password, type))
                                if Email:
                                    cursor.execute("INSERT INTO Login (Username, Password, Type, Name, Email, phone_number) VALUES (%s, %s, %s, %s, %s, %s)", (username, password, type, Name, Email, Ph_no))
                                else:
                                    cursor.execute("INSERT INTO Login (Username, Password, Type, Name, phone_number) VALUES (%s, %s, %s, %s, %s, %s)", (username, password, type, Name, Ph_no))

                                connection.commit()

                            except mysql.connector.Error as e:
                                st.error(f"Error inserting data: {e}")

                            st.success("Registered Successfully !!")

                            cursor.close()
                            connection.close()

                        else:
                            st.error("Invalid OTP... Please enter a Valid OTP")
                            
                    time.sleep(150)

                except Exception as e:
                    st.error(f"Error sending OTP: {e}")

                
        
        except Exception as e:
            st.warning(e)
                        
        finally:
            st.session_state.otp_verification_ongoing = False
            print("Register")