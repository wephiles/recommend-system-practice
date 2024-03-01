# -*- coding: utf-8 -*-
# @CreateTime : 2024/2/27 027 14:00
# @Author : 瑾瑜@20866
# @IDE : PyCharm
# @File : JupyterProjects/item_cf.py
# @Description : 
# @Interpreter : python 3.10
# @Motto : You must take your place in the circle of life!
# @Site : https://github.com/wephiles or https://gitee.com/wephiles

import sys

from RecommendSystemUserCF.recommender.user_cf import UserCF


class ItemCF(UserCF):
    """基于项目的协同过滤。"""

    def __init__(self):
        # UserCF.__init()
        self.train_data = None
        self.sim_matrix_path = r""
        self.item_sim_matrix = None

    def train(self, train_data=None, sim_matrix_path=r"./data/item_sim_cf.pkl"):
        self.train_data = train_data
        self.sim_matrix_path = sim_matrix_path

        # 初始化训练集
        UserCF._init_train(self.train_data)

        print("begin to train model ... ", file=sys.stderr)
        try:
            print("begin to load user cf matrix ...", file=sys.stderr)
            self.item_sim_matrix = load_file(sim_matrix_path)
        except FileExistsError:
            print("File is not exists, try to calculate the matrix", file=sys.stderr)
            print("try to calculate th matrix ...", file=sys.stderr)
            self.item_sim_matrix = self.item_similarity()
        print("successfully calculated the matrix.")
        print("Save the matrix ...")
        save_file(self.sim_matrix_path, self.item_sim_matrix)

    def recommend(self):
        pass

    def recommend_users(self):
        pass

# --END--
