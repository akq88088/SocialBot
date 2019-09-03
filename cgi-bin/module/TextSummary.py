# coding=utf-8
from sklearn.metrics import pairwise_distances
from sklearn.feature_extraction.text import CountVectorizer
from gensim.summarization import summarize #for TextRank Summary
import numpy as np

#句子與原文相似度
class TextSim_TextSum():
    def __init__(self, TextProcessor):
        self.TextProcessor = TextProcessor
    
    def summary(self, text, compression_ratio=0.4):
        text = self.TextProcessor.sentence_break(text)
        if compression_ratio<1:
            num_summary = int(len(text)*compression_ratio)
        else:
            num_summary = compression_ratio
        numsumary = min(len(text), num_summary)
        
        segments = self.TextProcessor.segement(text, 'boson')
            
        segments.insert(0, ' '.join(segments))
        
        countVectorizer = CountVectorizer()
        textVector = countVectorizer.fit_transform(segments)
        
        distance_matrix = pairwise_distances(textVector.toarray(), metric="cosine") #餘弦距離 = 1-餘閒相似度
        
        #np.argsort 由小排到大的位置
        rank = np.argsort(distance_matrix, axis=1)[0][1:num_summary+1]
        rank = sorted(rank)

        
        summary = [text[rank[i]-1] for i in range(num_summary)]
        
        return summary

#主題地圖
class TRMap_TextSum():
    def __init__(self, TextProcessor):
        self.TextProcessor = TextProcessor
    
    def summary(self, text, compression_ratio=0.4):
        text = self.TextProcessor.sentence_break(text)
        if compression_ratio<1:
            num_summary = int(len(text)*compression_ratio)
        else:
            num_summary = compression_ratio
        numsumary = min(len(text), num_summary)
        
        segments = self.TextProcessor.segement(text)
        
        countVectorizer = CountVectorizer()
        textVector = countVectorizer.fit_transform(segments)
        
        U,sigma,VT=np.linalg.svd(textVector.toarray())
        sigma = np.pad(sigma, (0, VT.shape[1] - sigma.shape[0]), mode='constant')
        sigma = sigma * np.identity(sigma.shape[0])
        
        mask = num_summary
        new_TextVector = np.matmul(np.matmul(U[:,:mask], sigma[:mask,:mask]), VT[:mask,:])

        distance_matrix = pairwise_distances(new_TextVector, metric="cosine")
        
        edge_count = []
        for row in distance_matrix:
            edge = 0
            for col in row:
                if col >= 0.3:
                    edge += 1
            edge_count.append(edge)

        rank = np.argsort(edge_count)[:num_summary+1]
        rank = sorted(rank)
        
        summary = [text[rank[i]] for i in range(num_summary)]
        return summary

#TextRank
class TextRank_TextSum():
    def __init__(self, TextProcessor):
        self.TextProcessor = TextProcessor
    
    def summary(self, text, compression_ratio=0.4):
        text = self.TextProcessor.sentence_break(text)
        if compression_ratio<1:
            num_summary = int(len(text)*compression_ratio)
        else:
            num_summary = compression_ratio
        numsumary = min(len(text), num_summary)
        
        segments = self.TextProcessor.segement(text, 'boson', use_stopwords=False)
        
        inputs = '. '.join(segments)
        
        summary = summarize(inputs, ratio=compression_ratio).replace(' ','').split('.\n')
        summary = [sum.replace('。.', '。')for sum in summary]
        return summary

if __name__ == '__main__':
    import TextProcessor
    text = '（中央社記者余曉涵台北4日電）插畫家李允權的作品入選今年義大利波隆那兒童書展，今天他說，畫作中的靈感來自於他的一個夢，夢中他看到人類回到已被毀滅的地球，在一處山洞裡看到壁畫。具指標意義的義大利波隆那兒童書展，自1967年開始舉辦插畫展，吸引全球出版社及插畫人才參加。台北書展基金會表示，台灣今年首度有9位插畫家入選插畫展，創史上最佳紀錄。其中入選者之一的李允權相關畫作正在礁溪老爺酒店舉辦個展，入選義大利波隆那兒童書展的5幅作品複製畫作，也放在酒店中讓旅客欣賞。李允權受訪表示，入選的這5幅畫作的創作靈感其實來自於他夢中的一個畫面，夢境是地球已被毀滅，而人類從別的星球回到地球上考古時，在一處殘破的山洞裡，看到了5幅壁畫。李允權說，他把這5幅壁畫定義為荒蕪、崛起、繁華、腐化以及歸零，這是循環的概念。他表示，雖然最後這不是他參選的命題，但是很多靈感都是從其中發想的。李允權指出，他參賽的題目 Faith，簡單來說就是一個希望跟信念，人只要有信念就能一直走下去。談到為何要報名義大利波隆那兒童書展，李允權笑說，這個展沒有年紀限制，也不需要報名費，可是要寄原稿給主辦單位。李允權表示，只有看到他本身作品的原稿，才能知道他畫的是什麼東西。李允權的畫大部分都是親手拿著代針筆一筆一筆慢慢地畫，他說，因為他比較老派，畫作的風格也是傾向極簡主義，但就是要很有耐心。「創作有時候不是一個完整的構圖，會隨著時間跟筆觸有不同」李允權指出，創作者有時候很多都無法講得很清楚，因為大部分都是很多畫面在創作者的腦袋裡，就像他的畫 my soul 呈現的就是個漩渦，因為有時候會繞進去，鑽牛角尖，有時候會繞出來。（編輯：陳清芳）1080704'

    process = TextProcessor.TextProcessor()

    Summary = TRMap_TextSum(process)
    print(' '.join(Summary.summary(text, compression_ratio=0.4)))