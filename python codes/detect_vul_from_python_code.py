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

	
#messages =  [  
#{'role':'system', 'content':'You are an assistant that speaks like Shakespeare.'},    
#{'role':'user', 'content':'tell me a joke'},   
#{'role':'assistant', 'content':'Why did the chicken cross the road'},   
#{'role':'user', 'content':'I don\'t know'}  ]

#response = get_completion_from_messages(messages, temperature=1)
#print(response)
Vul_code1 = """



labels = [
    "CWE-079", "CWE-489", "CWE-078", "CWE-094","CWE-015","CWE-022","CWE-089","CWE-1004"
    ,"CWE-614","CWE-095","CWE-020","CWE-080","CWE-090","CWE-099","CWE-113","CWE-116","CWE-117"
    ,"CWE-1204","CWE-193","CWE-200","CWE-209","CWE-215","CWE-250","CWE-252","CWE-259","CWE-269"
    ,"CWE-283","CWE-284","CWE-285","CWE-295","CWE-297","CWE-306","CWE-312","CWE-319","CWE-321"
    ,"CWE-326","CWE-327","CWE-329","CWE-330","CWE-331","CWE-339","CWE-347","CWE-367","CWE-377"
    ,"CWE-379","CWE-384","CWE-385","CWE-400","CWE-406","CWE-414","CWE-425","CWE-434","CWE-454"
    ,"CWE-462","CWE-477","CWE-488","CWE-502","CWE-521","CWE-522","CWE-595","CWE-601","CWE-605"
    ,"CWE-611","CWE-641","CWE-643","CWE-703","CWE-730","CWE-732","CWE-759","CWE-760","CWE-776"
    ,"CWE-798","CWE-827","CWE-835","CWE-841","CWE-918","CWE-941","CWE-943","CWE-352","CWE-409"
    ,"CWE-266","CWE-311","CWE-315","CWE-1240"
]

labels2 = [
    "CWE-79", "CWE-489", "CWE-78", "CWE-94","CWE-15","CWE-22","CWE-89","CWE-1004"
    ,"CWE-614","CWE-95","CWE-20","CWE-80","CWE-90","CWE-99","CWE-113","CWE-116","CWE-117"
    ,"CWE-1204","CWE-193","CWE-200","CWE-209","CWE-215","CWE-250","CWE-252","CWE-259","CWE-269"
    ,"CWE-283","CWE-284","CWE-285","CWE-295","CWE-297","CWE-306","CWE-312","CWE-319","CWE-321"
    ,"CWE-326","CWE-327","CWE-329","CWE-330","CWE-331","CWE-339","CWE-347","CWE-367","CWE-377"
    ,"CWE-379","CWE-384","CWE-385","CWE-400","CWE-406","CWE-414","CWE-425","CWE-434","CWE-454"
    ,"CWE-462","CWE-477","CWE-488","CWE-502","CWE-521","CWE-522","CWE-595","CWE-601","CWE-605"
    ,"CWE-611","CWE-641","CWE-643","CWE-703","CWE-730","CWE-732","CWE-759","CWE-760","CWE-776"
    ,"CWE-798","CWE-827","CWE-835","CWE-841","CWE-918","CWE-941","CWE-943","CWE-352","CWE-409"
    ,"CWE-266","CWE-311","CWE-315","CWE-1240"
]

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

#random sort
labels4= [
    "CWE-384","CWE-462","CWE-611","CWE-798","CWE-266","CWE-79","CWE-614","CWE-1204","CWE-283"
    ,"CWE-326","CWE-385","CWE-477","CWE-641","CWE-827","CWE-311","CWE-489","CWE-95","CWE-193"
    ,"CWE-284","CWE-327","CWE-400","CWE-488","CWE-643","CWE-835","CWE-315","CWE-78","CWE-20"
    ,"CWE-200","CWE-285","CWE-329","CWE-406","CWE-502","CWE-703","CWE-841","CWE-1240","CWE-94"
    ,"CWE-80","CWE-209","CWE-295","CWE-330","CWE-414","CWE-521","CWE-730","CWE-918","CWE-15"
    ,"CWE-90","CWE-215","CWE-297","CWE-331","CWE-425","CWE-522","CWE-732","CWE-941","CWE-22"
    ,"CWE-99","CWE-250","CWE-306","CWE-339","CWE-434","CWE-595","CWE-759","CWE-943","CWE-89"
    ,"CWE-113","CWE-252","CWE-312","CWE-347","CWE-454","CWE-601","CWE-760","CWE-352","CWE-1004"
    ,"CWE-116","CWE-259","CWE-319","CWE-367","CWE-605","CWE-776","CWE-409","CWE-117","CWE-269"
    ,"CWE-321","CWE-377","CWE-379"
]
#print(len({", ".join(labels3)}))
#Give your answer as list with 0 or 1 for each label.\

#List of topics: {", ".join(labels)}

directory = '/home/user/Desktop/python vul Datasets/PyT2/Labeled_files'

for filename in os.listdir(directory):
    f = os.path.join(directory, filename)
    # checking if it is a file
    if os.path.isfile(f):
        #print(f)
        with open(f,'r') as file:
            Vul_code=file.read()
            prompt3 = f"""
            You will be provided with a python code delimited by triple backticks. 
            If it contains any security vulnerability, identify the lines of vulnerable code and only write the line in quotation\ 
            If the code does not contain a vulnerability,\ 
            then simply write \"None\"

            python code: '''{Vul_code}'''
            """

            #print(prompt3)
            response = get_completion(prompt3)
            with open("/home/user/Desktop/python vul Datasets/PyT2/gpt_result.csv", "a") as output:
                s=str(response).replace('\n',' ').strip()
                output.write(rf'{filename},{s}')
                output.write('\n')
            print(response)
            time.sleep(20)


# prompt3 = f"""
#             You will be provided with a python code delimited by triple backticks. 
#             If it contains a vulnerability, identify the line of vulnerable code and write only the line\ 
#             If the code does not contain a vulnerability,\ 
#             then simply write \"None\"

#             python code: '''{Vul_code}'''
#             """

multiClass_prompt = f"""
    which of the following vulnerabilities from list of vulnerabilities exist in the python code which
            is delimited with triple backticks. also give the line of the vulnerability in the code.

            python code: '''{Vul_code}'''

            list of vulnerabilities: {", ".join(labels3)}

            Format your response as a list of JSON objects with \
            "label" and "line of Code" as the keys for each element.
            only answer with JSON.
            """

prompt = f"""
is the following python code vulnerable? identify the following items:

- CWE of the its vulnerability. \
- line of vulnerable code. \
The code is delimited with triple backticks.\
Format your response as a JSON object with \
"CWE" and "line of Code" as the keys.  
If the information isn't present, use "unknown" \
as the value.
Make your response as short as possible.

python code: '''{Vul_code}'''
"""


prompt2 = f"""
which of the following vulnerabilities from list of vulnerabilities exist in the python code which
is delimited with triple backticks.

python code: '''{Vul_code}'''

list of vulnerabilities: {", ".join(labels2)}

Give your answer as list with 0 or 1 for each vulnerability.
"""




prompt4 = f"""
find all the vulnerabilities with the CWE standard in the python code which
is delimited with triple backticks. also give the line of the vulnerability in the code.

python code: '''{Vul_code}'''

Format your response as a list of JSON objects with \
"label" and "line of Code" as the keys for each element.
only answer with JSON.
"""

