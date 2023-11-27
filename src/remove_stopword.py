from konlpy.tag import Komoran
import pandas as pd


def remove_stopword(file_path):
    try:
        komoran = Komoran()

        # raw csv load
        csv = pd.read_csv(file_path)

        csv['INTRO'] = csv['INTRO'].apply(lambda x: komoran.nouns(x))
        csv['TB'] = csv['TB'].apply(lambda x: komoran.nouns(x))

        # export preprocessing csv
        print("[SUCCESS] remove_stopword function executed successfully")
        return csv

    except Exception as e:
        print(f"[ERROR] Error in remove_stopword function: {e}")
