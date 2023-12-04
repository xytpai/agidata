import os
import json
import random
import hashlib
from tqdm import tqdm
from multiprocessing.pool import ThreadPool


def process_text(text: str):
    return text.strip()


def gen_question_answer(datas: list, category: str, out_dir: str = './', parallel=False, shuffle=False):
    assert os.path.isdir(out_dir)

    def gen(data):
        q = process_text(data['question'])
        a = process_text(data['answer'])
        jsonline = json.dumps({'question':q, 'answer':a}, ensure_ascii=False)
        return jsonline
    
    lines = []
    if not parallel:
        pbar = tqdm(total=len(datas))
        for data in datas:
            lines.append(gen(data))
            pbar.update(1)
        pbar.close()
    else:
        num_cores = os.cpu_count()
        p = ThreadPool(num_cores)
        print(f'parallel gen cores:{num_cores} ...')
        lines = p.map(gen, datas)
    
    if shuffle:
        random.shuffle(lines)
    
    data_info = {
        'category': category,
        'count': len(lines)
    }
    lines = [json.dumps(data_info, ensure_ascii=False)] + lines
    lines = '\n'.join(lines)

    md5hash = hashlib.md5()
    md5hash.update(lines.encode('utf-8'))
    hash_string = str(md5hash.hexdigest()) + '.agidata'
    
    fname = os.path.join(out_dir, hash_string)
    with open(fname, 'w') as f:
        f.write(lines)
    
    print(f'agidata:done {fname}')

    return
