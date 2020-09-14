# coding:utf-8
import warnings
import numpy as np
import pandas as pd
from load_data import LoadData
from match_policy import MatchPolicy


warnings.filterwarnings("ignore")
np.random.seed(0)


def match_policy(_df_new, _df_set):
    title_set = _df_set['title'].values.tolist()
    match_set = MatchPolicy(title_set)
    _df_new['match'] = _df_new['title'].apply(lambda x: match_set.match(x, flag=False, thread=0.5))
    return _df_new


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


def save_blood(_df, _dict_all):
    res_list = list()
    _df_temp = _df[['id', 'title', 'match']].copy()
    for index, row in _df_temp.iterrows():
        for var in row['match']:
            if row['id'] == _dict_all[var[0]]:
                continue
            temp_list = list()
            try:
                temp_list.append('0')
                temp_list.append(row['id'])
                temp_list.append(row['title'])
                temp_list.append(_dict_all[var[0]])
                temp_list.append(var[0])
                temp_list.append(var[1])
            except KeyError:
                continue
            res_list.append(temp_list)
    res_list = [i for i in res_list if i[0] != i[2]]
    df_match = pd.DataFrame(res_list, columns=['nums', 'POLICY_ID', 'POLICY_TITLE', 'SIMILARITY_ID', 'SIMILARITY_TITLE', 'SIMILARITY_PROB'])
    df_match.drop_duplicates(keep='first', inplace=True)
    df_match.to_csv('./test/policy_bj_match.txt', index=False, header=None, encoding='utf-8', sep='\t')


if __name__ == '__main__':
    # Init LoadData Class
    Load = LoadData()

    # Load Policy List Data (after run_policy_list)
    df_list = Load.load_data('./test/policy_bj_list.txt')

    # Load All Policy Title from Local File To Match
    history_policy = Load.load_data('./file/policy_content_include.txt')  # Which Policy include Content

    df_etc = match_policy(df_list, history_policy)
    dict_policy = trans_dict(df_list, history_policy)

    # 存储血缘关系
    save_blood(df_etc, dict_policy)
