# coding=utf-8
from sklearn.metrics import pairwise_distances
from sklearn.feature_extraction.text import CountVectorizer
from gensim.summarization import summarize #for TextRank Summary
import numpy as np
try:
    import TextProcessor
except:
    from module import TextProcessor

#句子與原文相似度
class TextSim_TextSum():
    def __init__(self):
        self.TextProcessor = TextProcessor.TextProcessor()
    
    def summary(self, text, compression_ratio=0.4):
        text = self.TextProcessor.sentence_break(text)
        if compression_ratio<1:
            num_summary = max(1, int(len(text)*compression_ratio))
        else:
            num_summary = compression_ratio
        num_summary = min(len(text), num_summary)
        
        segments = self.TextProcessor.segment(text, 'boson')
            
        segments.insert(0, ' '.join(segments))
        
        countVectorizer = CountVectorizer()
        textVector = countVectorizer.fit_transform(segments)
        
        distance_matrix = pairwise_distances(textVector.toarray(), metric="cosine") #餘弦距離 = 1-餘閒相似度
        
        #np.argsort 由小排到大的位置
        rank = np.argsort(distance_matrix, axis=1)[0][1:] #與原文相似度, 第一列是原文所以要去掉
        
        summary_idx=[rank[0]] #排序最大的優先當作摘要
        idx = 1
        while(len(summary_idx)<num_summary and idx<len(rank)): #直到取到足夠的摘要數或句子都不符合摘要條件
            current = rank[idx] #當前句子idx            
            for s in summary_idx: #相似度距離都要大於0.1, 否則不當作摘要
                if distance_matrix[current][s] < 0.1:
                    break
            else: #current與其他句子相似度距離都大於0.1
                summary_idx.append(current)
            idx=idx+1
         
        summary = [text[i-1] for i in sorted(summary_idx)] #原先的idx有包含原文, 所以要-1
        
        return summary

#主題地圖
class TRMap_TextSum():
    def __init__(self):
        self.TextProcessor = TextProcessor.TextProcessor()
    
    def summary(self, text, compression_ratio=0.4):
        text = self.TextProcessor.sentence_break(text)
        if compression_ratio<1:
            num_summary = max(1, int(len(text)*compression_ratio))
        else:
            num_summary = compression_ratio
        num_summary = min(len(text), num_summary)
        
        segments = self.TextProcessor.segment(text)
        
        countVectorizer = CountVectorizer()
        textVector = countVectorizer.fit_transform(segments)
        
        U,sigma,VT=np.linalg.svd(textVector.toarray())
        sigma = np.pad(sigma, (0, VT.shape[1] - sigma.shape[0]), mode='constant')
        sigma = sigma * np.identity(sigma.shape[0])
        
        mask = num_summary
        new_TextVector = np.matmul(np.matmul(U[:,:mask], sigma[:mask,:mask]), VT[:mask,:])

        distance_matrix = pairwise_distances(new_TextVector, metric="cosine")
        
        #計算句子鏈結數, 相似度距離<=0.3代表有鏈結
        edge_count = []
        for row in distance_matrix:
            edge = 0
            for col in row:
                if col <= 0.3:
                    edge += 1
            edge_count.append(edge)

        rank = np.argsort(edge_count) #排序
        
        summary_idx=[rank[0]] #排序最大的優先當作摘要 
        idx = 1
        while(len(summary_idx)<num_summary and idx<len(rank)): #直到取到足夠的摘要數或句子都不符合摘要條件
            current = rank[idx] #當前句子idx
            for s in summary_idx: #相似度距離都要大於0.1, 否則不當作摘要
                if distance_matrix[current][s] < 0.1:
                    break
            else: #current與其他句子相似度距離都大於0.1
                summary_idx.append(current)
            idx=idx+1
            
        summary = [text[i] for i in sorted(summary_idx)]
        
        return summary

#TextRank
class TextRank_TextSum():
    def __init__(self):
        self.TextProcessor = TextProcessor.TextProcessor()
    
    def summary(self, text, compression_ratio=0.4):
        text = self.TextProcessor.sentence_break(text)
        segments = self.TextProcessor.segment(text, 'boson', use_stopwords=False)
        
        inputs = '. '.join(segments)+'.'
        try:
            summary = summarize(inputs, ratio=compression_ratio).replace(' ','').split('.\n')
        except:
            summary = []
        
        for p in set('。」!?！？"'):
            summary = [sum.replace(p+'.', p) for sum in summary]
        return summary

