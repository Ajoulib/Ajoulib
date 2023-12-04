import pandas as pd
from src.get_word_similarity import similarity

#예시로 입력 키워드를 행복으로 setting
input_keywords = '행복'

total_keywords = pd.read_csv('data/total_keywords.csv')
total_keywords = total_keywords['Keyword'].tolist()

input_output_dict = {}


for i in total_keywords:
    res = similarity(input_keywords, i)
    input_output_dict[i] = res

input_output_dict = sorted(input_output_dict.items(), key=lambda x: x[1], reverse=True)
# print(input_output_dict)

if len(input_output_dict) > 3:
    input_output_dict = dict(input_output_dict[:3])

print(input_output_dict)

# 키워드 입력받았을 경우에 책 추천

top_5_keywords_csv = pd.read_csv('data/for_recommendation_datas/history-culture_data_for_recommendation.csv')
top_5_keywords_csv.drop_duplicates(subset=['Title'], keep='first', inplace=True)
top_5_keywords_csv = top_5_keywords_csv.sort_values(by='Rank', ascending=True)
# top_5_keywords_csv.to_csv('../data/chk.csv')

similarity_top3_list = list(input_output_dict.keys())
print(similarity_top3_list)

book_list_dict_rank1 = {}
book_list_dict_rank2 = {}
book_list_dict_rank3 = {}


for index, row in top_5_keywords_csv.iterrows(): 
    parsed_list = eval(row['Keywords'])
    # print(parsed_list)
    for i in range(3):
        for j in range(5):
            if parsed_list[j] == similarity_top3_list[i]:
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