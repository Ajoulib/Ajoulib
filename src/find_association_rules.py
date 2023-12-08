import os
import pandas as pd
from mlxtend.preprocessing import TransactionEncoder
from mlxtend.frequent_patterns import apriori, association_rules

PARENT_DIR = os.path.dirname(os.getcwd())
DATA_DIR = os.path.join(PARENT_DIR, 'data')
CSV_DIR = os.path.join(DATA_DIR, 'for_recommendation_datas')

dfs = []

if __name__ == "__main__":
    # Loop through each file in the directory and append to the list
    for filename in os.listdir(CSV_DIR):
        if filename.endswith('.csv'):
            file_path = os.path.join(CSV_DIR, filename)
            df = pd.read_csv(file_path)
            df['Keywords'] = df['Keywords'].apply(eval)
            dfs.append(df)

    # Combine all dataframes into one
    combined_df = pd.concat(dfs, ignore_index=True)

    # Extracting the 'Keywords' column for Apriori algorithm
    data = combined_df['Keywords'].tolist()

    # Convert data for Apriori
    te = TransactionEncoder()
    te_ary = te.fit(data).transform(data)
    df = pd.DataFrame(te_ary, columns=te.columns_)

    # Find frequent itemsets
    frequent_itemsets = apriori(df, min_support=0.001, use_colnames=True, max_len=None)

    # Generate association rules based on confidence
    rules = association_rules(frequent_itemsets, metric="confidence", min_threshold=0.7)

    # Converting frozenset to string
    rules['antecedents'] = rules['antecedents'].apply(lambda x: ', '.join(list(x)))
    rules['consequents'] = rules['consequents'].apply(lambda x: ', '.join(list(x)))

    # Filter for only the keywords in the rules
    rules_keywords = rules[['antecedents', 'consequents']]

    # Save the rules as a CSV file
    output_file = os.path.join(DATA_DIR, 'association_rules.csv')
    rules_keywords.to_csv(output_file, index=False)

    print(f"Association rules saved to: {output_file}")
