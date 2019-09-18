#!D:/Python/Python36/python.exe
#!C:/ProgramData/Anaconda3/python.exe
import cgi, cgitb
import os
import pandas as pd
import numpy as np
from module.NER import NER
from module.TextProcessor import TextProcessor
import json
#transfer [誰,v,n,ans]
class node:
    def __init__(self,data):
        self.data = data
        self.link = []
        self.transfer = []
        
def insert(a,lis,ite,transfer):
    if ite > len(lis) - 1:
        a.transfer.append(transfer)
        return a
    same = False
    for i in range(len(a.link)):
        if a.link[i].data == lis[ite]:
            same = True
            break
    if same:
        a.link[i] = insert(a.link[i],lis,ite + 1,transfer)
    else:
        a.link.append(node(lis[ite]))
        a.link[-1] = insert(a.link[-1],lis,ite + 1,transfer)  
    return a

root_list = []
data_dir = 'rule.csv'
df = pd.read_csv(data_dir,engine='python',encoding='utf_8_sig')
que_remain = []
with open('que_remain_long_test.txt','r',encoding='utf8') as fin:
    for row in fin:
        row = row.lstrip().rstrip()
        que_remain.append(row)
que_remain = que_remain[1:]

for i in range(len(df)):
    if not df.iloc[i,3] == df.iloc[i,3] or df.iloc[i,3] == None:
        continue
    if not df.iloc[i,4] == df.iloc[i,4] or df.iloc[i,4] == None:
        continue
    if df.iloc[i,5] != df.iloc[i,5]:
        continue
    rule = df.iloc[i,3]
    transfer = df.iloc[i,4]
    ans = df.iloc[i,5]
    transfer += ' + ' + ans
    rule = rule.split('+')
    for j in range(len(rule)):
        rule[j] = rule[j].lstrip().rstrip()
    root = rule[0]
    for j in range(len(root_list)):
        if root_list[j].data == root:
            root = root_list[j]
            
    if root == rule[0]:
        root = node(root)
        root_list.append(root)
    root = insert(root,rule,1,transfer)

def find_rule(index,p,flag_list):
    if index >= len(flag_list):
        all_transfer.extend(p.transfer)
        return 
    if p.transfer:
        all_transfer.extend(p.transfer)
    for ele in p.link:
        if ele.data == flag_list[index]:
            find_rule(index + 1,ele,flag_list)
    return

def rule_match(a,b):
    if abs(len(a) - len(b)) > 0:
        return False
    else:
        return True
    
def find_rule_main(root_list,data):
    global all_transfer
    data = data.split(' ')
    word_list = []
    flag_list = []
    df_return = []
    iRun = 1
    for i in range(len(data)):
        data[i] = data[i].split('_')
        try:
            word = data[i][0]
            flag = data[i][1]
        except:
            continue
        word_list.append(word)
        flag_list.append(flag)
    if word_list == [] or flag_list == []:
        return []
    for root in root_list:
        if root.data == flag_list[0]:
            all_transfer = []
            find_rule(1,root,flag_list)
            if all_transfer:
                all_transfer = list(set(all_transfer))
                for rule in all_transfer:
                    df = []
                    df.append(' + '.join(flag_list))
                    bool_list = []
                    for j in range(len(flag_list)):
                        bool_list.append(True)
                    aft_transfer = ''
                    rule = rule.split('+')
                    for j in range(len(rule)):
                        rule[j] = rule[j].lstrip().rstrip()
                    ans = rule[-1]
                    rule = rule[:-1]
                    df.append(' + '.join(rule))
                    for f in rule:
                        if f in que_remain:
                            aft_transfer += f
                            continue
                        for j in range(len(flag_list)):
                            if flag_list[j] == f and bool_list[j]:
                                aft_transfer += word_list[j]
                                bool_list[j] = False
                                break
                        for j in range(len(flag_list)):
                            if flag_list[j] == ans:
                                ans = word_list[j]
                                break
                    df.append(''.join(word_list))
                    df.append(aft_transfer)
                    df.append(ans)
                    if len(df) == 5 and rule_match(flag_list,rule):
                        df_return.append(df)
                all_transfer = []
    return df_return

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        pass
 
    try:
        import unicodedata
        unicodedata.numeric(s)
        return True
    except (TypeError, ValueError):
        pass
 
    return False

def remove_number(s):
    result = ''
    for ele in s:
        if not is_number(ele):
            result += ele
    return result

def p_flag_sort(data):
    flag_num_dict = {}
    result = []
    article_list = []
    for i in range(len(data)):
        temp = data[i].split('_')
        try:
            word = temp[0]
            flag = temp[1]
        except:
            continue
            
        flag = remove_number(flag)
        if flag == 'x' or flag == 'w':
            continue
        temp = flag_num_dict.get(flag)
        if temp == None:
            flag_num_dict.update({flag:2})
            flag = flag + '1'
        else:
            flag_num_dict[flag] += 1
            flag = flag + str(temp)
        result.append(word + '_' + flag)
        article_list.append(flag)
    return result,article_list

