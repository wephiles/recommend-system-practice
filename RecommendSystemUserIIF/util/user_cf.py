# -*- coding: utf-8 -*-
# @CreateTime : 2024/2/7 007 10:30
# @Author : 瑾瑜@20866
# @IDE : PyCharm
# @File : JupyterProjects/user_cf.py
# @Description : 
# @Interpreter : python 3.10
# @Motto : You must take your place in the circle of life!
# @Site : https://github.com/wephiles or https://gitee.com/wephiles

import sys
import math


class UserCF(object):
    """基于用户的协同过滤。"""

    def __init__(self):
        self.sim_matrix_path = r""
        self.origin_data = None
        self.user_sim_matrix = None

    def train(self, origin_data, sim_matrix_path):
        """

        :param origin_data:
        :type origin_data:
        :param sim_matrix_path:
        :type sim_matrix_path:
        :return:
        :rtype:
        """
        self.origin_data = origin_data
        self.sim_matrix_path = sim_matrix_path
        self._train_init(self.origin_data)
        print("开始训练模型...", file=sys.stderr)
        print("开始载入数据...", file=sys.stderr)
        try:
            self.user_sim_matrix = load_data()

    def _train_init(self, origin_data):
        """

        :param origin_data:
        :type origin_data:
        :return:
        :rtype:
        """
        pass

# END
