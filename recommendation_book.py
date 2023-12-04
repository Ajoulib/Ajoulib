from konlpy.tag import Komoran
from sklearn.feature_extraction.text import CountVectorizer
import pandas as pd
import numpy as np
from src.get_word_similarity import similarity

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
book_info = {
    "Title": "황금종이 1",
    "INTRO": "건축물은 인간의 생각과 세상의 물질이 만나 만들어진 결정체로, 많은 자본이 드는 만큼 여러 사람의 의견이 일치할 때만 완성되는 그 사회의 반영이자 단면이다. 그렇기에 건축물을 보면 당대 사람들이 세상을 읽는 관점, 물질을 다루는 기술 수준, 사회 경제 시스템, 인간에 대한 이해, 꿈꾸는 이상향, 생존을 위한 몸부림 등이 보인다.이 책은 건축가 유현준이 감명받거나 영감을 얻은 30개의 건축물을 소개한다. 이 작품들을 설계한 건축가들은 수백 년 된 전통을 뒤집거나 비트는 혁명적인 생각으로 건축의 새로운 시대를 열었다. 저자는 이 건축물들을 통해 건축 디자인이 무엇인지 배웠다고 해도 과언이 아니라고 말하며, “이 건축물들을 통해 독자들이 세상을 바라보는 또 하나의 시각을 만드는 데 도움이 되기를 바”란다는 말과 함께 건축물들을 소개한다.펼쳐보기",  # 여기에 목차 내용을 추가
    "TB": "여는 글1. 유럽1장. 빌라사보아: 건축은 기계다2장. 퐁피두센터: 건축의 본질은 무엇인가?3장. 루브르 유리 피라미드: 파리의 다보탑과 석가탑4장. 롱샹 성당: 결국 자연으로 돌아간다5장. 라 투레트 수도원: 무림 최고의 비서秘書6장. 피르미니 성당: 성당 진화의 끝판왕7장. 유니테 다비타시옹: 건물 안에 도시를 만들겠다는 야심8장. 독일 국회의사당: 국회의원은 국민보다 아랫사람이다9장. 브루더 클라우스 필드 채플: 빛이 들어오는 동굴 만들기10장. 발스 스파: 땅속에 숨겨진 신전 같은 목욕탕11장. 퀘리니 스탐팔리아: 자연과 대화하는 공간12장. 빌바오 구겐하임 미술관: 물고기를 좇은 건축가의 꿈2. 북아메리카13장. 바이네케 고문서 도서관: 빛이 투과되는 돌14장. 뉴욕 구겐하임 미술관: 미술관이 방일 필요는 없다15장. 시티그룹 센터: 좋은 디자인은 문제 해결의 답이다16장. 허스트 타워: 무엇을 보존할 것인가?17장. 낙수장: 건축이 자연이 될 수는 없을까?18장. 베트남전쟁재향군인기념관: 공간으로 만든 한 편의 영화19장. 더글라스 하우스: 살고 싶은 집20장. 킴벨 미술관: 침묵과 빛 사이에 위치한 건축21장. 소크 생물학 연구소: 채움보다 더 위대한 비움22장. 도미누스 와이너리: 아름다움은 무엇인가?23장. 해비타트 67: 그리스 언덕을 캐나다에 만들다3. 아시아24장. 윈드 타워: 실체는 무엇인가25장. 빛의 교회: 전통 건축의 파격적 재해석26장. 아주마 하우스: 권투 선수 출신 건축가가 자연을 대하는 방법27장. 데시마 미술관: 두꺼비집 미술관28장. CCTV 본사 빌딩: 21세기 고인돌, 과시 건축의 끝판왕29장. 홍콩 HSBC 빌딩: 제약은 새로운 창조의 어머니30장. 루브르 아부다비: 쇠로 만든 오아시스닫는 글주석도판 출처펼쳐보기",  # 여기에 소개 내용을 추가
}

book_info = pd.DataFrame([book_info])
book_info = remove_stopword(book_info)
# 임시로 sample.csv로 저장
book_info.to_csv('./sample.csv')
book_keywords = calculate_tf('./sample.csv', 0)

# print(book_info)
top_3_columns = book_keywords.mean().nlargest(3).index.tolist()
print(top_3_columns)

# 키워드 입력받았을 경우에 책 추천

top_5_keywords_csv = pd.read_csv('data/for_recommendation_datas/history-culture_data_for_recommendation.csv')
top_5_keywords_csv.drop_duplicates(subset=['Title'], keep='first', inplace=True)
top_5_keywords_csv = top_5_keywords_csv.sort_values(by='Rank', ascending=True)
# top_5_keywords_csv.to_csv('../data/chk.csv')

book_list_dict_rank1 = {}
book_list_dict_rank2 = {}
book_list_dict_rank3 = {}


for index, row in top_5_keywords_csv.iterrows(): 
    parsed_list = eval(row['Keywords'])
    # print(parsed_list)
    for i in range(3):
        for j in range(5):
            if parsed_list[j] == top_3_columns[i]:
                if i == 0:
                    book_list_dict_rank1[row['Title']] = j+1
                elif i == 1:
                    book_list_dict_rank2[row['Title']] = j+1
                else:
                    book_list_dict_rank3[row['Title']] = j+1

book_list_dict_rank1 = sorted(book_list_dict_rank1.items(), key=lambda x: x[1], reverse=False)
book_list_dict_rank2 = sorted(book_list_dict_rank2.items(), key=lambda x: x[1], reverse=False)
book_list_dict_rank3 = sorted(book_list_dict_rank3.items(), key=lambda x: x[1], reverse=False)

book_recommend_keywordRank1 = [item[0] for item in book_list_dict_rank1]
book_recommend_keywordRank2 = [item[0] for item in book_list_dict_rank2]
book_recommend_keywordRank3 = [item[0] for item in book_list_dict_rank3]

print(book_recommend_keywordRank1)
print(book_recommend_keywordRank2)
print(book_recommend_keywordRank3)