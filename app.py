import os.path

import streamlit as st
from utils.data_prep import  *


TARGET_DIR="./uploaded_data"

st.title("Hotel Review Analyzer")

st.header("Add text",divider='rainbow')
input_text = st.text_input("Reviews",placeholder="Customer Review")


st.header("Add files",divider='rainbow')
uploaded_files = st.file_uploader(label="Upload Files", type=['xlsx','csv'],accept_multiple_files=True )

if len(uploaded_files) > 0 :
    val = store_uploaded_files(uploaded_files,target_dir=TARGET_DIR)

button_click =  st.button("Get Customer Reviews Summary")

if button_click :
    list_of_reviews = []
    if os.path.exists(TARGET_DIR) :
        list_of_reviews = get_review_text(TARGET_DIR)
    list_of_reviews = list_of_reviews + [input_text]
    output = get_feedback(list_of_reviews)
    st.write(output)


