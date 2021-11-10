#!/usr/bin/env python
# coding=utf-8
"""
@FilePath: ML.py
@Author: Xu Mingyu
@Date: 2021-11-03 23:21:55
@LastEditTime: 2021-11-10 23:38:06
@Description: 
@Copyright 2021 Xu Mingyu, All Rights Reserved. 
"""
import numpy as np
import pandas as pd
import torch
import pdb

def convolution(inputs, filters, padding=(0,0), stride=(1,1)):
    """
    @description: 
    @param {*} inputs: size(N, C, H, W)
    @param {*} filters: size(D, C, h, w)
    @param {*} padding
    @param {*} stride
    @return {*}
    """
    assert inputs.shape[1] == filters.shape[1]
    inputs = np.pad(inputs, ((0,0), (0,0), (padding[0], padding[0]), (padding[1], padding[1])))

    N, C, H, W = inputs.shape
    D, C, h, w = filters.shape

    output = np.zeros((N, D, (H-h) // stride[0] + 1, (W-w) // stride[1] + 1))
    inputs = np.expand_dims(inputs, 1) # size(N, 1, C, H, W)
    filters = np.expand_dims(filters, 0) # size(1, D, C, H, W)

    for i in range(output.shape[2]):
        for j in range(output.shape[3]):
            output[:, :, i, j] = np.sum(inputs[:, :, :, i * stride[0]: i * stride[0] + h, j * stride[1]: j * stride[1] + w] * filters, axis=(2,3,4))
            
    return output

    
def convolution_backword(d_output, input, filters, padding=(0,0), stride=(1,1)):
    """
    @description: 
    @param {*} d_output: size(D, H, W)
    @param {*} input: size(C, ..., ...)
    @param {*} filter: size(D, C, h, w)
    @param {*} stride
    @param {*} 1
    @return {*}
    """
    H, W = d_output.shape
    D, C, h, w = filters.shape
    grad = np.zeros(filters.shape)
    d_output = np.expand_dims(d_output, axis=1) # size(D, 1, H, W)
    for i in range(h):
        for j in range(w):
            grad[:, :, i, j] = np.sum(d_output * input[:, i: H * stride[0]+i: stride[0], j: W * stride[1]+j: stride[1]], axis=(2,3)) # size(D, 1, H, W) * size(C, H, W)
            
    return grad

def cosine_dist(x,y):
    m, n = x.size(0), y.size(0)
    
    norm_x = x.norm(p=2, dim=1, keepdim=True).expand(m,n)
    norm_y = y.norm(p=2, dim=1, keepdim=True).expand(n,m).t()
    dist = torch.matmul(x, y.t()) / (norm_x * norm_y)
    return dist
    
def KNN(embeddings, chunk = 1024, k=50):
    topK_index= []
    topK_distance = []

    n = (embeddings.size(0) + chunk - 1) // chunk
    with torch.no_grad():
        for i in range(n):
            a = i*chunk
            b = min((i+1)*chunk, embeddings.size(0))
            x = embeddings[a:b]
            y = embeddings
            dist = cosine_dist(x,y)

            dist_desc = torch.sort(dist, descending=True)
            topK_idx, topK_dist = dist_desc[1][:, :k], dist_desc[0][:, :k] 
            topK_index.append(topK_idx)
            topK_distance.append(topK_dist)

            del x, y, dist, dist_desc
            torch.cuda.empty_cache()

    topK_index = torch.cat(topK_index, axis=0)
    topK_distance = torch.cat(topK_distance, axis=0)
   
    return topK_index, topK_distance
    
def test():
    image = np.array([[[0,0,1,0,2],[1,0,2,0,1],[1,0,2,2,0],[2,0,0,2,0],[2,1,2,2,0]],\
                  [[2,1,2,1,1],[2,1,2,0,1],[0,2,1,0,1],[1,2,2,2,2],[0,1,2,0,1]],\
                  [[2,1,1,2,0],[1,0,0,1,0],[0,1,0,0,0],[1,0,2,1,0],[2,2,1,1,1]]])
    image = image.reshape(1, *image.shape)

    f = np.array([[[[-1,0,1],[0,0,1],[1,-1,1]],[[-1,0,1],[1,-1,1],[0,1,0]],[[-1,1,1],[1,1,0],[0,-1,0]]],\
                    [[[0,1,-1],[0,-1,0],[0,-1,1]],[[-1,0,0],[1,-1,0],[1,-1,0]],[[-1,1,-1],[0,-1,-1],[1,0,0]]]])

    padding = (1,1)
    stride = (2,2)

    res = convolution(image, f, padding, stride)
    print(res.shape)
    print(res)

if __name__ == "__main__":
    test()