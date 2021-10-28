#!/usr/bin/env python
# coding=utf-8
"""
@FilePath: Structure.py
@Author: Xu Mingyu
@Date: 2021-10-28 14:31:01
@LastEditTime: 2021-10-28 14:56:26
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
        self.parent[self.find(index2)] = self.find(index1)

    def find(self, index: int) -> int:
        if self.parent[index] != index:
            self.parent[index] = self.find(self.parent[index])
        return self.parent[index]

class Trie:
    """
    Trie
    """
    def __init__(self):
        self.children = [None] * 26
        self.isEnd = False

    def insert(self, word: str) -> None:
        """
        @description: 插入
        @param {str} word
        @return {*}
        """
        node = self
        for ch in word:
            ch = ord(ch) - ord("a")
            if not node.children[ch]:
                node.children[ch] = Trie()
            node = node.children[ch]
        node.isEnd = True

    def searchPrefix(self, prefix: str) -> "Trie":
        """
        @description: 查询前缀
        @param {str} prefix
        @return {*}
        """
        node = self
        for ch in prefix:
            ch = ord(ch) - ord("a")
            if not node.children[ch]:
                return None
            node = node.children[ch]
        return node
    
    def search(self, word: str) -> bool:
        """
        @description: 查询
        @param {str} word
        @return {*}
        """
        node = self.searchPrefix(word)
        return node is not None and node.isEnd

    def startsWith(self, prefix: str) -> bool:
        return self.searchPrefix(prefix) is not None
