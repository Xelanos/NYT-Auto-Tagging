import os
import time
import requests
import pandas as pd

API_KEY = 'KrErdMVh5NdWBAqJK5HN4uRRRFFBAlWt'


def main():
    for year in range(2014, 2016):
        months = 13
        if year == 2020: months = 4
        for month in range(1, months):
            r = requests.get(f'https://api.nytimes.com/svc/archive/v1/{year}/{month}.json?api-key={API_KEY}')
            docs = r.json()['response']['docs']
            articles_df = pd.DataFrame(docs)
            articles_df = preprocess_articles_dataframe(articles_df)
            articles_df.to_csv(os.path.join(f'Articles{year}/', f'ArticlesNYT{year}-{month}.csv'), index=False)
            time.sleep(6)


def preprocess_articles_dataframe(df):
    '''Preprocesses the articles' dataframe.'''

    df.reset_index(inplace=True, drop=True)
    df.drop(['uri'], axis=1, inplace=True, errors='ignore')
    df.drop(['byline'], axis=1, inplace=True, errors='ignore')
    df.drop(['headline'], axis=1, inplace=True, errors='ignore')
    df = df.rename(
        columns={'_id': 'articleID', 'document_type': 'documentType',
                 'new_desk': 'newDesk', 'print_page': 'printPage',
                 'pub_date': 'pubDate',
                 'section_name': 'sectionName',
                 'type_of_material': 'typeOfMaterial',
                 'web_url': 'webURL', 'word_count': 'articleWordCount'})

    if 'printPage' in df.columns:
        df.printPage.fillna(0, inplace=True)
        df.printPage.replace('', 0, inplace=True)
        df.printPage.replace('21`', '21', inplace=True)
        df.printPage.replace('\d+[A-Z]', '0', regex=True, inplace=True)
        df.printPage.replace('[A-Z]\d+', '0', regex=True, inplace=True)
    else:
        df['printPage'] = 0

    if 'sectionName' in df.columns:
        df.sectionName.fillna('Unknown', inplace=True)
    else:
        df['sectionName'] = 'Unknown'

    if 'newDesk' in df.columns:
        df.newDesk.fillna('Unknown', inplace=True)
    else:
        df['newDesk'] = 'Unknown'

    if 'typeOfMaterial' in df.columns:
        df.typeOfMaterial.fillna('Unknown', inplace=True)
    else:
        df['typeOfMaterial'] = 'Unknown'

    df.keywords = df.keywords.apply(
        lambda keywords: [keyword['value'] for keyword in keywords])

    if 'multimedia' in df.columns:
        df.multimedia = df.multimedia.apply(lambda x: len(x))
    else:
        df['multimedia'] = 0

    if 'pubDate' in df.columns:
        df.pubDate = pd.to_datetime(df.pubDate, errors='coerce')

    # Specify dtypes:
    df.articleID = df.articleID.astype('category')
    df.documentType = df.documentType.astype('category')
    df.newDesk = df.newDesk.astype('category')
    df.printPage = df.printPage.astype('int32')
    df.sectionName = df.sectionName.astype('category')
    df.source = df.source.astype('category')
    df.typeOfMaterial = df.typeOfMaterial.astype('category')
    df.webURL = df.webURL.astype('category')
    return df

if __name__ == '__main__':
    main()