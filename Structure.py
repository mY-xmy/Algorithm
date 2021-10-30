#!/usr/bin/env python
# coding=utf-8
"""
@FilePath: Structure.py
@Author: Xu Mingyu
@Date: 2021-10-28 14:31:01
@LastEditTime: 2021-10-30 22:41:12
@Description: 
@Copyright 2021 Xu Mingyu, All Rights Reserved. 
"""
from collections import defaultdict, deque

class UnionFindSet:
    """
    UnionFindSet
    - union(index1, index2): 合并index1和index2所属集合
    - find(index): 查找index结点的父结点（含路径压缩）
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
    - insert(word): 插入单词word
    - search(word): 查询单词word. 如果字符串 word 在前缀树中，返回 true；否则，返回 false.
    - startsWith(prefix): 如果之前已经插入的字符串 word 的前缀之一为 prefix ，返回 true ；否则，返回 false 。
    """
    def __init__(self):
        self.children = [None] * 26
        self.isEnd=False

    def insert(self, word: str) -> None:
        cur = self
        for char in word:
            idx = ord(char) - ord("a")
            if cur.children[idx] is None:
                cur.children[idx] = Trie()
            cur = cur.children[idx]
        cur.isEnd = True

    def search(self, word: str) -> bool:
        cur = self
        for char in word:
            if cur is None:
                return False
            idx = ord(char) - ord("a")
            cur = cur.children[idx]
        return cur is not None and cur.isEnd

    def startsWith(self, prefix: str) -> bool:
        cur = self
        for char in prefix:
            if cur is None:
                return False
            idx = ord(char) - ord("a")
            cur = cur.children[idx]
        return cur is not None

class DeLinkedNode:
    """
    双向链表结点
    """
    def __init__(self, key = 0, value = 0):
        self.key = key
        self.value = value
        self.prev = None
        self.next = None
    
class DeLinkedList:
    """
    双向链表
    """
    def __init__(self):
        self.head = DeLinkedNode()
        self.tail = DeLinkedNode()
        self.head.next, self.tail.prev = self.tail, self.head
        self.length = 0

    def insertNode(self, node: "DeLinkedNode", index: int = 0):
        if index > self.length:
            raise IndexError("DeLinkedList index out of range")
        cur = self.head
        for _ in range(index):
            cur = cur.next
        node.next, node.prev = cur.next, cur
        cur.next.prev = node
        cur.next = node
        self.length += 1
        
    def removeNode(self, node):
        node.prev.next = node.next
        node.next.prev = node.prev
        self.length -= 1
        return node

class LRUCache:
    """
    Least Recently Used Cache
    - get(key): 获取数据. 如果密钥 (key) 存在于缓存中，则获取密钥的值（总是正数），否则返回 -1。
    - put(key, value): 写入数据. 如果密钥不存在，则写入其数据值。当缓存容量达到上限时，它应该在写入新数据之前删除最近最少使用的数据值，从而为新的数据值留出空间。
    """
    def __init__(self, capacity: int):
        if capacity < 0:
            raise ValueError("capacity must be non negative")
        self.capacity = capacity
        self.size = 0
        self.map = dict()
        self.cache = DeLinkedList()
    
    def get(self, key: int) -> int:
        if key not in self.map:
            return -1
        node = self.map[key]
        self.makeRecently(node)
        return node.value

    def put(self, key: int, value: int) -> None:
        if not self.capacity:
            return
            
        if key in self.map:
            node = self.map[key]
            node.value = value
            self.makeRecently(node)
        else:
            node = DeLinkedNode(key=key, value=value)
            self.map[key] = node
            self.cache.insertNode(node, index=0)
            self.size += 1
            if self.size > self.capacity:
                node = self.cache.removeNode(self.cache.tail.prev)
                self.map.pop(node.key)
                self.size -= 1
        
    def makeRecently(self, node: "DeLinkedNode") -> None:
        node = self.cache.removeNode(node)
        self.cache.insertNode(node, index=0)

class LFUCache:
    """
    Least Frequently Used Cache
    - get(key): 获取数据. 如果密钥 (key) 存在于缓存中，则获取密钥的值（总是正数），否则返回 -1。
    - put(key, value): 写入数据. 如果密钥不存在，则写入其数据值。当缓存容量达到上限时，它应该在写入新数据之前删除最不经常使用使用/(最近最久未使用)的项，从而为新的数据值留出空间。
    """
    def __init__(self, capacity: int): 
        if capacity < 0:
            raise ValueError("capacity must be non negative")
        self.capacity = capacity
        self.size = 0
        self.minFreq = 0
        self.map = dict()
        self.freq = dict()
        self.cache = defaultdict(DeLinkedList)
    
    def get(self, key: int) -> int:
        if key not in self.map:
            return -1
        self.makeRecently(key)
        node = self.map[key]
        return node.value

    def put(self, key: int, value: int) -> None:
        if not self.capacity:
            return

        if key in self.map:
            node = self.map[key]
            node.value = value
            self.makeRecently(key)
        else:
            if self.size >= self.capacity:
                node = self.cache[self.minFreq].removeNode(self.cache[self.minFreq].tail.prev)
                self.map.pop(node.key)
                self.freq.pop(node.key)
                self.size -= 1
            node = DeLinkedNode(key=key, value=value)
            self.map[key] = node
            self.freq[key] = 1
            self.cache[1].insertNode(node, index=0)
            self.size += 1
            self.minFreq = 1
    
    def makeRecently(self, key: int) -> None:
        freq, node = self.freq[key], self.map[key]
        node = self.cache[freq].removeNode(node)
        self.cache[freq+1].insertNode(node, index=0)
        self.freq[key] += 1
        if freq == self.minFreq and self.cache[freq].head.next == self.cache[freq].tail:
            self.minFreq += 1


class BTree:
    """
    Binary Tree
    """
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

    def preorder(self):
        left, right = [], []
        if self.left:
            left = self.left.preorder()
        if self.right:
            right = self.right.preorder()
        return [self.val] + left + right

    def inorder(self):
        left, right = [], []
        if self.left:
            left = self.left.inorder()
        if self.right:
            right = self.right.inorder()
        return left + [self.val] + right
    
    def postorder(self):
        left, right = [], []
        if self.left:
            left = self.left.postorder()
        if self.right:
            right = self.right.postorder()
        return left + right + [self.val]
    def levelorder(self):
        res = []
        queue = deque()
        queue.append(self)
        while queue:
            node = queue.popleft()
            res.append(node.val)
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)
        return res
    
def create_BTree(nums):
    def recur(index):
        if index >= len(nums) or nums[index] is None:
            return None
        root = BTree(nums[index])
        root.left = recur(2 * index + 1)
        root.right = recur(2 * index + 2)
        return root

    return recur(0)