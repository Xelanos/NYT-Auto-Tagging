from datasketch import MinHashLSHForest, MinHash
import pandas as pd
import pickle
import re
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from nltk.stem.wordnet import WordNetLemmatizer



class AutoTag():

    def __init__(self, num_permutation=60):
        self.__num_permutation = num_permutation
        self.__forest = MinHashLSHForest(self.__num_permutation)
        self.__lem = WordNetLemmatizer()
        stop_words = set(stopwords.words("english"))
        stop_words.add('—')
        stop_words.add('And')
        self.__stop_words = stop_words

    def fit(self, csv):
        df = pd.read_csv(csv)
        df.drop_duplicates(subset='webURL', keep=False, inplace=True)
        df.dropna(inplace=True)
        for index, row in df.iterrows():
            min_hash = self.make_min_hash(self.make_clean_words_list(row['Text']))
            self.__forest.add(row['webURL'], min_hash)
            if index % 100 == 0 :print(index)
        self.__forest.index()


    def make_clean_words_list(self, text):
        text = re.sub('[^a-zA-Z]', ' ', text)

        #Convert to lowercase
        text = text.lower()

        #remove tags
        text=re.sub("&lt;/?.*?&gt;"," &lt;&gt; ",text)

        # remove special characters and digits
        text=re.sub("(\\d|\\W)+"," ",text)

        ##Convert to list from string
        text = text.split()

        ##Stemming
        ps=PorterStemmer()
        #Lemmatisation
        lem = WordNetLemmatizer()
        text = [lem.lemmatize(word) for word in text if not word in
                                                            self.__stop_words]

        return text


    def predict(self, text, num_of_niebhors):
        #TODO : change results into tags
        query = self.make_min_hash(self.make_clean_words_list(text))
        return self.__forest.query(query, num_of_niebhors)




    def make_min_hash(self,words):
        min_hash = MinHash(self.__num_permutation)
        for word in words:
            min_hash.update(word.encode('utf8'))
        return min_hash


    def load_trained_model(self, trained_model_file_name):
        self.__forest = pickle.load(open(trained_model_file_name), 'rb')

    def save_model(self, file_name):
        pickle.dump(self.__forest, open(file_name, 'wb'))

