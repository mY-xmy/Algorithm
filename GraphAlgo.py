#!/usr/bin/env python
# coding=utf-8
"""
@FilePath: GraphAlgo.py
@Author: Xu Mingyu
@Date: 2021-10-27 23:21:11
@LastEditTime: 2021-10-28 01:04:06
@Description: 
@Copyright 2021 Xu Mingyu, All Rights Reserved. 
"""

from typing import List, Tuple, Dict
from queue import PriorityQueue

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

def Dijkstra(graph: List[List[int]], weight: Dict[int, Dict[int, float]], src: int, dst: int):
    """
    @description: Dijkstra(优先队列优化)
    @param {List[List[int]]} graph
    @param {Dict[int, Dict[int, float]]} weight
    @param {int} src
    @param {int} dst
    @return {*}
    """
    num_vertex = len(graph)
    dist = [float("inf")] * num_vertex
    visited = [False] * num_vertex
    dist[src] = 0
    #优先队列存放Tuple(dist, vertex)
    pq = PriorityQueue()
    pq.put((dist[src], src))
    while not pq.empty():
        u = pq.get()[1]
        visited[u] = True
        if u == dst: # 终止条件
            return dist[u]
        for v in graph[u]:
            if visited[v]:
                continue
            if u not in weight or v not in weight[u]:
                print("Error: Graph inconsistent with Weight!")
                return
            if dist[v] > dist[u] + weight[u][v]:
                dist[v] = dist[u] + weight[u][v]
                pq.put((dist[v], v))
    
    return dist[dst]


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