import os
import pandas as pd
import numpy as np
import math

class QA_train:

    class pair:
        def __init__(self,word,flag):
            self.flag = flag
            self.word = word

    def __init__(self):
        self.add_remain_dict = {}
        self.article_remain_list = []
        self.que_remain_list = []
        self.flag_que_remain_dict = {}
        self.sql_columns_list = []
        self.data_dir = os.path.join('module','QA_data')
        self.load_data()
    
    def train(self,abs_data_dir):
        result = []
        df = pd.read_csv(abs_data_dir)
        for i in range(len(df)):
            if not df.iloc[i,1] == df.iloc[i,1]:#判斷nan
                continue
            if not df.iloc[i,2] == df.iloc[i,2]:#判斷nan
                continue
            # if df.iloc[i,3] == df.iloc[i,3]:
            #     continue
            df.iloc[i,1] = self.article_pre(df.iloc[i,1])
            df.iloc[i,2] = self.article_pre(df.iloc[i,2])
            article = df.iloc[i,1]
            article = article.split(' ')
            while '' in article:
                article.remove('')
            article,word_in_article_remain = self.check_article_remain(article)
            if not word_in_article_remain:
                continue
            article,article_flag_list = self.p_flag_sort(article)
            ori_article = ' '.join(article)
            article_aft = ' + '.join(article_flag_list)
            que = df.iloc[i,2]
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
            row_data = [ori_article,df.iloc[i,2],ans_word,article_aft,que_aft,ans_flag]
            result.append(row_data)
        for row in result:
            print(row)
        self.save_sql(result)
    
    def save_sql(self,result):
        result = pd.DataFrame(np.array(result))
        result.to_csv('D:\\dektop\\work_data_backup_0923_2256\\rule.csv',encoding='utf_8_sig')

    def change_rule(self,flag):
        if flag < 0 or flag > 2:
            return 0
        if flag == 0:
            pass
        elif flag == 1:
            pass
        else:
            pass

    def load_data(self,add_remain = '',article_remain = 'article_remain_test.txt',que_remain = 'que_remain_long_test.txt',flag_que_remain = 'flag_que_remain_dict_test.txt'):
        print(os.getcwd())
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
        print('generate_ans_test')
        print(rule)
        print(que_transfer)
        # print(article)
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
    
    def article_pre(self,data):
        data = data.replace('\n',' ')
        data = data.replace('\r',' ')
        return data

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
    

