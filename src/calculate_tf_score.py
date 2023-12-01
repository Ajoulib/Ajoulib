from sklearn.feature_extraction.text import CountVectorizer
import pandas as pd
import numpy as np


def calculate_tf(file_path, min_tf_score):
    try:
        df = pd.read_csv(file_path)
        df.set_index('Title', inplace=True)

        # Convert lists of words to strings
        introduction_texts = df['INTRO'].apply(lambda x: ' '.join(eval(x)))

        vectorizer = CountVectorizer()
        count_matrix = vectorizer.fit_transform(introduction_texts)

        tf_matrix = count_matrix / np.sum(count_matrix, axis=1)
        tf_df = pd.DataFrame(tf_matrix.toarray(), columns=vectorizer.get_feature_names_out(), index=df.index)

        filtered_tf_df = tf_df.loc[:, (tf_df > min_tf_score).any(axis=0)]

        print("[SUCCESS] calculate_tf function executed successfully")
        return filtered_tf_df

    except Exception as e:
        print(f"[ERROR] Error in calculate_tf function: {e}")
