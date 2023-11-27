import pandas as pd


def map_keywords_from_tf(file_path):
    try:
        df = pd.read_csv(file_path)
        df.set_index('Title', inplace=True)

        # index(Title) Column 제외
        df_keywords = df.iloc[:, 1:]

        data_for_df = []

        for index, row in df_keywords.iterrows():
            keywords = row[row > 0].index.tolist()
            data_for_df.append({'Title': index, 'Keywords': ', '.join(keywords)})

        keywords_df = pd.DataFrame(data_for_df).set_index('Title')

        print("[SUCCESS] map_keywords_from_tf function executed successfully")
        return keywords_df

    except Exception as e:
        print(f"[ERROR] Error in map_keywords_from_tf function: {e}")
