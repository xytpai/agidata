import os
import random
import json
import bisect
import torch
from torch.utils.data import Dataset, DataLoader


class DataPool:
    def __init__(self, root_info):
        self.root_info = root_info
        self.categories = sorted(self.root_info.keys())
        length = 0
        self.f_names = []
        self.f_offsets = []
        self.f_prefix_offsets = [0]
        for c in self.categories:
            for file_count in self.root_info[c]['files']:
                self.f_names.append(file_count[0])
                length += int(file_count[1])
                self.f_offsets.append(length)
                self.f_prefix_offsets.append(length)
        self.length = length
        self.fdict = {}
    
    def __fopen(self, fname):
        if self.fdict.get(fname, None) is None:
            with open(fname, 'r') as f:
                lines = f.readlines()
            self.fdict[fname] = lines
        else:
            pass

    def __len__(self):
        return self.length
    
    def __getitem__(self, index):
        file_idx = bisect.bisect_left(self.f_offsets, 1+index)
        fname = self.f_names[file_idx]
        self.__fopen(fname)
        rel_index = index - self.f_prefix_offsets[file_idx]
        data = self.fdict[fname][1+rel_index] # skip head
        data = json.loads(data)
        return data


class SerializedTextDataset(Dataset):
    def __init__(self, root_file: str, encoder: callable, ignore_index: int):
        super().__init__()
        assert os.path.isfile(root_file)
        with open(root_file, 'r') as f:
            self.root_info = json.loads(f.read())
        self.data_pool = DataPool(self.root_info)
        self.encoder = encoder
        self.ignore_index = ignore_index
    
    def __len__(self):
        return len(self.data_pool)
    
    def __getitem__(self, index):
        data = self.data_pool[index]
        seq = f"{data['question']}\n{data['answer']}"
        seq = self.encoder(seq)
        return seq # LongTensor
    
    def collate_fn(self, data):
        batch_size = len(data)
        max_n = 0
        for b in range(batch_size):
            if data[b].shape[0] > max_n:
                max_n = data[b].shape[0]
        new_data = torch.full((batch_size, max_n), self.ignore_index).long()
        for b in range(batch_size):
            new_data[b, :data[b].shape[0]] = data[b]
            new_data[b, :data[b].shape[0]] = data[b]
        return new_data


if __name__ == '__main__':
    root = 'gptdataset'
    SerializedTextDataset(root)

