import openai
import os
import time
import urllib.parse
import requests
import pandas as pd
import re
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

	

df=pd.read_excel(rf'/home/user/Desktop/python vul Datasets/PyT2/PyTy2_final_labels.xlsx')
   

directory = '/home/user/Desktop/python vul Datasets/PyT2/Labeled_files' 
gpt_response_list=[]

df['Bandit'] = df['Bandit'].astype(str)

df['Bandit'] = df['Bandit'].apply(lambda x: re.sub(r'\b0(\d{1})\b|\b0(\d{2})\b', r'\1\2', x))

df['Bandit'] = df['Bandit'].apply(lambda x: re.sub(r'(CWE-\d+)-0(\d)', r'\1-\2', x))


for index, row in df.iterrows():            
    filename = str(row['Filename']) 
    banditLabels = str(row['Bandit'])
    semgrepLabels=str(row['Semgrep'])
    labels=",".join([banditLabels,semgrepLabels]).replace(',nan','').replace('nan,','')  
    print(filename) 
   # print(banditLabels,semgrepLabels)
    print(labels)
    #extracting only CWE-x from tools labels  
    labelsList=labels.split(',')
    listOfLabels=[]
    for i in labelsList:
       # print(i)
       if labels != 'nan':
            res=re.search('\(.*\)',i)
            value=res.group(0)
       # print(value)
            if value not in listOfLabels:
                listOfLabels.append(value)
    print(listOfLabels)
    #give the model the python file along with the labels of each python file
    f = os.path.join(directory, filename)
    # checking if it is a file
    if os.path.isfile(f):
        #print(f)
        with open(f,'r') as file:
            Vul_code=file.read()
           # print(Vul_code)
            prompt = f"""
            which of the following vulnerabilities from list of vulnerabilities exist in the python code which
            is delimited with triple backticks. also give the line of the vulnerability in the code.

            python code: '''{Vul_code}'''

            list of vulnerabilities: {", ".join(listOfLabels)}

            Format your response as a list of JSON objects with \
            "label" and "line of Code" as the keys for each element.
            only answer with JSON.
            """   
            response = get_completion(prompt)
            gpt_response_list.append(response)                       
            print(response)
            time.sleep(20)
print(gpt_response_list)  
df['gpt_perClass_response']=gpt_response_list
with pd.ExcelWriter('/home/user/Desktop/r.xlsx') as writer:  
                df.to_excel(writer, sheet_name='Bakhshandeh')


