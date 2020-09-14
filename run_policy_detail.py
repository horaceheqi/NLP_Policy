# coding:utf-8
import re
import warnings
import numpy as np
from tqdm import tqdm
from load_data import LoadData
from Model_Content.bert_mnn import Classify
from Model_Content.cut_paragraph import split_data

warnings.filterwarnings("ignore")
np.random.seed(0)


def clear_data(_data):
    sep_tag = ''
    print(_data)
    lines = _data.split('\b')
    lines = [i.strip() for i in lines]
    del_index = []
    for index, line in enumerate(lines):
        # 有可能一个html符号就是单独的一行，过滤后为\n
        temp = re.sub(r'<[A-Z, a-z, 0-9, !, \[, \], %, &, # , :, _, \-, ;, <, \\, >, =, ", /, \.,\', \s]{0,}>', '', line)
        temp = re.sub(r'&[a-z]{1,};', '', temp)
        temp = temp.strip()
        if temp == '':
            del_index.append(index)
    if del_index:
        lines = [i for index, i in enumerate(lines) if index not in del_index]
    each_line = split_data(lines, sep_tag)
    return each_line


if __name__ == '__main__':
    # Init LoadData Class
    Load = LoadData()

    # Load Policy Content List Data (after run_policy_list)
    df_list = Load.load_data('./test/policy_bj_content_list.txt', 'title')
    print(df_list.shape)

    # clear Data
    df_list.loc[:, 'content'] = df_list['content'].map(clear_data)

    # predict Data
    model = Classify()
    df_list = model.paragraph_classify(_df=df_list)
    df_list = df_list[['id', 'title', 'content', '政策背景', '支持内容', '申报条件', '申报材料', '申报方式', '其他内容', 'originalLink']]
    df_list.loc[:, 'content'] = df_list[['content']].applymap(lambda x: ''.join(x))
    print(df_list.shape)
    # df_list.to_excel('./test/policy_bj_content.xlsx', index=False, encoding='utf-8')
    # Load.save_data(df_list, _name='./test/policy_bj_content.txt', seg='\u0007')

