import os
import pandas as pd
from src.preprocessing.get_word_similarity import similarity


def recommend_by_keyword(input_keyword, directory='data/for_recommendation_datas'):
    # Load keywords
    total_keywords = pd.read_csv('data/total_keywords.csv')
    total_keywords = total_keywords['Keyword'].tolist()

    # Calculate similarity for each keyword
    input_output_dict = {}
    for i in total_keywords:
        res = similarity(input_keyword, i)
        input_output_dict[i] = res

    # Sort keywords by similarity and select top 3
    input_output_dict = sorted(input_output_dict.items(), key=lambda x: x[1], reverse=True)
    similarity_top3 = input_output_dict[:3] if len(input_output_dict) > 3 else input_output_dict

    # Initialize a dictionary to hold the recommended books for each category
    category_recommendations = {}

    # Iterate over each CSV file in the directory
    for filename in os.listdir(directory):
        if filename.endswith('.csv'):
            filepath = os.path.join(directory, filename)
            df = pd.read_csv(filepath)
            df.drop_duplicates(subset=['Title'], keep='first', inplace=True)

            # Extract category name from filename or other logic
            category_name = filename.replace('.csv', '')

            # Find books for each of the top 3 similar keywords
            for keyword, _ in similarity_top3:
                books_for_keyword = df[df['Keywords'].apply(lambda x: keyword in eval(x))]['Title'].tolist()
                if books_for_keyword:
                    if category_name not in category_recommendations:
                        category_recommendations[category_name] = {}
                    category_recommendations[category_name][keyword] = books_for_keyword

    print(category_recommendations)
    return category_recommendations
