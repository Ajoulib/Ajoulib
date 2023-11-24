from src.remove_stopword import remove_stopword
from src.calculate_tf_score import calculate_tf

import pandas as pd
import numpy as np
import os


DATA_DIR = os.path.join(os.getcwd(), "data")


if __name__ == "__main__":
    # 크롤링을 통한 데아터셋 생성

    # 데이터 불용어 처리 by 김시원
    book_data_file_path = os.path.join(DATA_DIR, "original_book_data.csv")
    bood_data_stopwords_removed_df = remove_stopword(book_data_file_path)
    bood_data_stopwords_removed_df.to_csv(f'{DATA_DIR}/book_info_stopwords_removed.csv')

    # TF-IDF를 통한 키워드 추출
    book_data_stopwords_removed_file_path = os.path.join(DATA_DIR, "book_info_stopwords_removed.csv")
    tf_df = calculate_tf(book_data_stopwords_removed_file_path, 0.05)
    tf_df.to_csv(f'{DATA_DIR}/output.csv', index=False)
