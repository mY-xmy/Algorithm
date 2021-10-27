#!/usr/bin/env python
# coding=utf-8
"""
@FilePath: BinarySearch.py
@Author: Xu Mingyu
@Date: 2021-10-27 15:05:59
@LastEditTime: 2021-10-27 15:16:12
@Description: 
@Copyright 2021 Xu Mingyu, All Rights Reserved. 
"""

def BinarySearch(nums, target):
    """
    @description: 有序数组中查找目标值
    @param {*} nums
    @param {*} target
    @return {*}
    """
    left, right = 0, len(nums)-1
    while left <= right:
        mid = (left+right ) // 2
        if nums[mid] == target:
            return mid
        elif nums[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    return -1


def SearchLeftBound(nums, target):
    """
    @description: 
    @param {*} nums
    @param {*} target
    @return {*}
    """
    left, right = 0, len(nums)-1
    while left <= right:
        mid = (left+right ) // 2
        if nums[mid] == target:
            right  = mid - 1
        elif nums[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    if left >= len(nums) or nums[left] != target:
        return -1
    return left 

def searchRightBound(nums, target):
    """
    @description: 
    @param {*} nums
    @param {*} target
    @return {*}
    """
    left, right = 0, len(nums)-1
    while left <= right:
        mid = (left+right ) // 2
        if nums[mid] == target:
            left = mid + 1
        elif nums[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    if right < 0 or nums[right] != target:
        return -1
    return right