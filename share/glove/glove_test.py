import os

class GloVe():
    def __init__(
        self, 
        n_gram_value: int, 
        vocab_min_word_count: int = 1,
        verbose: int = 2,
        memory: int = 40,
        window_size: int= 10,
        threads: int = 20,
        x_max: int = 100,
        iter_num: int = 10,
        vector_size: int = 200,
        binary: int = 2

        ):
        self.N = n_gram_value
        self.vocab_min_word_count = vocab_min_word_count
        self.verbose = verbose
        self.memory = memory
        self.window_size = window_size
        self.threads = threads
        self.x_max = x_max
        self.iter_num = iter_num
        self.vector_size = vector_size
        self.binary = binary

    # ボキャブラリー作成
    def make_vocab(self):
        vocab_count = "/Workspace/glove/glove/build/vocab_count"
        vocab_min_word_count = f"-min-count {self.vocab_min_word_count}"
        vocab_verbose = f"-verbose {self.verbose}"
        vocab_input_file = f"{self.N}_corpus.txt"
        vocab_output_file = f"{self.N}_vocab.txt"
        vocab_command_list = [
            vocab_count, vocab_min_word_count, vocab_verbose, "-max-vocab 100000", "<", vocab_input_file, ">", vocab_output_file
            ]
        vocab_command = " ".join(vocab_command_list)
        os.system(vocab_command)

    # 共起行列計算
    def cooccur(self):
        input_file = f"{self.N}_corpus.txt"
        cooccur = "/Workspace/glove/glove/build/cooccur"
        memory = f"-memory {self.memory}"
        vocab_file = f"-vocab-file {self.N}_vocab.txt"
        window_size = f"-window-size {self.window_size}"
        output_file = f"{self.N}_cooccurrence.txt"
        command_list = [cooccur, memory, vocab_file, window_size, "<", input_file, ">", output_file]
        command = " ".join(command_list)
        os.system(command)

    # 共起行列のシャッフル
    def shuffle(self):
        shuffle = "/Workspace/glove/glove/build/shuffle"
        output_file = f"{self.N}_cooccurrence_shuffle"
        memory = f"-memory {self.memory}"
        verbose = f"-verbose {self.verbose}"

        command_list = [shuffle, memory, verbose, "<", f"{self.N}_cooccurrence.txt", ">", output_file]
        command = " ".join(command_list)
        os.system(command)

    # 分散表現作成
    def make_glove(self):
        glove = "/Workspace/glove/glove/build/glove"
        save_file = f"-save-file {self.N}_vectors"
        threads = f"-threads {self.threads}"
        input_file = f"-input-file {self.N}_cooccurrence_shuffle"
        x_max = f"-x-max {self.x_max}"
        iter_num  = f"-iter {self.iter_num}"
        vector_size = f"-vector-size {self.vector_size}"
        binary = f"-binary {self.binary}"
        vocab_file = f"-vocab-file {self.N}_vocab.txt"
        command_list = [glove, save_file, threads, input_file, x_max, iter_num, vector_size, binary, vocab_file]
        command = " ".join(command_list)
        os.system(command)

    def __call__(self):
        self.make_vocab()
        self.cooccur()
        self.shuffle()
        self.make_glove()

if __name__ == "__main__":
    glove = GloVe(10)
    glove()
