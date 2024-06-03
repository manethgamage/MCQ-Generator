import os
import json
import traceback
import pandas as pd
from src.mcqGenerator.utils import read_file, get_table_data
import streamlit as st
from src.mcqGenerator.MCQGenerator import generate_evaluate_chain
from src.mcqGenerator.logger import logging

with open('Response.json','r') as file:
    RESPONSE_JSON = json.load(file)
    
#creating a title for the app
st.title("MCQ Generator")

#creating a form
with st.form("user_inputs"):
    #file upload
    uploaded_file = st.file_uploader("Upload a PDF or Text file")
    
    #Input Field
    mcq_count = st.number_input("No. of MCQs", min_value=3, max_value=50)
    
    #subject
    subject = st.text_input("Insert Subject", max_chars=20)
    
    #Quiz Tone
    tone = st.text_input("Complexity level of Questions",max_chars=20,placeholder="simple")
    
    #Add Button
    button = st.form_submit_button("create MCQs")
    
    #Check if the button is clicked and all fields have inputs
    if button and uploaded_file is not None and mcq_count and subject and tone:
        with st.spinner("loading..."):
            try:
                text = read_file(uploaded_file)
                reponse = generate_evaluate_chain(
                    {
                    "text": text,
                    "number": tone,
                    "subject":subject,
                    "tone":tone,
                    "response_json": json.dumps(RESPONSE_JSON)
                        }
                    
        
                )
            except Exception as e:
                traceback.print_exception(type(e), e, e.__traceback__)
                st.error("Error")
            
            else:
                if isinstance(reponse, dict):
                    #extract the quiz data from the response
                    quiz = reponse.get("quiz", None)
                    if quiz is not None:
                        table_data = get_table_data(quiz)
                        if table_data is not None:
                            df = pd.DataFrame(table_data)
                            df.index = df.index+1 
                            st.table(df)
                            st.text_area(label="Review", value=reponse["review"])
                        else:
                            st.error("error in the table data")
                else:
                    st.write(reponse)          
                
                
            
        
    