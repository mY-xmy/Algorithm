#!/usr/bin/env python
# coding=utf-8
"""
@FilePath: GraphAlgo.py
@Author: Xu Mingyu
@Date: 2021-10-27 23:21:11
@LastEditTime: 2021-10-28 11:30:52
@Description: 
@Copyright 2021 Xu Mingyu, All Rights Reserved. 
"""

from typing import List, Tuple, Dict, Optional
from queue import PriorityQueue
from collections import deque

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

def Dijkstra(graph: Dict[int, Dict[int, float]], src: int, dst: Optional[int] = None):
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
        if dst is not None and u == dst: # 终止条件
            return dist[u]
        for v in graph[u]:
            if visited[v]:
                continue
            if dist[v] > dist[u] + graph[u][v]:
                dist[v] = dist[u] + graph[u][v]
                pq.put((dist[v], v))
    
    return dist[dst] if dst is not None else dist

def BellmanFord(graph: Dict[int, Dict[int, float]], src: int, dst: Optional[int] = None):
    num_vertex = len(graph)
    dist = [float("inf")] * num_vertex
    visited = [False] * num_vertex
    dist[src] = 0
    queue = deque()
    queue.append(src)
    visited[src] = True

    for _ in range(num_vertex-1):
        if not queue:
            break
        n = len(queue)
        for i in range(n):
            u = queue.popleft()
            visited[u] = False
            for v in graph[u]:
                if dist[v] > dist[u] + graph[u][v]:
                    dist[v] = dist[u] + graph[u][v]
                    if not visited[v]:
                        queue.append(v)
                        visited[v] = True
    
    for u in graph:
        for v in graph[u]:
            if dist[v] > dist[u] + graph[u][v]:
                raise ValueError("Error: There exists negative cycle in graph!")
    
    return dist[dst] if dst is not None else dist
    


def main():
    """
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
    """
    non_negative_graph = {
        0: {1: 3, 2: 2, 3: 4},
        1: {2: 4},
        2: {3: 1},
        3: {}
    }
    negative_graph = {
        0: {1: -1, 2:  4},
        1: {2:  2, 3:  3, 4:  2},
        2: {},
        3: {1:  3, 2:  5},
        4: {3: -3}
    }
    print("Original Non-negative Graph:", non_negative_graph)
    print("Result of Dijkstra:", Dijkstra(non_negative_graph, 0))
    print("Result of Bellman-Ford:", BellmanFord(non_negative_graph, 0))

    print("Original Negative Graph:", negative_graph)
    print("Result of Dijkstra:", Dijkstra(negative_graph, 0))
    print("Result of Bellman-Ford:", BellmanFord(negative_graph, 0))

if __name__ == "__main__":
    main()