# n-gram + GloVeによる分散表現の作成

## 環境構築
```shell
docker-compose build
docker-compose up -d 
docker exec -it python3_malware bash
cd glove 
git clone https://github.com/stanfordnlp/glove
cd glove && make
```

## 実行方法
まず、はじめに`docker exec -it python3_malware bash`を実行しDocker内に入る。  

### 学習データの作成
FFRI2021 Dataから学習データを作成する。  
`share/data`内にFFRI2021 Datasetを配置し、malwareの学習データを作成する`share/program/create_dataset_malware.py`とcleanの学習データを作成する`share/program/create_dataset_cleanware.py`を実行することで学習データを作成することができる。  

### n-gram + GloVeによる分散表現
そして、n-gram + GloVeによる分散表現を行う。  
`share/grobe`内に移動し、`python main.py`を実行する。  
hydraを使用しているため`python main.py -m glove.N_gram=2,3,4,5,6,7`のように実行することでn-gramの範囲を2〜7として実行できる。

## ライブラリ
GloVe：https://nlp.stanford.edu/projects/glove/  
hydra：https://github.com/facebookresearch/hydra