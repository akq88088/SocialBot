import os
import pandas as pd
import numpy as np
import math
from module.NER import NER
import pymysql
import time
from module.QA_test import QA_test
class QA_train:

    class pair:
        def __init__(self,word,flag):
            self.flag = flag
            self.word = word
    
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

    def __init__(self,owner,p_name):
        self.add_remain_dict = {}
        self.ner_eng_ch_dict = {'per':'人','obj':'物','time':'時','place':'地','人':'per','物':'obj','時':'time','地':'place'}
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
        self.remain_transfer_dict = self.load_remain_transfer_dict()
        self.speech_dict = self.load_speech_dict()
        self.QA_test = QA_test(p_name)

    def remove_w(self,word,flag,ner):
        result_word = []
        result_flag = []
        result_ner = []
        for i in range(len(word)):
            if flag[i] == "w":
                continue
            result_word.append(word[i])
            result_flag.append(flag[i])
            result_ner.append(ner[i])
        return result_word,result_flag,result_ner

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
            try:
                que = self.word_cut(article,que)
            except:
                continue
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
        df = df.drop_duplicates(["原文規則","原文出題規則"])
        return df
    
    def save_sql(self,data):
        df = pd.DataFrame(np.array(data))
        df.to_csv('D:\\dektop\\work_data_backup_0923_2256\\rule.csv',encoding='utf_8_sig')

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
            
                    
    def call_NER(self,text):
        # print(text)
        # NER_class = NER(self.project_dir)
        word_cut_list = []
        text = text.replace('\r','')
        text = text.replace('\n','')
        text = text.replace(' ','')
        not_success = True
        error_run = 1
        segment,flag_list,ner = self.NER_class.predict_qa_train(text)
        for i in range(len(segment)):
            segment[i],flag_list[i],ner[i] = self.remove_w(segment[i],flag_list[i],ner[i])
            # with open("D:\\dektop\\QA_test_demo\\test_remove_w.txt",'a') as fout:
            #     fout.write(" ".join(segment[i]))
            #     fout.write(" ".join(flag_list[i]))
            #     fout.write(" ".join(ner[i]))
            #     fout.write("---")
        segment,flag_list,ner = self.speech_transfer(segment,flag_list,ner)
        segment,ner = self.remain_transfer(segment,ner)
        # with open("D:\\dektop\\QA_test_demo\\test_before_word_cut.txt",'w',encoding='utf_8_sig') as fout:
        #     for i in range(len(segment)):
        #         fout.write(" ".join(segment[i]) + '\n')
        #         fout.write(" ".join(flag_list[i]) + '\n')
        #         fout.write(" ".join(ner[i]) + '\n')
        #         fout.write("---")
        # while not_success:
        #     try:
        #         segment,flag_list,ner = self.NER_class.predict_qa_train(text)
        #         not_success = False
        #         # print("out of error_run!")
        #     except:
        #         # if error_run % 5 == 0:
        #             # print("error_run : " + str(error_run))
        #         error_run += 1
        for i in range(len(flag_list)):
            # segment[i],flag_list[i],ner[i] = self.remove_w(segment[i],flag_list[i],ner[i])
            try:
                word_cut = self.article_pre(segment[i],flag_list[i],ner[i])
            except:
                word_cut = ""
            word_cut_list.append(word_cut)
        # print('----')
        # with open('D:\\dektop\\QA_test_demo\\test.txt','w',encoding='utf_8_sig') as fout:
        #     fout.write("\n".join(word_cut_list))
        return word_cut_list

    def read_data_generate_rule_main(self):
        df = self.get_training_data()
        df = self.training_data2rule(df)
        try:
            df = df.dropna(subset=["原文規則","原文出題規則"])
        except:
            pass
        # df.to_csv("D:\\dektop\\QA_test_demo\\rule.csv",index=0,encoding='utf_8_sig')
        self.remove_qa_rule()#maybe remove?
        self.insert_rule(df)
        # self.training_data2rule("")


    def remove_qa_rule(self):
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
        # df_ln = len(df)
        # for i in range(df_ln):
        #     self.write_rule_progress(i,df_ln)
        #     sentence = df.iloc[i,0]
        #     sentence = self.call_NER(sentence)
        #     df.iloc[i,0] = sentence
        # df = self.train(df)
        sentence_list = df.iloc[:,0]
        sentence_list = self.call_NER(sentence_list)
        df.iloc[:,0] = sentence_list
        df = self.train(df)
        return df

    def remain_transfer_dict_train_main(self,df):
        data = df.fillna(value="")
        df_insert = data[data["datatype"] == "insert"]
        df_change = data[data["datatype"] == "change"]
        df_remove = data[data["datatype"] == "remove"]

        if not df_insert.empty:
            self.insert_remain_transfer_dict(df_insert)
        
        if not df_change.empty:
            self.change_remain_transfer_dict(df_change)
        
        if not df_remove.empty:
            self.remove_remain_transfer_dict(df_remove)

    def insert_remain_transfer_dict(self,df):
        db = pymysql.connect(self.db_information["IP"],self.db_information["user"],self.db_information["password"])
        # db = pymysql.connect(self.db_information["IP"],self.db_information["user"])
        cursor = db.cursor()
        cursor.execute("use socialbot")
        sql_order = "insert into qa_remain_transfer_dict(p_id,字詞,實體) values(%s,%s,%s)"
        sql_duplicate_order = "select * from qa_remain_transfer_dict where p_id = %s and 字詞 = %s and 實體 = %s"
        for i in range(len(df)):
            if df.iloc[i,0] != df.iloc[i,0]:
                continue
            if df.iloc[i,1] != df.iloc[i,1]:
                continue
            cursor.execute(sql_duplicate_order,(self.p_id,df["字詞"].iloc[i],df["實體"].iloc[i]))
            temp = cursor.fetchone()
            if temp != None:
                continue
            cursor.execute(sql_order,(self.p_id,df["字詞"].iloc[i],df["實體"].iloc[i]))
        db.commit()

    def change_remain_transfer_dict(self,df):
        db = pymysql.connect(self.db_information["IP"],self.db_information["user"],self.db_information["password"])
        # db = pymysql.connect(self.db_information["IP"],self.db_information["user"])
        cursor = db.cursor()
        cursor.execute("use socialbot")
        sql_order = "UPDATE qa_remain_transfer_dict SET 字詞 = %s,實體 = %s WHERE ID = %s AND p_id = %s"
        for i in range(len(df)):
            cursor.execute(sql_order,(df["字詞"].iloc[i],df["實體"].iloc[i],int(df["ID"].iloc[i]),self.p_id))
        db.commit()
    
    def remove_all_remain_transfer_dict(self):
        db = pymysql.connect(self.db_information["IP"],self.db_information["user"],self.db_information["password"])
        # db = pymysql.connect(self.db_information["IP"],self.db_information["user"])
        cursor = db.cursor()
        cursor.execute("use socialbot")
        sql_order = "delete from qa_remain_transfer_dict where p_id = %s;"
        cursor.execute(sql_order,(self.p_id))
        db.commit()

    def remove_remain_transfer_dict(self,df):
        db = pymysql.connect(self.db_information["IP"],self.db_information["user"],self.db_information["password"])
        # db = pymysql.connect(self.db_information["IP"],self.db_information["user"])
        cursor = db.cursor()
        cursor.execute("use socialbot")
        sql_order = "delete from qa_remain_transfer_dict where ID = %s and p_id = %s;"
        for i in range(len(df)):
            cursor.execute(sql_order,(int(df["ID"].iloc[i]),self.p_id))
        db.commit()

    def insert_training_data(self,df):
        db = pymysql.connect(self.db_information["IP"],self.db_information["user"],self.db_information["password"])
        # db = pymysql.connect(self.db_information["IP"],self.db_information["user"])
        cursor = db.cursor()
        cursor.execute("use socialbot")
        sql_order = "insert into qa_training(owner,p_id,課文,題目) values(%s,%s,%s,%s)"
        sql_duplicate_order = "select * from qa_training where p_id = %s and 課文 = %s and 題目 = %s"
        for i in range(len(df)):
            if df.iloc[i,0] != df.iloc[i,0]:
                continue
            if df.iloc[i,1] != df.iloc[i,1]:
                continue
            cursor.execute(sql_duplicate_order,(self.p_id,df["課文"].iloc[i],df["題目"].iloc[i]))
            temp = cursor.fetchone()
            if temp != None:
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
        sql_duplicate_order = "select * from qa_rule where p_id = %s and 原文規則 = %s and 原文出題規則 = %s and 原文出題規則答案 = %s"
        sql_order = "insert into qa_rule(owner,p_id,原文規則,原文出題規則,原文出題規則答案,原文斷詞,原文出題,原文出題答案)values(%s,%s,%s,%s,%s,%s,%s,%s);"
        for i in range(len(df)):
            cursor.execute(sql_duplicate_order,(self.p_id,df["原文規則"].iloc[i],df["原文出題規則"].iloc[i],df["原文出題規則答案"].iloc[i]))
            temp = cursor.fetchone()
            if temp != None:
                continue
            cursor.execute(sql_order,(self.owner,self.p_id,df["原文規則"].iloc[i],df["原文出題規則"].iloc[i],df["原文出題規則答案"].iloc[i],df["原文斷詞"].iloc[i],df["原文出題"].iloc[i],df["原文出題答案"].iloc[i]))

        db.commit()
    
    def change_rule(self,df):
        db = pymysql.connect(self.db_information["IP"],self.db_information["user"],self.db_information["password"])
        # db = pymysql.connect(self.db_information["IP"],self.db_information["user"])
        cursor = db.cursor()
        cursor.execute("use socialbot")
        sql_order = "UPDATE qa_rule SET 原文出題規則 = %s,原文出題規則答案 = %s,原文出題 = %s,原文出題答案 = %s WHERE ID = %s AND owner = %s AND p_id = %s"
        for i in range(len(df)):
            cursor.execute(sql_order,(df["原文出題規則"].iloc[i],df["原文出題規則答案"].iloc[i],df["原文出題"].iloc[i],df["原文出題答案"].iloc[i],int(df["ID"].iloc[i]),self.owner,self.p_id))
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

    def remove_qa_training(self):
        db = pymysql.connect(self.db_information["IP"],self.db_information["user"],self.db_information["password"])
        # db = pymysql.connect(self.db_information["IP"],self.db_information["user"])
        cursor = db.cursor()
        cursor.execute("use socialbot")
        sql_order = "delete from QA_training where p_id = %s;"
        cursor.execute(sql_order,(self.p_id))
        db.commit()

    def speech_call_NER_sub(self,segment,flag_list,ner):
        word_list = []
        verb_list = []
        for i in range(len(segment)):
            word = segment[i]
            n = ner[i]
            flag = flag_list[i]
            if n in self.boson_remain_list:
                n = self.ner_eng_ch_dict.get(ner[i])
            word_list.append(word)
            verb_list.append([flag,n])
        return word_list,verb_list

    def speech_call_NER(self,text):
        segment,flag_list,ner = self.NER_class.predict_qa_train(text)
        ner_word_list_list = []
        ner_verb_list_list = []
        for i in range(len(segment)):
            word_list,verb_list = self.speech_call_NER_sub(segment[i],flag_list[i],ner[i])
            ner_word_list_list.append(word_list)
            ner_verb_list_list.append(verb_list)
        return ner_word_list_list,ner_verb_list_list
    
    def get_speech_max_id(self):
        db = pymysql.connect(self.db_information["IP"],self.db_information["user"],self.db_information["password"])
        cursor = db.cursor()
        cursor.execute("use socialbot")
        sql_order = "select max(ID) from qa_speech where p_id = %s"
        cursor.execute(sql_order,(self.p_id))
        result = cursor.fetchone()[0]
        # with open("D:\\dektop\\QA_test_demo\\tt.txt",'a',encoding='utf_8_sig') as fout:
        #     fout.write("Test")
        #     fout.write(str(result))
        return result

    def speech_train_main(self,df):
        word_list_list = []
        flag_list_list = []
        sentence_list = []
        result_speech_list = []
        result_speech_sentence_list = []
        for i in range(len(df)):
            temp = df["斷詞修改"].iloc[i]
            temp = temp.split(' ')
            word_list = []
            flag_list = []
            for j in range(len(temp)):
                temp[j] = temp[j].lstrip().rstrip()
                sto = temp[j].split('_')
                try:
                    word,flag = sto[0],sto[1]
                except:
                    continue
                word_list.append(word)
                flag_list.append(flag)
            flag_list = self.flag_remove_num(flag_list)
            sentence = ''.join(word_list)
            word_list_list.append(word_list)
            flag_list_list.append(flag_list)
            sentence_list.append(sentence)
            result_speech_sentence_list.append([df["原文斷詞"].iloc[i],df["斷詞修改"].iloc[i]])

        ner_word_list_list,ner_verb_list_list = self.speech_call_NER(sentence_list)
        try:
            max_id = (self.get_speech_max_id()) + 1
        except:
            max_id = 1
        for i in range(len(word_list_list)):
            word_list,flag_list = word_list_list[i],flag_list_list[i]
            ner_word_list,ner_verb_list = ner_word_list_list[i],ner_verb_list_list[i]
            ner_word_bool_list = [True] * len(ner_word_list)
            id_set_list = []
            for j in range(len(word_list)):
                word = word_list[j]
                bFind = False
                for k in range(len(ner_word_list)):
                    if word == ner_word_list[k] and ner_word_bool_list[k]:
                        result_speech_list.append([max_id,word,ner_verb_list[k][0],ner_verb_list[k][1]])
                        id_set_list.append(str(max_id))
                        max_id += 1
                        bFind = True
                        ner_word_bool_list[k] = False
                        continue
                if not bFind:
                    # if flag_list[j][0] in self.boson_remain_list:
                    if flag_list[j][0] in ["人","物","地","時"]:
                        result_speech_list.append([max_id,word,'x',flag_list[j]])
                        id_set_list.append(str(max_id))
                        max_id += 1
                    else:
                        result_speech_list.append([max_id,word,flag_list[j],'x'])
                        id_set_list.append(str(max_id))
                        max_id += 1
            id_set_str = ",".join(id_set_list)
            result_speech_sentence_list[i].append(id_set_str)
        # with open("D:\\dektop\\QA_test_demo\\test.txt",'w',encoding='utf_8_sig') as fout:
        #     for row in result_speech_sentence_list:
        #         fout.write(str(row[0]) + str(row[1]) + str(row[2]) + str(row[3]) + '\n')
        self.insert_speech(result_speech_list)
        self.insert_speech_sentence(result_speech_sentence_list)

    def delete_speech(self,ass_id_set_str):
        db = pymysql.connect(self.db_information["IP"],self.db_information["user"],self.db_information["password"])
        cursor = db.cursor()
        cursor.execute("use socialbot")
        sql_order = "delete from qa_speech where p_id = %s and ID in {}".format(ass_id_set_str)
        cursor.execute(sql_order,(self.p_id))
        db.commit()

    def speech_sentence_train_main(self,df):
        db = pymysql.connect(self.db_information["IP"],self.db_information["user"],self.db_information["password"])
        cursor = db.cursor()
        cursor.execute("use socialbot")
        id_list = list(df["ID"])
        id_list.append("-1")
        id_str = ",".join(id_list)
        id_str = "(" + id_str + ")"
        sql_order = "select ass_id from qa_speech_sentence where p_id = %s and ID in {}".format(id_str)
        cursor.execute(sql_order,(self.p_id))
        temp = cursor.fetchall()
        ass_id_list = []
        for i in range(len(temp)):
            ass_id_list.append(temp[i][0])
        ass_id_list.append("-1")
        ass_id_set_str = ",".join(ass_id_list)
        ass_id_set_str = "(" + ass_id_set_str + ")"
        sql_order ="delete from qa_speech_sentence where p_id = %s and ID in {}".format(id_str)
        cursor.execute(sql_order,(self.p_id))
        db.commit()
        self.delete_speech(ass_id_set_str)
        
    def insert_speech(self,data):
        db = pymysql.connect(self.db_information["IP"],self.db_information["user"],self.db_information["password"])
        # db = pymysql.connect(self.db_information["IP"],self.db_information["user"])
        # with open("C:\\Users\\student\\Desktop\\json_test.txt",'w') as fout:
        #     fout.write(str(df.head()))
        cursor = db.cursor()
        cursor.execute("use socialbot")
        sql_duplicate_order = "select * from qa_speech where p_id = %s and 字詞 = %s and 詞性 = %s and 實體 = %s"
        sql_order = "insert into qa_speech(ID,p_id,字詞,詞性,實體)values(%s,%s,%s,%s,%s);"
        for i in range(len(data)):
            cursor.execute(sql_duplicate_order,(self.p_id,data[i][1],data[i][2],data[i][3]))
            temp = cursor.fetchone()
            if temp != None:
                continue
            cursor.execute(sql_order,(data[i][0],self.p_id,data[i][1],data[i][2],data[i][3]))
        db.commit()

    def insert_speech_sentence(self,data):
        db = pymysql.connect(self.db_information["IP"],self.db_information["user"],self.db_information["password"])
        # db = pymysql.connect(self.db_information["IP"],self.db_information["user"])
        # with open("C:\\Users\\student\\Desktop\\json_test.txt",'w') as fout:
        #     fout.write(str(df.head()))
        cursor = db.cursor()
        cursor.execute("use socialbot")
        sql_duplicate_order = "select * from qa_speech_sentence where p_id = %s and 斷詞修改前 = %s"
        sql_order = "insert into qa_speech_sentence(p_id,斷詞修改前,斷詞修改後,ass_id)values(%s,%s,%s,%s);"
        for i in range(len(data)):
            cursor.execute(sql_duplicate_order,(self.p_id,data[i][0]))
            temp = cursor.fetchone()
            if temp != None:
                continue
            cursor.execute(sql_order,(self.p_id,data[i][0],data[i][1],data[i][2]))
        db.commit()

    def QA_train_main(self,data):
        data = data.fillna(value="")
        df_insert = data[data["datatype"] == "insert"]
        df_upload = data[data["datatype"] == "upload"]
        df_insert = pd.concat([df_insert,df_upload],axis=0)
        df_change = data[data["datatype"] == "change"]
        df_remove = data[data["datatype"] == "remove"]
        
        df_change = self.QA_test.change_sentence_for_rule_change(df_change)
        # df_change.to_csv("df_change.csv",encoding='utf_8_sig',index=0)
        
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
    

