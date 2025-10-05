import streamlit as st
import requests

API_BASE_URL = "https://8000-dep-01k6sj99nxkqpr1m5srkmwgyk8-d.cloudspaces.litng.ai" 

st.title("User Authentication")

menu = st.sidebar.selectbox("Menu", ["Sign Up", "Sign In"])

if menu == "Sign Up":
    st.subheader("Create a new account")

    name = st.text_input("Name")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    money = st.number_input("Initial Balance", min_value=0, value=1000)

    if st.button("Sign Up"):
        payload = {
            "name": name,
            "email": email,
            "password": password,
            "money": money
        }
        response = requests.post(f"{API_BASE_URL}/sign-up/", json=payload)

        if response.status_code == 201:
            st.success("Account created successfully!")
        else:
            st.error(response.json().get("error", "Something went wrong"))


elif menu == "Sign In":
    st.subheader("Sign in to your account")

    email = st.text_input("Email", key="signin_email")
    password = st.text_input("Password", type="password", key="signin_password")

    if st.button("Sign In"):
        payload = {
            "email": email,
            "password": password
        }
        response = requests.post(f"{API_BASE_URL}/sign-in/", json=payload)

        if response.status_code == 200:
            token = response.json().get("token")
            st.success("Logged in successfully!")
            st.session_state['token'] = token
        else:
            st.error(response.json().get("error", "Login failed"))
