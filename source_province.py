# coding=utf-8
# 对政策发布机构映射其所在省市县
# 参考https://github.com/DQinYuan/chinese_province_city_area_mapper
import cpca
import numpy as np
import pandas as pd
from map_areas import MapAreas


def judge_source(_location):
    result = cpca.transform(_location, cut=False)
    result = result[['省', '市', '区']]
    maps = MapAreas()
    for var in result.columns:
        result[var] = result[var].apply(lambda x: maps.trans_map(x))
    if result.loc[(result['省'] == '') & (result['市'] == '') & (result['区'] == '')].shape[0] > 0:
        result.loc[(result['省'] == '') & (result['市'] == '') & (result['区'] == ''), ['省']] = '000000'
    return result


if __name__ == '__main__':
    df = pd.DataFrame()
    df['user'] = ['A', 'B']  # ,'C', 'D'
    df['policy'] = ['北京市东城区文化发展促进中心', '国家']  # , '北京市新闻出版局', '科学技术部'
    # print(type(df['policy']))
    print(df['policy'].shape)
    df_ = judge_source(df['policy'])
    # print(type(df_))
    # print(df_['区'].values.tolist())
    print(df_)
