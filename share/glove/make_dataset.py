#%%
from tqdm import tqdm
import subprocess
import gzip
from gensim.corpora import Dictionary

def n_gram(n, string):
    # 改行削除
    string = string.replace("\n", "")
    # 基準を1文字(単語)ずつ ずらしながらn文字分抜き出す
    return [string[idx:idx + n] for idx in range(len(string) - n + 1)]

# livedoorニュースコーパスを全て分かち書きして１つのファイルに書き込む
# カテゴリを配列で取得
#%%
class MakeDataset():
    def __init__(self, path_malware_data: str, path_clean_data: str, N_gram_value: int, ):
        # malware  初期変数
        self.path_malware_data: str = path_malware_data
        self.malware_file_count = int(subprocess.Popen(f'zcat {path_malware_data} | wc -l' , shell=True, stdout=subprocess.PIPE).communicate()[0])
        self.malware_dictionary_flag = False
        # clean 初期変数
        self.path_clean_data: str = path_clean_data
        self.clean_file_count = int(subprocess.Popen(f'zcat {path_clean_data} | wc -l' , shell=True, stdout=subprocess.PIPE).communicate()[0])
        self.clean_dictionary_flag = False

        self.N: int = N_gram_value
        self.malware_dictionary_name: str = f"{self.N}_malware_dictionary.dict"
        self.clean_dictionary_name: str = f"{self.N}_clean_dictionary.dict"
    
    def file_open(self):
        self.save_file = open(f"{self.N}_corpus.txt", "w", encoding="utf-8")
        self.malware_file = gzip.open(self.path_malware_data, mode="r")
        self.clean_file = gzip.open(self.path_clean_data, mode="r")
    
    def file_close(self):
        self.save_file.close()
        self.malware_file.close()
        self.clean_file.close()

    def make_n_gram(self, read_file, file_count, write_file, dict_file_name):
        frist_data = read_file.readline()
        # lineをstr化
        line = frist_data.decode()
        n_gram_data = n_gram(self.N, line)
        dictionary: Dictionary = Dictionary([n_gram_data])
        for num, line in enumerate(tqdm(read_file, total=file_count)):
            # debug
            # if num > 10:
            #     break
            # lineをstr化
            line = line.decode()
            n_gram_data = n_gram(self.N, line)
            dictionary.add_documents([n_gram_data], prune_at=None)
            write_file.write(" ".join(n_gram_data) + "\n")
        dictionary.save(dict_file_name)
    
    def make_corpus(self):
        pass
    
    def make_unique_word(self):
        malware_token2id = Dictionary.load(self.malware_dictionary_name).token2id
        malware_words = set([word for word in malware_token2id])

        clean_token2id = Dictionary.load(self.clean_dictionary_name).token2id
        clean_words = set([word for word in clean_token2id])

        common_unique_word = malware_words & clean_words
        malware_unique_word = malware_words - common_unique_word
        clean_unique_word = clean_words - common_unique_word
        # %%
        with open(f"{self.N}_common_unique_word.txt", mode="w") as save_f:
            save_f.write("\n".join(list(common_unique_word)))
            
        with open(f"{self.N}_malware_unique_word.txt", mode="w") as save_f:
            save_f.write("\n".join(list(malware_unique_word)))
            
        with open(f"{self.N}_clean_unique_word.txt", mode="w") as save_f:
            save_f.write("\n".join(list(clean_unique_word)))

        print(f"common_unique_word : {len(common_unique_word)}")
        print(f"malware_unique_word : {len(malware_unique_word)}")
        print(f"clean_unique_word : {len(clean_unique_word)}")

        with open(f"{self.N}_ben.txt", mode="w") as f:
            f.write(f"common_unique_word : {len(common_unique_word)}\n")
            f.write(f"malware_unique_word : {len(malware_unique_word)}\n")
            f.write(f"clean_unique_word : {len(clean_unique_word)}\n")


    def __call__(self):
        self.file_open()
        # マルウェア
        self.make_n_gram(self.malware_file, self.malware_file_count, self.save_file, self.malware_dictionary_name)
        # クリーン
        self.make_n_gram(self.clean_file, self.clean_file_count, self.save_file, self.clean_dictionary_name)

        self.file_close()

        self.make_unique_word()

# if __name__ == "__main__":
#     # # malwareに必要な変数宣言
#     # path_malware_data = "../data/sample-ffridataset2021_malware_10000_strings.txt.gz"

#     # # cleanに必要な変数宣言
#     # path_clean_data = "../data/sample-ffridataset2021_cleanware_10000_strings.txt.gz"

#     # N: int = 10

#     # make_dataset = MakeDataset(path_malware_data, path_clean_data, N)
#     # make_dataset()
