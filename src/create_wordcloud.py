import os
import pandas as pd
import matplotlib.pyplot as plt

from wordcloud import WordCloud

PARENT_DIR = os.path.dirname(os.getcwd())
DATA_DIR = os.path.join(PARENT_DIR, 'data')
TARGET_DIR = os.path.join(DATA_DIR, 'tfidf_score_datas')
SAVE_DIR = os.path.join(DATA_DIR, 'wordcloud_images')


def create_word_cloud(filename, text, field):
    wordcloud = WordCloud(
        width=1280, 
        height=720, 
        background_color='white', 
        min_font_size=10,
        font_path=f'{PARENT_DIR}/AjouTTF.ttf'  # Specify the font path here
    ).generate(text)
    plt.figure(figsize=(8, 8), facecolor=None)
    plt.imshow(wordcloud)
    plt.axis("off")
    plt.tight_layout(pad=0)

    # Directory for the specific field
    field_dir = os.path.join(SAVE_DIR, field)
    if not os.path.exists(field_dir):
        os.makedirs(field_dir)

    # Save the word cloud image in the specific field directory
    wordcloud_img_filename = os.path.join(field_dir, f"{filename}_wordcloud.png")
    wordcloud.to_file(wordcloud_img_filename)

    print(f"Saved word cloud image in '{field}': {wordcloud_img_filename}")
    plt.close()  # 현재 생성한 그래프를 닫아 메모리 해제


def process_files(root_dir):
    for subdir, dirs, files in os.walk(root_dir):
        for file in files:
            if file.endswith('.csv'):  # Only process CSV files
                file_path = os.path.join(subdir, file)
                try:
                    df = pd.read_csv(file_path)
                    text = ' '.join(df['keyword'].tolist())  # Replace 'text' with the actual column name

                    # Extract field from filename
                    field = file.split('_')[0]

                    create_word_cloud(os.path.splitext(file)[0], text, field)
                except Exception as e:
                    print(f"Error processing file {file_path}: {e}")


if __name__ == "__main__":
    process_files(TARGET_DIR)
