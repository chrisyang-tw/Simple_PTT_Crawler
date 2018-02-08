import requests
from bs4 import BeautifulSoup
from pretty_print import pretty_print ## 美化輸出
import urllib.parse ## url 相關應用

# index = 'https://www.ptt.cc/bbs/movie/index.html'
index = str(input('請輸入ptt看板網址(ex: https://www.ptt.cc/bbs/movie/index.html)：\n'))
pages = eval(input('請輸入想爬的頁數：'))

not_exist = BeautifulSoup('<a>(本文已被刪除)</a>', 'lxml').a ## '本文已被刪除'的結構不同，自行生成<a>

def get_articles_on_ptt(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml') ## 網頁原始碼
    articles = []

    for i in soup.find_all('div', 'r-ent'):
        meta = i.find('div', 'title').find('a') or not_exist ## 當爬到是空的，讓 meta = 0
        articles.append({
            'title': meta.getText().strip(), ## strip 去除頭尾字符，預設是空白
            'push': i.find('div', 'nrec').getText(),
            'date': i.find('div', 'date').getText(),
            'author': i.find('div', 'author').getText(),
        })

    next_link = soup.find('div', 'btn-group-paging').find_all('a', 'btn')[1].get('href') ## 控制頁面選項(上一頁)

    return articles, next_link

def get_pages(num): ## 要爬幾頁
    page_url = index
    all_articles = []

    for j in range(num):
        articles, next_link = get_articles_on_ptt(page_url)
        all_articles += articles
        page_url = urllib.parse.urljoin(index, next_link) ## 將上一頁按鈕的網址和 index 網址比對後取代
    
    return all_articles

# if __name__ == '__main__': ## 在此程式為主程式才執行
#    pages = 5

for k in get_pages(pages):
    pretty_print(k['push'], k['title'], k['date'], k['author'])