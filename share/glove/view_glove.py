#%%
from gensim.test.utils import datapath, get_tmpfile
from gensim.models import KeyedVectors
from gensim.scripts.glove2word2vec import glove2word2vec

import pandas as pd
import numpy as np

from sklearn.decomposition import PCA
import pprint
import matplotlib.pyplot as plt
from tqdm import tqdm

class View_GloVe():
    def __init__(self, n_gram_value: int):
        self.N = n_gram_value

    def load_model(self):
        vectors = pd.read_csv(f'{self.N}_vectors.txt', delimiter=' ', index_col=0, header=None)

        with open(f'{self.N}_vectors.txt', 'r') as original, open(f'{self.N}_gensim_vectors.txt', 'w') as transformed:
            vocab_count = vectors.shape[0]  # 単語数
            size = vectors.shape[1]  # 次元数

            transformed.write(f'{vocab_count} {size}\n')
            transformed.write(original.read())
        self.model = KeyedVectors.load_word2vec_format(f'{self.N}_gensim_vectors.txt', binary=False)

    def make_vec_list(self):
        self.token2id = self.model.index_to_key
        self.word2vec_vec = []
        for index, token in enumerate(tqdm(self.token2id, total=len(self.token2id))):
            self.word2vec_vec.append(self.model.vectors[index])


    def make_PCA_to_pig(self):
        # PCAの処理
        pca = PCA(n_components=2)
        vec = pca.fit_transform(self.word2vec_vec)
        x_list = []
        y_list = []
        color_list = []
        with open(f"{self.N}_common_unique_word.txt", mode="r") as read_f:
            common_unique_word = read_f.read().split("\n")
            set_common_unique_word = set(common_unique_word)
            
        with open(f"{self.N}_malware_unique_word.txt", mode="r") as read_f:
            malware_unique_word = read_f.read().split("\n")
            set_malware_unique_word = set(malware_unique_word)
            
        with open(f"{self.N}_clean_unique_word.txt", mode="r") as read_f:
            clean_unique_word = read_f.read().split("\n")
            set_clean_unique_word = set(clean_unique_word)

        for token ,(x, y) in tqdm(zip(self.token2id, vec), total=len(self.token2id)):
            # tokenがどれに属するか
            if token in set_malware_unique_word:
                color = "red"
            elif token in set_clean_unique_word:
                color = "blue"
            else:
                if self.N == 2:
                    color = "green"
                else:
                    continue
                    
            x_list.append(x)
            y_list.append(y)
            color_list.append(color)

        fig = plt.figure()
        ax = fig.add_subplot(111)
        ax.scatter(x_list, y_list, color=color_list, alpha=0.1)

        plt.savefig(f"{self.N}-gram-test.png") 
    
    def __call__(self):
        self.load_model()
        self.make_vec_list()
        self.make_PCA_to_pig()


# view = View_GloVe(10)
# view()

# glove_file = datapath('/Workspace/glove/10_vectors.txt')
# tmp_file = get_tmpfile("test_word2vec.txt")

# _ = glove2word2vec(glove_file, tmp_file)

# model = KeyedVectors.load_word2vec_format(tmp_file)

# # %%
# n = 2
# token2id = model.index_to_key
# word2vec_vec = []
# for index, token in enumerate(tqdm(token2id, total=len(token2id))):
#     word2vec_vec.append(model.vectors[index])

# # PCAの処理
# pca = PCA(n_components=2)
# vec = pca.fit_transform(word2vec_vec)
# x_list = []
# y_list = []
# color_list = []
# with open("./common_unique_word.txt", mode="r") as read_f:
#     common_unique_word = read_f.read().split("\n")
#     set_common_unique_word = set(common_unique_word)
    
# with open("./malware_unique_word.txt", mode="r") as read_f:
#     malware_unique_word = read_f.read().split("\n")
#     set_malware_unique_word = set(malware_unique_word)
    
# with open("./clean_unique_word.txt", mode="r") as read_f:
#     clean_unique_word = read_f.read().split("\n")
#     set_clean_unique_word = set(clean_unique_word)

# for token ,(x, y) in tqdm(zip(token2id, vec), total=len(token2id)):
#     # tokenがどれに属するか
#     if token in set_malware_unique_word:
#         color = "red"
#     elif token in set_clean_unique_word:
#         color = "blue"
#     else:
#         color = "green"
#     x_list.append(x)
#     y_list.append(y)
#     color_list.append(color)

# fig = plt.figure()
# ax = fig.add_subplot(111)
# ax.scatter(x_list, y_list, color=color_list, alpha=0.1)

# plt.savefig(f"{n}-gram-test.png")



# %%

# %%
