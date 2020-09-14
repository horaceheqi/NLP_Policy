#!/usr/bin/python
# -*- coding: UTF-8 -*-
import os
import re
import pandas as pd
from glob import glob
from Model_Content.bert_mnn import Classify
from Model_Content.cut_paragraph import split_data


def classify(arr):
    html = str(arr[0])
    ori_content_list = split_data(html.split('\n'))
    clean_content_list = []
    for content in ori_content_list:
        temp = re.sub(r'<[a-z, 0-9, %, &, :, _, \-, ;, <, >, =, ", /, \.,\',\s]{1,}>', '', content)
        temp = re.sub(r'&[a-z]{1,};', '', temp)
        clean_content_list.append(temp)
    pred_list = Classify.predict(clean_content_list)
    c_1_list = []
    c_2_list = []
    c_3_list = []
    c_4_list = []
    c_5_list = []
    c_0_list = []
    for c, p in zip(ori_content_list, pred_list):
        if p == 1:
            c_1_list.append(c)
        elif p == 2:
            c_2_list.append(c)
        elif p == 3:
            c_3_list.append(c)
        elif p == 4:
            c_4_list.append(c)
        elif p == 5:
            c_5_list.append(c)
        elif p == 0:
            c_0_list.append(c)

    return '\n'.join(c_1_list), '\n'.join(c_2_list), '\n'.join(c_3_list), '\n'.join(c_4_list), '\n'.join(c_5_list), '\n'.join(c_0_list)


def classify_content(_path):
    txt_files = glob(_path)  # 'in/*.txt'
    df = pd.DataFrame(columns=['txt_id', 'content'])
    for txt_file in txt_files:
        with open(txt_file, mode='r', encoding='utf-8') as f:
            lines = f.readlines()
        ids = os.path.split(txt_file)[1]
        df = df.append({'txt_id': ids, 'content': '\n'.join(lines)}, ignore_index=True)
    df[['background', 'support', 'condition', 'material', 'method', 'rest']] = df[['content']].apply(classify, axis=1, result_type='expand')
    return df
    # df.to_excel('./Data/policy_content', index=False)
