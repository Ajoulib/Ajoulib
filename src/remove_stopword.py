from konlpy.tag import Komoran
import pandas as pd


def remove_stopword(file_path):
    komoran = Komoran()

    # raw csv load
    csv = pd.read_csv(file_path)

    csv['INTRO'] = csv['INTRO'].apply(lambda x: komoran.nouns(x))
    csv['TB'] = csv['TB'].apply(lambda x: komoran.nouns(x))

    # export preprocessing csv
    return csv
    csv.to_csv('book_info_stopwords_removed.csv')
