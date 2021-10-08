#%%
import gzip

file_path = '../data/sample-ffridataset2021_malware_10000_strings.txt.gz'

with gzip.open(file_path, mode='r') as f:
    for i, string in enumerate(f):
        if i > 100:
            break
        print(string)

# %%