def article_pre(data):
    data = data.replace('\n','')
    data = data.replace('\r',' ')
    return data
"""
df = pd.read_csv('all.csv')
df.drop_duplicates('課文','first',inplace = True)
df_result = []
que_ans_dict = {}
for i in range(len(df)):
    if not df.iloc[i,1] == df.iloc[i,1] or df.iloc[i,1] == None:#判斷nan
        continue
    if not df.iloc[i,2] == df.iloc[i,2] or df.iloc[i,2] == None:#判斷nan
        continue
    if df.iloc[i,3] == df.iloc[i,3]:
        continue
    df.iloc[i,1] = article_pre(df.iloc[i,1])
    temp,b = p_flag_sort((df.iloc[i,1]).split(' '))
    temp = ' '.join(temp)
    find_rule_temp = find_rule_main(root_list,temp)
    if len(find_rule_temp) > 0:
        df_result.extend(find_rule_temp)
for i in range(len(df_result)):
    que = df_result[i][3]
    ans = df_result[i][4]
    temp = [que,ans]
    que_ans_dict.update({str(i):temp})
df_result = pd.DataFrame(np.array(df_result))
df_result.to_csv('C:\\Users\\student\\Desktop\\test.csv',index=0,encoding='utf_8_sig')
"""
boson_remain = []
ner_eng_ch_dict = {'per':'人','obj':'物','time':'時','place':'地'}
with open('boson_remain.txt','r',encoding='utf8') as fin:
    bFR = True
    for row in fin:
        if bFR:
            bFR = False
            continue
        row = row.lstrip().rstrip()
        boson_remain.append(row)
boson_simpler_dict = {}
with open('boson_simpler.txt','r',encoding='utf8') as fin:
    bFR = True
    for row in fin:
        if bFR:
            bFR = False
            continue
        row = row.lstrip().rstrip()
        row = row.split(' ')
        boson_simpler_dict.update({row[0]:row[1]})
        
NER = NER()
parameter = cgi.FieldStorage()
text = parameter.getvalue('text')
# text = "小美喜歡小明"

# text = """
# 大自然會說話，你相信嗎？
# 當你看到天空潔淨，白雲飄
# 得高高時，它告訴你：「今天是晴
# 天，你可以計畫去旅遊。」
# 如果天空陰沉沉的，烏雲一
# 片片的聚在一起，它就是通知
# 你：「要下雨了，出門別忘了帶把
# 傘。」

# 當地上的螞蟻急急忙忙的搬
# 家，從地上搬到樹上，它是換一
# 個方式告訴你：「快要下雨了。」
# 你看到樹枝長出紅色或綠色
# 的新芽，或是池塘裡的青蛙，嘓
# 嘓叫個不停時，它們就告訴你：
# 「春天來了！」
# 一圈圈的年輪，告訴你樹有
# 多少年紀了。

# 葉子從樹上飄下來，你就知
# 道：「秋天來了，天氣轉涼了，要
# 記得多穿幾件衣服。」
# 大自然的語言處處都看得
# 見，喜歡學習的人，認真觀察的
# 人，隨時可以從大自然的變化
# 中，學到知識。
# """
tp = TextProcessor()
sentence_list = tp.sentence_break(text,split_char="，!?。！？")
df_result = []
for sentence in sentence_list:
    # print(sentence)
    # print('---')
    segment, flag_list, ner = NER.predict(sentence)
    word_cut_list = []
    for i in range(len(segment)):
        word = segment[i]
        flag = ner[i] 
        if flag in boson_remain:
            flag = ner_eng_ch_dict.get(ner[i])
        else:
            flag = boson_simpler_dict.get(flag_list[i])
            if flag == None:
                flag = flag_list[i]
        word_cut_list.append(word + '_' + flag)
    word_cut = ' '.join(word_cut_list)
    word_cut = article_pre(word_cut)
    word_cut,b = p_flag_sort(word_cut.split(' '))
    word_cut = ' '.join(word_cut)
    # print(word_cut)
    # print('---')
    find_rule_temp = find_rule_main(root_list,word_cut)
    # print(find_rule_temp)
    # print('---')
    df_result.extend(find_rule_temp)
que_ans_dict = {}
for i in range(len(df_result)):
    que_ans_dict.update({i:[df_result[i][3],df_result[i][4]]})

#將輸入丟進規則樹
print("Content-type:text/html") #必須
print('') #必須
#print(que_ans_dict)
# print(que_ans_dict)
print(json.dumps(que_ans_dict))
