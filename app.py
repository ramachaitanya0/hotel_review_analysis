import os.path

import pandas as pd
import streamlit as st
from utils.data_prep import  *
from utils.reco import *


TARGET_DIR="./uploaded_data"
button_click = st.empty()
re_button_click = st.empty()
st.session_state.button_click = False
st.session_state.re_button_click = False

st.title("Hotel Review Analyzer")

st.header("Add text",divider='rainbow')
input_text = st.text_input("Reviews",placeholder="Customer Review")


st.header("Add files",divider='rainbow')
uploaded_files = st.file_uploader(label="Upload Files", type=['xlsx','csv'],accept_multiple_files=True )

if len(uploaded_files) > 0 :
    val = store_uploaded_files(uploaded_files,target_dir=TARGET_DIR)

button_click =  st.button("Get Customer Reviews Summary")

if button_click :
    st.session_state.button_click = True

if st.session_state.button_click :
    list_of_reviews = []
    if os.path.exists(TARGET_DIR) :
        list_of_reviews = get_review_text(TARGET_DIR)
    list_of_reviews = list_of_reviews + [input_text]
    output = get_feedback(list_of_reviews)
    st.write(output)


re_button_click =  st.button("Get Recommendations")
if re_button_click :
    st.session_state.re_button_click = True

if st.session_state.re_button_click :
    list_of_reviews = []
    if os.path.exists(TARGET_DIR) :
        list_of_reviews = get_review_text(TARGET_DIR)
    reco_df = pd.DataFrame()
    for review in list_of_reviews :
        print("The Current Review is -->",review)
        temp_df = get_data_from_review(review)
        reco_df = pd.concat([reco_df,temp_df],axis=0)

    perc_of_positive_location_reviews = 0
    perc_of_positive_service_reviews = 0
    perc_of_positive_facility_reviews = 0
    perc_of_positive_money_reviews = 0
    perc_of_positive_safety_reviews = 0
    perc_of_positive_food_reviews = 0
    if reco_df[reco_df['Location']!="Not Available"].shape[0] > 0 :
        perc_of_positive_location_reviews = round((reco_df[reco_df['Location']=="Positive"].shape[0]/reco_df[reco_df['Location']!="Not Available"].shape[0])*100,1)
    if reco_df[reco_df['Service']!="Not Available"].shape[0] > 0 :
        perc_of_positive_service_reviews = round((reco_df[reco_df['Service']=="Positive"].shape[0]/reco_df[reco_df['Service']!="Not Available"].shape[0])*100,1)
    if reco_df[reco_df['Facilities_and_Amenities']!="Not Available"].shape[0] > 0 :
        perc_of_positive_facility_reviews = round((reco_df[reco_df['Facilities_and_Amenities']=="Positive"].shape[0]/reco_df[reco_df['Facilities_and_Amenities']!="Not Available"].shape[0])*100,1)
    if reco_df[reco_df['Value_for_Money']!="Not Available"].shape[0] > 0 :
        perc_of_positive_money_reviews = round((reco_df[reco_df['Value_for_Money']=="Positive"].shape[0]/reco_df[reco_df['Value_for_Money']!="Not Available"].shape[0])*100,1)
    if reco_df[reco_df['Safety_and_Security']!="Not Available"].shape[0] > 0 :
        perc_of_positive_safety_reviews = round((reco_df[reco_df['Safety_and_Security']=="Positive"].shape[0]/reco_df[reco_df['Safety_and_Security']!="Not Available"].shape[0])*100,1)
    if reco_df[reco_df['Dining_and_Food_Quality']!="Not Available"].shape[0] > 0 :
        perc_of_positive_food_reviews = round((reco_df[reco_df['Dining_and_Food_Quality']=="Positive"].shape[0]/reco_df[reco_df['Dining_and_Food_Quality']!="Not Available"].shape[0])*100,1)

    st.header("Recommendations", divider='rainbow')

    st.write(f"""
    1. {perc_of_positive_location_reviews } % of Customers Has given Positive Review About the Location of the Hotel  
    2.  {perc_of_positive_service_reviews } % of Customers Has given Positive Review About the Service of the Hotel 
    3.  {perc_of_positive_facility_reviews } % of Customers Has given Positive Review About the Facilities and Amenities of the Hotel 
    4.  {perc_of_positive_money_reviews } % of Customers Has given Positive Review About the Value for the Money on the Hotel  
    5.  {perc_of_positive_safety_reviews } % of Customers Has given Positive Review About the Safety and Security of the Hotel 
    6.  {perc_of_positive_food_reviews } % of Customers Has given Positive Review About the Dining and Food Quality of the Hotel 
     """)

    st.header("Data Used for Recommendations ",divider='rainbow')

    st.write("The Data Frame used for the Analysis and recommendations. I have extracted this Data Using ChatGPT and Langchain ")
    st.dataframe(reco_df[['Review','Location','Service','Facilities_and_Amenities','Value_for_Money','Safety_and_Security','Dining_and_Food_Quality','Overall_Experience']])






