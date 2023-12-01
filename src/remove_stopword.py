from konlpy.tag import Komoran
import pandas as pd


def remove_stopword(df):
    try:
        komoran = Komoran()

        df['INTRO'] = df['INTRO'].apply(lambda x: komoran.nouns(x))
        df['TB'] = df['TB'].apply(lambda x: komoran.nouns(x))

        # Return the modified DataFrame
        print("[SUCCESS] remove_stopword function executed successfully")
        return df

    except Exception as e:
        print(f"[ERROR] Error in remove_stopword function: {e}")
