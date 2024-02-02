# utils.py

import os
import pickle

def save_data(file_path, data):
    """保存数据
    
    :param file_path: 保存路径
    :param data: 要保存的数据
    :return: None
    """
    parent_path = file_path[: file_path.rfind("/")]
    
    if not os.path.exists(parent_path):
        os.mkdir(parent_path)
    with open(file_path, "wb") as fp:
        pickle.dump(data, fp)
            
def load_data(file_path):
    """加载二进制数据
    
    :param file_path: 文件路径
    :return: binary object data.
    """
    with open() as fp:
        data = pickle.load()
        
    return data


def open_text(file_path, skip_row=0):
    """打开文本文件
    
    :param file_path: 文件路径
    :param skip_row: 需要跳过的行数
    :return: 一个生成器对象，每一行的文本
    """
    with open(file_path, "r", encoding="utf-8") as fp:
        for i, line in enumerate(fp):
            if i < skip_row:
                continue
            yield line
        
    
        

    