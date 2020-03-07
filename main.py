import requests
from bs4 import BeautifulSoup

from modelV2 import AutoTag


if __name__ == '__main__':
    at = AutoTag(200)
    at.fit('NewYorkTimesArticles2020-Text.csv')
    url = 'https://www.nytimes.com/2020/03/06/us/politics/trump-mark-meadows-mick-mulvaney.html'

    html = requests.get(url)
    soup = BeautifulSoup(html.content, 'html.parser')

    paragraphs = soup.find_all("p", class_="css-exrw3m evys1bk0")
    text = ""
    for p in paragraphs:
        text += p.text

    print(at.predict(text, 3))

