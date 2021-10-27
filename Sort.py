#!/usr/bin/env python
# coding=utf-8
"""
@FilePath: Sort.py
@Author: Xu Mingyu
@Date: 2021-10-27 15:25:35
@LastEditTime: 2021-10-27 16:16:21
@Description: 
@Copyright 2021 Xu Mingyu, All Rights Reserved. 
"""

def QuickSort(nums):
    """
    @description: 快速排序
    @param {*} nums
    @return {*}
    """
    def partition(nums, left, right):
        """
        @description: 双指针交替扫描
        @param {*} nums
        @param {*} left
        @param {*} right
        @return {*}
        """
        i, j = left, right
        pivot = nums[left]
        while i < j:
            while i < j and nums[j] >= pivot:
                j -= 1
            else:
                nums[i] = nums[j]
            while i < j and nums[i] < pivot:
                i += 1
            else:
                nums[j] = nums[i]
        nums[i] = pivot
        return i      
    
    def quick_sort(nums, left, right):
        if left < right:
            mid = partition(nums, left, right)
            quick_sort(nums, left, mid-1)
            quick_sort(nums, mid+1, right)
    
    left, right = 0, len(nums) - 1
    quick_sort(nums, left, right)

def MergeSort(nums):
    """
    @description: 归并排序
    @param {*} nums
    @return {*}
    """
    def merge(nums, left, mid, right):
        """
        @description: 合并
        @param {*} nums
        @param {*} left
        @param {*} mid
        @param {*} right
        @return {*}
        """
        m, n = mid - left + 1, right - mid
        arr1, arr2 = nums[left: mid+1], nums[mid+1:right+1]
        i, j, k = 0, 0, left
        while i < m and j < n:
            if arr1[i] <= arr2[j]:
                nums[k] = arr1[i]
                i += 1
            else:
                nums[k] = arr2[j]
                j += 1
            k += 1
        while i < m:
            nums[k] = arr1[i]
            i += 1
            k += 1
        while j < n:
            nums[k] = arr2[j]
            j += 1
            k += 1
        
    def merge_sort(nums, left, right):
        if left < right:
            mid = (left + right) // 2
            merge_sort(nums, left, mid)
            merge_sort(nums, mid+1, right)
            merge(nums, left, mid, right)
    
    left, right = 0, len(nums) - 1
    merge_sort(nums, left, right)

def main():
    """
    @description: 
    @param {*}
    @return {*}
    """
    nums = [2,0,2,1,1,0]
    QuickSort(nums)
    print("Result of QuickSort:", nums)

    nums = [2,0,2,1,1,0]
    MergeSort(nums)
    print("Result of MergeSort:", nums)

if __name__ == "__main__":
    main()