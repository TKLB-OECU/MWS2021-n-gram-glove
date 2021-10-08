from gensim.corpora import Dictionary

def n_gram(n: int, string: str):
    # 改行削除
    string = string.replace("\n", "")
    # 基準を1文字(単語)ずつ ずらしながらn文字分抜き出す
    return [ string[idx:idx + n] for idx in range(len(string) - n + 1)]

def dictionary_create(word_list):
    return Dictionary(word_list)

if __name__ == "__main__":
    n: int = input("input number: ")
    file_path: str = "sample-ffridataset2021_malware_strings_cleaning_10000.txt"
    word_list = []

    with open(file_path, "r") as f:
        for i, string in enumerate(f):
            word_list.append(n_gram(int(n), string))
            # if i > 100:
            #     break

    dic = dictionary_create(word_list)
    # print(len(dic))
    dic.save_as_text("test.dict.txt")
    # for i in range(5):
    #     print(word_list[i])
    # print(word_list)
    # print(len(corpus))
    # model = word_2_vec(corpus)

# def dictionary_create(strings):
#     word_list = []

#     word_list.append(strings)
#     return Dictionary(word_list)

# if __name__ == "__main__":
#     strings = []
#     file_path: str = "test.txt"

#     with open(file_path, "r") as f:
#         for i, string in enumerate(f):
#             strings.append(string.split("\t")[0])
#             # if i > 100:
#             #     break

#     dct = dictionary_create(strings)
#     dct.save_as_text("test2.dict.txt")

#     # print(dct.token2id)
