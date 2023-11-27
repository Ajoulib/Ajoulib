from src.remove_stopword import remove_stopword
from src.calculate_tf_score import calculate_tf
from src.map_keywords_from_tf import map_keywords_from_tf

import os


DATA_DIR = os.path.join(os.getcwd(), "data")

# 키워드 분류를 위한 최소값
MIN_TF_SCORE = 0.02


if __name__ == "__main__":
    # 크롤링을 통한 데아터셋 생성

    # 데이터 불용어 처리 by 김시원
    book_data_file_path = os.path.join(DATA_DIR, "original_book_data.csv")
    bood_data_stopwords_removed_df = remove_stopword(book_data_file_path)
    bood_data_stopwords_removed_df.to_csv(f'{DATA_DIR}/book_data_stopwords_removed.csv')

    # TF를 통한 키워드 추출 by 노수인
    book_data_stopwords_removed_file_path = os.path.join(DATA_DIR, "book_data_stopwords_removed.csv")
    tf_df = calculate_tf(book_data_stopwords_removed_file_path, MIN_TF_SCORE)
    tf_df.to_csv(f'{DATA_DIR}/book_data_tf_score.csv')

    # TF Score 파일을 기반으로 도서별 키워드 매핑 by 노수인
    book_daat_tf_score_file_path = os.path.join(DATA_DIR, "book_data_tf_score.csv")
    keywords_df = map_keywords_from_tf(book_daat_tf_score_file_path)
    keywords_df.to_csv(f'{DATA_DIR}/book_data_keyword_mapping.csv')
