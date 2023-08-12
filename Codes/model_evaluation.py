import pandas as pd
import numpy as np
import re
#df = pd.read_excel('/home/user/Desktop/r.xlsx', sheet_name = 'Bakhshandeh')

df = pd.read_excel(r'/home/user/Desktop/python vul Datasets/all/results/newperclass_label_ALL_v2.xlsx', sheet_name = 'Bakhshandeh')
#labels = pd.read_excel('labels.xlsx', sheet_name = 'Mr chekidet labels')

df['Sonar'] = df['Sonar'].astype(str)

df['Sonar'] = df['Sonar'].apply(lambda x: re.sub(r'\b0(\d{1})\b|\b0(\d{2})\b', r'\1\2', x))

df['Sonar'] = df['Sonar'].apply(lambda x: re.sub(r'(CWE-\d+)-0(\d)', r'\1-\2', x))

df['Semgrep'] = df['Semgrep'].astype(str)

df['Semgrep'] = df['Semgrep'].apply(lambda x: re.sub(r'\b0(\d{1})\b|\b0(\d{2})\b', r'\1\2', x))

df['Semgrep'] = df['Semgrep'].apply(lambda x: re.sub(r'(CWE-\d+)-0(\d)', r'\1-\2', x))

#df['Bandit']=df['Bandit'].str.replace(r'\(blacklist\)', '', regex=True)


df['Bandit'] = df['Bandit'].astype(str)

df['Bandit'] = df['Bandit'].apply(lambda x: re.sub(r'\b0(\d{1})\b|\b0(\d{2})\b', r'\1\2', x))

df['Bandit'] = df['Bandit'].apply(lambda x: re.sub(r'(CWE-\d+)-0(\d)', r'\1-\2', x))



df['GPT_perClass_label'] = df['GPT_perClass_label'].astype(str)

df['GPT_perClass_label'] = df['GPT_perClass_label'].apply(lambda x: re.sub(r'\b0(\d{1})\b|\b0(\d{2})\b', r'\1\2', x))

df['GPT_perClass_label'] = df['GPT_perClass_label'].apply(lambda x: re.sub(r'(CWE-\d+)-0(\d)', r'\1-\2', x))


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
df['Sonar'] = df['Sonar'].apply(lambda x: ','.join(remove_duplicates(x)))
df['Semgrep'] = df['Semgrep'].apply(lambda x: ','.join(remove_duplicates(x)))
df['Bandit'] = df['Bandit'].apply(lambda x: ','.join(remove_duplicates(x)))
df['GPT_perClass_label'] = df['GPT_perClass_label'].apply(lambda x: ','.join(remove_duplicates(x)))



labels=df
#this function returns x-y(CWE-num) in which x is the number of row of df and
#  y is the number of line of code that is included in the label
def reder(col):
    temp = df[col][df[col].notna()].str.split(',').explode()
    preds = (temp.index.astype(str) + '-' + temp)
    preds = preds[preds.notna()].values
    return preds

#print(df.columns)
bandpreds = reder('Bandit')
print(bandpreds)
gptpreds = reder('GPT_perClass_label')
print(gptpreds)
sempreds = reder('Semgrep')
print(sempreds)
sonarpreds=reder('Sonar')
print(sonarpreds)
# sonarpreds = reder('Mr. Chekideh sonarqube')
# codeqlpreds = reder('Mr. Chekideh codeql')  
exploded_labels = labels['Mr. Chekideh'].str.split(',').explode()
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
    return len(tp)/len([x for x in preds if '-nan' not in x])

def my_f1(labels, preds):
    tp = [x for x in preds if x in labels]
    if len(preds) == 0:
        return 0
    return len(tp)/len([x for x in preds if '-nan' not  in x])

def fp(labels, preds):
    tp = [x for x in preds if x in labels]
    [x for x in preds] 
     
def bench_it(labels, preds, attack = ''):
    if attack != '':
        attack = '('+attack+')'
    labels = [x for x in labels if attack.lower() in x.lower()]
    attack.lower()
    preds = [x for x in preds if attack.lower() in x.lower()]
    
    pre = my_pre(labels, preds)
    rec = my_rec(labels, preds)
    # if attack == '':
    #     print(pre, 'labels:', labels, 'preds:', preds)

    
    #print(pre, labels, preds)

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
    #print('*****', name)
    df = full_bench(preds)
    df.columns = pd.MultiIndex.from_tuples([(name, x) for x in full_bench(df).columns])
    return df 
 
final_res_df=pd.concat([mc(sempreds, 'semgrep'), mc(bandpreds, 'bandit'), mc(gptpreds,'gpt'), mc(sonarpreds,'sonar')], axis=1)

with pd.ExcelWriter(r'/home/user/Desktop/final_rslt.xlsx') as writer:  
    final_res_df.to_excel(writer, sheet_name='Bakhshandeh')