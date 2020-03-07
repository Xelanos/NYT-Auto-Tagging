from datasketch import  MinHash, MinHashLSHForest
import pandas as pd


class MinLSHModel():
    def __init__(self, csv):
        self.__csv = pd.read_csv(csv)
