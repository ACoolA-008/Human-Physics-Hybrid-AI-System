import numpy as np
import os, shutil
import pickle
import random
import torch
from torch.utils.data import Dataset, DataLoader

import cv2

class InputHandle(Dataset):
    def __init__(self, input_param):
        self.input_data_type = input_param.get('input_data_type', 'float32')
        self.output_data_type = input_param.get('output_data_type', 'float32')
        self.img_width = input_param['image_width']
        self.img_height = input_param['image_height']
        self.length = input_param['total_length']
        self.data_path = input_param['data_path']
        self.type = input_param['type'] #train/test/valid
        self.annotation_mask_path = input_param.get('annotation_mask_path', None)

        self.case_list = []
        name_list = os.listdir(self.data_path)
        name_list.sort()
        for name in name_list:
            case = []
            for i in range(29):
                case.append(self.data_path + '/' + name + '/' + name + '-' + str(i).zfill(2) + '.png')
            self.case_list.append(case)

        # If annotation masks are provided, build mask paths
        if self.annotation_mask_path is not None:
            self.mask_list = []
            for name in name_list:
                # Assumes one mask per case, named as 'mask.png' in each folder
                mask_path = os.path.join(self.annotation_mask_path, name, 'mask.png')
                self.mask_list.append(mask_path)
        else:
            self.mask_list = None

    def load(self, index):
        data = []
        for img_path in self.case_list[index]:
            img = cv2.imread(img_path, 2)
            data.append(np.expand_dims(img, axis=0))
        data = np.concatenate(data, axis=0).astype(self.input_data_type) / 10.0 - 3.0
        assert data.shape[1]<=1024 and data.shape[2]<=1024 
        return data

    def __getitem__(self, index):
        data = self.load(index)[-self.length:].copy()

        mask = np.ones_like(data)
        mask[data < 0] = 0
        data[data < 0] = 0
        data = np.clip(data, 0, 128)
        vid = np.zeros((self.length, self.img_height, self.img_width, 2))
        vid[..., 0] = data
        vid[..., 1] = mask
        img = dict()
        img['radar_frames'] = vid
        # Load annotation mask if available
        if self.mask_list is not None:
            mask_path = self.mask_list[index]
            if os.path.exists(mask_path):
                ann_mask = cv2.imread(mask_path, 0)  # Load as grayscale
                ann_mask = cv2.resize(ann_mask, (self.img_width, self.img_height))
                img['annotation_mask'] = ann_mask
            else:
                img['annotation_mask'] = np.zeros((self.img_height, self.img_width), dtype=np.uint8)
        return img

    def __len__(self):
        return len(self.case_list)
