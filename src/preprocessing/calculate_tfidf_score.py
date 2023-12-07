import pandas as pd
import os
from sklearn.feature_extraction.text import TfidfVectorizer


def calculate_tfidf_score(file_path, threshold):
    all_tfidf_scores = pd.DataFrame()  # 누적될 DataFrame 초기화

    try:
        # Load data
        df = pd.read_csv(file_path)

        # Check if 'Year' column exists
        if 'Year' not in df.columns:
            print("[ERROR] 'Year' column not found in the data")
            return

        base_name = os.path.basename(file_path).split('_')[0]

        output_dir = os.path.join(os.getcwd(), 'data', 'tfidf_score_datas', base_name)
        os.makedirs(output_dir, exist_ok=True)

        # Process each year separately
        for year, group in df.groupby('Year'):
            # Create text data by combining 'INTRO' and 'TB' columns
            text_data = group['INTRO'].astype(str) + " " + group['TB'].astype(str)

            # Initialize TF-IDF converter
            vectorizer = TfidfVectorizer()
            tfidf_matrix = vectorizer.fit_transform(text_data)

            # Convert word list and TF-IDF score to data frame
            tfidf_df = pd.DataFrame(tfidf_matrix.toarray(), columns=vectorizer.get_feature_names_out())

            # Keep only items that are above the threshold
            tfidf_df = tfidf_df.map(lambda x: x if x >= threshold else 0)
            tfidf_df = tfidf_df.loc[:, (tfidf_df != 0).any(axis=0)]

            # Convert and sort the data frame into 'keyword: tfidf score' format
            tfidf_scores = pd.DataFrame(tfidf_df.sum(), columns=['tfidf_score']).reset_index()
            tfidf_scores.rename(columns={'index': 'keyword'}, inplace=True)
            tfidf_scores = tfidf_scores[tfidf_scores['tfidf_score'] > 0].sort_values(by='tfidf_score', ascending=False)
            tfidf_scores['Year'] = year  # 년도 정보 추가

            # 누적 DataFrame에 추가
            all_tfidf_scores = pd.concat([all_tfidf_scores, tfidf_scores])

            # Construct the output file name and path
            output_file_name = f"{base_name}_{year}.csv"
            output_file_path = os.path.join(output_dir, output_file_name)

            # Save to CSV in the specified directory
            tfidf_scores.to_csv(output_file_path, index=False)

    except Exception as e:
        print(f"[ERROR] Error in calculate_tfidf_score_and_save_by_year function: {e}")

    print("[SUCCESS] TF-IDF scores function executed successfully")
    return all_tfidf_scores
