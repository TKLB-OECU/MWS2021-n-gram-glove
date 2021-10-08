from collections import Counter
import matplotlib.pyplot as plt

def word_to_id_create():
    string_to_id = {}
    id_to_string = {}

    with open("sample-ffridataset2021_malware_strings_cleaning.txt", "r") as f:
        for i, string in enumerate(f):
            if i != 1000000:
                if string not in string_to_id:
                    new_id = len(string_to_id)
                    string_to_id[string] = new_id
                    id_to_string[new_id] = string
            else:
                break
    
    # print(string_to_id)
    print(id_to_string)

def count():
    str_con = Counter()
    strings = []
    
    with open("sample-ffridataset2021_malware_strings_cleaning.txt", "r") as f:
        # for i, string in enumerate(f):
        #     if i != 100:
        #         str_con.update(string)
        #     else:
        #         break

        # for string in f:
        #     str_con.update(string)

        for i, string in enumerate(f):
            if i != 1000:
                string = string.replace("\n", "")

                if i % 10 != 0:
                    strings.append(string)
                    # print(strings)
                else:
                    str_con.update(strings)
                    strings = []
                    # print(strings)
                    
            else:
                break

    # print(str_con)
    fig = plt.figure()
    plt.bar(list(str_con.keys()), list(str_con.values()))
    fig.savefig("strings_count.png")

if __name__ == "__main__":
    count()
