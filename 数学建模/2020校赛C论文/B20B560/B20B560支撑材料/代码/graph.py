import numpy as np

class Graph(object):

    # 初始化
    # size: 结点个数
    def __init__(self, nodes, edges):

        # 存储变量
        self.Inf = 10 ** 9
        self.nodes = nodes
        self.edges = edges
        self.size = len(nodes)

        # 初始化ID字典 (对结点标号)
        self.idx = dict()
        for i in range(self.size):
            self.idx[nodes[i]] = i

        # 初始化邻接矩阵
        self.graph = [[self.Inf for i in range(self.size)] for j in range(self.size)]
        for node in range(self.size):
            self.graph[node][node] = 0
        for edge in edges:
            self.add_edge(*edge)

        # 初始化更新标记
        self.update = False


    # 添加边
    def add_edge(self, u, v, w=1):
        self.graph[self.idx[u]][self.idx[v]] = w
        self.graph[self.idx[v]][self.idx[u]] = w
        self.update = False


    # 获取边
    def get_edge(self, u, v):
        return self.graph[self.idx[u]][self.idx[v]]


    # 获取两点间最短距离
    def get_min_distance(self, u, v):
        if not self.update:
            self.flyod()
        return self.graph[self.idx[u]][self.idx[v]]


    # flyod 算法求最短路
    def flyod(self):
        for k in range(self.size):
            for u in range(self.size):
                for v in range(self.size):
                    self.graph[u][v] = min(self.graph[u][v], self.graph[u][k] + self.graph[k][v])
        self.update = True


    # 求结点的权重
    # P: 一维数组， 表示各个结点的人流量
    # 返回 结点权重列表
    def get_weight(self, P):
        weight = dict()
        for u in range(self.size):
            weight[self.nodes[u]] = 0
            for v in range(self.size):
                weight[self.nodes[u]] += (self.graph[u][v] / 100 + 1) ** -1 * P[v]
        return weight
