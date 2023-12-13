# Ajoulib
![image](./ajoulib_mainimage.png)
Repository for AjouUniv Datamining SCE3313 Team Project

## Topic

- Analysis of trends based on best-selling data for each year
- Recommend similar books based on input keywords and book-title

## Using Algorithms

1. TF-IDF: Create an initial dataset by extracting keywords based on the introduction of bestsellers
2. Association rule (ex, A-Priori): Find related rules based on the extracted keywords and analyze trends
3. Recommendation System (Cosine Similarity, Fasttext): Recommend similar books based on input keywords and book-title

## How to use

### Requirements 

This project <b>works on MacOS.</b>
It has <b>not been verified on Linux and Windows</b>, so please be careful.

### Setup Initial Settings

```bash
# initial setting with pyenv
pyenv virtualenv 3.10.6 ajoulib
pyenv activate ajoulib
```
```bash
# initial setting with conda
conda create -n ajoulib python=3.10.6
conda activate ajoulib
```
<br>

```bash
# install packages (MacOS)
pip install -r requirements.txt

# install packages (Windows)
pip install -r requirements_windows.txt
```

### Setup Word vectors
아래 Setup과정은 <b>MacOS</b>기준입니다.
<br>
<b>Windows는 wget을 따로 설치후 cmd에서 진행</b>하셔야 합니다. (PowerShell X)<br>또한, gzip과 unzip명령어 대신 압축해제 프로그램을 사용해 현재 폴더에 압축해제 해주시면 됩니다. (다만 Windows환경은 검증되지 않았습니다.) 
<br>

```bash
# Download Pre-trained word vector model, similar words
cd similarity_data

wget https://dl.fbaipublicfiles.com/fasttext/vectors-crawl/cc.ko.300.vec.gz
gzip -d cc.ko.300.vec.gz

wget https://github.com/spellcheck-ko/hunspell-dict-ko/releases/download/0.7.92/ko-aff-dic-0.7.92.zip
unzip ko-aff-dic-0.7.92.zip

cd ..
cd src
python create_wordvector.py
```

### Setup Pre-datas

Pre-data for actual functional operation is already uploaded, and data frames processed in the middle (Stopwords removed, TF, TFIDF, etc.) can be generated and checked through the corresponding code

```bash
# This is not required, but if you start from an empty directory, you must do the following.
# 프로그램을 실행하기 위한 사전데이터는 모두 깃허브에 업로드되어있습니다.
# 따라서, 제공하는 시스템의 실행을 위해서는 아래 작업을 수행하지 않아도 괜찮습니다.
# 다만 실제 프로그램의 동작 방식을 설명하기 위해 아래 command를 첨부하였습니다.
# 아래 작업을 수행하지 않으려면 아래쪽의 Run Main Feature Command로 이동하십시오.

cd src

# for creating dataframe
python create_dataframe.py

# for creating wordcloud images
# for finding association rules
# wordcloud images and association_rules.csv is alreay uploaded.
python create_wordcloud.py
python find_association_rules.py
```

### Run Main Feature

When the main function is executed, the GUI for the actual function operation is activated. The GUI is divided into two tabs, and the first tab is for a recommendation system based on keywords. The second tabs are trend analysis images for each field & year based on crawled data.

```bash
# CWD : Ajoulib/
python main.py
```
