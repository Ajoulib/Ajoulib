from konlpy.tag import Komoran
from sklearn.feature_extraction.text import CountVectorizer
import pandas as pd
import numpy as np
import os
from src.preprocessing.get_word_similarity import similarity
from src.preprocessing.searchingbook import bookkeyword


def remove_stopword(df):
    try:
        komoran = Komoran()

        # Function to process each text entry
        def process_text(text):
            try:
                # Normalize and/or replace line breaks
                normalized_text = text.replace('\r\n', ' ').replace('\n', ' ')
                return komoran.nouns(normalized_text)
            except Exception as e:
                print(f"Error processing text: {e}")
                return []  # Return an empty list in case of an error

        df['INTRO'] = df['INTRO'].apply(process_text)
        df['TB'] = df['TB'].apply(process_text)

        print("[SUCCESS] remove_stopword function executed successfully")
        return df

    except Exception as e:
        print(f"[ERROR] Global error in remove_stopword function: {e}")


def calculate_tf(file_path, min_tf_score=0.05):
    try:
        df = pd.read_csv(file_path)

        # Convert strings of words to lists of words
        df['INTRO'] = df['INTRO'].apply(eval)

        # Convert lists of words to strings
        introduction_texts = df['INTRO'].apply(lambda x: ' '.join(x))

        vectorizer = CountVectorizer()
        count_matrix = vectorizer.fit_transform(introduction_texts)

        # Use numpy array for computations
        count_array = count_matrix.toarray()

        # Calculate term frequency (TF)
        tf_matrix = count_array / np.sum(count_array, axis=1)[:, None]
        tf_df = pd.DataFrame(tf_matrix, columns=vectorizer.get_feature_names_out(), index=df.index)

        # Filter TF DataFrame
        filtered_tf_df = tf_df.loc[:, (tf_df > min_tf_score).any(axis=0)]

        print("[SUCCESS] calculate_tf function executed successfully")
        return filtered_tf_df

    except Exception as e:
        print(f"[ERROR] Error in calculate_tf function: {e}")


# 입력받은 책 정보가 아래에 들어가야함.
def recommend_by_bookinfo(title, directory='data/for_recommendation_datas'):
    book_info = bookkeyword(title)

    book_info = pd.DataFrame([book_info])
    book_info = remove_stopword(book_info)

    if not book_info['INTRO'][0]:
        return None

    # 임시로 sample.csv로 저장
    book_info.to_csv('./sample.csv')
    book_keywords = calculate_tf('./sample.csv', 0)
    os.remove('./sample.csv')

    top_3_columns = book_keywords.mean().nlargest(3).index.tolist()

    # 모든 추천 결과를 저장할 딕셔너리 초기화
    all_recommendations = {}

    # 특정 디렉토리 내의 모든 CSV 파일을 순회
    for filename in os.listdir(directory):
        if filename.endswith('.csv'):
            filepath = os.path.join(directory, filename)
            df = pd.read_csv(filepath)
            df.drop_duplicates(subset=['Title'], keep='first', inplace=True)

            # 각 파일에 대해 추천 로직 실행
            book_list_dict_rank1 = {}
            book_list_dict_rank2 = {}
            book_list_dict_rank3 = {}

            for index, row in df.iterrows():
                parsed_list = eval(row['Keywords'])
                for i in range(3):
                    for j in range(5):
                        if parsed_list[j] == top_3_columns[i]:
                            if i == 0:
                                book_list_dict_rank1[row['Title']] = j+1
                            elif i == 1:
                                book_list_dict_rank2[row['Title']] = j+1
                            else:
                                book_list_dict_rank3[row['Title']] = j+1

            # 각 키워드별로 추천된 책 목록 정렬
            book_list_dict_rank1 = sorted(book_list_dict_rank1.items(), key=lambda x: x[1], reverse=False)
            book_list_dict_rank2 = sorted(book_list_dict_rank2.items(), key=lambda x: x[1], reverse=False)
            book_list_dict_rank3 = sorted(book_list_dict_rank3.items(), key=lambda x: x[1], reverse=False)

            # 추천 결과 병합
            all_recommendations[filename.replace('.csv', '')] = {
                top_3_columns[0]: [item[0] for item in book_list_dict_rank1],
                top_3_columns[1]: [item[0] for item in book_list_dict_rank2],
                top_3_columns[2]: [item[0] for item in book_list_dict_rank3]
            }

    return all_recommendations
