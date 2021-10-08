import json
import difflib

executable_file_id = []
executable_file_strings = []

with open("../data/ffridataset2021_cleanware.jsonl", "r") as f:
    with open("../data/sample-ffridataset2021_cleanware_100_strings_version2.txt", "w") as save_strings:
        with open("../data/sample-ffridataset2021_cleanware_100_fuzzyhashes_version2.txt", "w") as save_fuzzyhashes:
            for num, l in enumerate(f):
                if num > 100:
                    break
                # ここが一つのjson
                obj = json.loads(l)
                strings = obj["strings"]
                clean_string = "".join(strings)
                save_strings.write(f"{clean_string}\n")
                
                fuzzyhash = obj["hashes"]["ssdeep"]
                save_fuzzyhashes.write(f"{fuzzyhash}\n")