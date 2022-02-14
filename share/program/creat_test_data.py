from asyncore import read
import json
import difflib
import gzip
from random import shuffle

executable_file_id = []
executable_file_strings = []

with open("../data/ffridataset2021_cleanware.jsonl", "r") as cleanware_file:
    with open("../data/ffridataset2021_malware.jsonl", "r") as malware_file:
        with gzip.open("../data/sample-ffridataset2021_strings.txt.gz", "wt") as save_strings:
            for num, l in enumerate(cleanware_file, 1):
                if num < 2000:
                    continue
                if num > 2025:
                    break
                # ここが一つのjson
                obj = json.loads(l)
                strings = obj["strings"]
                cleanware_string = "".join(strings)
                save_strings.write(f"{cleanware_string}\tdata_label={0}\n")

            for num, l in enumerate(malware_file, 1):
                if num < 2000:
                    continue
                if num > 2025:
                    break
                # ここが一つのjson
                obj = json.loads(l)
                strings = obj["strings"]
                malware_string = "".join(strings)
                save_strings.write(f"{malware_string}\tdata_label={1}\n")

with gzip.open("../data/sample-ffridataset2021_strings.txt.gz", "rt") as read_file:
    # with open("../data/test_data.txt", 'w') as write_file:
    data = []
    for num, l in enumerate(read_file):
        # if num > 5:
        #     break
        # data.append(l.split("\tlabel="))
        data.append(l)
        # print(data)
    # print(len(data))
    shuffle(data)
    # for num, l in enumerate(data):
    #     if num > 5:
    #         break
    #     print(f"{l}\n")

with gzip.open("../data/train_data.txt.gz", "wt") as write_file:
    for num, l in enumerate(data):
        # if num > 3:
        #     break
        write_file.write(f"{l}")

# with gzip.open("../data/train_data.txt.gz", "rt") as read_file:
#     for num, l in enumerate(read_file, 1):
#         # if num > 5:
#         #     break
#         # print(f"{l}")
#         print(num)
#         # if num == 815:
#         #     data = l.split("\tdata_label=")
#         #     # print(f"{data[1]}")
#         #     print(f"{len(data)}")

