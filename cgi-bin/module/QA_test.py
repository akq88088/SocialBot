#!D:/Python/Python36/python.exe
#!C:/ProgramData/Anaconda3/python.exe
import cgi, cgitb
import os
import pandas as pd
import numpy as np
from module.NER import NER
from module.TextProcessor import TextProcessor
import json
import time
#transfer [誰,v,n,ans]
class QA_test:
    class node:
        def __init__(self,data):
            self.data = data
            self.link = []
            self.transfer = []

    def __init__(self):
        self.boson_remain_list = []
        self.boson_simpler_dict = {}
        self.que_remain_list = []
        self.sql_columns_list = []
        self.ner_eng_ch_dict = {'per':'人','obj':'物','time':'時','place':'地'}
        self.root_list = []
        self.data_dir = os.path.join('module','QA_data')
        self.load_data()
        self.create_root_tree()

    def predict(self,text):
        result = self.call_NER(text)
        result = pd.DataFrame(np.array(result))
        if len(result.columns) == 9:
            result.columns = ["匹配規則","匹配出題規則","輸入語句","輸入出題","輸入答案","RID","原文斷詞","原文出題","輸入斷詞"]
            result = result[["RID","輸入語句","輸入斷詞","輸入出題","輸入答案","匹配規則","匹配出題規則","原文斷詞","原文出題"]]
        return result
        

    def read_sql(self,data):
        pass

    def create_root_tree(self):
        # data_dir = 'D:\\dektop\\work_data_backup_0923_2256\\rule_one_dragon.csv'
        data_dir = os.path.join(os.getcwd(),'module','QA_data','rule.csv')
        df = pd.read_csv(data_dir,engine='python',encoding='utf_8_sig')
        #df = read_sql
        for i in range(len(df)):
            if df.iloc[i,4] != df.iloc[i,4]:
                continue
            if df.iloc[i,5] != df.iloc[i,5]:
                continue
            if df.iloc[i,6] != df.iloc[i,6]:
                continue
            id_num = df.iloc[i,0]
            rule = df.iloc[i,4]
            transfer = df.iloc[i,5]
            ans = df.iloc[i,6]
            transfer += ' + ' + ans
            transfer += ' + ' + str(id_num)
            rule = rule.split('+')
            for j in range(len(rule)):
                rule[j] = rule[j].lstrip().rstrip()
            root = rule[0]
            for j in range(len(self.root_list)):
                if self.root_list[j].data == root:
                    root = self.root_list[j]
                    
            if root == rule[0]:
                root = self.node(root)
                self.root_list.append(root)
            root = self.insert(root,rule,1,transfer)

    def load_data(self,boson_remain = 'boson_remain.txt',boson_simpler='boson_simpler.txt',que_remain='que_remain_long_test.txt'):
        with open(os.path.join(self.data_dir,que_remain),'r',encoding='utf8') as fin:
            for row in fin:
                row = row.lstrip().rstrip()
                self.que_remain_list.append(row)
        self.que_remain_list = self.que_remain_list[1:]
      
        with open(os.path.join(self.data_dir,boson_remain),'r',encoding='utf8') as fin:
            bFR = True
            for row in fin:
                if bFR:
                    bFR = False
                    continue
                row = row.lstrip().rstrip()
                self.boson_remain_list.append(row)

        # with open(os.path.join(self.data_dir,boson_simpler),'r',encoding='utf8') as fin:
        #     bFR = True
        #     for row in fin:
        #         if bFR:
        #             bFR = False
        #             continue
        #         row = row.lstrip().rstrip()
        #         row = row.split(' ')
        #         self.boson_simpler_dict.update({row[0]:row[1]})
    
    def insert(self,a,lis,ite,transfer):
        if ite > len(lis) - 1:
            a.transfer.append(transfer)
            return a
        same = False
        for i in range(len(a.link)):
            if a.link[i].data == lis[ite]:
                same = True
                break
        if same:
            a.link[i] = self.insert(a.link[i],lis,ite + 1,transfer)
        else:
            a.link.append(self.node(lis[ite]))
            a.link[-1] = self.insert(a.link[-1],lis,ite + 1,transfer)  
        return a 
    
    def find_rule(self,index,p,flag_list):
        if index >= len(flag_list):
            all_transfer.extend(p.transfer)
            return 
        if p.transfer:
            all_transfer.extend(p.transfer)
        for ele in p.link:
            if ele.data == flag_list[index]:
                self.find_rule(index + 1,ele,flag_list)
        return

    def rule_match(self,a,b):
        if abs(len(a) - len(b)) > 0:
            return False
        else:
            return True
    
    def find_rule_main(self,data):#change to match multiy rule
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
        for root in self.root_list:
            if root.data == flag_list[0]:
                all_transfer = []
                self.find_rule(1,root,flag_list)
                if all_transfer:
                    # print('in all transfer!')
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
                        ans = rule[-2]
                        id_num = rule[-1]
                        rule = rule[:-2]
                        df.append(' + '.join(rule))
                        for f in rule:
                            if f in self.que_remain_list:
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
                        df.append(id_num)
                        if len(df) == 6 and self.rule_match(flag_list,rule):
                            df_return.append(df)
                    all_transfer = []
        return df_return
        
    def is_number(self,s):
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

    def remove_number(self,s):
        result = ''
        for ele in s:
            if not self.is_number(ele):
                result += ele
        return result

    def p_flag_sort(self,data):
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
                
            flag = self.remove_number(flag)
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

    def call_NER(self,text):
        NER_class = NER()
        text = text.replace('\r','')
        text = text.replace('\n','')
        text = text.replace(' ','')
        t0 = time.time()
        words,flags,ners = NER_class.predict(text)
        # print(time.time() - t0)
        # print('ner predict test')
        # print(a)
        # print('1---')
        # print(b)
        # print('2---')
        # print(c)
        # print('3---')
        df_result = []
        # data_dir = 'D:\\dektop\\work_data_backup_0923_2256\\rule.csv'#change to sql
        data_dir = os.path.join(os.getcwd(),'module','QA_data','rule.csv')
        df_origin_article = pd.read_csv(data_dir)
        for i in range(len(words)):
            segment = words[i]
            flag_list = flags[i]
            ner = ners[i]
            word_cut = self.article_pre(segment,flag_list,ner)
            # print(word_cut)
            # print('---')
            find_rule_temp = self.find_rule_main(word_cut)
            if find_rule_temp:
                # print('find_rule_temp')
                # print(find_rule_temp)
                # print('---')
                #find_rule_temp match origin article
                for i in range(len(find_rule_temp)):
                    id_num = int(float(find_rule_temp[i][-1]))
                    # print('test!!!')
                    # print(id_num)
                    origin_article = df_origin_article[df_origin_article["RID"] == id_num]
                    # print(origin_article)
                    # print('---')
                    find_rule_temp[i].append(origin_article["原文斷詞"].iloc[0])
                    find_rule_temp[i].append(origin_article["原文出題"].iloc[0])
                    find_rule_temp[i].append(word_cut)

                #----
            else:
                pass
                # print('x')
            df_result.extend(find_rule_temp)
        return df_result

    def article_pre(self,segment,flag_list,ner):#待修正
        word_cut_list = []
        for i in range(len(segment)):
            word = segment[i]
            flag = ner[i] 
            if flag in self.boson_remain_list:
                flag = self.ner_eng_ch_dict.get(ner[i])
            else:
                flag = flag_list[i]
            word_cut_list.append(word + '_' + flag)
        word_cut = ' '.join(word_cut_list)
        word_cut = word_cut.replace('\n','')
        word_cut = word_cut.replace('\r',' ')
        word_cut,b = self.p_flag_sort(word_cut.split(' '))
        word_cut = ' '.join(word_cut)
        return word_cut







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

        
