from sklearn.feature_extraction.text import CountVectorizer

import pandas as pd
import numpy as np


def calculate_tf(file_path, min_tf_score):
    df = pd.read_csv(file_path)
    introduction_texts = df['INTRO']

    vectorizer = CountVectorizer()
    count_matrix = vectorizer.fit_transform(introduction_texts)

    tf_matrix = count_matrix / np.sum(count_matrix, axis=1)
    tf_df = pd.DataFrame(tf_matrix.toarray(), columns=vectorizer.get_feature_names_out())

    filtered_tf_df = tf_df.loc[:, (tf_df > min_tf_score).any(axis=0)]
    return filtered_tf_df
