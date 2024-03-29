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

	


labels3 = [
    
    "CWE-379","CWE-384","CWE-385","CWE-400","CWE-406","CWE-414","CWE-425","CWE-434","CWE-454"
    ,"CWE-462","CWE-477","CWE-488","CWE-502","CWE-521","CWE-522","CWE-595","CWE-601","CWE-605"
    ,"CWE-611","CWE-641","CWE-643","CWE-703","CWE-730","CWE-732","CWE-759","CWE-760","CWE-776"
    ,"CWE-798","CWE-827","CWE-835","CWE-841","CWE-918","CWE-941","CWE-943","CWE-352","CWE-409"
    ,"CWE-266","CWE-311","CWE-315","CWE-1240"
    ,"CWE-79", "CWE-489", "CWE-78", "CWE-94","CWE-15","CWE-22","CWE-89","CWE-1004"
    ,"CWE-614","CWE-95","CWE-20","CWE-80","CWE-90","CWE-99","CWE-113","CWE-116","CWE-117"
    ,"CWE-1204","CWE-193","CWE-200","CWE-209","CWE-215","CWE-250","CWE-252","CWE-259","CWE-269"
    ,"CWE-283","CWE-284","CWE-285","CWE-295","CWE-297","CWE-306","CWE-312","CWE-319","CWE-321"
    ,"CWE-326","CWE-327","CWE-329","CWE-330","CWE-331","CWE-339","CWE-347","CWE-367","CWE-377"
]


directory = '/home/user/Desktop/python vul Datasets/misc/labeled_files'

for filename in os.listdir(directory):
    f = os.path.join(directory, filename)
    # checking if it is a file
    if os.path.isfile(f):
        #print(f)
        with open(f,'r') as file:
            Vul_code=file.read()
            
           multiClass_prompt = f"""
    	    which of the following vulnerabilities from list of vulnerabilities exist in the python code which
            is delimited with triple backticks. also give the line of the vulnerability in the code.

            python code: '''{Vul_code}'''

            list of vulnerabilities: {", ".join(labels3)}

            Format your response as a list of JSON objects with \
            "label" and "line of Code" as the keys for each element.
            only answer with JSON.
            """
            #print(prompt3)
            response = get_completion(binary_claissification_prompt)
            with open("/home/user/Desktop/python vul Datasets/misc/test.csv", "a") as output:
                s=str(response).replace('\n',' ').strip()
                output.write(rf'{filename},{s}')
                output.write('\n')
            print(response)
            time.sleep(20)


