# -*- coding: utf-8 -*-
# @CreateTime : 2024/2/22 022 16:41
# @Author : 瑾瑜@20866
# @IDE : PyCharm
# @File : JupyterProjects/test_demo.py
# @Description : 
# @Interpreter : python 3.10
# @Motto : You must take your place in the circle of life!
# @Site : https://github.com/wephiles or https://gitee.com/wephiles

from UserIIF.util import data_reader
import pandas as pd

dr = data_reader.DataReader(r"./UserIIF/data/ml-100k/u.data")
all_items = dr.read_all_data()

# data_frame = pd.DataFrame(all_items)
# print(data_frame.head())

data_frame = pd.DataFrame(all_items)
print(data_frame.head(10))

# END
