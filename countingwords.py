import requests
from bs4 import BeautifulSoup
import nltk
# nltk.download()
from nltk.corpus import stopwords
from collections import Counter
from sklearn.metrics import jaccard_similarity_score
from tqdm import tqdm

import pandas as pd

import time

stop_words = set(stopwords.words('english'))
stop_words.add('—')
stop_words.add('And')
tqdm.pandas()




# url = 'https://www.nytimes.com/2017/03/31/theater/hairy-ape-review-bobby-cannavale-eugene-oneill.html'
# url1 = "https://www.nytimes.com/2018/04/24/dining/noma-restaurant-copenhagen.html"
# trunp_url="https://www.nytimes.com/2018/04/24/world/europe/trump-macron-iran-climate.html"
# trunp_2 = "https://www.nytimes.com/2018/04/23/opinion/supreme-court-travel-ban-trump.html"

def extract_text(url):
    text = ''
    try:
        html = requests.get(url)
        soup = BeautifulSoup(html.content, 'html.parser')
    except requests.exceptions.HTTPError as e:
        print(e)
        print(f'ERROR IN URL:{url}')

    paragraphs = soup.find_all("p", class_="css-exrw3m evys1bk0")
    for p in paragraphs:
        text += p.text

    return text


def make_set_of_most_common_words(url, num_of_commom_words=50):
    text = extract_text(url)

    # text = " i like big buts and i cannot lie, your other brothers can't deny"
    # split() returns list of all the words in the string
    split_it = text.split()



    stop_filtered = [w for w in split_it if not w in stop_words]

    # Pass the split_it list to instance of Counter class.
    counter = Counter(stop_filtered)

    # most_common() produces k frequently encountered
    # input values and their respective counts.



    most_occur = counter.most_common(num_of_commom_words)

    most_occur_words = [x[0] for x in most_occur]

    # print(set(most_occur_words))
    return most_occur_words



# A = make_set_of_most_common_words(url1)
# B = make_set_of_most_common_words(trunp_2)



def grade_of_jaccard_similarity (A,B):
    inters = A.intersection(B)
    union = A.union(B)
    jacc = len(inters)/len(union)
    return jacc


#
# print (grade_of_jaccard_similarity(A,B))


def return_jaccard_score_from_2_urls(url1,url2):
    set1 = make_set_of_most_common_words(url1)
    set2 = make_set_of_most_common_words(url2)
    return grade_of_jaccard_similarity(set1,set2)




def save_file_with_frequent_words(origin_csv):
    df = pd.read_csv(origin_csv)

    # most_common = []
    #
    #
    # for ind, row in df.iterrows():
    #     URL = row['webURL']
    #
    #     most_common.append(make_set_of_most_common_words(URL))
    #
    #     if (ind%500==0):
    #         print (ind)
    #         print (time.time()-start)


    df['frequent_words'] = df['webURL'].progress_apply(make_set_of_most_common_words)


    # print (df['webURL'].to_string())
    # df['frequentwords'] = make_set_of_most_common_words(df['webURL'].to_string(index=False))
    # print (df.head(4))
    df.to_csv(r'NewYorkTimesArticlesWithFrequentWords.csv')

if __name__=="__main__":

    csv = "ArticlesNYT2020-3.csv"
    start = time.time()
    save_file_with_frequent_words(csv)
