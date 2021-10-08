import re

def cleaning():
    strings = []

    with open("sample-ffridataset2021_malware_strings.txt", "r") as f:
        for i, string in enumerate(f):
            with open("sample-ffridataset2021_malware_strings_cleaning.txt", "a") as save_file:
                if re.search("\S", string):
                    save_file.write(f"{string.strip()}\n")
                else:
                    pass

if __name__ == "__main__":
    cleaning()
