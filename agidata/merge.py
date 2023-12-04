import os
import sys
import json
import subprocess
from collections import defaultdict


def main():
    root = str(sys.argv[1]).strip()
    root = os.path.abspath(root)
    assert os.path.isdir(root)
    froot = os.path.join(root, 'root.json')

    c = input(f'Ready gen {froot} ? [y/n]:')
    if c == 'y' or c == 'Y':
        pass
    else:
        sys.exit(1)
    
    subprocess.check_call([f'rm -rf {froot}'], shell=True)

    data_file_list = []
    for path, _, file_list in os.walk(root):
        for file in file_list:
            if file.endswith('.agidata'):
                data_file_list.append(os.path.join(path, file))
    
    data = defaultdict(list)
    total = defaultdict(int)
    
    for file in data_file_list:
        with open(file, 'r') as f:
            head = f.readline()
            head = json.loads(head)
            category = head['category']
            count = head['count']
            data[category].append([file, count])
            total[category] += count
    
    data_ = {}
    for k, v in data.items():
        data_[k] = {
            'count': total[k],
            'files': v
        }
    
    with open(froot, 'w') as f:
        f.write(json.dumps(data_, indent=4, ensure_ascii=False))
