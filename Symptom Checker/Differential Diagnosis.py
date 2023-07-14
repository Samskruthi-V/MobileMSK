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

# Define the list of symptoms and associated conditions
symptoms = {
    'back pain': ['muscle strain', 'herniated disc', 'spinal stenosis'],
    # Add more symptoms and associated conditions
}

# Define the VINDICATE acronym and associated condition categories
vindicate = {
    'V': ['vascular condition'],
    'I': ['infection', 'inflammatory condition'],
    'N': ['neoplastic condition'],
    'D': ['degenerative condition', 'deficiency disorder'],
    'I': ['intoxication'],
    'C': ['congenital condition', 'collagen disorder'],
    'A': ['autoimmune condition', 'allergy'],
    'T': ['trauma'],
    'E': ['endocrine disorder', 'metabolic disorder']
    # Add more categories and conditions
}

# Generate a differential diagnosis based on selected symptoms using LLM
def generate_differential_diagnosis(selected_symptoms):
    differential_diagnosis = []

    for symptom in selected_symptoms:
        if symptom in symptoms:
            differential_diagnosis.extend(symptoms[symptom])

    return differential_diagnosis

# Organize the differential diagnosis using the VINDICATE acronym
def organize_differential_diagnosis(differential_diagnosis):
    organized_diagnosis = {key: [] for key in vindicate.keys()}

    for condition in differential_diagnosis:
        for key, categories in vindicate.items():
            for category in categories:
                if category.lower() in condition.lower():
                    organized_diagnosis[key].append(condition)
                    break

    return organized_diagnosis

# Generate a differential diagnosis using LLM for improved accuracy
def generate_differential_diagnosis_llm(selected_symptoms):
    symptom_string = ', '.join(selected_symptoms)
    prompt = f"I am experiencing {symptom_string}. What could be the possible causes?"
    response = openai.Completion.create(
        engine='text-davinci-003',
        prompt=prompt,
        max_tokens=100,
        n=5,  # Adjust the number of completions as needed
        stop=None,
        temperature=0.5
    )
    completions = response.choices

    differential_diagnosis = []
    for completion in completions:
        differential_diagnosis.append(completion.text.strip())

    return differential_diagnosis

# Example usage
selected_symptoms = ['back pain']

# Generate and organize the differential diagnosis using LLM
differential_diagnosis_llm = generate_differential_diagnosis_llm(selected_symptoms)
organized_diagnosis_llm = organize_differential_diagnosis(differential_diagnosis_llm)

# Print the differential diagnosis
print("Differential Diagnosis (with LLM):")
for key, conditions in organized_diagnosis_llm.items():
    if conditions:
        print(f"{key}:")
        for condition in conditions:
            print(f"- {condition}")
