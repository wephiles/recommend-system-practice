"""
User-IIF
"""

import math
import sys
from collections import defaultdict
from operator import itemgetter

from RecommendSystemUserIIF.util.utils import load_data, save_data


class UserIIF(object):

    def __init__(self):
        """初始化算法类。

        """
        self.sim_matrix_path = ""
        self.origin_data = None
        self.user_sim_matrix = None

    def train(self, origin_data, sim_matrix_path=r"./RecommendSystemUserIIF/data/user_sim.pkl"):
        """训练数据

        :param origin_data: 原始数据
        :type origin_data: 字典 dict()
        :param sim_matrix_path: 用户协同矩阵文件路径
        :type sim_matrix_path: str
        :return:
        :rtype:
        """
        # UserCF.train(self, origin_data, sim_matrix_path=sim_matrix_path)  # 可以使用以前写的UserCF算法，这次自己写一个
        self.origin_data = origin_data
        self._train_init(self.origin_data)
        print("模型开始训练...", file=sys.stderr)
        try:
            print("载入用户协同矩阵...", file=sys.stderr)
            self.user_sim_matrix = load_data(sim_matrix_path)
            print("载入用户协同矩阵完成！", file=sys.stderr)
        except FileNotFoundError as e:
            print("载入用户协同矩阵失败，计算用户协同矩阵！", e, file=sys.stderr)
            self.user_sim_matrix = self.user_similarity()
        print("保存用户协同矩阵...", file=sys.stderr)
        save_data(sim_matrix_path, self.user_sim_matrix)
        print("保存用户协同矩阵完成！", file=sys.stderr)
        print("模型训练结束！", file=sys.stderr)

    def _train_init(self, origin_data):
        """初始化训练数据。

        :param origin_data: 原始数据集
        :type origin_data: 字典
        :return:
        :rtype:
        """
        print("正在初始化原始训练数据...")
        self.train = dict()
        for user, item, _ in origin_data:
            # 如果有数据，返回值，但不操作；如果没数据，那么设置其默认值为一个空的集合，并插入字典一个新元素
            self.train.setdefault(user, set())

            # 每一个用户都有一个物品集合，每个集合可以插入元素
            self.train[user].add(item)

        print("初始化原始训练数据完毕！")

    def user_similarity(self):
        """建立用户的协同过滤矩阵-UserIIF

        :return: dict 用户协同矩阵
        """
        # 建立用户-物品倒排表
        item_user = dict()
        # self.train是一个字典 {user1: {item1, item2, ...}, user2: {item3, item4, ...}}
        for user, items in self.train.items():
            for item in items:
                item_user.setdefault(item, set())  # 没有就插入set()
                item_user[item].add(user)
                # item_user是一个字典: {item1: {user1, user2, ...}, }

        # 建立用户协同矩阵
        user_sim_matrix = dict()
        N = defaultdict(int)  # 记录用户购买商品数
        # item_user是一个字典: {item1: {user1, user2, ...}, item2: {user3, user4, ...}}
        for item, users in item_user.items():
            for u in users:
                # N[u]表示用户u购买的商品数量
                N[u] += 1
                for v in users:
                    if u == v:  # 如果是同一个用户，直接略过，不用再操作
                        continue
                    user_sim_matrix.setdefault(u, defaultdict(int))  # {user: {}}
                    # 这里就能看出setdefault()函数的作用了。注意，user_sim_matrix[u][v]的初始值是0
                    user_sim_matrix[u][v] += 1. / math.log(1 + len(item_user[item]))

        # 计算相关度
        # user_sim_matrix = {user1: {user2: 0.5, user3: 0.3, ...},
        #                    user2: {user1: 0.5, user3: 0.2, ...},
        #                    ...}
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
        print("推荐算法运行中...")
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
        print("推荐算法运行完毕！")
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
