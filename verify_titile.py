# coding:utf-8
# 验证跟新的文章title在已有的库中是否存在
# 先验证有文章内容的Title (./file/policy_content_include.txt)
# 再和只有标题id和title的数据进行验证，获取id
import warnings
import numpy as np
from load_data import LoadData
from match_policy import MatchPolicy


warnings.filterwarnings("ignore")
np.random.seed(0)


def verify_title(_df_new, _df_set):
    title_set1 = _df_set['title'].values.tolist()
    match_set1 = MatchPolicy(title_set1)
    _df_new['match'] = _df_new[['title']].applymap(lambda x: match_set1.match(x, flag=False, thread=0.9))
    res_df = _df_new[_df_new['match'].apply(lambda x: True if len(x) > 0 else False)]
    if res_df.shape[0] > 0:
        print("\n待跟新的政策表中与历史录入的政策有名称相似的政策，请确认！")
        print(res_df[['title', 'match']])


if __name__ == '__main__':
    # Init LoadData Class
    Load = LoadData()

    # Load Policy List Data (after run_policy_list)
    df_list = Load.load_data('./test/policy_bj_list.txt')

    # Firstly Match Policy list, Second Match Whole Pool with No Match Policy
    pool_policy_1 = Load.load_data('./file/policy_content_include.txt')  # Which Policy include Content
    verify_title(df_list, pool_policy_1)  # 通过 FLAG_VERIFY 返回值，判断是否直接更新 policy_content_include.txt表 还是后续手动更新

    # pool_policy_2 = Load.load_data('./file/policy_content_exclude.txt')  # Which Policy exclude Content
    # verify_title(df_list, pool_policy_2)  # 通过 FLAG_VERIFY 返回值，判断是否直接更新 policy_content_include.txt表 还是后续手动更新
