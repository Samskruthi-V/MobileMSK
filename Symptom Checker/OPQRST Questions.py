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

# Generate OPQRST questions using LLM
def generate_opqrst_questions(selected_symptoms):
    question_prompt = f"I am experiencing {', '.join(selected_symptoms)}. Please provide details for the following:"

    questions = ['Onset:', 'Provocation/Palliation:', 'Quality:', 'Region/Radiation:', 'Severity:', 'Timing:']

    for i in range(len(questions)):
        prompt = f"{question_prompt}\n\nQ{i+1}: {questions[i]}"
        response = openai.Completion.create(
            engine='text-davinci-003',
            prompt=prompt,
            max_tokens=30,
            n=1,
            stop=None,
            temperature=0.5
        )
        completion = response.choices[0].text.strip()
        questions[i] += ' ' + completion

    return questions

# Example usage
selected_symptoms = ['back pain']

# Generate OPQRST questions using LLM
opqrst_questions = generate_opqrst_questions(selected_symptoms)

# Print the OPQRST questions
print("OPQRST Questions:")
for question in opqrst_questions:
    print(question)
