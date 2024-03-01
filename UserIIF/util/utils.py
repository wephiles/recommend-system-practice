# -*- coding: utf-8 -*-
# @CreateTime : 2024/2/22 022 16:00
# @Author : 瑾瑜@20866
# @IDE : PyCharm
# @File : JupyterProjects/utils.py
# @Description : 工具类
# @Interpreter : python 3.10
# @Motto : You must take your place in the circle of life!
# @Site : https://github.com/wephiles or https://gitee.com/wephiles

import os
import pickle


def save_data(file_path=r"", data=None):
    """
    保存数据到文件中
    Args:
        file_path ():
        data ():

    Returns:

    """
    parent_path = file_path[:file_path.rfind("/")]

    if not os.path.exists(parent_path):
        os.mkdir(parent_path)

    try:
        with open(file_path, "wb") as fp:
            pickle.dump(data, fp)
    except IOError as e:
        print("Save data default: ", e)


def load_data(file_path=r""):
    """

    Args:
        file_path ():

    Returns:

    """
#     try:
#         with open(file_path, "rb") as fp:
#             loaded_data = pickle.load(fp)
#             return loaded_data
#     except FileNotFoundError as e:
#         print("File Not Found: ", e)
    with open(file_path, "rb") as fp:
        loaded_data = pickle.load(fp)
        return loaded_data


def open_text(file_path=r"", skip_rows=None):
    """

    Args:
        file_path ():
        skip_rows (list):

    Returns:

    """
    if skip_rows is None:
        skip_rows = []
    with open(file_path, "r", encoding="utf-8") as fp:
        for i, line in enumerate(fp):
            if i in skip_rows:
                continue
            yield line

# END
