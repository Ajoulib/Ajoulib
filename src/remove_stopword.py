from konlpy.tag import Komoran


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