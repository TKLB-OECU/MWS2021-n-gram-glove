import collections
import subprocess
from tqdm import tqdm
from gensim.corpora import Dictionary

def word_list_create(n: int, data: str, word_list: list) -> list:
    n_gram_list = n_gram(int(n), data)
    word_list.append(n_gram_list)
    # print(n_gram_list)
        
    return word_list

def n_gram(n: int, string: str) -> dict:
    # 改行削除
    string = string.replace("\n", "")
    # 基準を1文字(単語)ずつ ずらしながらn文字分抜き出す
    return [ string[idx:idx + n] for idx in range(len(string) - n + 1)]

def dictionary_create(word_list: list) -> list:
    return Dictionary(word_list, prune_at=None)

def list_to_set(word_list: list) -> set:
    for i, words in enumerate(word_list):
        if i > 0:
            for string in words:
                list_set.add(string)
        else:
            list_set = set(words)

    return list_set

if __name__ == "__main__":
    n: int = input("input number: ")
    num: int = 10000
    clean_file_path: str =  "../data/sample-ffridataset2021_cleanware_10000_strings.txt"
    clean_file_count = int(subprocess.check_output(['wc', '-l', clean_file_path]).decode().split(' ')[0])
    malware_file_path: str =  "../data/sample-ffridataset2021_malware_10000_strings.txt"
    malware_file_count = int(subprocess.check_output(['wc', '-l', malware_file_path]).decode().split(' ')[0])

    clean_word_list = []
    with open(clean_file_path, mode="r") as f_clean:
        for i, data in enumerate(tqdm(f_clean, total = clean_file_count)):
            if i > num:
                break
            clean_word_list = word_list_create(n, data, clean_word_list)

    common_dictionary = dictionary_create(clean_word_list)
    clean_dictionary = dictionary_create(clean_word_list)
    print("clean_dictionary:")
    print(clean_dictionary)

    set_clean = list_to_set(clean_word_list)
    # print(set_clean)
    # print(len(set_clean))

    malware_word_list = []
    with open(malware_file_path, mode="r") as f_malware:
        for i, data in enumerate(tqdm(f_malware, total = malware_file_count)):
            if i > num:
                break
            malware_word_list = word_list_create(n, data, malware_word_list)

    common_dictionary = dictionary_create(malware_word_list)
    malware_dictionary = dictionary_create(malware_word_list)
    print("malware_dictionary:")
    print(malware_dictionary)

    set_malware = list_to_set(malware_word_list)
    # print(set_malware)
    # print(len(set_malware))
 
    vocab_count = "/root/glove/build/vocab_count"
    min_word_count = "-min-count 5"
    verbose = "-verbose 2"
    input_clean = 
    output_clean_file = "clean_vocab.txt"
    input_malware = 
    output_malware_file = "malware_vocab.txt"
    command_list = [vocab_count, min_word_count, verbose, "<", input_file, ">", output_file]
    command = " ".join(command_list)
    os.system(command)





