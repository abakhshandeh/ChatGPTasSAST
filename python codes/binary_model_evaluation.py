import pandas as pd
import numpy as np
import re
df = pd.read_excel('/home/user/Desktop/python vul Datasets/all/all_dataset_final_labels.xlsx', sheet_name = 'Bakhshandeh')
#labels = pd.read_excel('labels.xlsx', sheet_name = 'Mr chekidet labels')

#print(df)
labels=df
#this function returns x-y(CWE-num) in which x is the number of row of df and
#  y is the number of line of code that is included in the label
def reder(col):
    temp = df[col][df[col].notna()].astype(str).str.split(',').explode().astype(float).astype(int).astype(str)
 #   print("temp "+temp)
    
    #print(temp)
    preds = (temp.index.astype(str) + '-' + temp)
  #  print('preds '+preds)
    preds = preds[preds.notna()].values
    return preds

#print(df.columns)
bandpreds = reder('Bandit_binary')
gptpreds = reder('gpt_binary')
sempreds = reder('Semgrep_binary')
# sonarpreds = reder('Mr. Chekideh sonarqube')
# codeqlpreds = reder('Mr. Chekideh codeql')  
exploded_labels = labels['Mr. Chekideh_binary'].str.split(',').explode()
#print(exploded_labels)
dist_labels = (exploded_labels.index.astype(str) + '-' + exploded_labels).values
#print(dist_labels) 
def my_rec(labels, preds):
    rec_samples = [x for x in preds if x in labels]
    return len(rec_samples)/len(labels)

def my_pre(labels, preds):
    tp = [x for x in preds if x in labels]
    if len(preds) == 0:
        return 0
    return len(tp)/len(preds)

def fp(labels, preds):
    tp = [x for x in preds if x in labels]
    [x for x in preds] 
     
def bench_it(labels, preds, attack = ''):
    # print('attack '+attack)
    # print('labels ',labels)
    # labels = [x for x in labels if attack.lower() in x.lower()]
    #attack.lower()
    preds = [x for x in preds if attack.lower() in x.lower()]
    print('label ', labels)
    print('preds ',preds)
    pre = my_pre(labels, preds)
    rec = my_rec(labels, preds)
    if (pre + rec) == 0:
        return [pre, rec, 0]
    def f1(precision, recall):
        return 2 * (precision * recall) / (precision + recall)
    return [pre, rec, f1(pre, rec)]

labels_dist = exploded_labels.str.extract('\((.*)\)')[0].value_counts()  
#print(labels_dist)

def full_bench(preds):
    atts = list(labels_dist.index)
    atts.append('')
    #print(labels_dist)
    sems = []
    for attack in atts:
        temp = bench_it(dist_labels, preds, attack)
        temp.extend([attack if attack != '' else 'all', labels_dist[attack] if attack != '' else sum(labels_dist)])
        sems.append(temp)
    df = pd.DataFrame(sems, columns = ['Precision', 'Recall', 'F1-Score', 'Attack', 'Support'])
    df = df.set_index('Attack')
    return df 
 
def mc(preds, name):
    df = full_bench(preds)
    df.columns = pd.MultiIndex.from_tuples([(name, x) for x in full_bench(df).columns])
    return df 
 
#print(mc(gptpreds, 'gpt'))

final_res_df=pd.concat([mc(sempreds, 'semgrep'), mc(bandpreds, 'bandit'),mc(gptpreds,'gpt')], axis=1)

with pd.ExcelWriter('/home/user/Desktop/final_res.xlsx') as writer:  
    final_res_df.to_excel(writer, sheet_name='Bakhshandeh')