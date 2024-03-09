import pandas as pd
from langchain.output_parsers import PydanticOutputParser
from langchain.pydantic_v1 import BaseModel, Field
from langchain.callbacks import  get_openai_callback
from langchain.prompts import PromptTemplate
from langchain.embeddings import OpenAIEmbeddings
from langchain.document_loaders import DataFrameLoader
from langchain.vectorstores import Chroma
from langchain.chat_models import AzureChatOpenAI
import json

from dotenv import load_dotenv
load_dotenv()

import streamlit as st
import os
def create_folder(folder_path):
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
@st.cache_data
def store_uploaded_files(uploaded_files:list,target_dir:str):
    create_folder(target_dir)
    print("Created the directory for the uploaded files")
    for uploaded_file in uploaded_files:
        file_path = os.path.join(target_dir, uploaded_file.name)
        with open(file_path, "wb") as f:
            f.write(uploaded_file.read())
    print("Written all the files successfully")
    return True

def get_review_text(target_dir:str):
    df = pd.DataFrame()
    for file in os.listdir(target_dir):
        if file.endswith(".xlsx") :
            temp_df = pd.read_excel(target_dir+'/'+file)[["Review"]]
            df = pd.concat([df,temp_df],axis=0)
        if file.endswith(".csv") :
            temp_df = pd.read_csv(target_dir+'/'+file)[["Review"]]
            df = pd.concat([df, temp_df], axis=0)
    return df['Review'].to_list()

# Dont restrict to 4 points on each Sentiment. you can generate as many points as you can but based on the text only

@st.cache_data
def get_feedback(text : list) :
    template = """
    You are an AI Assistant who helps in understanding the Customer reviews given to Hotels in Trip Advisor Website. 

    You have given a text delimited by three dashes . Summarize the given text and write Positive Feedback , negative Feedback and Neutral Feedback in crisp points \
    Location, Food and Dining Quality, Safety and Security, Service , Value for the Money , Facilities and Amenities. 

    ---
    text : {text}
    ---

    Output Example : 

    Positive Topics :
    1. Positive Topic 1
    2. Positive Topic 2
    3. Positive Topic 3
    4. Positive Topic 4

    Negative Topics :
    1. Negative Topic 1
    2. Negative Topic 2
    3. Negative Topic 3
    4. Negative Topic 4
    
     Neutral Topics :
    1. Neutral Topic 1
    2. Neutral Topic 2
    3. Neutral Topic 3
    4. Neutral Topic 4

    """

    prompt = PromptTemplate(
        template=template,
        input_variables=["text"],
    )
    model = AzureChatOpenAI()

    text  = " ".join(text)
    output = model.invoke(prompt.invoke({"text": text}).to_string(), engine="gpt_4_32k").content
    return output