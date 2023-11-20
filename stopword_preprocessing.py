from konlpy.tag import Komoran
import pandas as pd

komoran = Komoran()
# raw csv load
csv = pd.read_csv("프로젝트_샘플DB_RAW.csv")

csv['Index'] = csv['Index'].apply(lambda x: komoran.nouns(x))
csv['Introduction'] = csv['Introduction'].apply(lambda x: komoran.nouns(x))

# export preprocessing csv
csv.to_csv('프로젝트_샘플DB_불용어_konlp.csv')