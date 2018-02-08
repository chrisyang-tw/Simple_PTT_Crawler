# 利用Python製作ptt爬蟲程式
>這個程式只有單純的爬蟲功能，我並沒有做其他資料分析、文本分析，不過爬完資料後能做的事真的相當多！像是分析Stock版的行情，觀察與景氣的關聯性；或是分析Movie版，得知近期熱門的電影，也能得知一部電影的評價好壞等等。很多人可能覺得爬蟲很難，個人覺得身為Python初學者的我們可以在了解網頁HTML/CSS的語法後，再從網頁架構簡單的網頁(例如ptt)開始學起～
## 主要功能：
1. 可自行輸入欲爬蟲的ptt網址，及欲抓取的頁數。
2. 印出抓取的結果，並將輸出美化。
3. 可選擇是否要匯出成csv檔。
## PTT長什麼樣？
+ [PTT Movie版](https://www.ptt.cc/bbs/movie/index.html)
+ [PTT NTU版](https://www.ptt.cc/bbs/NTU/index.html)
## Code
+ **import**
```ruby
import requests
from bs4 import BeautifulSoup
from pretty_print import pretty_print
import urllib.parse
```
+ **爬取一頁的文章**
```ruby
index = str(input('想抓取哪個ptt看板？(ex: Movie版請輸入 https://www.ptt.cc/bbs/movie/index.html)：\n'))
pages = eval(input('想抓取幾頁呢？ex: 5：'))

not_exist = BeautifulSoup('<a>(本文已被刪除)</a>', 'lxml').a ## '本文已被刪除'的結構不同，自行生成<a>

def get_articles_on_ptt(url): ## 爬取一頁的文章
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml') ## 得到網頁原始碼
    articles = []

    for i in soup.find_all('div', 'r-ent'):
        meta = i.find('div', 'title').find('a') or not_exist
        articles.append({
            'title': meta.getText().strip(), ## strip 去除頭尾字符，預設是空白
            'push': i.find('div', 'nrec').getText(),
            'date': i.find('div', 'date').getText(),
            'author': i.find('div', 'author').getText(),
        })

    next_link = soup.find('div', 'btn-group-paging').find_all('a', 'btn')[1].get('href') ## 控制頁面選項(上一頁)

    return articles, next_link
```
+ **要爬幾頁**
```ruby
def get_pages(num): ## 要爬幾頁
    page_url = index
    all_articles = []

    for j in range(num):
        articles, next_link = get_articles_on_ptt(page_url)
        all_articles += articles
        page_url = urllib.parse.urljoin(index, next_link) ## 將上一頁按鈕的網址和 index 網址比對後取代
    
    return all_articles
```
+ **輸出至螢幕**
```ruby
data = get_pages(pages)

for k in data: ## 輸出至螢幕
    pretty_print(k['push'], k['title'], k['date'], k['author'])
```
+ **匯出csv**
```ruby
csv_or_not = input('輸入 y 以匯出成csv檔，輸入其他結束程式：')

if csv_or_not == 'y':
    board = index.split('/')[-2] ## 取出看板名
    csv = open('./ptt_%s版_前%d頁.csv'%(board, pages), 'a+', encoding='utf-8') ## 檔名格式，'a+'代表可覆寫
    csv.write('推文數,標題,發文日期,作者ID,\n')
    for l in data:
        l['title'] = l['title'].replace(',', '，') ## 與用來分隔的逗點作區別
        csv.write(l['push'] + ',' + l['title'] + ',' + l['date'] + ',' + l['author'] + ',\n')
    csv.close()
    print('csv檔案已儲存在您的資料夾中。')
else:
    quit()
```
