import requests
from bs4 import BeautifulSoup as bs
import csv

Base_url = 'https://u24.ru/news/city/?p=0'

headers = {'accept': '*/*',
           'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.157 Safari/537.36'}


def U24_parse(Base_url, headers):
    news = []
    session = requests.Session()
    request = session.get(Base_url, headers=headers)
    if request.status_code == 200:
        soup = bs(request.content, 'lxml')
        divs = soup.find_all('div', attrs={'class': 'col-sm-9'})
        for div in divs:
            title = div.find('div', attrs={'class': 'title'}).text
            href = 'https://u24.ru' + div.find('a')['href']
            text = div.find('a', attrs={'class': 'txt'}).text
            date = div.find('div', attrs={'class': 'newsdate'}).text
            divs_img = soup.find_all ('div', attrs = {'class': 'col-sm-3'})
            for div in divs_img:
                img = div.find ('img')[ 'src' ]
            news.append({
                'title': title,
                'href': href,
                 'text ': text ,
                'date': date,
                'img': img
                })
    else:
        print('Error')
    return news


def files_writer(news):
    with open('parsed_news.csv', 'w') as file:
        a_pen = csv.writer(file)
        a_pen.writerow(("Новость", "URL", "Загаловок", "Фото", "Дата"))
        for new in news:
            a_pen.writerow((new['title'], new['href'], new['text '], new['img'], new['date']))

news = U24_parse(Base_url, headers)
files_writer(news)
