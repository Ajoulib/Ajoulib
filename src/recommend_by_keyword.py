import os
import pandas as pd
from src.preprocessing.get_word_similarity import similarity


def recommend_by_keyword(input_keyword, directory='data/for_recommendation_datas'):
    # Load total keywords
    total_keywords = pd.read_csv('data/total_keywords.csv')
    total_keywords = total_keywords['Keyword'].tolist()

    # Load association rules
    association_rules = pd.read_csv('data/association_rules.csv')
    associated_keywords = get_associated_keywords(input_keyword, association_rules)

    # Calculate similarity for each keyword
    input_output_dict = {}
    for i in total_keywords:
        res = similarity(i, input_keyword)
        input_output_dict[i] = res

    # Sort keywords by similarity and select top 3
    input_output_dict = sorted(input_output_dict.items(), key=lambda x: x[1], reverse=True)
    similarity_top3 = input_output_dict[:3] if len(input_output_dict) > 3 else input_output_dict

    # Add associated keywords to the top of the list
    for associated_keyword in associated_keywords:
        similarity_top3.insert(0, (associated_keyword, 1.0))

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

            # Find books for each of the top similar keywords
            for keyword, _ in similarity_top3:
                books_for_keyword = df[df['Keywords'].apply(lambda x: keyword in eval(x))]['Title'].tolist()
                if books_for_keyword:
                    if category_name not in category_recommendations:
                        category_recommendations[category_name] = {}
                    category_recommendations[category_name][keyword] = books_for_keyword

    print(category_recommendations)
    return category_recommendations


def get_associated_keywords(input_keyword, association_rules):
    # Initialize list to hold associated keywords
    associated_keywords = []

    # Iterate over each row in the association_rules dataframe
    for index, row in association_rules.iterrows():
        # Split antecedents into individual keywords
        antecedents = row['antecedents'].split(', ')
        # Check if input_keyword is in the list of antecedents
        if input_keyword in antecedents:
            # Add the consequents to the associated_keywords list
            associated_keywords.extend(row['consequents'].split(', '))

    # Remove duplicates from the list
    associated_keywords = list(set(associated_keywords))

    print(associated_keywords)
    return associated_keywords
