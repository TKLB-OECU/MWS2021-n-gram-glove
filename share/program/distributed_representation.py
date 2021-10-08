from gensim.corpora import Dictionary
from gensim.models import word2vec
from sklearn.decomposition import PCA
import pprint
import matplotlib.pyplot as plt
from tqdm import tqdm

def n_gram(n: int, string: str):
    # 改行削除
    string = string.replace("\n", "")
    # 基準を1文字(単語)ずつ ずらしながらn文字分抜き出す
    return [string[idx:idx + n] for idx in range(len(string) - n + 1)]

def word_2_vec(word_list):
    # Word2vecの処理
    model = word2vec.Word2Vec(word_list,  min_count=0, window=10)
    return model

if __name__ == "__main__":
    n: int = input("input number: ") 
    file_path: str = "sample-ffridataset2021_malware_strings_cleaning_10000.txt"
    word_list: list[str] = []

    with open(file_path, mode="r") as f:
        for i, string in enumerate(f):
            word_list.append(n_gram(int(n), string))

    model = word_2_vec(word_list)
    dct = Dictionary(word_list,prune_at=None)
    token2id = dct.token2id
    word2vec_vec = []
    for token in tqdm(token2id, total=len(token2id)):
        word2vec_vec.append(model.wv[token])

    # PCAの処理
    pca = PCA(n_components=2)
    vec = pca.fit_transform(word2vec_vec)
    x_list = []
    y_list = []
    with open("test_vec.txt", mode="w") as f:
        for token ,(x, y) in tqdm(zip(token2id, vec), total=len(token2id)):
            x_list.append(x)
            y_list.append(y)
            f.write(f"{token}\t{x}\t{y}\n")

    plt.scatter(x_list, y_list)
    # [plt.annotate(str(i), (x_list[i], y_list[i])) for i, label in tqdm(enumerate(token2id), total=len(token2id))]
    plt.savefig(f"{n}-gram-test.png")
