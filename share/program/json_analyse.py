import json
import difflib

executable_file_id = []
executable_file_strings = []

with open("ffridataset2021_malware.jsonl", "r") as f:
    for l in f:
        obj = json.loads(l)
        strings = obj["strings"]
        with open("sample-ffridataset2021_malware_strings.txt", "a") as save_file:
            for string in strings:
                save_file.write(f"{string}\n")


        #     f.write()
    # for i, strings in enumerate(executable_file_strings):
    #    for j in range(len(strings)):
    #        f.write(strings[j] + "\n")
    #    f.write("\n")
 