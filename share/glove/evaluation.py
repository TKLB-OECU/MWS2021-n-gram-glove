#%%
import gzip
import os
# os.environ["CUDA_VISIBLE_DEVICES"] = "-1"

from gensim.models import KeyedVectors
import tensorflow as tf
from tensorflow import keras
import pandas as pd
import numpy as np
from tqdm import tqdm

import sys

args = sys.argv

MAX_LENGTH = 2695160
FILE_DATE_PATH = "2022-02-13/11-40-52"

def n_gram(n, string):
    # 改行削除
    string = string.replace("\n", "")
    # 基準を1文字(単語)ずつ ずらしながらn文字分抜き出す
    return [string[idx:idx + n] for idx in range(len(string) - n + 1)]

class Evaluation():
    # 初期値
    def __init__(self, file_number: int):
        self.file_number = file_number
        with open(f"./multirun/{FILE_DATE_PATH}/{self.file_number}/parameter.txt", "r") as f:
            line = f.read()
            print(line.split(","))
            self.vacter_size, self.N = [int(i) for i in line.split(",")]
        # self.N = n_gram_value
        # self.dir_num = dir_num
        # print(self.vacter_size)
        # print(self.N)

        self.savefile_path = f"./result/{FILE_DATE_PATH}"
        os.makedirs(self.savefile_path, exist_ok=True)
        self.save_file_point = open(f"{self.savefile_path}/score_{self.vacter_size}_{self.N}.txt", "w")


    def load_model(self):
        # vectors = pd.read_csv(f'{self.N}_vectors.txt', delimiter=' ', index_col=0, header=None)
        vectors = pd.read_csv(f'./multirun/{FILE_DATE_PATH}/{self.file_number}/{self.N}_vectors.txt', delimiter=' ', index_col=0, header=None, encoding='utf-8', engine='python', error_bad_lines=False)

        # with open(f'{self.N}_vectors.txt', 'r') as original, open(f'{self.N}_gensim_vectors.txt', 'w') as transformed:
        with open(f'./multirun/{FILE_DATE_PATH}/{self.file_number}/{self.N}_vectors.txt', 'r') as original, open(f'./multirun/{FILE_DATE_PATH}/{self.file_number}/{self.N}_gensim_vectors.txt', 'w') as transformed:
            vocab_count = vectors.shape[0]  # 単語数
            self.size = vectors.shape[1]  # 次元数

            transformed.write(f'{vocab_count} {self.size}\n')
            transformed.write(original.read())
        # self.w2v = KeyedVectors.load_word2vec_format(f'{self.N}_gensim_vectors.txt', binary=False)
        self.w2v = KeyedVectors.load_word2vec_format(f'./multirun/{FILE_DATE_PATH}/{self.file_number}/{self.N}_gensim_vectors.txt', binary=False)

    def get_embedding_matrix(self):
        self.char_indices = dict([(key, value) for (value, key) in enumerate(self.w2v.index_to_key, 1)])
        self.indices_char = dict([(value, key) for (key, value) in self.char_indices.items()])

        null_word = np.zeros(self.vacter_size)

        # gensim modelの分散表現を格納するための変数を宣言
        self.embedding_matrix = np.zeros((len(self.char_indices)+1, self.vacter_size))

        for id, word in self.indices_char.items():
            try:
                self.embedding_matrix[id] = self.w2v[word]
            except:
                self.embedding_matrix[id] = null_word
        # print(self.embedding_matrix[1])
        # print(self.embedding_matrix.shape)

    def make_data(self, file_path: str, train_or_test: str):
        make_data = []
        make_label = []
        # with gzip.open("../data/train_data.txt.gz", "rt") as read_file:
        with gzip.open(file_path, "rt") as read_file:
            print("===================================================")
            print(f"============= make {train_or_test} data start ===============")
            print("===================================================\n")
            for num, line in enumerate(tqdm(read_file, total=250), 1):
                # if num > 500:
                #     break
                data = []
                line, label = line.split("\tdata_label=")
                self.n_gram_data = n_gram(self.N, line)

                if len(self.n_gram_data) > MAX_LENGTH:
                    print(self.n_gram_data[MAX_LENGTH])
                    for num, word in enumerate(tqdm(self.n_gram_data, total=MAX_LENGTH)):
                        if num > MAX_LENGTH:
                            break
                        try:
                            data.append(self.char_indices[word])
                        except:
                            data.append(0)
                    make_data.append(data)
                    make_label.append(int(label))
                    self.n_gram_data = self.n_gram_data[2695161:]
                    data = []
                    print(self.n_gram_data[0])

                for word in tqdm(self.n_gram_data, total=len(self.n_gram_data)):
                    try:
                        data.append(self.char_indices[word])
                    except:
                        data.append(0)
                make_data.append(data)
                make_label.append(int(label))
            # paddingしたデータ作成
            padded_data = keras.preprocessing.sequence.pad_sequences(make_data, maxlen=MAX_LENGTH, padding='post')
            print(padded_data.shape)
            print(len(padded_data))
            print(len(make_label))
            print("===================================================")
            print(f"=============== make {train_or_test} data end ===============")
            print("===================================================\n")

        return padded_data, make_label
    
    def make_model(self):
        self.model = keras.Sequential()
        self.model.add(keras.layers.Embedding(len(self.char_indices)+1, self.vacter_size, weights=[self.embedding_matrix], mask_zero=True))
        self.model.add(keras.layers.GlobalAveragePooling1D())
        # self.model.add(keras.layers.Dense(len(self.char_indices)+1, activation='relu'))
        self.model.add(keras.layers.Dense(200, activation='relu'))
        self.model.add(keras.layers.Dense(1, activation='sigmoid'))

        self.model.summary()

        self.model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

    # 学習を行う関数
    def train_model(self, traing_tesor, traing_label):
        x_val = np.array(traing_tesor[:80])
        # print(f"x_val = {len(x_val)}")
        y_val = np.array(traing_label[:80])
        # print(f"y_val = {len(y_val)}")

        partial_x_train = np.array(traing_tesor[80:])
        # print(f"partial_x_train = {len(partial_x_train)}")
        partial_y_train = np.array(traing_label[80:])
        # print(f"partial_y_train = {len(partial_y_train)}")

        print(x_val.shape, y_val.shape)
        print(partial_x_train.shape, partial_y_train.shape)

        history = self.model.fit(x_val, y_val, epochs=10, batch_size=1, validation_data=(partial_x_train, partial_y_train), verbose=1)
        print(history.history)
        self.train_result = self.model.evaluate(x_val, y_val, batch_size=1, verbose=1)

        # self.model.fit(partial_x_train, partial_y_train, epochs=1, batch_size=2, validation_data=(x_val, y_val), verbose=1)

    def evaluate_model(self, test_tensor, test_label):
        x_val = np.array(test_tensor)
        y_val = np.array(test_label)
        self.test_result = self.model.evaluate(x_val, y_val, batch_size=1, verbose=1)
        

    def __call__(self):
        path_train_data = "../data/train_data.txt.gz"
        path_test_data = "../data/test_data.txt.gz"
        self.load_model()
        self.get_embedding_matrix()
        train_tensor, train_label = self.make_data(path_train_data, "train")
        test_tensor, test_label = self.make_data(path_test_data, "test")
        self.make_model()
        self.train_model(train_tensor, train_label)
        self.evaluate_model(test_tensor, test_label)
        self.save_file_point.write(f"{self.vacter_size},{self.N},{self.train_result[0]},{self.train_result[1]},{self.test_result[0]},{self.test_result[1]}")
        

if __name__ == "__main__":
    args = sys.argv
    _eval = Evaluation(args[1])
    _eval()
