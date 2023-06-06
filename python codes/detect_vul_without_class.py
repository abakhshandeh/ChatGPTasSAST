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
#     print(str(response.choices[0].message))
    return response.choices[0].message["content"]



directory = '/home/user/Desktop/python vul Datasets/PyT1/Labeled_files'

for filename in os.listdir(directory):
    f = os.path.join(directory, filename)
    # checking if it is a file
    if os.path.isfile(f):
        #print(f)
        with open(f,'r') as file:
            Vul_code=file.read()
            prompt3 = f"""
            your task is to determine whether the following python code which is delimited with triple backticks,is vulnerable or not?
            identify the following items:
                - CWE of the its vulnerabilities. \
                - lines of vulnerable code. \
            Format your response as a list of JSON objects with \
            "label" and "line of Code" as the keys for each vulnerability.
            If the information isn't present, use "unknown" \
            as the value.
            Make your response as short as possible and only answer with JSON. .
            python code: '''{Vul_code}'''                
            """

            #print(prompt3)
            response = get_completion(prompt3)
            with open("/home/user/Desktop/python vul Datasets/PyT1/gpt_result_withoutclass.txt", "a") as output:
                s=str(response).replace('\n',' ').strip()
                output.write(rf'{filename}#{s}')
                output.write('\n')
            print(response)
            time.sleep(20)



