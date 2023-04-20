import os
import sys
import re
import random
import subprocess
import argparse
from itertools import combinations


def is_line_valid(line):
    if not (line.startswith('[BOS0] ') and line.endswith(' [EOS]\n')):
        return False
    ct_bos0 = line.count('[BOS0]')
    ct_bos1 = line.count('[BOS1]')
    ct_bos2 = line.count('[BOS2]')
    ct_eos = line.count('[EOS]')
    if ct_bos1 <= 0:
        return False
    if (ct_bos0 + ct_bos1 + ct_bos2) != ct_eos:
        return False
    pattern = r"\[BOS\d\] (?:(?!\[EOS\]).)* \[EOS\]"
    matches = re.findall(pattern, line)
    new_line = ' '.join(matches) + '\n'
    return new_line == line


def get_grouped_files(args, ends='.txtl', size_mb=4*1024):
    files = []
    for path, dir_list, file_list in os.walk(args.dir):
        for file in file_list:
            if file.endswith(ends) and 'merges' not in path:
                fname = os.path.join(path, file)
                files.append([fname, os.path.getsize(fname)/(1024**2)]) # MB
    files.sort(key=lambda x: x[1])
    print(len(files))
    print(files)
    file_groups = []
    fsize_mb = 0
    temp = []
    for file in files:
        temp.append(file)
        fsize_mb += file[1]
        if fsize_mb >= size_mb: # ~4GB per file
            file_groups.append({'files': temp, 'total_size': fsize_mb})
            fsize_mb = 0
            temp = []
    if len(temp) > 0:
        file_groups.append({'files': temp, 'total_size': fsize_mb})
    return file_groups


def write_out_file_groups(file_groups):
    os.mkdir('merges')
    out_files = []
    total_lines = 0
    for ig, group in enumerate(file_groups):
        print('Processing group ' + str(ig))
        merges = []
        for item in group['files']:
            file, fsz = item
            print('Load ' + file)
            with open(file, 'r') as f:
                lines = f.readlines()
                lines = [line for line in lines if is_line_valid(line)]
            merges += lines
        total_lines += len(merges)
        print(len(merges))
        print('Shuffling ...')
        random.shuffle(merges)
        print('Writting ...')
        ofname = str(ig).zfill(8) + '.txtl'
        ofname = os.path.join('merges', ofname)
        with open(ofname, 'w') as f:
            f.write(''.join(merges))
        out_files.append(ofname)
        print('done')
    print('total_lines: ' + str(total_lines))
    return out_files, total_lines


def shuffle_output_files(out_files):
    cbs = combinations(out_files, 2)
    for file_pairs in cbs:
        print('Shuffling ' + str(file_pairs))
        src0 = file_pairs[0]
        src1 = file_pairs[1]
        lines = []
        with open(src0, 'r') as f:
            lines += f.readlines()
        with open(src1, 'r') as f:
            lines += f.readlines()
        random.shuffle(lines)
        splen = len(lines)//2
        print('Writting ...')
        with open(src0, 'w') as f:
            f.write(''.join(lines[:splen]))
        with open(src1, 'w') as f:
            f.write(''.join(lines[splen:]))


def verify(out_files, ref_total_lines):
    print('Verifying ...')
    total_lines = 0
    for file in out_files:
        with open(file, 'r') as f:
            nlines = sum(1 for line in f)
            total_lines += nlines
            print(file + ' ' + str(nlines))
    assert total_lines == ref_total_lines
    print('ok')


if __name__ == '__main__':
    c = input('Ready to merge? [y/n]:')
    if c == 'y' or c == 'Y':
        pass
    else:
        sys.exit(1)
    parser = argparse.ArgumentParser(description='datasets/merge.py')
    parser.add_argument('--dir', type=str, required=True)
    args = parser.parse_args()
    subprocess.check_call(['rm -rf ./merges'], shell=True)
    file_groups = get_grouped_files(args)
    out_files, total_lines = write_out_file_groups(file_groups)
    shuffle_output_files(out_files)
    verify(out_files, total_lines)
