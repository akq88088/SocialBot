#!D:/Python/Python36/python.exe
#!C:/ProgramData/Anaconda3/python.exe
import cgi, cgitb
import os
import pandas as pd
import numpy as np
import json
from module.QA_test import QA_test
from module import TextSummary
import glob
text_list = [
"""
107國語2上課文

一、我的相簿

我有一本厚厚的相簿，

一張張、一頁頁，

是我的生活剪貼簿。


打開相簿，

我張大眼睛看著媽媽，

身上還包著尿布。

打開相簿，

我像一隻小鴨子，

搖搖晃晃學走路。


打開相簿，

我和同學又唱又跳，

開開心心的演出。


厚厚的相簿，

就是笑臉收集簿，

一張又一張相片

都能說出我的故事。 
""",
"""
二、身高樹

我喜歡靠著牆，讓爸爸幫我量身高，只要我長高一點，爸爸就會在牆上畫一條線。牆上的線條越畫越多，也越畫越高了。

星期天的早上，爸爸帶我去公園玩。我在單槓下，像以前一樣用力往上跳，沒想到，這次我握住單槓了。爸爸笑著說：「你長高了！」我拉著單槓，感覺好有力氣。

我們回到家，吃了點心，我把盤子洗好、收好。爸爸說：「你會做家事，真的是懂事了！」

那一天，爸爸幫我量身高，又畫出一條新的線。我們把牆上的線條畫成大樹，這就是我的身高樹。
""",
"""
三、種子找新家

昭和草的種子，

長著白色的毛，

如果風兒吹過，

就能輕快的飛呀飛。


鬼針草的種子，

像小小的針，

如果動物經過，

就能跟著動物去旅行。


指甲花的種子，

在果子裡等了又等，

ㄅㄥ！

果子一裂開，

馬上跳向四面八方。


種子成熟時，

會出去找新家。

生了根，

發了芽，

開開心心的長大。 
""",
"""
四、變得不一樣了

在一個荷花池裡，大肚魚和小蝌蚪一起游泳，一起玩水，他們是最好的朋友。

大肚魚看到小蝌蚪一天天長大，腳越來越長，尾巴卻越來越短。有一天，他沒有見到小蝌蚪，只看到荷葉上寫著：

大肚魚：

    我正在學唱歌，五天後，我會在這裡等你，請你來聽我唱歌。

                                                    小蝌蚪留

九月二十日早上十點 

五天後，大肚魚來到荷葉旁，卻沒有看到小蝌蚪，只聽到一隻小青蛙叫著：「大肚魚，是我呀！我可以跳出水面玩了，真好！」

大肚魚張大眼睛說：「哇！你少了一條尾巴，卻多了一個圓圓的大肚子，還可以跳來跳去，變得不一樣了！」

小青蛙開心的又跳又唱：「ㄍㄨㄚ ㄍㄨㄚ  ㄍㄨㄚ！ㄍㄨㄚ ㄍㄨㄚ  ㄍㄨㄚ！」
""",
"""
五、天空愛畫畫

天空是個畫家，

每天不停的畫畫。

 

晴天時，

用金黃色的彩色筆，

慢慢畫出火熱的太陽。

 

下大雨前，

用沾了墨汁的毛筆，

快快畫出灰黑的雲朵。

 

黃昏時，

用五顏六色的水彩，

輕輕畫出彩色的晚霞。

 

天空最愛畫畫，

只要抬頭

就能欣賞他的畫。
""",
"""
六、神奇的本領

大海裡，怎麼會有黑黑的煙？是誰在汙染海水？原來，那是章魚噴出墨

汁，想從大魚眼前逃跑。

大海裡，怎麼會有可愛的小雨傘？是誰會在海裡撐傘？原來，那是有毒的水母，一開一合，要去找食物。

大海裡，怎麼會有亮亮的燈光？是誰在開晚會？原來，那是發光魚點了燈，等著捉小魚。

大海裡，噴墨的章魚、有毒的水母、點燈的發光魚，都有不同的本領，真的好神奇！
""",
"""
七、樹林裡的祕密

奶奶家附近有一片樹林。星期天的早上，她帶我和哥哥到樹林裡散步，奶奶說：「這裡有很多小昆蟲，我們來找一找！」

哥哥很快就找到停在落葉上的枯葉蝶，我卻什麼都找不到。奶奶笑著跟我說：「想找到小昆蟲，不只要張大眼睛，還要細心找，不能太著急。」

過了不久，我發現一根會走動的小樹枝，開心的大叫：「哈！我找到竹節蟲了。」哥哥說：「你看！這裡有一隻綠色的小蟲，身體好像一片葉子。」我和哥哥都叫不出名字，很好奇。奶奶笑著說：「我們回去查一查吧！」

回家的路上，我聽見昆蟲的叫聲，好像在輕輕的說：「我們是樹林裡的祕密，請不要說出去呀！」
""",
"""
閱讀樂園一

小白和小灰  許玲慧

「咕嚕咕嚕……」

「嘎！嘎！」

濃密的樹林裡，住了好多鷺鷥鳥，小白鷺小白和夜鷺小灰就住在這裡。

全身雪白的小白，兩隻腳細細長長的，特別喜歡踩在水田裡。身體灰藍的小灰，兩隻腳短短的，靠著銳利的眼睛、敏銳的動作，不用踩到水裡，就能吃到小蟲。

白天，小白和同伴們在附近的池塘玩耍、找東西吃。小灰留在樹林裡休息，直到小白回來，一起談天說笑。一陣子後，小灰才開始一天的活動。

這天，天色漸漸暗下來，鷺鷥們從四面八方飛回來。小灰看到小白，高興的叫著：「小白，你回來了，今天有什麼開心的事呀！」小白說：「有哇！今天跟在水牛旁邊，吃到好多小蟲呢！有蟲吃真棒！」

「為什麼跟在水牛旁邊就有東西吃呢？」

「水牛幫主人犁田，只要他走過的田，泥土都會被翻鬆。」

「喔！把田翻鬆，小蟲就會跑出來。」

「對啊！」

「小白，你在水田裡還有找到什麼好吃的嗎？」

「魚、蝦、青蛙……通通都有！我只要看到想吃的東西，一步一步慢慢的走過去，眼睛盯著獵物，用尖尖的嘴巴快速的啄下去，不管是魚、是蝦都跑不掉。」

「是啊！你細細長長的腳和尖尖的嘴，是最棒的武器，只要睜大眼睛、動作快，想吃什麼都不是問題。」

「小灰，你的眼睛也很厲害，就算四周黑漆漆的，也難不倒你。哪天我帶你一起出去玩，白天的池塘可熱鬧了！」

「好哇！可是我活動了一整晚，不知道還有沒有辦法陪你出去玩？」

「好玩的事等著你，一定要想辦法早早起來呀！」

「咦！小白、小白！睡著了啊？剛剛還說著話，怎麼就睡著了呢？只好等明天再說了！」小灰看到小白睡著，拍拍翅膀，在空中轉了一圈就飛出去了。
""",
"""
八、阿金的長尾巴

老鼠阿金的尾巴很長很長，一不小心會被朋友踩到，也常常害朋友跌倒。阿金覺得長尾巴真麻煩。

這天，阿金和平常一樣，來到河邊找食物，忽然聽見「救命啊！救命啊！」的喊叫聲，原來是一隻小老鼠掉進河裡了！水很急，小老鼠一下子被沖到河中央，一下子被沖到河邊，他覺得好害怕。阿金著急的說：「要是有繩子，我就能救他了。」

阿金看了看四周，看到了他的長尾巴，等到小老鼠快被沖到河邊時，他拉住旁邊的樹枝，再把長尾巴甩進水中，大叫：「快！快捉住我的尾巴！」

阿金救了小老鼠。他發現，原來長尾巴的用處那麼大！
""",
"""
九、奇怪的鏡子

有一天晚上，小鴨來到水池，發現池裡有個發亮的東西，他忍不住大叫：「好圓好亮的鏡子啊！」

小鴨想把鏡子撿起來，但是還沒碰到，鏡子就碎成一片一片了。不一會兒，又圓了起來。

小鴨急忙找小青蛙來幫忙。小青蛙張開大大的嘴巴，想咬住鏡子，沒想到鏡子又碎了。

小鴨又找螃蟹來幫忙。螃蟹伸出兩把大剪刀，想夾住鏡子，可是鏡子又碎了。大家都覺得很奇怪，這是怎麼一回事呢？ 

樹上的貓頭鷹全都看見了，哈哈大笑說：「那不是鏡子，是月亮在水面上的倒影！」大家聽了抬起頭，看看天空，又看看水面，都笑了起來。
""",
"""
十、賣房子

山上有一間房子，住著老爺爺和老奶奶。

老奶奶常說：「這個房子太灰暗了，屋外又沒有好看的風景。」所以，他們想把房子賣掉。

過了幾個月，老爺爺在門外，聽到有人說：「這房子加點顏色才好看。」老爺爺聽了，就把屋外的牆刷成紅色，把門刷成白色。

沒多久，又有人說：「我喜歡這房子，可是屋裡太灰暗了。」老爺爺就把屋裡的牆刷成淡黃色。

後來，有人很想買這個房子，只是覺得院子空空的。老奶奶知道後，就在院子裡種了花和樹。

過了一陣子，老奶奶跟老爺爺說：「我發現我們的房子，屋裡溫暖明亮，屋外鳥語花香，住在這裡真好。我們為什麼要賣房子呢？」
""",
"""
十一、魯班造傘

從前，有個喜歡發明東西的人，叫做魯班。

有一天，忽然下起一陣大雨，魯班看見路上的行人東奔西跑，就是找不到躲雨的地方。魯班想了又想，請人造了一個亭子，讓路過的人躲雨。

亭子造好了，魯班還是不滿意，他心裡想：「如果這個亭子能移動，人們就不用一直待在亭子裡等雨停。」這時，魯班看見一群孩子，每個人手上都舉著一片大荷葉，開心的跑過去。他想：「把亭子變小，就可以帶在身上了！」

魯班照著荷葉的樣子，先用竹枝做架子，再貼上羊皮。他的妻子說：「不用的時候，如果可以把它合起來，那就更好了。」

最後，魯班和妻子一起做出可以張開和合上的「傘」。有了傘，人們下雨天出門就方便多了。
""",
"""
十二、一起騎單車

我家附近有一條長長的單車道，很多人會在這裡騎單車。看他們笑容滿面，我們一家人也好想加入。

放學後，爸爸準備了手套和安全帽，教我和哥哥騎單車，我和哥哥開心得不得了。我們先在家門前的小路練習，再騎上長長的單車道，一起加入騎車的行列。

天氣好的時候，我們會騎到更遠的地方，爸爸在前，中間是哥哥，後面跟著我和媽媽。騎在單車上，一陣陣的微風吹在臉上，送來花香和草香，真舒服！

現在只要一到假期，我們一家人就會騎上最愛的單車，欣賞美麗的風景，享受快樂的時光。
""",
"""
十三、賽跑

操場上的跑道，

是一條條的五線譜。

跑道上的我們，

是跳動的小音符。


一陣一陣

是老師、家長的加油聲，

此起彼落

是同學的尖叫聲。


不小心跌倒，

只是短短的休止符，

起來再奔跑，

音樂還沒有結束。


曲子的最後，

有歡笑聲、

有嘆氣聲，

最多的還是

送給我們的掌聲。
""",
"""
十四、快樂小書迷

○月○日  星期六  天氣晴

今天是社區圖書館的「好書交換日」，爸爸、媽媽和我都帶了書，要和別人交換不一樣的好書。

我本來捨不得把書送出去，媽媽笑著說：「你可以換到沒看過的書，別人可以看到你喜歡的書，不是一舉兩得嗎？」

來換書的人好多，志工姐姐笑著說：「你的舊書，是我的新書，一本換一本，歡迎來交換。」大家像尋寶一樣，在書架前找來找去。我找了一會兒，發現一本小蝌蚪找媽媽，看了幾頁，覺得很新奇，就換了這本書。

不久，我的同學阿光也來了，他換到的竟然是我帶來的書呢！等他看完，我要問問他，最喜歡故事裡的哪一個人物？
""",
"""
閱讀樂園二

早起的一天  賴馬

我今天好早好早就起床了，不用鬧鐘大吼小叫，也不需要媽媽費心叫我起床。四周靜悄悄的，我刷好牙，把臉擦一擦，看見哥哥還在睡覺，爸爸還在睡覺，媽媽也還在睡覺。

我今天好早好早就起床了，外面的天空暗暗的。哈！連太陽公公也還沒起床。我走到奶奶的房間，奶奶已經起床，正在等我呢！因為，說好的，我要幫奶奶的忙。

天漸漸亮了，我和奶奶到了熱鬧的市場。要買些什麼呢？我低頭看了一下購物清單，說：「奶奶，我們先來買爺爺最喜歡吃的麵條吧！」奶奶笑著點點頭。接著，走哇走，逛啊逛，我們經過了花店，這裡的花又香又漂亮。花店旁邊就是蛋糕店，我們帶了一束百合花和一個大蛋糕回家。

回到家，我好忙好忙啊！我認真的掃地，又跟奶奶一起洗菜，也幫忙拿碗盤，不管哪一樣都難不倒我！奶奶看了一直笑。

我今天好忙好忙，還畫了一張卡片，寫些什麼呢？只有我和收到卡片的人知道。

傍晚，爸爸、媽媽回來了。伯伯、叔叔一家人也來了。啊！本來有事的姑姑也來了，大家都來了！每個人臉上都是笑容，因為今天是一個特別的日子。

桌上擺滿了好多好吃的東西，都是今天我和奶奶一起準備的。大家開開心心的把杯子舉高，大聲對著爺爺說：「生日快樂！」爺爺的臉紅了。

我今天好早好早就起床了。我想我一定比蜜蜂還要勤勞，所以，我現在好想好想睡覺。
"""
]
def getSummary(text,algorithm="textsim",percentage=0.4):
    algoritm_dic = {"textsim": TextSummary.TextSim_TextSum(),
                    "textrank": TextSummary.TextRank_TextSum(),
                    "textmap": TextSummary.TRMap_TextSum()}

    Summary = algoritm_dic[algorithm]
    return " ".join(Summary.summary(text, compression_ratio=percentage))

