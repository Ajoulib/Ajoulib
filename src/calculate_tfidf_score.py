import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer


def calculate_tfidf_score(file_path, threshold):
    try:
        # 데이터 불러오기
        df = pd.read_csv(file_path)

        # 'INTRO'와 'TB' 컬럼 결합하여 텍스트 데이터 생성
        text_data = df['INTRO'].astype(str) + " " + df['TB'].astype(str)

        # TF-IDF 변환기 초기화
        vectorizer = TfidfVectorizer()
        tfidf_matrix = vectorizer.fit_transform(text_data)

        # 단어 목록과 TF-IDF 점수를 데이터프레임으로 변환
        tfidf_df = pd.DataFrame(tfidf_matrix.toarray(), columns=vectorizer.get_feature_names_out())

        # 임계값 이상인 항목만 보존 및 0.0인 항목 제외
        tfidf_df = tfidf_df.map(lambda x: x if x >= threshold else 0)
        tfidf_df = tfidf_df.loc[:, (tfidf_df != 0).any(axis=0)]

        # 데이터프레임을 'keyword: tfidf score' 형태로 변환 및 정렬
        tfidf_scores = pd.DataFrame(tfidf_df.sum(), columns=['tfidf_score']).reset_index()
        tfidf_scores.rename(columns={'index': 'keyword'}, inplace=True)
        tfidf_scores = tfidf_scores[tfidf_scores['tfidf_score'] > 0].sort_values(by='tfidf_score', ascending=False)

        print("[SUCCESS] TF-IDF scores saved to CSV successfully")
        return tfidf_scores

    except Exception as e:
        print(f"[ERROR] Error in calculate_tfidf_score_and_save_to_csv function: {e}")
