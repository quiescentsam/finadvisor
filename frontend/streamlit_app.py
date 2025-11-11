import streamlit as st
import requests

st.title("💰 Financial Dashboard")

backend_url = "http://127.0.0.1:8000/api/rag?q=stock+price+of+Apple"

if st.button("Get Finance Data"):
    response = requests.get(backend_url)
    if response.status_code == 200:
        data = response.json()
        st.write("Stock:", data["stock"])
        st.write("Price:", data["price"])
    else:
        st.error("Error connecting to backend!")
