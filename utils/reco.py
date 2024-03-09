from langchain.output_parsers import PydanticOutputParser
from langchain.pydantic_v1 import BaseModel, Field
from langchain.prompts import PromptTemplate
from langchain.callbacks import  get_openai_callback
from langchain.chat_models import AzureChatOpenAI
import pandas as pd
import streamlit as st
import json
@st.cache_data
def get_data_from_review(text):
  class Applicant(BaseModel):
    Location : str = Field(description="If the given review has text about Location of the Hotel or resort, is it positive or Negative. if its positive return 'Positive',\
     if its Negative return 'Negative' if its Neutral return 'Neutral' ,if the customer didn't write about location return 'Not Available'. The Output should a String ")
    Service : str = Field(description="If the given review has text about Service of the Hotel or resort ,is it positive or Negative ?.if its positive return 'Positive',\
     if its Negative return 'Negative' if its Neutral return 'Neutral' ,if the customer didn't write about Service then return  'Not Available'. The Output should a String ")
    Facilities_and_Amenities : str = Field(description="If the given review has text about Facilities and Amenities of the Hotel or resort like pools, fitness centers, spas, and recreational activities ,\
    is it positive or Negative ?.if its positive return 'Positive',\
     if its Negative return 'Negative' if its Neutral return 'Neutral' ,if the customer didn't write about Facilities and Amenities then return  'Not Available'.The Output should a String  ")
    Value_for_Money : str = Field(descripion= "If the given review has text about Value for Money on the Hotel or resort ,\
    is it positive or Negative ?.if its positive return 'Positive',\
     if its Negative return 'Negative' if its Neutral return 'Neutral' ,if the customer didn't write about Value for Money then return  'Not Available'. The Output should a String")
    Safety_and_Security : str = Field(description="If the given review has text about Safety and Security on the Hotel or resort ,\
    is it positive or Negative ?.if its positive return 'Positive',\
     if its Negative return 'Negative' if its Neutral return 'Neutral' ,if the customer didn't write about Safety and Security then return  'Not Available'. The Output should a String")
    Dining_and_Food_Quality : str = Field(description="If the given review has text about Dining and Food Quality of Hotel or resort ,\
    is it positive or Negative ?.if its positive return 'Positive',\
     if its Negative return 'Negative' if its Neutral return 'Neutral' ,if the customer didn't write about Dining and Food Quality then return  'Not Available'. The Output should a String")
    Overall_Experience : str = Field(description="Classify the Overall Experience as  'positive' or 'negative' or 'Neutral'. The Output should a String")
  # Set up a parser + inject instructions into the prompt template.
  parser = PydanticOutputParser(pydantic_object=Applicant)

  prompt = PromptTemplate(
      template="Provide the answers only from the given text.\n{format_instructions}\n{text}\n",
      input_variables=["text"],
      partial_variables={"format_instructions": parser.get_format_instructions()},
  )

  with get_openai_callback() as cr :
      model = AzureChatOpenAI()
      val = model.invoke(prompt.invoke({"text": text}).to_string(), engine="gpt_4_32k")
      # st.session_state.Amount_Spent+=cr.total_cost

  output = json.loads(val.content)

  df = pd.DataFrame.from_dict(output,orient='index').T
  df['Review'] = text
  return df