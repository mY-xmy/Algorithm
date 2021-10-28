#!/usr/bin/env python
# coding=utf-8
"""
@FilePath: Structure.py
@Author: Xu Mingyu
@Date: 2021-10-28 14:31:01
@LastEditTime: 2021-10-28 15:09:40
@Description: 
@Copyright 2021 Xu Mingyu, All Rights Reserved. 
"""
class UnionFindSet:
    """
    UnionFindSet
    """
    def __init__(self, n):
        self.parent = list(range(n))

    def union(self, index1: int, index2: int):
        """
        @description: 合并
        @param {int} index1
        @param {int} index2
        @return {*}
        """
        self.parent[self.find(index2)] = self.find(index1)

    def find(self, index: int) -> int:
        """
        @description: 查询
        @param {int} index
        @return {*}
        """
        if self.parent[index] != index:
            self.parent[index] = self.find(self.parent[index])
        return self.parent[index]

class Trie:
    """
    Trie
    """
    def __init__(self):
        self.children = [None] * 26
        self.isEnd=False

    def insert(self, word: str) -> None:
        """
        @description: 插入
        @param {str} word
        @return {*}
        """
        cur = self
        for char in word:
            idx = ord(char) - ord("a")
            if cur.children[idx] is None:
                cur.children[idx] = Trie()
            cur = cur.children[idx]
        cur.isEnd = True

    def search(self, word: str) -> bool:
        """
        @description: 查询
        @param {str} word
        @return {*}
        """
        cur = self
        for char in word:
            if cur is None:
                return False
            idx = ord(char) - ord("a")
            cur = cur.children[idx]
        return cur is not None and cur.isEnd

    def startsWith(self, prefix: str) -> bool:
        """
        @description: 查询前缀
        @param {str} prefix
        @return {*}
        """
        cur = self
        for char in prefix:
            if cur is None:
                return False
            idx = ord(char) - ord("a")
            cur = cur.children[idx]
        return cur is not None
