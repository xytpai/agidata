import random
import jieba
from tqdm import tqdm
from multiprocessing.pool import ThreadPool


def process_text(text: str):
    text = text.strip()
    out = [item.lower() for item in jieba.cut(text) if item != ' ']
    out = ' '.join(out)
    out = out.replace('\n', '[SEP]')
    return out


def gen_question_answer(fname: str, datas: list, parallel=False):
    print('gen_question_answer ' + fname)
    lines = []
    if not parallel:
        pbar = tqdm(total=len(datas))
        for data in datas:
            q = process_text(data['question'])
            a = process_text(data['answer'])
            line = '[BOS0] ' + q + ' [EOS] [BOS1] ' + a + ' [EOS]\n'
            lines.append(line)
            pbar.update(1)
        pbar.close()
    else:
        def gen(data):
            q = process_text(data['question'])
            a = process_text(data['answer'])
            line = '[BOS0] ' + q + ' [EOS] [BOS1] ' + a + ' [EOS]\n'
            return line
        p = ThreadPool(32)
        print('parallel gen ...')
        lines = p.map(gen, datas)
    random.shuffle(lines)
    lines = ''.join(lines)
    with open(fname, 'w') as f:
        f.write(lines)
    return
