import os

import openai
os.environ["OPENAI_API_KEY"] = "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"
from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv()) # read local .env file
openai.api_key = os.environ['OPENAI_API_KEY']
from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.chains import LLMChain
from langchain.chains import SimpleSequentialChain
from langchain.agents import tool
from langchain.agents.agent_toolkits import create_python_agent
from langchain.agents import load_tools, initialize_agent
from langchain.agents import AgentType
from langchain.tools.python.tool import PythonREPLTool
from langchain.python import PythonREPL
from langchain.chat_models import ChatOpenAI
import openai
import os
import re
import requests
import sys
from num2words import num2words
import os
import pandas as pd
import numpy as np
from openai.embeddings_utils import get_embedding, cosine_similarity
import tiktoken

"""API_KEY = os.getenv("AZURE_OPENAI_API_KEY")
RESOURCE_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")

openai.api_type = "azure"
openai.api_key = API_KEY
openai.api_base = RESOURCE_ENDPOINT
print(openai.api_base)
print(openai.api_key)
openai.api_version = "2022-12-01"

url = openai.api_base + "/openai/deployments?api-version=2022-12-01"

r = requests.get(url, headers={"api-key": API_KEY})

print(r.text)"""

import os

os.environ["OPENAI_API_TYPE"]="azure"
os.environ["OPENAI_API_VERSION"]="2023-03-15-preview"
os.environ["OPEN_API_BASE"]=" "
os.environ["OPEN_API_KEY"]=" "
from langchain.llms import AzureOpenAI

def get_completion(prompt, model="gpt-3.5-turbo"):
    messages = [{"role": "user", "content": prompt}]
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=0, 
    )
    return response.choices[0].message["content"]


# Define the Agent class
class PatientAgent:
    def __init__(self, name, age):
        self.name = name
        self.age = age
        self.symptoms = []

    def add_symptom(self, symptom):
        self.symptoms.append(symptom)

    def get_context(self):
        context = f"The patient's name is {self.name} and their age is {self.age}."
        if self.symptoms:
            context += f" They are experiencing {', '.join(self.symptoms)} in terms of back pain."
        return context

# Define the email generation function using the Agent
def generate_email(agent,email):
    context = agent.get_context()

    email_prompt = f""" You are an AI service bot and you are writing a email to the patient\
    after diagnosing them based on the symtoms described in {context}. Write the mail in a professional\
    manner and do not provide any specific details about the diagnosis. Always contain an assuring tone in the\
    email. Sign the email by Red_Flags. End the email properly. Send the email to {email}
    """

    agent_message = {
        "role": "user",
        "content": email_prompt
    }

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a doctor."},
            agent_message
        ],
        
    )

    return response.choices[0].message['content']

# Create an instance of the PatientAgent and add symptoms
patient = PatientAgent("John Doe", 45)
patient.add_symptom("lower back pain")
patient.add_symptom("muscle stiffness")

# Generate the email based on patient information
email=input("Enter your email")
generated_email = generate_email(patient,email)

# Print the generated email
print(generated_email)


