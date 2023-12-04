### AGIDATA

To offer an easy-to-use tool for integrating agi-model training data.

#### For question & answer data generation

/data/gen.py

```python
from agidata import gen_question_answer
inputs = []
inputs.append({'question': 'What is the answer of 1 + 1 ?', 'answer': 'The answer is 2'})
gen_question_answer(inputs, 'math_qa')
```

```bash
agimerge /data/ # generate root.json 
```

#### SerializedTextDataset

```python
from tokenization import Tokenizer
from agidata import SerializedTextDataset

if __name__ == '__main__':
    tokenizer = Tokenizer('tokenizer.model')
    dataset = SerializedTextDataset('root.json', tokenizer, -1)
    for i in range(len(dataset)):
        data = dataset[i]
        info = f"{i}: {data} -> {tokenizer.decode(data)}"
        print(info)
```
