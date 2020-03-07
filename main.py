import itertools

from datasketch import MinHash, MinHashLSHForest
from countingwords import make_set_of_most_common_words
from bs4 import BeautifulSoup
import pandas as pd
import requests
import pickle
import ast
import re
import numpy as np
from nltk import PorterStemmer
ps = PorterStemmer()

import multiprocessing
from multiprocessing import Pool
from functools import partial

from pandarallel import pandarallel

forest = MinHashLSHForest(num_perm=50)



def make_min_hash(words, num_perm=50):
    min_hash = MinHash(num_perm)
    for word in words:
        min_hash.update(word.encode('utf8'))
    return min_hash


def make_min_hash_list(df):
    res = []
    i = 0
    full = len(df.webURL)
    for url in df.webURL:
        html = requests.get(url)
        soup = BeautifulSoup(html.content, 'html.parser')

        paragraphs = soup.find_all("p", class_="css-exrw3m evys1bk0")
        text = ""
        for p in paragraphs:
            text += p.text
        wordList = re.sub("[^\w]", " ", text).split()
        res.append((url, make_min_hash(wordList, 60)))
        if i % 100 == 0: print(f'{i}/{full}')
        i += 1
    return res


def download_article(df):
    result = {}
    i = 0
    full = len(df.webURL)
    for url in df.webURL:
        html = requests.get(url)
        soup = BeautifulSoup(html.content, 'html.parser')

        paragraphs = soup.find_all("p", class_="css-exrw3m evys1bk0")
        text = ""
        for p in paragraphs:
            text += p.text
        result[url] = text
        if i % 100 == 0: print(f'{i}/{full}')
        i += 1

    return pd.DataFrame.from_dict(result, orient='index', columns=['webURL, Text'])





def parallelize_dataframe(df, func, n_cores=4):
    df_split = np.array_split(df, n_cores)
    pool = Pool(n_cores)
    # multi = pool.map(func, df_split)
    # result = list(itertools.chain.from_iterable(multi))
    df = pd.concat(pool.map(func,df_split))

    pool.close()
    pool.join()
    return df

if __name__ == '__main__':
    csv = 'ArticlesByYearWithCommonWords/NewYorkTimesArticles2020-CommonWords.csv'
    df = pd.read_csv(csv)
    df.drop_duplicates(subset='webURL', keep=False, inplace=True)
    min_hased = parallelize_dataframe(df, download_article)
    min_hased.to_csv('NewYorkTimesArticles2020-Text.csv')
    # forest = MinHashLSHForest(num_perm=60)
    # for min in min_hased:
    #     url, hashed = min
    #     forest.add(url, hashed)
    # df.webURL.parallel_apply(add_to_forest)
    # for index, words in freq_words.iteritems():
    #     words = ast.literal_eval(words)
    #     min_hash = make_min_hash(words)
    #     forest.add(f'{index}', min_hash)

    # forest.index()
    #
    # pickle.dump(forest, open("forest2020-2.p", "wb"))

    # forest = pickle.load(open('forest.p', 'rb'))
    #
    # # url = 'https://www.nytimes.com/2020/03/07/world/coronavirus-news.html'
    # # url = 'https://www.nytimes.com/2020/02/23/world/australia/climate-change-extremes.html'
    # url = 'https://www.nytimes.com/2020/03/06/us/politics/trump-mark-meadows-mick-mulvaney.html'
    #
    # html = requests.get(url)
    # soup = BeautifulSoup(html.content, 'html.parser')
    #
    # paragraphs = soup.find_all("p", class_="css-exrw3m evys1bk0")
    # text = ""
    # for p in paragraphs:
    #     text += p.text
    # wordList = re.sub("[^\w]", " ", text).split()
    #
    # print(make_set_of_most_common_words(url))
    #
    # query = make_min_hash(wordList, 60)
    # result = forest.query(query, 2)
    # for url in result:
    #     print(url)
    #     row = df[df['webURL'] == url]
    #     print(row['keywords'].values)
    #     print(row['frequent_words'].values)
    #     print('\n')


    # print(result)
