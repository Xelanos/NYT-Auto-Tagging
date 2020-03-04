from sklearn.metrics import jaccard_similarity_score
from sklearn.neighbors import KDTree


class Model():

    def __init__(self,
                 distance_metric=jaccard_similarity_score, knn_model=KDTree,
                 k=10):
        self.__knn_model = knn_model
        self.__metric = distance_metric
        self.__k = k
        self.__keywords = None
        self.__knn = None


    def fit(self, articles_vectors, keywords):
        self.__knn = self.__knn_model(articles_vectors, metric=self.__metric)
        self.__keywords = keywords

    def predict(self, article_vectors):
        predictions = []
        for article in article_vectors:
            dist, ind = self.__knn.query(article, self.__k)
            all_keywords = []
            for i in ind:
                keywords = self.__keywords[i]
                for keyword in keywords:
                    all_keywords.append(keyword)
            predictions.append(all_keywords)
        return predictions



