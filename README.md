# Ajoulib

Repository for Dataming Team Project

## Topic

- Analysis of trends based on best-selling data for each year
- Recommend new books based on user-specific reading lists

## Using Algorithms

1. TF-IDF: Create an initial dataset by extracting keywords based on the introduction of bestsellers
2. Association rule (ex, A-Priori): Find related rules based on the extracted keywords and analyze trends
3. Recommendation System (LSH or Jacquard Similarity): Based on each user's reading list, recommend the most relevant new book

## How to use

### Setup Initial Settings

```python
# initial setting
pyenv virtualenv 3.10.6 ajoulib
pyenv activate ajoulib
```

<br>

```python
# install packages
pip install -r requirements.txt
```

### Setup Word vectors

```bash
# Download Pre-Data for Comparison Similar word
cd similarity_data

wget https://dl.fbaipublicfiles.com/fasttext/vectors-crawl/cc.ko.300.vec.gz
gzip -d cc.ko.300.vec.gz

wget https://github.com/spellcheck-ko/hunspell-dict-ko/releases/download/0.7.92/ko-aff-dic-0.7.92.zip
unzip ko-aff-dic-0.7.92.zip

cd ..
cd src
python create_wordvector.py
```

### Other Codes for creating Pre-datas

Pre-data for actual functional operation is already uploaded, and data frames processed in the middle (Stopwords removed, TF, TFIDF, etc.) can be generated and checked through the corresponding code

```python
cd src

# for creating dataframe
python create_dataframe.py

# for creating wordcloud images
python create_wordcloud.py
```

### Run Main Feature

When the main function is executed, the GUI for the actual function operation is activated. The GUI is divided into two tabs, and the first tab is for a recommendation system based on keywords. The second tabs are trend analysis images for each field & year based on crawled data.

```python
# CWD : Ajoulib/
python main.py
```
