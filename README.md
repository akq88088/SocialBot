# SocialBot

為幫助學齡兒童學習課文知識，本研究使用深度學習技術來分析國小課文，使用命名實體識別(Named Entity Recognition NER)、情緒辨識與文本摘要，並根據辨識出來的實體(Ex. 人、事、物、地、時)，來產生對應的問題，此外本專案使用網頁搭建了對應的前台與後台系統，前端使用JavaScript後端使用PHP與Python。

## 前台介紹
前台共可分成匯入資料、摘要與情緒分析還有出題問答共三個區塊，如下圖的匯入資料區塊，在選擇文字模型部分，可以選擇對應的語義模型，輸入文章的部分，則可透過上傳文字檔或是將文章貼至右方的文字框來完成。

<img width="444" height="243" src="/img/前台_匯入資料.png">

按下分析按鈕後，會在下圖的摘要與情緒分析區塊顯示文章的摘要結果，還有各個情緒字詞占文章的比例，摘要的部分可以透過選取%數來決定要保留多少資訊量。

<img width="442" height="257" src="/img/前台_摘要與情緒分析.jpg">

按下分析按鈕後，在下圖的出題答案區塊，也會根據輸入的文章，產生對應的問題與答案。

## 後台介紹
後台則有命名實體、出題規則、文本摘要與情緒辨識共四個頁面，每個頁面都對應其功能，後台這邊主要負責資料的上傳、修改與刪除，還有模型的訓練。


