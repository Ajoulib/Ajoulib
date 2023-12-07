import pandas as pd


def make_dataframe_for_recommend(file_path, tf_file_path):
    try:
        original_df = pd.read_csv(file_path)
        tf_df = pd.read_csv(tf_file_path)

        recommendation_data = []

        for index, row in tf_df.iterrows():
            book_name = row['Title']  # Assuming 'Title' column has the book name
            top_keywords = row.drop('Title').sort_values(ascending=False).head(5).index.tolist()

            # Find the corresponding rank in the original data
            original_row = original_df.loc[original_df['Title'] == book_name]
            rank = original_row['Rank'].iloc[0]
            year = original_row['Year'].iloc[0]
            
            recommendation_data.append({
                'Year': year,
                'Title': book_name,
                'Rank': rank,
                'Keywords': top_keywords
            })

        recommendation_df = pd.DataFrame(recommendation_data)

        print("[SUCCESS] Dataframe for recommendation saved to CSV successfully")
        return recommendation_df

    except Exception as e:
        print(f"[ERROR] Error in make_dataframe_for_recommend function: {e}")
