#!/usr/bin/python
# -*- coding: UTF-8 -*-
import os

import numpy as np
import torch.nn as nn
import torch
from model_service.pytorch_model_service import PTServingBaseService

class Linear(nn.Module):
    def __init__(self, in_dim, 
                 n_hidden_1, n_hidden_2,
                 out_dim, dropout_p=0.5):
        super().__init__()
        self.layer1 = nn.Linear(in_dim, n_hidden_1)
        self.layer2 = nn.Linear(n_hidden_1, n_hidden_2)
        self.layer3 = nn.Linear(n_hidden_2, out_dim)
        self.relu = nn.ReLU()
        self.dropout = nn.Dropout(p=dropout_p)
        self.softmax = nn.Softmax(dim=-1)
 
    def forward(self, x):
        x = self.layer1(x)
        x = self.relu(x)
        x = self.dropout(x)
        x = self.layer2(x)
        x = self.relu(x)
        x = self.dropout(x)
        x = self.layer3(x)
        x = self.softmax(x)
        return x

class PredictService(PTServingBaseService):
    def __init__(self, model_name, model_path):
        super(PredictService, self).__init__(model_name, model_path)

        model = Linear(1999, 1024, 512,3, dropout_p=0.)
        #model = Linear(1999, 512,512,512, 3, dropout_p=0.)
        model.load_state_dict(torch.load(model_path, map_location ='cpu'))
        model.eval()
        self.model = model
        self.load_preprocess()

    def load_preprocess(self, mean_name='mean.npy', std_name='std.npy'):
      dir_path = os.path.dirname(os.path.realpath(self.model_path))

      mean_path = os.path.join(dir_path, mean_name)
      std_path = os.path.join(dir_path, std_name)
      self.mean = np.load(mean_path)
      self.std = np.load(std_path)

    def _preprocess(self, data):
        print('pre_data:{}'.format(data))
        preprocessed_data = {}

        for d in data:
            for k, v in data.items():
                for file_name, features_path in v.items():
                    x = np.load(features_path)
                    # deploy environment numpy version
                    x = (x - self.mean) / self.std
                    x = np.nan_to_num(x)
                    x[x>1000000] = 0
                    x[x<-1000000] = 0
                    x = torch.from_numpy(x).to(torch.float32)
                    preprocessed_data[k] = x
        return preprocessed_data

    def _postprocess(self, data):
        print('post_data:{}'.format(data))
        infer_output = {}

        for output_name, result in data.items():
            infer_output['scores'] = result.tolist()

        return infer_output
