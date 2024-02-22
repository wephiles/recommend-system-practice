# -*- coding: utf-8 -*-
# @CreateTime : 2024/2/7 007 11:30
# @Author : 瑾瑜@20866
# @IDE : PyCharm
# @File : JupyterProjects/utils.py
# @Description : 
# @Interpreter : python 3.10
# @Motto : You must take your place in the circle of life!
# @Site : https://github.com/wephiles or https://gitee.com/wephiles

import os
import pickle


def load_data(file_path):
    """加载二进制数据。

    :param file_path: 文件路径
    :type file_path: str
    :return:
    :rtype:
    """
    try:
        with open(file_path, mode="rb") as fp:
            data = pickle.load(fp)
    except FileNotFoundError as e:
        print("File not found in", file_path, e)
        data = None
    return data


def save_data(file_path, data):
    """保存数据。

    :param file_path:
    :type file_path:
    :param data:
    :type data:
    :return:
    :rtype:
    """
    parent_path = file_path[: file_path.rfind("/")]
    if not os.path.exists(parent_path):
        os.mkdir(parent_path)
    with open(file_path, mode="wb") as fp:
        pickle.dump(data, fp)


def open_txt_file(file_path, skip_row=0):
    """打开文本文件。

    :param file_path:
    :type file_path:
    :param skip_row:
    :type skip_row:
    :return:
    :rtype:
    """
    try:
        with open(file_path, 'r', encoding="utf-8") as fp:
            for i, line in enumerate(fp):
                if i < skip_row:
                    continue
                yield line
    finally:
        raise FileNotFoundError

# END
