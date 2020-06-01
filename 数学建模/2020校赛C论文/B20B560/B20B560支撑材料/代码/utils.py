import numpy as np


## x: 自变量分布; mu: 均值; sigma: 标准差
def Normal(x,mu=0,sigma=1):
    normal = np.exp(-((x - mu)**2)/(2*sigma**2)) / (sigma * np.sqrt(2*np.pi))
    return normal


def get_traffic(F, dur=30, bias=15):
    P = np.zeros(len(F))
    s = 0
    for i in range(len(F)):
        s += F[i]
        if i >= dur:
            s -= F[i-dur]
        P[i] = s
    return P


def get_accumulation(F):
    P = np.zeros(len(F))
    s = 0
    for i in range(len(F)):
        s += F[i]
        P[i] = s
    return P


def get_erosion(F, Ori):
    P = np.zeros(len(F))
    s = Ori
    for i in range(len(F)):
        s -= F[i]
        P[i] = s
    return P


def load_graph():
    nodes = ['DX','HT', 'ZY', 'DC', 'HC', 'ZC', 'AB', 'CD', 'EFG']
    with open('./data/mapdata.txt') as data:
        edges = data.readlines()
        for i in range(len(edges)):
            edges[i] = edges[i].split(' ')
            edges[i][2] = int(edges[i][2])
            edges[i] = tuple(edges[i])
    return nodes, edges


if __name__ == '__main__':
    pass