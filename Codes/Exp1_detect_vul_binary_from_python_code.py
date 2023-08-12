import openai
import os
import time
import urllib.parse
import requests
#from IPython import display,HTML
#from dotenv import load_dotenv,find_dotenv
openai.api_key=""


def get_completion(prompt, model="gpt-3.5-turbo"):
    messages = [{"role": "user", "content": prompt}]
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=0, # this is the degree of randomness of the model's output
    )
    return response.choices[0].message["content"]


def get_completion(prompt, model="gpt-3.5-turbo",temperature=0): # Andrew mentioned that the prompt/ completion paradigm is preferable for this class
    messages = [{"role": "user", "content": prompt}]
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=temperature, # this is the degree of randomness of the model's output
    )
    return response.choices[0].message["content"]

def get_completion_from_messages(messages, model="gpt-3.5-turbo", temperature=0):
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=temperature, # this is the degree of randomness of the model's output
    )
    return response.choices[0].message["content"]



directory = '/home/user/Desktop/python vul Datasets/misc/labeled_files'

for filename in os.listdir(directory):
    f = os.path.join(directory, filename)
    # checking if it is a file
    if os.path.isfile(f):
        #print(f)
        with open(f,'r') as file:
            Vul_code=file.read()
            
            binary_claissification_prompt = f"""
            You will be provided with a python code delimited by triple backticks. 
            If it contains any security vulnerability, identify the lines of vulnerable code and only write the line in quotation\ 
            If the code does not contain a vulnerability,\ 
            then simply write \"None.\"

            python code: '''{Vul_code}'''
            """
            #print(prompt3)
            response = get_completion(binary_claissification_prompt)
            with open("/home/user/Desktop/python vul Datasets/misc/test.csv", "a") as output:
                s=str(response).replace('\n',' ').strip()
                output.write(rf'{filename},{s}')
                output.write('\n')
            print(response)
            time.sleep(20)


