from src.remove_stopword import remove_stopword
from src.calculate_tf_score import calculate_tf
from src.map_keywords_from_tf import map_keywords_from_tf
from src.calculate_tfidf_score import calculate_tfidf_score
from src.make_dataframe_for_recommend import make_dataframe_for_recommend

import os
import glob
import pandas as pd

TF_SCORE_THRESHOLD = 0.02
TFIDF_SCORE_THRESHOLD = 0.1

DATA_DIR = os.path.join(os.getcwd(), 'data')
ORIGINAL_DIR = os.path.join(DATA_DIR, 'original_datas')
STOPWORDS_DIR = os.path.join(DATA_DIR, 'stopwords_removed_datas')
TF_SCORE_DIR = os.path.join(DATA_DIR, 'tf_score_datas')
TFIDF_SCORE_DIR = os.path.join(DATA_DIR, 'tfidf_score_datas')
KEYWORD_DIR = os.path.join(DATA_DIR, 'keywords_mapping_datas')
RECOMMENDATION_DIR = os.path.join(DATA_DIR, 'for_recommendation_datas')

# Create directories if they don't exist
os.makedirs(STOPWORDS_DIR, exist_ok=True)
os.makedirs(TF_SCORE_DIR, exist_ok=True)
os.makedirs(TFIDF_SCORE_DIR, exist_ok=True)
os.makedirs(KEYWORD_DIR, exist_ok=True)
os.makedirs(RECOMMENDATION_DIR, exist_ok=True)

if __name__ == "__main__":
    original_csv_files = glob.glob(os.path.join(ORIGINAL_DIR, "*original*.csv"))
    all_keywords = set()

    for file in original_csv_files:
        try:
            print(f"Processing {file}")

            df = pd.read_csv(file)
            df.dropna(subset=['INTRO', 'TB'], inplace=True)

            # Stopwords Removal
            stopwords_removed_df = remove_stopword(df)
            stopwords_file = os.path.join(STOPWORDS_DIR, os.path.basename(file).replace('original.csv', 'stopwords_removed.csv'))
            stopwords_removed_df.to_csv(stopwords_file)

            # TF Score Calculation
            tf_df = calculate_tf(stopwords_file, TF_SCORE_THRESHOLD)
            tf_score_file = os.path.join(TF_SCORE_DIR, os.path.basename(file).replace('original.csv', 'tf_score.csv'))
            tf_df.to_csv(tf_score_file)

            # TF-IDF Score Calculation
            tfidf_df = calculate_tfidf_score(stopwords_file, TFIDF_SCORE_THRESHOLD)
            tfidf_score_file = os.path.join(TFIDF_SCORE_DIR, os.path.basename(file).replace('original.csv', 'tfidf_score.csv'))
            tfidf_df.to_csv(tfidf_score_file)

            # Keyword Mapping
            keywords_df = map_keywords_from_tf(tf_score_file)
            keyword_mapping_file = os.path.join(KEYWORD_DIR, os.path.basename(file).replace('original.csv', 'keyword_mapping.csv'))
            keywords_df.to_csv(keyword_mapping_file)

            # Extract new keywords from TF-IDF DataFrame
            new_keywords = tfidf_df['keyword'].unique()
            all_keywords.update(new_keywords)

            # Recommendation DataFrame Creation
            recommendation_df = make_dataframe_for_recommend(file, tf_score_file)
            recommendation_file = os.path.join(RECOMMENDATION_DIR, os.path.basename(file).replace('original.csv', 'for_recommendation.csv'))
            recommendation_df.to_csv(recommendation_file)
        except Exception as e:
            print(f"[Error] Error occurred while processing {file}: {str(e)}")
            continue

    # Save all extracted keywords
    keywords_df = pd.DataFrame(sorted(all_keywords), columns=['Keyword'])
    keywords_df.to_csv(os.path.join(DATA_DIR, 'total_keywords.csv'), index=False)
