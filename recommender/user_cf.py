# user-cf 基于用户的协同过滤算法

import os
from collections import defaultdict
import math
from operator import itemgetter
import sys
from utils.utils import save_data, load_data


class UserCF(object):
    def __init__(self):
        self.sim_matrix_path = ""
        self.origin_data = None
        self.user_sim_matrix = None

    def train(self, origin_data, sim_matrix_path="./data/user_sim.pkl"):
        """模型训练
        
        :param origin_data: 原始数据。
        :sim_matrix_path: 协同矩阵保存的路径。
        :return: 
        """
        self.origin_data = origin_data
        self._init_train(origin_data)
        print("开始模型训练...", file=sys.stderr)
        try:
            print("开始载入用户协同矩阵...", file=sys.stderr)
            self.sim_matrix_path = load_data(sim_matrix_path)
            print("载入用户协同矩阵完成。", file=sys.stderr)
        except BaseException:
            print("载入用户过滤矩阵失败，请重新计算用户矩阵。", file=sys.stderr)
            # 计算用户相似度
            self.user_sim_matrix = self.user_similarity()
        print("开始保存用户协同矩阵", file=sys.stderr)
        save_data(sim_matrix_path, self.user_sim_matrix)
        print("保存用户协同矩阵完成", file=sys.stderr)

    def _init_train(self, origin_data):
        """初始化训练数据集

        :param origin_data: 原始数据
        """
        self.train = dict()
        for user, item, _ in origin_data:
            self.train.setdefault(user, set())
            self.train[user].add(item)

    def user_similarity(self):
        """建立用户协同矩阵。

        :return: 字典，用户协同矩阵
        """
        # 建立用户-物品倒排表
        item_user = dict()
        for user, items in self.train.items():
            for item in items:
                item_user.setdefault(item, set())
                item_user[item].add(user)
        # 建立用户协同矩阵
        user_sim_matrix = dict()
        N = defaultdict(int)  # 记录用户购买商品数
        for item, users in item_user.items():
            for u in users:
                N[u] += 1
                for v in users:
                    if u == v:
                        continue
                    user_sim_matrix.setdefault(u, defaultdict(int))
                    user_sim_matrix[u][v] += 1

        # 计算相关度
        for u, related_users in user_sim_matrix.items():
            for v, con_items_count in related_users.items():
                user_sim_matrix[u][v] = con_items_count / math.sqrt(N[u] * N[v])
        return user_sim_matrix

    def recommend(self, user, N, K):
        """给user用户推荐。
        
        :param user: 用户
        :param N: 推荐的商品个数
        :param K: 查找最相似的用户个数
        :return: 商品字典{商品： 相似性打分情况}
        """
        related_items = self.train.get(user, set)
        recommends = dict()
        for v, sim in sorted(self.user_sim_matrix.get(user, dict).items(),
                             key=itemgetter(1),
                             reverse=True)[:K]:
            for item in self.train[v]:
                if item in related_items:
                    continue
                recommends.setdefault(item, 0)
                recommends[item] += sim
        return dict(sorted(recommends.items(), key=itemgetter(1), reverse=True)[:N])

    def recommend_users(self, users, N, K):
        """推荐测试集

        :param users: 用户列表
        :param N: 推荐的商品个数
        :param K: 查找最相似的用户个数
        :return: 推荐字典 { 用户： 推荐商品的list }
        """
        recommends = dict()

        for user in users:
            user_recommends = list(self.recommend(user, N, K).keys())
            recommends[user] = user_recommends
        return recommends

