import unicodedata
import pickle
import sqlite3
import unicodedata
import re
import numpy as np

from numpy import array
from transformers import TextClassificationPipeline, BertForSequenceClassification, AutoTokenizer
from tqdm import tqdm
from typing import Set


def is_hangul(text) -> bool:
    return bool(re.match(r'^[\u3130-\u318F\uAC00-\uD7A3]+$', text))


def load_dic(path: str) -> Set[str]:
    rtn = set()
    with open(path, 'r', encoding='utf-8') as f:
        for line in f.readlines():
            word = line.strip()
            word = unicodedata.normalize('NFC', word)
            if is_hangul(word):
                rtn.add(word)
    return rtn


def blocks(files, size=65536):
    while True:
        b = files.read(size)
        if not b: break
        yield b


def count_lines(filepath):
    with open(filepath, "r", encoding="utf-8", errors='ignore') as f:
        return sum(bl.count("\n") for bl in tqdm(blocks(f), desc='Counting lines', mininterval=1))


if __name__ == '__main__':
    # frequent_words
    with open('../similarity_data/frequent_words.txt', 'r', encoding='UTF-8') as f:
        words = list(unicodedata.normalize('NFC', line.strip()) for line in tqdm(f))
    filtered_words = []

    for word in tqdm(words, total=len(words)):
        processed_word = unicodedata.normalize('NFC', word.strip())
        filtered_words.append(processed_word)

    with open('../similarity_data/filtered_frequent_words.txt', 'w', encoding='UTF-8') as f:
        f.write('\n'.join(tqdm(filtered_words)))

    # dictionary
    with open('../similarity_data/ko-aff-dic-0.7.92/ko.dic', 'r', encoding='UTF-8') as f:
        words = list(unicodedata.normalize('NFC', line.strip().split('/')[0]) for line in tqdm(f))
    filtered_words = []

    for word in tqdm(words, total=len(words)):
        processed_word = unicodedata.normalize('NFC', word.strip())
        filtered_words.append(processed_word)

    with open('../similarity_data/ko-aff-dic-0.7.92/ko_filtered.txt', 'w', encoding='UTF-8') as f:
        f.write('\n'.join(tqdm(filtered_words)))

    connection = sqlite3.connect('../similarity_data/valid_guesses.db')
    cursor = connection.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS guesses (word text PRIMARY KEY, vec blob)""")
    print("created table")
    normal_words = load_dic('../similarity_data/ko-aff-dic-0.7.92/ko_filtered.txt')
    print("# words in dictionary:", len(normal_words))
    valid_nearest = []
    valid_nearest_mat = None
    eliminated = 0
    checked_words = set()
    total_lines = count_lines('../similarity_data/cc.ko.300.vec') - 1
    with open('../similarity_data/cc.ko.300.vec', 'r', encoding='utf-8', errors='ignore') as w2v_file:
        _ = w2v_file.readline()
        t = tqdm(total=total_lines, desc='Processing vectors', mininterval=1)
        for n, line in enumerate(w2v_file):
            # careful! some data sets (e.g. dewiki100.txt) have non-breaking spaces, which get split
            # others have trailing spaces (e.g. COW.token.wang2vec), meaning an empty string is included with split(' ')
            words = line.rstrip().split(' ')
            word = words[0]
            word = unicodedata.normalize('NFC', word)
            if not is_hangul(word) or word in checked_words:
                eliminated += 1
            else:
                vec = array([float(w1) for w1 in words[1:]])
                if word in normal_words:
                    valid_nearest.append(word)
                    if valid_nearest_mat is None:
                        valid_nearest_mat = [vec]
                    else:
                        valid_nearest_mat.append(vec)
                cursor.execute("""INSERT INTO guesses values (?, ?)""", (word, pickle.dumps(vec)))
            checked_words.add(word)
            if n % 100000 == 0:
                connection.commit()
            t.update()
        t.refresh()
    connection.commit()
    connection.close()
    print("invalid:", eliminated)
    valid_nearest_mat = np.array(valid_nearest_mat)
    print("valid nearest shape:", valid_nearest_mat.shape)
    with open('../similarity_data/valid_nearest.dat', 'wb') as f:
        pickle.dump((valid_nearest, valid_nearest_mat), f)
    print("done pickling matrix")
