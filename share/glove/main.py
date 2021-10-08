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

    make_dataset = MakeDataset(malware_path, clean_path, N_gram)
    make_dataset()

    glove = GloVe(N_gram)
    glove()

    view = View_GloVe(N_gram)
    view()

if __name__ == "__main__":
    main()