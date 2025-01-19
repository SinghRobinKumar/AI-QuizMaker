import os
import json
import pandas as pd
import traceback
from langchain import LLMChain
from langchain.prompts import PromptTemplate
from langchain.chains import SequentialChain
import PyPDF2


from dotenv import load_dotenv

load_dotenv()

KEY = os.getenv("GOGGLE_GEMINI_API_KEY")


from langchain_google_genai import ChatGoogleGenerativeAI

llm = ChatGoogleGenerativeAI(model="gemini-pro", temperature=0.3, api_key=KEY)


TEMPLATE = """
Text: {text}

You are an expert MCQ maker. Given the above text, it is your job to 
create a quiz of {number} multiple-choice questions for {subject} students in {tone} tone.
Make sure the questions are not repeated and check all the questions to conform to the text as well.
Make sure to format your response like RESPONSE_JSON below and use it as a guide. 
Ensure to make {number} MCQs.

### RESPONSE_JSON
{response_json}
"""

quiz_generation_propmt = PromptTemplate(
    input_variables=["text", "number", "subject", "tone", "response_json"],
    template=TEMPLATE,
)

quiz_chain = LLMChain(
    llm=llm, prompt=quiz_generation_propmt, output_key="quiz", verbose=True
)

TEMPLATE2 = """
You are an expert English grammarian and writer. Given a Multiple Choice Quiz for {subject} students.
You need to evaluate the complexity of the question and give a complete analysis of the quiz. Only use at max 50 words for complexity analysis.
If the quiz is not at par with the cognitive and analytical abilities of the students,
update the quiz questions which need to be changed and adjust the tone such that it perfectly fits the students' abilities.

Quiz_MCQs:
{quiz}

Check from an expert English Writer of the above quiz:
"""

quiz_evaluation_propmt = PromptTemplate(
    input_variables=["subject", "quiz"], template=TEMPLATE2
)

review_chain = LLMChain(
    llm=llm, prompt=quiz_evaluation_propmt, output_key="review", verbose=True
)

generate_evaluate_chain = SequentialChain(
    chains=[quiz_chain, review_chain],
    input_variables=["text", "number", "subject", "tone", "response_json"],
    output_variables=["quiz", "review"],
    verbose=True,
)
