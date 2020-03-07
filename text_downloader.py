from multiprocessing.pool import Pool
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import requests


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