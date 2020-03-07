from datasketch import MinHash, MinHashLSHForest
from countingwords import make_set_of_most_common_words
from bs4 import BeautifulSoup
import pandas as pd
import requests
import pickle
import ast
import re

import multiprocessing
from functools import partial

from tqdm import tqdm
import numpy as np

tqdm.pandas()

forest = MinHashLSHForest(num_perm=50)


def make_min_hash(words, num_perm=20):
    min_hash = MinHash(num_perm)
    for word in words:
        min_hash.update(word.encode('utf8'))
    return min_hash


def add_to_forest(url):
    html = requests.get(url)
    soup = BeautifulSoup(html.content, 'html.parser')

    paragraphs = soup.find_all("p", class_="css-exrw3m evys1bk0")
    text = ""
    for p in paragraphs:
        text += p.text
    wordList = re.sub("[^\w]", " ", text).split()
    min_hash = make_min_hash(wordList, 50)
    forest.add(url, min_hash)


def _df_split(tup_arg, **kwargs):
    split_ind, df_split, df_f_name = tup_arg
    return (split_ind, getattr(df_split, df_f_name)(**kwargs))


def df_multi_core(df, df_f_name, subset=None, njobs=-1, **kwargs):
    if njobs == -1:
        njobs = multiprocessing.cpu_count()
    pool = multiprocessing.Pool(processes=njobs)

    try:
        splits = np.array_split(df[subset], njobs)
    except ValueError:
        splits = np.array_split(df, njobs)

    pool_data = [(split_ind, df_split, df_f_name) for split_ind, df_split in
                 enumerate(splits)]
    results = pool.map(partial(_df_split, **kwargs), pool_data)
    pool.close()
    pool.join()
    results = sorted(results, key=lambda x: x[0])
    results = pd.concat([split[1] for split in results])
    return results


if __name__ == '__main__':
    csv = 'ArticlesByYearWithCommonWords/NewYorkTimesArticles2020-CommonWords.csv'
    df = pd.read_csv(csv)
    df.drop_duplicates(subset='webURL', keep=False, inplace=True)
    df.webURL.progress_apply(add_to_forest)
    # for index, words in freq_words.iteritems():
    #     words = ast.literal_eval(words)
    #     min_hash = make_min_hash(words)
    #     forest.add(f'{index}', min_hash)

    forest.index()

    pickle.dump(forest, open("forest.p", "wb"))

    url = 'https://www.nytimes.com/2019/10/02/sports/california-college-athletes-paid-ncaa.html'

    tt = make_set_of_most_common_words(url)
    query = make_min_hash(tt)
    result = forest.query(query, 3)
    print(result)
