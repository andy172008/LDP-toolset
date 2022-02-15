# -*- coding: utf-8 -*-
# @Time : 2022/1/12 4:09 下午
# @Author : 钟康维
# @File : FLH.py
# @Software: PyCharm


import numpy as np
import xxhash
import random


class FLH_USER(object):
    def __init__(self, epsilon: float, domain: list, k: int, data: int, g=2):
        super(FLH_USER, self).__init__()
        # 隐私预算
        self.epsilon = epsilon
        # 原始数据定义域
        self.domain = domain
        # 原始数据定义域长度
        self.d = len(domain)
        # 哈希函数的数量
        self.k = k
        self.g = g
        # 用户原始数据
        self.data = data
        # 扰动数据
        self.per_data = []
        # e^\epsilon
        e_epsilon = np.exp(self.epsilon)
        # 协议中的扰动概率
        self.p = e_epsilon / (e_epsilon + self.g - 1)
        self.q = 1.0 / (e_epsilon + self.g - 1)

    def run(self):
        encode_x = self.encode(self.data)
        perturb_x = self.perturb(encode_x)
        self.per_data = perturb_x

    def encode(self, data: int):
        seed = random.randint(0, self.k - 1)
        hash_data = (xxhash.xxh32(str(data), seed=seed).intdigest() % self.g)
        return seed, hash_data

    # 返回扰动后的数据
    def perturb(self, encode_list):
        per_x = encode_list[1]
        p_sample = np.random.random_sample()
        if p_sample > self.p - self.q:
            per_x = np.random.randint(0, self.g)
        return encode_list[0], per_x

    def get_per_data(self):
        return self.per_data


class FLH_SERVER(object):
    def __init__(self, epsilon: float, domain: list, k: int, per_datalist: list, g=2):
        super(FLH_SERVER, self).__init__()
        # 隐私预算
        self.epsilon = epsilon
        # 原始数据定义域
        self.domain = domain
        # 原始数据定义域长度
        self.d = len(domain)
        # 哈希函数的数量
        self.k = k
        self.g = g
        # 用户原始数据
        self.per_datalist = per_datalist
        # 用户数量
        self.n = len(per_datalist)
        # 哈希计数矩阵
        self.hash_counts = np.zeros((self.k, self.g))
        # 频率估计结果
        self.es_data = []
        # e^\epsilon
        e_epsilon = np.exp(self.epsilon)
        # 初始化hash矩阵
        matrix = np.empty((self.k, self.d))
        for i in range(0, self.k):
            for j in range(0, self.d):
                matrix[i][j] = xxhash.xxh32(str(j), seed=i).intdigest() % self.g
        self.hash_matrix = matrix
        # 协议中的扰动概率
        self.p = e_epsilon / (e_epsilon + self.g - 1)
        self.q = 1.0 / (e_epsilon + self.g - 1)

    def aggregate(self, per_data):
        seed = per_data[1]
        per_data = per_data[0]
        self.hash_counts[seed][per_data] += 1

    def estimate(self):
        def add(x):
            res = 0
            for index_x, val_x in enumerate(x):
                res += self.hash_counts[index_x, int(val_x)]
            return res

        self.aggregated_data = np.apply_along_axis(add, 0, self.hash_matrix)
        a = self.g / (self.p * self.g - 1)
        b = self.n / (self.p * self.g - 1)
        rs = a * self.aggregated_data - b
        self.es_data.append(rs)

    def get_es_data(self):
        return self.es_data