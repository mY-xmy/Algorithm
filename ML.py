#!/usr/bin/env python
# coding=utf-8
"""
@FilePath: ML.py
@Author: Xu Mingyu
@Date: 2021-11-03 23:21:55
@LastEditTime: 2021-11-04 22:59:04
@Description: 
@Copyright 2021 Xu Mingyu, All Rights Reserved. 
"""
import numpy as np

def convolution(inputs, filters, padding=(0,0), stride=(1,1)):
    """
    @description: 
    @param {*} inputs: size(N, C, H, W)
    @param {*} filters: size(D, C, h, w)
    @param {*} padding
    @param {*} stride
    @return {*}
    """
    assert inputs.shape[0] == filters.shape[1]
    N, C, H, W = inputs.shape
    D, C, h, w = filters.shape

    output = np.zeros(N, D, ((H-h) // stride[0] + 1, (W-w) // stride[1] + 1))
    inputs = np.expand_dims(inputs, 1) # size(N, 1, C, H, W)
    filters = np.expand_dims(filters, 0) # size(1, D, C, H, W)

    for i in range(output.shape[2]):
        for j in range(output.shape[3]):
            output[:, :, i, j] = np.sum(inputs[:, i * stride[0]: i * stride[0] + h, j * stride[1]: j * stride[1] + w] * filters, axis=(2,3,4))
            
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
    
    