# -*- coding: utf-8 -*-
# @CreateTime : 2024/2/22 022 15:59
# @Author : 瑾瑜@20866
# @IDE : PyCharm
# @File : JupyterProjects/user_iif.py
# @Description : 
# @Interpreter : python 3.10
# @Motto : You must take your place in the circle of life!
# @Site : https://github.com/wephiles or https://gitee.com/wephiles

import math
import sys
from collections import defaultdict
from operator import itemgetter

from UserIIF.util import utils


class UserIIF(object):
    """UserIIF类，用以实现基于用户的协同过滤算法，经过优化。"""

    def __init__(self):
        self.sim_matrix_path = r""
        self.train_data = None
        self.user_sim_matrix = None

    def _init_train(self, train_data) -> bool:
        """

        Args:
            train_data ():

        Returns:

        """
        print("initializing train data...")
        self.train = dict()
        for user, item, _ in train_data:
            self.train.setdefault(user, set())
            self.train[user].add(item)
        print("data has been initialized.")

    def train(self, train_data, sim_matrix_path=r""):
        """

        Args:
            train_data (dict): 训练数据
            sim_matrix_path (str): 

        Returns:

        """
        self.train_data = train_data
        self._init_train(self.train_data)
        print("begin to train model...")
        try:
            print("loading user similarity matrix...", file=sys.stderr)
            self.user_sim_matrix = utils.load_data(file_path=sim_matrix_path)
            print("user similarity matrix had been loaded.")
        except FileNotFoundError:
            print("fail to load user similarity matrix.", file=sys.stderr)
            # 计算用户相似度
            print("begin to computer user similarity...", file=sys.stderr)
            self.user_sim_matrix = self.user_similarity()
        self.sim_matrix_path = sim_matrix_path
        print("try to save user similarity matrix again...", file=sys.stderr)
        utils.save_data(file_path=self.sim_matrix_path, data=self.user_sim_matrix)
        print("successfully saved user similarity matrix.", file=sys.stderr)
        print("successfully train the model.", file=sys.stderr)

    def user_similarity(self):
        """
        计算相似度。
        Returns:

        """
        # 用户-物品倒排表
        print("Item-User reverse table are building...")
        item_user = dict()
        for user, items in self.train.items():
            for item in items:
                item_user.setdefault(item, set())
                item_user[item].add(user)
        print("Item-User reverse table had been built.")

        # 计算用户相似度矩阵
        print("computing user similarity matrix...")
        user_sim_matrix = dict()
        N = defaultdict(int)
        for item, users in item_user.items():
            for u in users:
                N[u] += 1
                for v in users:
                    if u == v:
                        continue
                    user_sim_matrix.setdefault(u, defaultdict(int))
                    user_sim_matrix[u][v] += 1. / math.log(1 + len(item_user[item]))
        print("successfully calculated user similarity matrix.")

        # 计算最终的用户相似度矩阵
        print("calculating final similarity matrix...")
        for u, related_users in user_sim_matrix.items():
            for v, con_items_count in related_users.items():
                user_sim_matrix[u][v] = con_items_count / math.sqrt(N[u] * N[v])
        print("successfully calculated final similarity matrix.")
        return user_sim_matrix

    def recommend(self, user, N, K):
        """
        给用户User推荐物品。
        Args:
            user (int): user id.
            N (int): the number of item.
            K (int): recommend k items to user.

        Returns (list): [item1, item2, ...]

        """
        related_items = self.train.get(user, set)
        recommends = dict()
        print("recommend system is running...")
        for v, sim in sorted(self.user_sim_matrix.get(user, dict).items(),
                             key=itemgetter(1),
                             reverse=True)[:K]:
            for item in self.train[v]:
                if item in related_items:
                    continue
                recommends.setdefault(item, 0)
                recommends[item] += sim
        print("recommend system run over.")
        return dict(sorted(recommends.items(), key=itemgetter(1), reverse=True)[:N])

    def recommend_users(self, users, N, K):
        """
        推荐测试集.
        Args:
            users ():
            N ():
            K ():

        Returns:

        """
        recommends = dict()
        for user in users:
            user_recommends = list(self.recommend(user, N, K).keys())
            recommends[user] = user_recommends
        return recommends

# --END--
