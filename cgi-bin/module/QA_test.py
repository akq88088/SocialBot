import cgi, cgitb
import os
import pandas as pd
import numpy as np
from module.NER import NER
from module.TextProcessor import TextProcessor
import json
import time
import pymysql
#transfer [誰,v,n,ans]
class QA_test:
    class node:
        def __init__(self,data):
            self.data = data
            self.link = []
            self.transfer = []

    class SPEECH:
        def __init__(self,verb,ner):
            self.verb = verb
            self.ner = ner

    class SPEECH_INDEX:
        def __init__(self,word,verb,ner,start_index):
            self.word = word
            self.verb = verb
            self.ner = ner
            self.start_index = start_index

    def __init__(self,p_name):
        self.df_origin_article = ""
        self.boson_remain_list = []
        self.boson_simpler_dict = {}
        self.que_remain_list = []
        self.sql_columns_list = []
        self.ner_eng_ch_dict = {'per':'人','obj':'物','time':'時','place':'地','人':'per','物':'obj','時':'time','地':'place'}
        self.root_list = []
        self.data_dir = os.path.join('module','QA_data')
        # self.db_information = {"IP":"localhost","user":"root","password":"","db":""}
        self.db_information = {"IP":"120.125.85.96","user":"socialbot","password":"mcuiii","db":""}
        self.p_id = self.get_p_id(p_name)[0]
        try:
            self.project_dir = os.path.join(os.getcwd(),"module","model",self.p_id[0])
        except:
            self.project_dir = ""
        self.NER_class = NER(self.project_dir)
        self.remain_transfer_dict = self.load_remain_transfer_dict()
        self.speech_dict = self.load_speech_dict()
        self.load_data()
        self.create_root_tree()
        self.df_rule_scan = []
        self.create_rule_scan()
    
    def load_speech_dict(self):
        db = pymysql.connect(self.db_information["IP"],self.db_information["user"],self.db_information["password"])
        cursor = db.cursor()
        cursor.execute("use socialbot")
        sql_order = "SELECT 字詞,詞性,實體 FROM qa_speech WHERE p_id = %s"
        cursor.execute(sql_order,(self.p_id))
        result = cursor.fetchall()
        result_dict = {}
        for row in result:
            try:
                word,verb,ner = row[0],row[1],row[2]
                word = word.lstrip().rstrip()
                verb = verb.lstrip().rstrip()
                ner = ner.lstrip().rstrip()
            except:
                continue
           
            speech = self.SPEECH(verb,ner)
            result_dict.update({word:speech})
        return result_dict

    def load_remain_transfer_dict(self):
        db = pymysql.connect(self.db_information["IP"],self.db_information["user"],self.db_information["password"])
        cursor = db.cursor()
        cursor.execute("use socialbot")
        sql_order = "SELECT 字詞,實體 FROM qa_remain_transfer_dict WHERE p_id = %s"
        cursor.execute(sql_order,(self.p_id))
        result = cursor.fetchall()
        result_dict = {}
        for row in result:
            try:
                a,b = row[0],row[1]
            except:
                continue
            a = a.lstrip().rstrip()
            b = b.lstrip().rstrip()
            result_dict.update({a:b})
        return result_dict

    def remain_transfer(self,segment,ner):
        for i in range(len(segment)):
            for j in range(len(segment[i])):
                temp = self.remain_transfer_dict.get(segment[i][j])
                temp = self.ner_eng_ch_dict.get(temp)
                if temp != None:
                    try:
                        ner[i][j] = temp
                    except:
                        pass
        return segment,ner

    def speech_transfer(self,segment,flag_list,ner):
        for i in range(len(segment)):
            sentence_origin = "".join(segment[i])
            sentence = sentence_origin
            speech_index_list = []
            word_list = []
            verb_list = []
            ner_list = []
            for key in self.speech_dict.keys():
                find_index = sentence.find(key)
                if find_index != -1:
                    sentence = sentence.replace(key,"")
                    speech_index_list.append(self.SPEECH_INDEX(key,self.speech_dict[key].verb,self.speech_dict[key].ner,find_index))
            for j in range(len(segment[i])):
                word = segment[i][j]
                flag = flag_list[i][j]
                n = ner[i][j]
                find_index = sentence.find(word)
                if find_index != -1:
                    find_index = sentence_origin.find(word)
                    speech_index_list.append(self.SPEECH_INDEX(word,flag,n,find_index))
            speech_index_list = sorted(speech_index_list,key = lambda ele:ele.start_index)
            for j in range(len(speech_index_list)):
                word_list.append(speech_index_list[j].word)
                verb_list.append(speech_index_list[j].verb)
                ner_list.append(speech_index_list[j].ner)
            segment[i] = word_list
            flag_list[i] = verb_list
            ner[i] = ner_list
        return segment,flag_list,ner

    def get_p_id(self,p_name):
        db = pymysql.connect(self.db_information["IP"],self.db_information["user"],self.db_information["password"])
        # db = pymysql.connect(self.db_information["IP"],self.db_information["user"])
        cursor = db.cursor()
        cursor.execute("use socialbot")
        sql_order = "select p_id from model where p_name = %s"
        cursor.execute(sql_order,(p_name))
        p_id = cursor.fetchone()
        return p_id

    def predict(self,text):
        result = self.call_NER(text)
        result = pd.DataFrame(np.array(result))
        if len(result.columns) == 10:
            result.columns = ["匹配規則","匹配出題規則","匹配出題規則答案","輸入語句","輸入出題","輸入答案","RID","原文斷詞","原文出題","輸入斷詞"]
            result = result[["RID","輸入語句","輸入斷詞","輸入出題","輸入答案","匹配規則","匹配出題規則","匹配出題規則答案","原文斷詞","原文出題"]]
        # result = self.p_id
        return result
    
    def predict_rule_scan(self,text):
        result = self.call_NER_rule_scan(text)
        result = pd.DataFrame(np.array(result))
        
        if len(result.columns) == 10:
            result.columns = ["匹配規則","匹配出題規則","匹配出題規則答案","輸入語句","輸入出題","輸入答案","RID","原文斷詞","原文出題","輸入斷詞"]
            result = result[["RID","輸入語句","輸入斷詞","輸入出題","輸入答案","匹配規則","匹配出題規則","匹配出題規則答案","原文斷詞","原文出題"]]
        # result = self.p_id
        return result

    def read_sql(self):
        db = pymysql.connect(self.db_information["IP"],self.db_information["user"],self.db_information["password"])
        # db = pymysql.connect(self.db_information["IP"],self.db_information["user"])
        cursor = db.cursor()
        cursor.execute("use socialbot")
        sql_order = "SELECT * from qa_rule where p_id = %s"
        cursor.execute(sql_order,(self.p_id))
        db.commit()
        data = cursor.fetchall()
        data = pd.DataFrame(np.array(data))
        try:
            data.columns = ["ID","owner","p_id","原文規則","原文出題規則","原文出題規則答案","原文斷詞","原文出題","原文出題答案"]
        except:
            pass
        self.df_origin_article = data
        db.close()
        return data

    def create_root_tree(self):
        # data_dir = 'D:\\dektop\\work_data_backup_0923_2256\\rule_one_dragon.csv'
        # data_dir = os.path.join(os.getcwd(),'module','QA_data','rule.csv')
        # df = pd.read_csv(data_dir,engine='python',encoding='utf_8_sig')
        df = self.read_sql()
        #df = read_sql
        for i in range(len(df)):
            if df.iloc[i,3] != df.iloc[i,3]:
                continue
            if df.iloc[i,4] != df.iloc[i,4]:
                continue
            if df.iloc[i,5] != df.iloc[i,5]:
                continue
            id_num = df.iloc[i,0]
            rule = df.iloc[i,3]
            transfer = df.iloc[i,4]
            ans = df.iloc[i,5]
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

    def create_rule_scan(self):
        df = self.read_sql()
        rule_scan = []
        rule_head = []
        for i in range(len(df)):
            if df["原文規則"][i] != df["原文規則"][i]:
                continue
            if df["原文出題規則"][i] != df["原文出題規則"][i]:
                continue
            if df["原文出題規則答案"][i] != df["原文出題規則答案"][i]:
                continue
            rule = df["原文規則"][i]
            transfer = df["原文出題規則"][i]
            ans = df["原文出題規則答案"][i]
            rule = rule.split('+')
            for j in range(len(rule)):
                rule[j] = rule[j].lstrip().rstrip()
            transfer = transfer.split("+")
            for j in range(len(transfer)):
                transfer[j] = transfer[j].lstrip().rstrip()
            rule_head.append(rule[0])
            rule_scan.append([df["ID"][i],rule,transfer,ans])
        self.df_rule_scan = pd.DataFrame(np.array(rule_scan))
        self.df_rule_scan["rule_head"] = rule_head
        try:
            self.df_rule_scan.columns = ["ID","原文規則","原文出題規則","原文出題規則答案","rule_head"]
        except:
            pass
        
    def load_data(self,boson_remain = 'boson_remain.txt',boson_simpler='boson_simpler.txt',que_remain='que_remain_long_test.txt',remain_transfer='remain_transfer_dict.txt'):
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

        with open(os.path.join(self.data_dir,remain_transfer),'r',encoding='utf8') as fin:
            bFR = True
            for row in fin:
                if bFR:
                    bFR = False
                    continue
                row = row.lstrip().rstrip()
                try:
                    temp = row.split(' ')
                    a,b = temp[0],temp[1]
                except:
                    continue
                
                a = a.lstrip().rstrip()
                b = b.lstrip().rstrip()
                self.remain_transfer_dict.update({a:b})

        self.read_sql()
    
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

    def lcs(self,s1,s2):
        m = [[0 for i in range(len(s2) + 1)] for j in range(len(s1) + 1)]  # 生成0矩陣，爲方便後續計算，比字符串長度多了一列
        mmax = 0  # 最長匹配的長度
        p = 0  # 最長匹配對應在s1中的最後一位
        for i in range(len(s1)):
            for j in range(len(s2)):
                if s1[i] == s2[j]: # 如果相等，則加入現有的公共子串
                    m[i + 1][j + 1] = m[i][j] + 1
                    if m[i + 1][j + 1] > mmax:
                        mmax = m[i + 1][j + 1]
                        p = i + 1
        return s1[p - mmax:p], mmax  # 返回最長子串及其長度

    def rule_scan_match(self,rule,rule_find):
        a = rule
        b = rule_find
        sub_s,sub_s_ln = self.lcs(a,b)
        # if sub_s_ln / len(a) > 0.8 and sub_s_ln / len(b) > 0.8:
        #     return True
        # else:
        #     return False
        # if sub_s_ln == len(a) and sub_s_ln / len(b) > 0.8:
        #     return True
        # else:
        #     return False
        if sub_s == a and sub_s == b:
            return True
        else:
            return False
    
    def rule2list(self,data):
        data = data.split("+")
        for i in range(len(data)):
            data[i] = data[i].lstrip().rstrip()
        return data

    def word_cut2word_flag_list(self,word_cut):
        temp = word_cut.split(" ")
        word_list = []
        flag_list = []
        for i in range(len(temp)):
            try:
                word,flag = temp[i].split('_')
            except:
                continue
            word = word.lstrip().rstrip()
            flag = flag.lstrip().rstrip()
            word_list.append(word)
            flag_list.append(flag)
        return word_list,flag_list

    def change_sentence_for_rule_change(self,df_change):
        #根據規則與問題轉換規則來產生問題
        for i in range(len(df_change)):
            rule = self.rule2list(df_change["原文規則"].iloc[i])
            transfer = self.rule2list(df_change["原文出題規則"].iloc[i])
            ans = df_change["原文出題規則答案"].iloc[i]
            word_list,flag_list = self.word_cut2word_flag_list(df_change["原文斷詞"].iloc[i])
            bool_list = []
            for j in range(len(flag_list)):
                bool_list.append(True)
            aft_transfer = ''
            for f in transfer:
                if f in self.que_remain_list:
                    aft_transfer += f
                    continue
                for k in range(len(flag_list)):
                    if flag_list[k] == f and bool_list[k]:
                        aft_transfer += word_list[k]
                        bool_list[k] = False
                        break
                for k in range(len(flag_list)):
                    if flag_list[k] == ans:
                        ans = word_list[k]
                        break
            if ans == df_change["原文出題規則答案"].iloc[i]:
                continue
            df_change["原文出題"].iloc[i] = aft_transfer
        return df_change 
                
        

    def rule_scan_main(self,data):
        data = data.split(' ')
        word_list = []
        flag_list = []
        df_return = []
        for i in range(len(data)):
            data[i] = data[i].split('_')
            try:
                word = data[i][0]
                flag = data[i][1]
            except:
                continue
            word_list.append(word)
            flag_list.append(flag)
        df_rule_find = self.df_rule_scan[self.df_rule_scan["rule_head"] == flag_list[0]]
        for i in range(len(df_rule_find)):
            rule = df_rule_find["原文規則"].iloc[i]
            if self.rule_scan_match(flag_list,rule):
                # print("rule match!")
                # print(rule)
                #根據規則與問題轉換規則來產生問題
                transfer = df_rule_find["原文出題規則"].iloc[i]
                ans = df_rule_find["原文出題規則答案"].iloc[i]
                # print(transfer)
                # print(ans)
                id_num = df_rule_find["ID"].iloc[i]
                df = []
                df.append(' + '.join(rule))
                bool_list = []
                for j in range(len(flag_list)):
                    bool_list.append(True)
                aft_transfer = ''
                for f in transfer:
                    if f in self.que_remain_list:
                        aft_transfer += f
                        continue
                    for k in range(len(flag_list)):
                        if flag_list[k] == f and bool_list[k]:
                            aft_transfer += word_list[k]
                            bool_list[k] = False
                            break
                    for k in range(len(flag_list)):
                        if flag_list[k] == ans:
                            ans = word_list[k]
                            break
                if ans == df_rule_find["原文出題規則答案"].iloc[i]:
                    continue
                df.append(' + '.join(transfer))
                df.append(df_rule_find["原文出題規則答案"].iloc[i])
                df.append(''.join(word_list))
                df.append(aft_transfer)
                df.append(ans)
                df.append(id_num)
                if len(df) == 7:
                    df_return.append(df)
        return df_return
        
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
                    # print(all_transfer)
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
                        original_ans = ans
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
                        df.append(original_ans)
                        df.append(''.join(word_list))
                        df.append(aft_transfer)
                        df.append(ans)
                        df.append(id_num)
                        if len(df) == 7 and self.rule_match(flag_list,rule):
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

    def remain_transfer(self,segment,ner):
        for i in range(len(segment)):
            for j in range(len(segment[i])):
                temp = self.remain_transfer_dict.get(segment[i][j])
                temp = self.ner_eng_ch_dict.get(temp)
                if temp != None:
                    try:
                        ner[i][j] = temp
                    except:
                        pass
        return segment,ner

    def call_NER_rule_scan(self,text):
        text = text.replace('\r','')
        text = text.replace('\n','')
        text = text.replace(' ','')
        words,flags,ners = self.NER_class.predict_qa_test(text)
        words,flags,ners = self.speech_transfer(words,flags,ners)
        words,ners = self.remain_transfer(words,ners)
        df_result = []
        for i in range(len(words)):
            segment = words[i]
            flag_list = flags[i]
            ner = ners[i]
            try:
                word_cut = self.article_pre(segment,flag_list,ner)
            except:
                word_cut = ""
            if len(word_cut) < 1:
                continue
            # print('word_cut : ' + word_cut)
            rule_scan_temp = self.rule_scan_main(word_cut)
            if rule_scan_temp:
                for j in range(len(rule_scan_temp)):
                    id_num = str(int(float(rule_scan_temp[j][-1])))
                    origin_article = self.df_origin_article[self.df_origin_article["ID"] == id_num]
                    rule_scan_temp[j].append(origin_article["原文斷詞"].iloc[0])
                    rule_scan_temp[j].append(origin_article["原文出題"].iloc[0])
                    rule_scan_temp[j].append(word_cut)
                df_result.extend(rule_scan_temp)    

                #----
        return df_result

    def call_NER(self,text):
        text = text.replace('\r','')
        text = text.replace('\n','')
        text = text.replace(' ','')
        words,flags,ners = self.NER_class.predict_qa_test(text)
        words,flags,ners = self.speech_transfer(words,flags,ners)
        words,ners = self.remain_transfer(words,ners)
        df_result = []
        for i in range(len(words)):
            segment = words[i]
            flag_list = flags[i]
            ner = ners[i]
            try:
                word_cut = self.article_pre(segment,flag_list,ner)
            except:
                word_cut = ""
            if len(word_cut) < 1:
                continue
            find_rule_temp = self.find_rule_main(word_cut)
            if find_rule_temp:
                # print('find_rule_temp')
                # print(find_rule_temp)
                # print('---')
                #find_rule_temp match origin article
                for i in range(len(find_rule_temp)):
                    id_num = str(int(float(find_rule_temp[i][-1])))
                    # print('id num')
                    # print(id_num)
                    # print(type(id_num))
                    # print('id')
                    # print(self.df_origin_article["ID"].iloc[0])
                    # print(type(self.df_origin_article["ID"].iloc[0]))
                    origin_article = self.df_origin_article[self.df_origin_article["ID"] == id_num]
                    # print('origin_article')
                    # print(origin_article.head())
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

    def article_pre(self,segment,flag_list,ner):
        word_cut_list = []
        for i in range(len(segment)):
            word = segment[i]
            flag = flag_list[i]
            n = ner[i]
            if n in ["人","事","物","地","時"]:
                flag = n
            else:
                if n in self.boson_remain_list:
                    flag = self.ner_eng_ch_dict.get(ner[i])
                # else:
                #     flag = flag_list[i][0]
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

        
