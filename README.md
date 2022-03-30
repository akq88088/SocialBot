# SocialBot

為幫助學齡兒童學習課文裡面的知識，本研究針對國小課文使用深度學習應用在命名實體識別(Named Entity Recognition NER)、情緒辨識與文本摘要等技術，並根據辨識出來的實體(Ex. 人、事、物、地、時)，來產生對應的問答，此外本專案使用網頁搭建了對應的前台與後台系統，前端使用JavaScript後端使用PHP與Python。

## 前台介紹
前台共可分成匯入資料、摘要與情緒分析還有出題問答共三個區塊，如下圖的匯入資料區塊，在選擇文字模型部分，可以選擇對應的語義模型，輸入文章的部分，則可透過上傳文字檔或是將文章貼至右方的文字框來完成。

<img width="444" height="243" src="/img/前台_匯入資料.png">

按下分析按鈕後，會在下圖的摘要與情緒分析區塊顯示文章的摘要結果，還有各個情緒字詞占文章的比例，摘要的部分可以透過選取百分比來決定要保留多少資訊量。

<img width="442" height="257" src="/img/前台_摘要與情緒分析.jpg">

按下分析按鈕後，在下圖的出題答案區塊，也會根據輸入的文章，產生對應的問題與答案。

<img width="440" height="125" src="/img/前台_出題答案.jpg">

## 後台介紹
後台則有命名實體、出題規則、文本摘要與情緒辨識共四個頁面，每個頁面都對應其功能，後台這邊主要功能有資料的上傳、修改與刪除，還有模型的訓練。

在下圖的命名實體後台頁面，在匯入資料區塊可以上傳標記好的實體資料，並按下開始訓練來重新訓練模型，在命名實體區塊則可以對實體做新增與修改。

<img width="9" height="240" src="/img/後台_命名實體.jpg">

在出題規則後台頁面，在匯入資料區塊可以上傳對應的出題規則，在出題規則區塊會顯示資料庫現有的規則，同樣可以對規則做新增、刪除與修改。

<img width="945" height="240" src="/img/後台_出題規則.jpg">

在文本摘要後台頁面，可以選擇要用萃取式的或是生成式文本摘要模型來做訓練，在文本摘要區塊會顯示文章摘要的結果，可以選取不同的百分比，來調整文本摘要保留的資訊量，並可將摘要結果儲存下來。

<img width="945" height="240" src="/img/後台_文本摘要.jpg">

在情緒辨識後台頁面，同樣可以上傳帶有情緒詞標註的資料，在情緒辨識區塊也可以對現有的情緒詞做修改。

<img width="945" height="240" src="/img/後台_情緒辨識.jpg">
