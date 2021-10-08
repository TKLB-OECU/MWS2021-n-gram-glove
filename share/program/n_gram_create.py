import collections

def n_gram(n: int, string: str):
    # 改行削除
    string = string.replace("\n", "")
    # 基準を1文字(単語)ずつ ずらしながらn文字分抜き出す
    return [ string[idx:idx + n] for idx in range(len(string) - n + 1)]

if __name__ == "__main__":
    n: int = input("input number: ")
    file_path: str =  "sample-ffridataset2021_malware_strings_cleaning_10000.txt"
    counter = collections.Counter()

    with open(file_path, "r") as f:
        for i, string in enumerate(f):
            word_list = n_gram(int(n), string)
            counter.update(word_list)
            # if i > 10000:
            #     break
    with open ("./test.txt", mode="w") as f:
        for _id in counter:
            f.write(f"{_id}\t{counter[_id]}\n")
