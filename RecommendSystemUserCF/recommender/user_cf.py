# user-cf 基于用户的协同过滤算法

import os
from collections import defaultdict
import math
from operator import itemgetter
import sys
from RecommendSystemUserCF.utils.utils import save_data, load_data
import pandas as pd


class UserCF(object):
    def __init__(self):
        self.sim_matrix_path = ""
        self.origin_data = None
        self.user_sim_matrix = None

    def train(self, origin_data, sim_matrix_path="./RecommendSystemUserCF/data/sim_matrix.pkl"):
        """模型训练
        
        :param origin_data: 原始数据。
        :param sim_matrix_path: 协同矩阵保存的路径。
        :return: 
        """
        self.origin_data = origin_data
        self._init_train(origin_data)
        print("开始模型训练...", file=sys.stderr)
        try:
            print("开始载入用户协同矩阵...", file=sys.stderr)
            self.user_sim_matrix = load_data(sim_matrix_path)
            print("载入用户协同矩阵完成。", file=sys.stderr)
        except FileNotFoundError:
            print("载入用户过滤矩阵失败，请重新计算用户矩阵。", file=sys.stderr)
            # 计算用户相似度
            self.user_sim_matrix = self.user_similarity()
        print("开始保存用户协同矩阵", file=sys.stderr)
        save_data(sim_matrix_path, self.user_sim_matrix)
        print("保存用户协同矩阵完成", file=sys.stderr)
        print("模型训练完毕")

    def _init_train(self, origin_data):
        """初始化训练数据集

        :param origin_data: 原始数据
        """
        print("正在初始化数据...")
        self.train = dict()
        for user, item, _ in origin_data:
            self.train.setdefault(user, set())
            self.train[user].add(item)
        print("初始化数据完毕。")

    def user_similarity(self):
        """建立用户协同矩阵。

        :return: 字典，用户协同矩阵
        """
        # 建立用户-物品倒排表
        print("建立用户-物品倒排表...")
        item_user = dict()
        for user, items in self.train.items():
            for item in items:
                item_user.setdefault(item, set())  # setdefault方法等价于dict里面的get方法
                item_user[item].add(user)
        print("建立用户-物品倒排表完毕")
                
        # 建立用户协同矩阵
        print("计算用户协同矩阵...")
        user_sim_matrix = dict()
        N = defaultdict(int)  # 记录用户购买商品数 N={}

        # defaultdict表示如果查找字典键值的时候没有这个键，那么就加入这个键
        # 并将键的初值置为0

        for item, users in item_user.items():
            for u in users:
                N[u] += 1  # dict["key"]
                for v in users:
                    if u == v:
                        continue
                    user_sim_matrix.setdefault(u, defaultdict(int))
                    user_sim_matrix[u][v] += 1
        print("计算用户协同矩阵完毕")

        # 计算相关度
        print("计算相关度...")

        # 下面代码本人不是很懂
        for u, related_users in user_sim_matrix.items():
            for v, con_items_count in related_users.items():
                user_sim_matrix[u][v] = con_items_count / math.sqrt(N[u] * N[v])
        print("计算相关度完毕")
        
        print("整个用户协同矩阵建立完毕。")
        
#         print("正在使用pandas dataframe化...")
#         df = pd.DataFrame(user_sim_matrix)
#         print("pandas dataframe化完毕")
        
#         print(df.head(10))
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
        :return: 推荐字典 { 用户： 推荐商品的list,  用户： 推荐商品的list, ...}
        """
        recommends = dict()

        for user in users:
            user_recommends = list(self.recommend(user, N, K).keys())
            recommends[user] = user_recommends
        return recommends

