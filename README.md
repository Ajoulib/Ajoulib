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

<br>

```python
# run code
python main.py
```
