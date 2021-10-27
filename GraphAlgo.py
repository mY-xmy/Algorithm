#!/usr/bin/env python
# coding=utf-8
"""
@FilePath: GraphAlgo.py
@Author: Xu Mingyu
@Date: 2021-10-27 23:21:11
@LastEditTime: 2021-10-27 23:55:24
@Description: 
@Copyright 2021 Xu Mingyu, All Rights Reserved. 
"""

from typing import List, Tuple, Dict

def TopologicalSort(graph: List[List[int]]):
    """
    @description: 拓扑排序（含环检测）
    @param {List} graph
    @return {*}
    """
    num_vertex = len(graph)
    inDegree = [0] * num_vertex
    for u in range(num_vertex):
        for v in graph[u]:
            inDegree[v] += 1
    queue = [u for u in range(num_vertex) if inDegree[u] == 0]
    sequence = list()
    while queue:
        u = queue.pop()
        sequence.append(u)
        for v in graph[u]:
            inDegree[v] -= 1
            if not inDegree[v]:
                queue.append(v)
    if len(sequence) == num_vertex:
        return sequence
    else:
        print("Error: there exists circle in graph!")
        return False

def main():
    G = [
        [1,5],
        [2,3,5],
        [3],
        [4,5],
        [5],
        []
    ]
    print("Original Graph:", G)
    print("Result of Topological Sort:", TopologicalSort(G))

if __name__ == "__main__":
    main()