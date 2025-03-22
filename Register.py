import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_option_menu import option_menu
from PIL import Image
import time
import requests
from streamlit_lottie import st_lottie
import hashlib
import sqlite3 

# Set page configuration
st.set_page_config(layout="wide")

# Load CSS
def load_css(filename):
    with open(filename) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Call the function with the CSS file name
load_css("style1.css")  # Ensure this file exists in the same directory

# Security functions
def make_hashes(password):
    return hashlib.sha256(str.encode(password)).hexdigest()

def check_hashes(password, hashed_text):
    if make_hashes(password) == hashed_text:
        return hashed_text
    return False

# DB Management
conn = sqlite3.connect('data.db')
c = conn.cursor()

# DB Functions
def create_usertable():
    c.execute('CREATE TABLE IF NOT EXISTS userstable(username TEXT,password TEXT)')

def add_userdata(username, password):
    c.execute('INSERT INTO userstable(username,password) VALUES (?,?)', (username, password))
    conn.commit()

def login_user(username, password):
    c.execute('SELECT * FROM userstable WHERE username =? AND password = ?', (username, password))
    data = c.fetchall()
    return data

def view_all_users():
    c.execute('SELECT * FROM userstable')
    data = c.fetchall()
    return data

# Initialize session state
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False
if 'signup_success' not in st.session_state:
    st.session_state['signup_success'] = False  # Track successful signup

selected = None  # Ensure selected is always initialized

# Sidebar menu (Only visible before login)
if not st.session_state['logged_in']:
    with st.sidebar:
        selected = option_menu(
            menu_title="Start Here!",
            options=["Signup", "Login"],
            icons=["box-seam-fill", "box-seam-fill"],
            menu_icon="home",
            default_index=0
        )

# Signup Section
if selected == "Signup":
    st.title(":iphone: :blue[Create New Account]")
    new_user = st.text_input("Username")
    new_password = st.text_input("Password", type='password')
    
    if st.button("Signup"):
        create_usertable()
        add_userdata(new_user, make_hashes(new_password))
        st.session_state['signup_success'] = True  # Store success flag
        st.success("You have successfully created a valid Account")
        st.info("Go to Login Menu to login")

# Show login success message after signup
if st.session_state['signup_success']:
    st.success("You Have Logged In Successfully!")

# Login Section
elif selected == "Login":
    st.title(":calling: :blue[Login Section]")
    username = st.text_input("User Name")
    password = st.text_input("Password", type='password')
    
    if st.button("Login"):
        create_usertable()
        hashed_pswd = make_hashes(password)
        result = login_user(username, check_hashes(password, hashed_pswd))
        
        prog = st.progress(0)
        for per_comp in range(100):
            time.sleep(0.05)
            prog.progress(per_comp + 1)
        
        if result:
            st.session_state['logged_in'] = True
            st.session_state['signup_success'] = False  # Reset signup success message
            st.success(f"Logged In as {username}")
            st.warning("😊 Now You Can Access Other Pages!")
            st.rerun()  # Refresh page to show logout button
        else:
            st.warning("Incorrect Username/Password")

# Main Page (After Login)
if st.session_state['logged_in']:
    
    # Show "You logged in successfully!" message
    st.success("✅ You logged in successfully!")
    
    # Logout Button on Main Interface
    if st.button("Logout", key="main_logout"):
        st.session_state.clear()
        st.rerun()
