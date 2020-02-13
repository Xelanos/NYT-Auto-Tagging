import pandas as pd
import requests

API_KEY = 'KrErdMVh5NdWBAqJK5HN4uRRRFFBAlWt'

from nytcomments import get_articles


get_articles(API_KEY, save=True, page_upper=200)

