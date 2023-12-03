from src.remove_stopword import remove_stopword
from src.calculate_tf_score import calculate_tf
from src.map_keywords_from_tf import map_keywords_from_tf
from src.calculate_tfidf_score import calculate_tfidf_score
from src.make_dataframe_for_recommend import make_dataframe_for_recommend

import os
import glob
import pandas as pd


DATA_DIR = os.path.join(os.getcwd(), "data")

# 키워드 분류를 위한 최소값
TF_SCORE_THRESHOLD = 0.02
TFIDF_SCORE_THRESHOLD = 0.1


if __name__ == "__main__":
    # 크롤링을 통한 데아터셋 생성

    # 크롤링한 original 데이터들을 조회하여 전처리 수행
    original_csv_files = glob.glob(os.path.join(DATA_DIR, "*original*.csv"))

    # 전체 키워드 추출을 위한 셋
    all_keywords = set()

    for file in original_csv_files:
        # NaN인 데이터들을 Drop한 뒤 일련의 작업 수행
        df = pd.read_csv(file)
        df.dropna(subset=['INTRO', 'TB'], inplace=True)

        # 데이터 불용어 처리
        stopwords_removed_df = remove_stopword(df)
        stopwords_removed_df.to_csv(file.replace('original.csv', 'stopwords_removed.csv'))

        # TF를 통한 키워드 추출
        file_path = os.path.join(DATA_DIR, file.replace('original.csv', 'stopwords_removed.csv'))
        tf_df = calculate_tf(file_path, TF_SCORE_THRESHOLD)
        tf_df.to_csv(file.replace('original.csv', 'tf_score.csv'))

        # 트렌트 분석을 위해 키워드별 TF-IDF 점수 계산
        file_path = os.path.join(DATA_DIR, file.replace('original.csv', 'stopwords_removed.csv'))
        tfidf_df = calculate_tfidf_score(file_path, TFIDF_SCORE_THRESHOLD)
        tfidf_df.to_csv(file.replace('original.csv', 'tfidf_score.csv'))

        # TF Score 파일을 기반으로 도서별 키워드 매핑
        file_path = os.path.join(DATA_DIR, file.replace('original.csv', 'tf_score.csv'))
        keywords_df = map_keywords_from_tf(file_path)
        keywords_df.to_csv(file.replace('original.csv', 'keyword_mapping.csv'))

        # TF-IDF 데이터프레임 중 키워드만 추출하여 전체 키워드를 별도로 저장
        new_keywords = tfidf_df['keyword'].unique()
        all_keywords.update(new_keywords)
        
        # 추천을 위한 데이터프레임 생성
        tf_file_path = os.path.join(DATA_DIR, file.replace('original.csv', 'tf_score.csv'))
        recommendation_df = make_dataframe_for_recommend(file, tf_file_path)
        recommendation_df.to_csv(file.replace('original.csv', 'for_recommendation.csv'))

    keywords_df = pd.DataFrame(sorted(all_keywords), columns=['Keyword'])
    keywords_df.to_csv(os.path.join(DATA_DIR, 'total_keywords.csv'), index=False)
