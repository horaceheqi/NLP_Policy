# coding:utf-8
import warnings
import numpy as np
import pandas as pd
import clear_data as cd
from load_data import LoadData
from match_policy import MatchPolicy
from regex_extract import extract_policy


warnings.filterwarnings("ignore")
np.random.seed(0)


def verify_title(_df_new, _df_set):
    title_set = _df_set['title'].values.tolist()
    match_set = MatchPolicy(title_set)
    _df_new['father'] = _df_new['contain_policy'].apply(lambda i: match_set.match(i, flag=True, thread=0.96))
    _df_new['fin_policy'] = _df_new[['contain_policy', 'father']].apply(replace_policy, axis=1)  # 当查询到父政策时需要将ID进行替换
    no_math = pd.DataFrame(match_set.return_no_match(), columns=['title'])
    no_match_df = get_id(no_math)
    return _df_new, no_match_df


def replace_policy(_arr):
    if _arr[1]:  # 匹配到了父政策，需要替换
        res_list = [_arr[1][i] if _arr[1][i] != '' else _arr[0][i] for i in range(len(_arr[1]))]
    else:  # 未匹配到父政策
        res_list = [i for i in _arr[2]]
    return res_list


def trans_dict(_df1, _df2=''):
    cols = ['id', 'title']
    if isinstance(_df2, pd.core.frame.DataFrame):

        _df = pd.concat([_df1[cols], _df2[cols]], axis=0)
    else:
        _df = _df1[cols]
    _dict = _df.set_index('title').T.to_dict('list')
    for k, v in _dict.items():
        _dict[k] = v[0]
    return _dict


# 对未匹配的父政策数据进行存储(主要计算ID)
def get_id(_df):
    _df.loc['title'] = _df['title'].apply(lambda x: cd.filter_title(x))
    _df['level'] = '0'
    _df['state'] = '0'
    _df['province'] = '000000'
    _df['city'] = '000000'
    _df['county'] = '000000'
    _df['id'] = _df[['level', 'state', 'province', 'city', 'county']].apply(cd.calculate_id, axis=1)
    return _df


def save_blood(_df, _dict_all):
    res_list = list()
    title_set = set()
    _df_temp = _df[['id', 'title', 'fin_policy']].copy()
    for index, row in _df_temp.iterrows():
        for var in row['fin_policy']:
            temp_list = list()
            try:
                temp_list.append('0')
                temp_list.append(row['id'])
                temp_list.append(row['title'])
                temp_list.append(_dict_all[var])
                temp_list.append(var)
                title_set.add(var)  # filter_title
            except KeyError:
                continue
            res_list.append(temp_list)
    res_list = [i for i in res_list if i[0] != i[2]]
    df_blood = pd.DataFrame(res_list, columns=['nums', 'POLICY_ID', 'POLICY_TITLE', 'FATHER_ID', 'FATHER_TITLE'])
    df_blood.to_csv('./test/policy_bj_blood.txt', index=False, header=None, encoding='utf-8', sep='\t')


if __name__ == '__main__':
    # Init LoadData Class
    Load = LoadData()
    FLAG_VERIFY = True   # 是否验证跟新数据在目前库中存在

    # Load Policy Content Data (after run_policy_detail)
    df_content = Load.load_data('./test/policy_bj_content.txt')

    # Extract Father Policy
    df_temp = df_content[['id', 'title', 'content', '政策背景', '支持内容']].copy()
    df_etc = extract_policy(df_temp)

    # Load All Policy Title from Local File To Match Father
    # Firstly Match Policy list, Second Match Whole Pool with No Match Policy
    pool_policy_1 = Load.load_data('./file/policy_content_include.txt')  # Which Policy include Content
    # pool_policy_2 = Load.load_data('./file/policy_content_exclude.txt')  # Which Policy exclude Content

    if FLAG_VERIFY:
        # 通过 FLAG_VERIFY 返回值，判断是否直接更新 policy_content_include.txt表 还是后续手动更新
        df_etc, pool_policy_new = verify_title(df_etc, pool_policy_1)
        # verify_title(df_etc, pool_policy_2, father_dict)  # 通过 FLAG_VERIFY 返回值，判断是否直接更新 policy_content_include.txt表 还是后续手动更新

    dict_policy = trans_dict(pool_policy_1, pool_policy_new)  # 将历史录入政策 id 和 title 转换成字典

    # 存储血缘关系
    save_blood(df_etc, dict_policy)
