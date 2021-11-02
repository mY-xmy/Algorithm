#!/usr/bin/env python
# coding=utf-8
"""
@FilePath: String.py
@Author: Xu Mingyu
@Date: 2021-11-02 11:07:57
@LastEditTime: 2021-11-02 20:34:54
@Description: 
@Copyright 2021 Xu Mingyu, All Rights Reserved. 
"""

def KMP(pattern: str, string: str) -> int:
    """
    @description: KMP string match(LC.28) ref: https://www.zhihu.com/question/21923021
    @param {str} pattern
    @param {str} string
    @return {*}
    """
    def buildNxt(pattern):
        """
        compute prefix function
        next[x] 定义为： P[0]~P[x] 这一段字符串，使得k-前缀恰等于k-后缀的最大的k.
        """
        m = len(pattern)
        pnext = [0] * m
        index=  0
        for i in range(1, m):
            while index > 0 and pattern[index] != pattern[i]:
                index = pnext[index-1]
            if pattern[index] == pattern[i]:
                index += 1
            pnext[i] = index
        return pnext
    
    pnext = buildNxt(pattern)
    n, m = len(string), len(pattern)
    i, j = 0, 0
    while i < n and j < m:
        # MATCH
        if string[i] == pattern[j]:
            i += 1
            j += 1
        # DOES NOT MATCH
        elif j != 0:
            j = pnext[j-1]
        else:
            i += 1
    if j == m:
        return i - j
    else:
        return -1


def MinWindowSubstring(string: str, target: str) -> str:
    """
    @description: 最小覆盖子串(LC.76): 返回 string 中涵盖 target 所有字符的最小子串
    @param {str} string
    @param {str} target
    @return {*}
    """
    need = dict()
    for char in target:
            need[char] = need.get(char, 0) + 1
    cond_num = len(need)
    valid_num = 0
    cnt = dict()
    min_left, min_len = -1, float("inf")
    left, right = 0, 0
    while right < len(string):
        # extend
        char = string[right]
        cnt[char] = cnt.get(char, 0) + 1
        if cnt[char] == need.get(char, 0):
            valid_num += 1
        # shrink
        while valid_num == cond_num:
            if right - left + 1 < min_len:
                    min_len = right - left + 1
                    min_left = left
            char = string[left]
            cnt[char] -= 1
            if cnt[char] == need.get(char, 0) - 1:
                valid_num -= 1
            left += 1
        right += 1
    return "" if min_left == -1 else string[min_left: min_left + min_len]