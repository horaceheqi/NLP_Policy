# coding:utf-8
import numpy as np
import warnings
import clear_data as cd
from load_data import LoadData

warnings.filterwarnings("ignore")
np.random.seed(0)


if __name__ == '__main__':
    # Init LoadData Class
    Load = LoadData()

    # Load zg_bj Data
    df = Load.load_data('./test/clear_zg_bj_0908.txt', 'title')
    # Load.save_data(df, './test/clear_zg_bj_0831.txt')  # 保存清洗后的数据

    # # Load All Data
    # df_match = Load.load_data('./clear/clear_zg_all_0831.txt', 'title')
    # # Load.save_data(df_match, './test/clear_zg_all_0831.txt')  # 保存数据
    #
    # nums = df_match.shape[0]
    cols = ['title', 'level', 'scope', 'source', 'province', 'city', 'county', 'power', 'funds', 'set', 'txt_id', 'originalLink', 'start_time',
            'end_time', 'content']
    df_ = df[cols].copy()

    # Fill province, city, county
    df_fill = cd.fill_data(df_)
    df_list = df_fill[['id', 'title', 'state', 'level', 'set', 'scope', 'source', 'province', 'city', 'county', 'power', 'funds', 'start_time',
                       'end_time']]
    Load.save_data(df_list, './test/policy_bj_list.txt')  # 将结果保存，T_POLICY_LIST

    # 保存待处理政策内容列表
    df_content = df_fill[['id', 'title', 'content', 'originalLink']]
    df_content.to_csv('./test/policy_bj_content_list.txt', index=False, header=None, encoding='utf-8', sep='\t')




