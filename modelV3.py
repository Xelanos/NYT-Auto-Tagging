from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from nltk.stem.wordnet import WordNetLemmatizer
from scipy.sparse import coo_matrix
import pandas as pd
import pickle
import re

from nltk.corpus import stopwords
stop_words = set(stopwords.words('english'))
stop_words.add('—')
stop_words.add('And')


class AutoTagNLP:

    def __init__(self):
        stop_words = set(stopwords.words("english"))
        stop_words.add('—')
        stop_words.add('And')
        self.__stop_words = stop_words
        self.__emded_model = CountVectorizer(max_df=0.8, stop_words=stop_words, max_features=20000, ngram_range=(1, 3))
        self.__transform_model = TfidfTransformer(smooth_idf=True, use_idf=True)


    def fit(self, csv):
        df = pd.read_csv(csv)
        df.drop_duplicates(subset='webURL', keep=False, inplace=True)
        df.dropna(inplace=True)
        all_texts = []
        total = df.shape[0]
        for index, row in df.iterrows():
            clean_text = ' '.join(self.make_clean_words_list(row['Text']))
            all_texts.append(clean_text)
            if index % 2000 == 0 : print(f'{index}/{total}')
        embed = self.__emded_model.fit_transform(all_texts)
        print('finished training embed')
        self.__transform_model.fit(embed)


    def load_trained_model(self, emded_model_file_name, transform_model_file_name):
        self.__emded_model = pickle.load(open(emded_model_file_name, 'rb'))
        self.__transform_model = pickle.load(open(transform_model_file_name, 'rb'))

    def save_model(self, file_name):
        pickle.dump(self.__emded_model, open(f'{file_name}_emded.pic', 'wb'))
        pickle.dump(self.__transform_model, open(f'{file_name}_transform.pic', 'wb'))


    def predict(self, text, num_tags=10):
        clean_text = ' '.join(self.make_clean_words_list(text))
        clean_text = [clean_text]
        embed = self.__emded_model.transform(clean_text)
        transform = self.__transform_model.transform(embed)

        # Make coo sparse matrix and sort it
        sparse_matrix_coo = transform.tocoo()
        sorted_coo = sorted(zip(sparse_matrix_coo.col, sparse_matrix_coo.data), key=lambda x: (x[1], x[0]), reverse=True)

        # We want num_tags most most frequent
        sorted_coo = sorted_coo[:num_tags]

        # word index and corresponding tf-idf score
        scores = []
        features = []
        for idx, score in sorted_coo:
            scores.append(round(score, 3))
            features.append(self.__emded_model.get_feature_names()[idx])

        # Pretiify results
        results = {}
        for idx in range(len(features)):
            results[features[idx]] = scores[idx]

        return results


    def make_clean_words_list(self, text):
        text = re.sub('[^a-zA-Z]', ' ', text)

        #Convert to lowercase
        text = text.lower()

        #remove tags
        text = re.sub("&lt;/?.*?&gt;"," &lt;&gt; ",text)

        # remove special characters and digits
        text = re.sub("(\\d|\\W)+"," ",text)

        #Lemmatisation
        text = text.split()
        lem = WordNetLemmatizer()
        text = [lem.lemmatize(word) for word in text if not word in self.__stop_words]

        return text
