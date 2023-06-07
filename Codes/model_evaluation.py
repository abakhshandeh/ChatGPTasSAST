import pandas as pd
import numpy as np
import re
df = pd.read_excel('/home/user/Desktop/python vul Datasets/all/noclass_final_res.xlsx', sheet_name = 'Bakhshandeh')

df['Bandit'] = df['Bandit'].astype(str)

df['Bandit'] = df['Bandit'].apply(lambda x: re.sub(r'\b0(\d{1})\b|\b0(\d{2})\b', r'\1\2', x))

df['Bandit'] = df['Bandit'].apply(lambda x: re.sub(r'(CWE-\d+)-0(\d)', r'\1-\2', x))

#df['Bandit']=df['Bandit'].str.replace(r'\(blacklist\)', '', regex=True)

def remove_spaces(text):
    return re.sub(r'(\d) +\(', r'\1(', text)

df['Mr. Chekideh'] = df['Mr. Chekideh'].astype(str)


df['Mr. Chekideh'] = df['Mr. Chekideh'].apply(remove_spaces)
df['Mr. Chekideh'] = df['Mr. Chekideh'].apply(lambda x: re.sub(r'\b0(\d{1})\b|\b0(\d{2})\b', r'\1\2', x))
df['Mr. Chekideh'] = df['Mr. Chekideh'].str.replace(', ', ',')


def remove_duplicates(cwe_list):
    if isinstance(cwe_list, float) and np.isnan(cwe_list):
        return []
    else:
        return sorted(list(set(cwe_list.split(','))))


df['Mr. Chekideh'] = df['Mr. Chekideh'].apply(lambda x: ','.join(remove_duplicates(x)))
df['Semgrep'] = df['Semgrep'].apply(lambda x: ','.join(remove_duplicates(x)))
df['Bandit'] = df['Bandit'].apply(lambda x: ','.join(remove_duplicates(x)))
df['GPT_NoClass_label'] = df['GPT_NoClass_label'].apply(lambda x: ','.join(remove_duplicates(x)))



labels=df
#this function returns x-y(CWE-num) in which x is the number of row of df and
#  y is the number of line of code that is included in the label
def reder(col):
    temp = df[col][df[col].notna()].str.split(',').explode()
    preds = (temp.index.astype(str) + '-' + temp)
    preds = preds[preds.notna()].values
    return preds


bandpreds = reder('Bandit')
gptpreds = reder('GPT_NoClass_label')
sempreds = reder('Semgrep')

exploded_labels = labels['Mr. Chekideh'].str.split(',').explode()

dist_labels = (exploded_labels.index.astype(str) + '-' + exploded_labels).values
 
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
    labels = [x for x in labels if attack.lower() in x.lower()]
    attack.lower()
    preds = [x for x in preds if attack.lower() in x.lower()]
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


final_res_df=pd.concat([mc(sempreds, 'semgrep'), mc(bandpreds, 'bandit'),mc(gptpreds,'gpt')], axis=1)

with pd.ExcelWriter('/home/user/Desktop/final_res.xlsx') as writer:  
    final_res_df.to_excel(writer, sheet_name='Bakhshandeh')
