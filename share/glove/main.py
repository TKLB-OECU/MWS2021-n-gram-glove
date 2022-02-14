#%%

#%%

from make_dataset import MakeDataset
from glove_test import GloVe
from view_glove import View_GloVe

import hydra
from omegaconf import DictConfig, OmegaConf

@hydra.main(config_path="config", config_name="config")
def main(cfg : DictConfig) -> None:
    malware_path = cfg["glove"]["malware_path"]
    clean_path = cfg["glove"]["clean_path"]
    N_gram = cfg["glove"]["N_gram"]
    vector_size = cfg["glove"]["vector_size"]

    make_dataset = MakeDataset(malware_path, clean_path, N_gram)
    make_dataset()
    print(vector_size)
    print(type(vector_size))

    glove = GloVe(N_gram, vector_size=vector_size)
    glove()

    # view = View_GloVe(N_gram)
    # view()

    with open("parameter.txt", "w") as f:
        f.write(f"{vector_size},{N_gram}")

if __name__ == "__main__":
    main()
