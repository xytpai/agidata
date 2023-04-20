import random
import jieba
from tqdm import tqdm


def process_text(text: str):
    text = text.strip()
    out = [item.lower() for item in jieba.cut(text) if item != ' ']
    out = ' '.join(out)
    out = out.replace('\n', '[SEP]')
    return out


def gen_question_answer(name: str, datas: list):
    print('gen_question_answer ' + name)
    pbar = tqdm(total=len(datas))
    lines = []
    for data in datas:
        q = process_text(data['question'])
        a = process_text(data['answer'])
        line = '[BOS0] ' + q + ' [EOS] [BOS1] ' + a + ' [EOS]\n'
        lines.append(line)
        pbar.update(1)
    random.shuffle(lines)
    lines = ''.join(lines)
    pbar.close()
    return lines
