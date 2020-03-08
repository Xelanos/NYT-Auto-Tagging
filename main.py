import requests
from bs4 import BeautifulSoup

from modelV2 import AutoTag
from modelV3 import AutoTagNLP


if __name__ == '__main__':


    at = AutoTagNLP()
    # at.fit('ArticleText/NewYorkTimesArticleTextFullDb.csv')
    # at.save_model('savedNLP')
    at.load_trained_model('savedNLP_emded.pic', 'savedNLP_transform.pic')




    url = 'https://www.nytimes.com/2020/03/06/us/politics/trump-mark-meadows-mick-mulvaney.html'
    # url = 'https://www.nytimes.com/2020/03/07/world/asia/china-coronavirus-cost.html'
    html = requests.get(url)
    soup = BeautifulSoup(html.content, 'html.parser')

    paragraphs = soup.find_all("p", class_="css-exrw3m evys1bk0")
    text = ""
    for p in paragraphs:
        text += p.text

    print(text)
    tags = at.predict(text, 10)
    print("\ntags:")
    for k in tags:
        print(k, tags[k])

