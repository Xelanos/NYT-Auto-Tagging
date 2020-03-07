
import ast

import pandas as pd



df = pd.read_csv('NewYorkTimesArticles2020sWithFrequentWords.csv')


all_frequent_words = set()
all_docs = []
for ind, row in df.iterrows():
    all_docs.append(ind)
    frequent_words_list  = ast.literal_eval(row['frequent_words'])
    if (ind%100==0):
        print(ind)
    for word in frequent_words_list:
        all_frequent_words.add(word)





df_of_articles_and_freq_words = pd.DataFrame(columns=list(all_frequent_words),index= all_docs)

print("before sedond loop")

for ind, row in df.iterrows():
    print(ind)
    list_of_zero_one = [None]*len(all_frequent_words)
    frequent_words_list = ast.literal_eval(row['frequent_words'])
    for word in range(len(all_frequent_words)):
        if word in frequent_words_list:
            list_of_zero_one[word] =1
        else:
            list_of_zero_one[word] =0

    df_of_articles_and_freq_words.loc[ind] = list_of_zero_one


print (df_of_articles_and_freq_words.head(10))




