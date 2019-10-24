import os
import pandas as pd
import numpy as np
import math
from module.NER import NER
import pymysql
import time
class QA_train:

    class pair:
        def __init__(self,word,flag):
            self.flag = flag
            self.word = word

    def __init__(self,owner,p_name):
        self.add_remain_dict = {}
        self.ner_eng_ch_dict = {'per':'人','obj':'物','time':'時','place':'地'}
        self.article_remain_list = []
        self.que_remain_list = []
        self.flag_que_remain_dict = {}
        self.sql_columns_list = []
        self.data_dir = os.path.join('module','QA_data')
        self.boson_remain_list = []
        self.boson_flag_list = []
        self.load_data()
        # self.db_information = {"IP":"localhost","user":"root","password":"","db":""}
        self.db_information = {"IP":"120.125.85.96","user":"socialbot","password":"mcuiii","db":""}
        self.owner = owner
        self.p_id = self.get_p_id(p_name)
        try:
            self.project_dir = os.path.join(os.getcwd(),"module","model",self.p_id[0])
        except:
            self.project_dir = ""
        self.NER_class = NER(self.project_dir)
    def get_p_id(self,p_name):
        db = pymysql.connect(self.db_information["IP"],self.db_information["user"],self.db_information["password"])
        # db = pymysql.connect(self.db_information["IP"],self.db_information["user"])
        cursor = db.cursor()
        cursor.execute("use socialbot")
        sql_order = """
        select p_id
        from model
        where p_name = %s
        """
        cursor.execute(sql_order,(p_name))
        p_id = cursor.fetchone()
        return p_id

    def set_columns(self,df):
        if len(df.columns) == 6:
            df.columns = ["原文規則","原文出題規則","原文出題規則答案","原文斷詞","原文出題","原文出題答案"]
        return df

    def train(self,df):
        result = []
        for i in range(len(df)):
            article = df.iloc[i,0]
            que = df.iloc[i,1]
            if article != article:#判斷nan
                continue
            if que != que:#判斷nan
                continue
            # if df.iloc[i,3] == df.iloc[i,3]:
            #     continue
            # df.iloc[i,1] = self.article_pre(df.iloc[i,1])
            # df.iloc[i,2] = self.article_pre(df.iloc[i,2])
            article = article.replace('\r',' ')
            article = article.replace('\n',' ')
            article = article.split(' ')
            que = que.replace('\r',' ')
            que = que.replace('\n',' ')
            while '' in article:
                article.remove('')
            article,word_in_article_remain = self.check_article_remain(article)
            if not word_in_article_remain:
                continue
            article,article_flag_list = self.p_flag_sort(article)
            ori_article = ' '.join(article)
            article_aft = ' + '.join(article_flag_list)
            que = self.word_cut(article,que)
            word_in_que_remain = self.check_que_remain(que)
            if not word_in_que_remain:
                que,err = self.add_remain_word(article_flag_list,que)
                if err:
                    continue
            que_aft = ' + '.join(que)
            ans_word,ans_flag = self.generate_ans(article_flag_list,que,article)
            if ans_word == '':
                continue
            # row_data = [i + 2,ori_article,df.iloc[i,2],article_aft,que_aft,ans_flag,ans_word]
            # row_data = [ori_article,df.iloc[i,2],ans_word,article_aft,que_aft,ans_flag]
            row_data = [article_aft,que_aft,ans_flag,ori_article,df.iloc[i,1],ans_word]
            result.append(row_data)
        # for row in result:
        #     print(row)
        df = pd.DataFrame(np.array(result))
        # print(df.head(10))
        df = self.set_columns(df)
        return df
    
    def save_sql(self,data):
        df = pd.DataFrame(np.array(data))
        df.to_csv('D:\\dektop\\work_data_backup_0923_2256\\rule.csv',encoding='utf_8_sig')

    def call_NER(self,text):
        # print(text)
        # NER_class = NER(self.project_dir)
        text = text.replace('\r','')
        text = text.replace('\n','')
        text = text.replace(' ','')
        not_success = True
        error_run = 1
        while not_success:
            try:
                segment,flag_list,ner = self.NER_class.predict_qa_train(text)
                not_success = False
                # print("out of error_run!")
            except:
                # if error_run % 5 == 0:
                    # print("error_run : " + str(error_run))
                error_run += 1
        try:
            word_cut = self.article_pre(segment,flag_list,ner)
        except:
            word_cut = ""
        # print('----')
        return word_cut

    def read_data_generate_rule_main(self):
        df = self.get_training_data()
        df = self.training_data2rule(df)
        self.delete_qa_rule()
        self.insert_rule(df)
        # self.training_data2rule("")


    def delete_qa_rule(self):
        db = pymysql.connect(self.db_information["IP"],self.db_information["user"],self.db_information["password"])
        # db = pymysql.connect(self.db_information["IP"],self.db_information["user"])
        cursor = db.cursor()
        cursor.execute("use socialbot")
        sql_order = "delete from QA_rule where owner = %s and p_id = %s;"
        cursor.execute(sql_order,(self.owner,self.p_id))
        # cursor.execute("drop table qa_rule")
        # cursor.execute(
        #     """
        #     create table qa_rule(
        #     ID int(11) auto_increment primary key,
        #     owner varchar(255),
        #     p_id varchar(255),
        #     原文規則 varchar(100),
        #     原文出題規則 varchar(100),
        #     原文出題規則答案 varchar(100),
        #     原文斷詞 varchar(100),
        #     原文出題 varchar(100),
        #     原文出題答案 varchar(100)
        #     );
        #     """)
        # cursor.execute("alter table qa_rule change 原文規則 原文規則 varchar(100) character set utf8mb4 collate utf8mb4_bin")
        # cursor.execute("alter table qa_rule change 原文出題規則 原文出題規則 varchar(100) character set utf8mb4 collate utf8mb4_bin")
        # cursor.execute("alter table qa_rule change 原文出題規則答案 原文出題規則答案 varchar(100) character set utf8mb4 collate utf8mb4_bin")
        # cursor.execute("alter table qa_rule change 原文斷詞 原文斷詞 varchar(100) character set utf8mb4 collate utf8mb4_bin")
        # cursor.execute("alter table qa_rule change 原文出題 原文出題 varchar(100) character set utf8mb4 collate utf8mb4_bin")
        # cursor.execute("alter table qa_rule change 原文出題答案 原文出題答案 varchar(100) character set utf8mb4 collate utf8mb4_bin")
        db.commit()

    def get_training_data(self):
        # 目前不判斷owner
        db = pymysql.connect(self.db_information["IP"],self.db_information["user"],self.db_information["password"])
        # db = pymysql.connect(self.db_information["IP"],self.db_information["user"])
        cursor = db.cursor()
        cursor.execute("use socialbot")
        sql_order = "select 課文,題目 from qa_training where owner = %s and p_id = %s"
        cursor.execute(sql_order,(self.owner,self.p_id))
        data = cursor.fetchall()
        df = pd.DataFrame(np.array(data))
        return df

    def write_rule_progress(self,i,df_ln):
        pass
        # i = int(i * 100 / df_ln)
        # i = str(i)
        # with open(os.path.join(self.project_dir,'progress.txt'),'w',encoding='utf_8_sig') as fout:
        #     fout.write(str(i))
        # f = open(os.path.join(self.project_dir,'progress.txt'),'w',encoding='utf_8_sig')
        # f.write(str(i))
        # f.close()

    def read_rule_progress(self):
        result = ''
        # with open(os.path.join(self.project_dir,'progress.txt'),'r',encoding='utf_8_sig') as fin:
        #     result = fin.read()
        return result

    def training_data2rule(self,df):
        df_ln = len(df)
        for i in range(df_ln):
            self.write_rule_progress(i,df_ln)
            sentence = df.iloc[i,0]
            sentence = self.call_NER(sentence)
            df.iloc[i,0] = sentence
        df = self.train(df)
        # i = 0
        # while True:
        #     if i > 3:
        #         break
        #     self.write_rule_progress(i,200)
        #     time.sleep(3)
        #     i += 1
        return df

    def insert_training_data(self,df):
        db = pymysql.connect(self.db_information["IP"],self.db_information["user"],self.db_information["password"])
        # db = pymysql.connect(self.db_information["IP"],self.db_information["user"])
        cursor = db.cursor()
        cursor.execute("use socialbot")
        sql_order = "insert into qa_training(owner,p_id,課文,題目) values(%s,%s,%s,%s)"
        for i in range(len(df)):
            if df.iloc[i,0] != df.iloc[i,0]:
                continue
            if df.iloc[i,1] != df.iloc[i,1]:
                continue
            cursor.execute(sql_order,(self.owner,self.p_id,df["課文"].iloc[i],df["題目"].iloc[i]))
        db.commit()

    def insert_rule(self,df):
        db = pymysql.connect(self.db_information["IP"],self.db_information["user"],self.db_information["password"])
        # db = pymysql.connect(self.db_information["IP"],self.db_information["user"])
        # with open("C:\\Users\\student\\Desktop\\json_test.txt",'w') as fout:
        #     fout.write(str(df.head()))
        cursor = db.cursor()
        cursor.execute("use socialbot")
        sql_order = "insert into qa_rule(owner,p_id,原文規則,原文出題規則,原文出題規則答案,原文斷詞,原文出題,原文出題答案)values(%s,%s,%s,%s,%s,%s,%s,%s);"
        for i in range(len(df)):
            cursor.execute(sql_order,(self.owner,self.p_id,df["原文規則"].iloc[i],df["原文出題規則"].iloc[i],df["原文出題規則答案"].iloc[i],df["原文斷詞"].iloc[i],df["原文出題"].iloc[i],df["原文出題答案"].iloc[i]))

        db.commit()
    
    def change_rule(self,df):
        db = pymysql.connect(self.db_information["IP"],self.db_information["user"],self.db_information["password"])
        # db = pymysql.connect(self.db_information["IP"],self.db_information["user"])
        cursor = db.cursor()
        cursor.execute("use socialbot")
        sql_order = "UPDATE qa_rule SET 原文出題規則 = %s,原文出題規則答案 = %s  WHERE ID = %s AND owner = %s AND p_id = %s"
        for i in range(len(df)):
            cursor.execute(sql_order,(df["原文出題規則"].iloc[i],df["原文出題規則答案"].iloc[i],int(df["ID"].iloc[i]),self.owner,self.p_id))
        db.commit()
    
    def remove_rule(self,df):
        db = pymysql.connect(self.db_information["IP"],self.db_information["user"],self.db_information["password"])
        # db = pymysql.connect(self.db_information["IP"],self.db_information["user"])
        cursor = db.cursor()
        cursor.execute("use socialbot")
        sql_order = "delete from QA_rule where ID = %s and owner = %s and p_id = %s;"
        for i in range(len(df)):
            cursor.execute(sql_order,(int(df["ID"].iloc[i]),self.owner,self.p_id))
        db.commit()

    def QA_train_main(self,data):
        data = data.fillna(value="")
        df_insert = data[data["datatype"] == "insert"]
        df_upload = data[data["datatype"] == "upload"]
        df_insert = pd.concat([df_insert,df_upload],axis=0)
        df_change = data[data["datatype"] == "change"]
        df_remove = data[data["datatype"] == "remove"]
        
        if not df_insert.empty:
            self.insert_rule(df_insert)
        
        if not df_change.empty:
            self.change_rule(df_change)
        
        if not df_remove.empty:
            self.remove_rule(df_remove)

    def get_rule_check_data(self):
        return self.article_remain_list,self.que_remain_list,self.flag_que_remain_dict,self.boson_flag_list

    def load_data(self,add_remain = '',article_remain = 'article_remain_test.txt',que_remain = 'que_remain_long_test.txt',flag_que_remain = 'flag_que_remain_dict_test.txt',boson_remain = 'boson_remain.txt',boson_flag = 'boson_flag.txt'):
        self.add_remain_dict = {'人':'誰','事':'什麼','物':'什麼','地':'哪裡','時':'何時'}
        with open(os.path.join(self.data_dir,article_remain),'r',encoding='utf8') as fin:
            for row in fin:
                row = row.lstrip().rstrip()
                self.article_remain_list.append(row)
        self.article_remain_list = self.article_remain_list[1:]

        with open(os.path.join(self.data_dir,que_remain),'r',encoding='utf8') as fin:
            for row in fin:
                row = row.lstrip().rstrip()
                self.que_remain_list.append(row)
        self.que_remain_list = self.que_remain_list[1:]

        with open(os.path.join(self.data_dir,flag_que_remain),'r',encoding = 'utf8') as fin:
            for row in fin:
                row = row.lstrip().rstrip()
                row = row.split(' ')
                try:
                    lis = []
                    for i in range(1,len(row)):
                        lis.append(row[i])
                    self.flag_que_remain_dict.update({row[0]:lis})
                except:
                    continue
        
        with open(os.path.join(self.data_dir,boson_remain),'r',encoding='utf8') as fin:
            bFR = True
            for row in fin:
                if bFR:
                    bFR = False
                    continue
                row = row.lstrip().rstrip()
                self.boson_remain_list.append(row)
        
        with open(os.path.join(self.data_dir,boson_flag),'r',encoding='utf8') as fin:
            bFR = True
            for row in fin:
                if bFR:
                    bFR = False
                    continue
                row = row.lstrip().rstrip()
                self.boson_flag_list.append(row)
                
    def word_cut(self,article,s):#article = [大自然_人1,會_v1,說話_v2] s = '誰會說話' output = [pair,pair]
        all_word = []
        all_flag = []
        result = []
        for i in range(len(article)):
            temp = article[i].split('_')
            try:
                word = temp[0]
                flag = temp[1]
            except:
                continue
            all_word.append(word)
            all_flag.append(flag)
            article[i] = self.pair(word,flag) 
        i = 0
        while i < len(s):
            i_temp = i
            bCut = False
            k = 0   
            for word in all_word:
                if i >= len(s):
                    break
                i = i_temp
                if s[i] == word[0]:
                    j = 0
                    same_word = ''
                    while i < len(s) and j < len(word) and s[i] == word[j]:
                        same_word += s[i]
                        i += 1
                        j += 1
                    if same_word == word:
                        bCut = True
                        result.append(all_flag[k])
                        break
                k += 1
            if bCut:
                continue
            else:
                i = i_temp
                
            for word in self.que_remain_list:
                if i >= len(s):
                    break
                i = i_temp
                if s[i] == word[0]:
                    j = 0
                    same_word = ''
                    while i < len(s) and j < len(word) and s[i] == word[j]:
                        same_word += s[i]
                        i += 1
                        j += 1
                    if same_word == word:
                        bCut = True
                        result.append(same_word)
                        break
            if bCut:
                continue
            else:
                i = i_temp
            
            i += 1
        return result
    
    def flag_remove_num(self,lis):
        for i in range(len(lis)):
            temp = ''
            for j in range(len(lis[i])):
                if not lis[i][j].isdigit():
                    temp += lis[i][j]
            lis[i] = temp
        return lis
    
    def generate_ans(self,rule,que_transfer,article):
        que_transfer_no_num = self.flag_remove_num(que_transfer[:])
        rule_no_num = self.flag_remove_num(rule[:])
        ans = ''
        result = ''
        result_word = ''
        result_list = []
        word_in_que_list = []
        que_remain_ite = 0
        for word in que_transfer_no_num:
            if word in self.que_remain_list:
                ans = self.flag_que_remain_dict.get(word)
                if ans != None and ans != []:
                    break
            que_remain_ite += 1
        if ans == None or ans == []:
            return '',''
        iRun = 0
        for i in range(len(rule_no_num)):
            word_no_num = rule_no_num[i]
            word = rule[i]
            if word_no_num in ans and word not in que_transfer:
                result_list.append(iRun)
            iRun += 1
        min_dis = max(len(que_transfer),len(rule)) + 1
        
        for ite in result_list:
            if abs(ite - que_remain_ite) < min_dis:
                min_dis = abs(ite - que_remain_ite)
                result = rule[ite]
                result_word = article[ite].word
        return result_word,result

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
            if not ele.isdigit():
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
            if flag == 'x':
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
    
    def get_special_word(self,data):
        result_dict = {}
        for row in data:
            temp = row.split('_')
            try:
                word = temp[0]
                flag = temp[1]
            except:
                continue
            if flag[0] == '人' or flag in self.article_remain_list:
                result_dict.update({word:flag})
        return result_dict
    
    def check_article_remain(self,data):
        word_in_article_remain = False
        result = []
        for row in data:
            temp = row.split('_')
            try:
                word = temp[0]
                flag = temp[1]
                if flag[0] == '人':
                    flag = '人'
                elif flag[0] == '事':
                    flag = '事'
                elif flag[0] == '物':
                    flag = '物'
                elif flag[0] == '地':
                    flag = '地'
                elif flag[0] == '時':
                    flag = '時'
                else:
                    pass
                if flag in self.article_remain_list:
                    word_in_article_remain = True
            except:
                continue
            result.append(word + '_' + flag)
        return result,word_in_article_remain
    
    def check_que_remain(self,data):
        word_in_que_remain = False
        for i in range(len(data)):
            temp = data[i]
            temp = self.remove_number(temp)
            if temp in self.que_remain_list:
                word_in_que_remain = True
                break
        return word_in_que_remain
    
    def add_remain_word(self,article_flag,que_flag):
        que_flag_index = []
        result = []
        remain_index = 0
        remain_word = ''
        err = False
        for i in range(len(que_flag)):
            que_flag_index.append(article_flag.index(que_flag[i]))
        for flag in article_flag:
            temp = self.remove_number(flag)
            if temp in self.article_remain_list and flag not in que_flag:
                remain_index = article_flag.index(flag)
                remain_word = self.add_remain_dict.get(self.remove_number(flag))
                break
        que_flag_index.append(remain_index)
        que_flag_index = sorted(que_flag_index)
        for index in que_flag_index:
            if index >= 0:
                if index == remain_index:
                    result.append(remain_word)
                else:
                    result.append(article_flag[index])
        if remain_word == '':
            err = True
        return result,err
    
    def article_pre(self,segment,flag_list,ner):#待修正
        word_cut_list = []
        for i in range(len(segment)):
            word = segment[i]
            flag = ner[i]
            if flag in self.boson_remain_list:
                flag = self.ner_eng_ch_dict.get(ner[i])
            else:
                flag = flag_list[i][0]
            word_cut_list.append(word + '_' + flag)
        word_cut = ' '.join(word_cut_list)
        word_cut = word_cut.replace('\n','')
        word_cut = word_cut.replace('\r',' ')
        word_cut,b = self.p_flag_sort(word_cut.split(' '))
        word_cut = ' '.join(word_cut)
        return word_cut
    

