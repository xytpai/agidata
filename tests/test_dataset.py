
from tokenization import Tokenizer
from agidata import SerializedTextDataset


if __name__ == '__main__':
    tokenizer = Tokenizer('tokenizer.model')
    dataset = SerializedTextDataset('root.json', tokenizer, -1)
    for i in range(len(dataset)):
        data = dataset[i]
        info = f"{i}: {data} -> {tokenizer.decode(data)}"
        print(info)