if __name__ == '__main__':
    import TextProcessor
    import re
    from os import listdir

    TextSim = TextSim_TextSum()
    TextRank = TextRank_TextSum()
    TRMap = TRMap_TextSum()

    # i = 0
    # path = 'C:/Users/mcu/Downloads/課文轉檔(7~12冊)'
    # with open('C:/Users/mcu/Downloads/summarize.csv', 'w', encoding='utf-8-sig') as r:
    #     r.write('演算法,20%,30%,40%,50%\n')
    #     for p in listdir(path):
    #         with open(path+'/'+p, 'r', encoding='utf-8') as f:
    #             text = ''
    #             for line in f.readlines()[1:]:
    #                 text += re.sub(r"\s","",line)
    #         try:
    #             TR2 = ' '.join(TextRank.summary(text, 0.2))
    #             TS2 = ' '.join(TextSim.summary(text, 0.2))
    #             TM2 = ' '.join(TRMap.summary(text, 0.2))

    #             TR3 = ' '.join(TextRank.summary(text, 0.3))
    #             TS3 = ' '.join(TextSim.summary(text, 0.3))
    #             TM3 = ' '.join(TRMap.summary(text, 0.3))

    #             TR4 = ' '.join(TextRank.summary(text, 0.4))
    #             TS4 = ' '.join(TextSim.summary(text, 0.4))
    #             TM4 = ' '.join(TRMap.summary(text, 0.4))

    #             TR5 = ' '.join(TextRank.summary(text, 0.5))
    #             TS5 = ' '.join(TextSim.summary(text, 0.5))
    #             TM5 = ' '.join(TRMap.summary(text, 0.5))

    #             r.write('original text,'+ text +'\n')

    #             r.write('TextRank,'+ TR2 +','+ TR3 +','+ TR4 +','+ TR5 +'\n')
    #             r.write('TextSim,'+ TS2 +','+ TS3 +','+ TS4 +','+ TS5 +'\n')
    #             r.write('TextMap,'+ TM2 +','+ TM3 +','+ TM4 +','+ TM5 +'\n')

    #             r.write('\n')
    #         except:
    #             print(p)
    #         i += 1
    #         if i> 1000:
    #             break
    # text = '（中央社記者余曉涵台北4日電）插畫家李允權的作品入選今年義大利波隆那兒童書展，今天他說，畫作中的靈感來自於他的一個夢，夢中他看到人類回到已被毀滅的地球，在一處山洞裡看到壁畫。具指標意義的義大利波隆那兒童書展，自1967年開始舉辦插畫展，吸引全球出版社及插畫人才參加。台北書展基金會表示，台灣今年首度有9位插畫家入選插畫展，創史上最佳紀錄。其中入選者之一的李允權相關畫作正在礁溪老爺酒店舉辦個展，入選義大利波隆那兒童書展的5幅作品複製畫作，也放在酒店中讓旅客欣賞。李允權受訪表示，入選的這5幅畫作的創作靈感其實來自於他夢中的一個畫面，夢境是地球已被毀滅，而人類從別的星球回到地球上考古時，在一處殘破的山洞裡，看到了5幅壁畫。李允權說，他把這5幅壁畫定義為荒蕪、崛起、繁華、腐化以及歸零，這是循環的概念。他表示，雖然最後這不是他參選的命題，但是很多靈感都是從其中發想的。李允權指出，他參賽的題目 Faith，簡單來說就是一個希望跟信念，人只要有信念就能一直走下去。談到為何要報名義大利波隆那兒童書展，李允權笑說，這個展沒有年紀限制，也不需要報名費，可是要寄原稿給主辦單位。李允權表示，只有看到他本身作品的原稿，才能知道他畫的是什麼東西。李允權的畫大部分都是親手拿著代針筆一筆一筆慢慢地畫，他說，因為他比較老派，畫作的風格也是傾向極簡主義，但就是要很有耐心。「創作有時候不是一個完整的構圖，會隨著時間跟筆觸有不同」李允權指出，創作者有時候很多都無法講得很清楚，因為大部分都是很多畫面在創作者的腦袋裡，就像他的畫 my soul 呈現的就是個漩渦，因為有時候會繞進去，鑽牛角尖，有時候會繞出來。（編輯：陳清芳）1080704'
    # text = '從前有一個人，種了許多漆樹。他每年割樹皮取樹汁，把樹汁裝在木桶裡，運到大城市去賣。這種漆樹的汁叫做「生漆」，是做油漆的原料。大城市裡的商人都知道他賣的漆最純了，所以都樂意向他買。幾年以後，他的生意越做越大，一個人沒法子分身，只得專心在家鄉種漆樹，不再做零賣的事了。有一天，有一個收買生漆的人來他家，這個人聽了非常生氣，那個收買生漆的人聽了，滿臉通紅的走了。例如做人虛假不實，不講信用做事隨便草率。'
    
    # Summary = TextSim_TextSum()
    # print(' '.join(Summary.summary(text, 0.3)))

    # Summary = TextRank_TextSum()
    # print(' '.join(Summary.summary(text)))

    # Summary = TRMap_TextSum()
    # # print(' '.join(Summary.summary(text)))
