import os
import json
import traceback
import streamlit as st
import pandas as pd
from dotenv import load_dotenv

from src.mcqgenerator.utils import read_file, get_table_data
from src.mcqgenerator.MCQGenerator import generate_evaluate_chain
from src.mcqgenerator.logger import logging

# loading Response JSON
with open("Response.json", "r") as f:
    RESPONSE_JSON = json.load(f)

# for Streamlit App
st.title("MCQ Generator with Langchain")

with st.form("user_inputs"):
    uploaded_file = st.file_uploader("Please upload a PDF or TXT file")

    mcq_count = st.number_input("No. of MCQs", min_value=3, max_value=50)

    subject = st.text_input("Enter Subject", max_chars=20)

    tone = st.text_input(
        "Complexity Level of the Questions", max_chars=20, placeholder="Simple"
    )

    button = st.form_submit_button("Generate MCQs")

    if button and uploaded_file is not None and mcq_count and subject and tone:
        with st.spinner("loading..."):
            try:
                text = read_file(uploaded_file)

                response = generate_evaluate_chain(
                    {
                        "text": text,
                        "number": mcq_count,
                        "subject": subject,
                        "tone": tone,
                        "response_json": json.dumps(RESPONSE_JSON),
                    }
                )

            except Exception as e:
                traceback.print_exception(type(e), e, e.__traceback__)
                st.error("Error")

            # Else will run everytime
            else:
                if isinstance(response, dict):
                    unrefined_quiz = response.get("quiz", None)

                    # This is for Google Gemini Pro API

                    # quiz = unrefined_quiz.strip('"').replace("### RESPONSE_JSON\\n", "")
                    quiz = unrefined_quiz.strip('"').replace("### RESPONSE_JSON", "")

                    # To remove Slashes for eg){\\"mcq\\": \\"Which of the following is NOT a core concept of AI?\\",}
                    json_string = quiz.encode().decode("unicode_escape")

                    if quiz is not None:
                        table_data = get_table_data(json_string)

                        if table_data is not None:

                            df = pd.DataFrame(table_data)
                            df.index = df.index + 1

                            # Streamlit Table
                            st.table(df)
                            # Display review in text-area
                            st.text_area(label="Review", value=response["review"])
                        else:
                            st.error("Error is the table data")

                else:
                    st.write(response)