def txt2text_list(data_dir='D:\\dektop\\QA_test_demo\\泰北課文'):
    result_list = []
    text_list = glob.glob(os.path.join(data_dir,'*.txt'))
    for txt in text_list:
        with open(txt,'r',encoding='utf_8_sig') as fin:
            result_list.append(fin.read())
    return result_list

parameter = cgi.FieldStorage()
text = parameter.getvalue('text')
p_name = parameter.getvalue('p_name')
# p_name = "tt"
owner = parameter.getvalue('owner')
QA_test = QA_test(p_name)


iRun = 0
insert_id = 0
result_list = []
que_ans_dict = {}
df_result = QA_test.predict(text)
if len(df_result.columns) == 10:
    que_ans_dict = {}
    for i in range(len(df_result)):
        que_ans_dict.update({insert_id:[df_result["輸入出題"][i],df_result["輸入答案"][i]]})
        insert_id += 1
else:
    que_ans_dict.update({insert_id:["沒有產生問題","沒有產生答案"]})
print("Content-type:text/html") #必須
print('') #必須
print(json.dumps(que_ans_dict))
# text_list = txt2text_list()
# iRun = 0
# result_list = []
# while True:
#     if iRun >= len(text_list):
#         break
#     # if iRun >= 10:
#     #     break
#     print(iRun)
#     # text = text_list[iRun]
#     # text = getSummary(text)
#     # df_result = QA_test.predict_rule_scan(text)
#     not_success = True
#     while not_success:
#         try:
#             text = text_list[iRun]
#             text = getSummary(text)
#             df_result = QA_test.predict_rule_scan(text)
#             not_success = False
#         # break
#         except:
#             print('QA test predict error!')
#             continue
#     if len(df_result) > 0:
#         df_result["n_article"] = text
#         result_list.append(df_result)
#     iRun += 1

# df = pd.concat(result_list,axis=0)
# df.to_csv(os.path.join('D:\\dektop\\QA_test_demo','QA_test_1116.csv'),index=0,encoding='utf_8_sig')
# print('finish')

