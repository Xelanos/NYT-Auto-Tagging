import os
import glob
import pandas as pd

target_folder = os.path.abspath('ArticlesByYear/')

for year in range(2013, 2021):
    os.chdir(f"Articles{year}/")
    extension = 'csv'
    all_filenames = [i for i in glob.glob('*.{}'.format(extension))]
    combined_csv = pd.concat([pd.read_csv(f) for f in all_filenames])
    combined_csv.to_csv(os.path.join(target_folder,f"NewYorkTimesArticles{year}.csv"), index=False, encoding='utf-8-sig')
    os.chdir('..')


os.chdir(target_folder)
extension = 'csv'
all_filenames = [i for i in glob.glob('*.{}'.format(extension))]
combined_csv = pd.concat([pd.read_csv(f) for f in all_filenames])
combined_csv.to_csv(
    os.path.join(target_folder, f"NewYorkTimesArticlesFullDb.csv"),
    index=False, encoding='utf-8-sig')


