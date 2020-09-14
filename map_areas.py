# coding=utf-8
# 对省市县映射其所对应的code

import numpy as np
import pandas as pd


class MapAreas(object):

    def __init__(self):
        file_path = './file/map_dict.txt'
        df = pd.read_table(file_path, header=None, encoding='utf-8', sep=',')
        df.drop_duplicates(inplace=True)
        df.columns = ['code', 'ares']
        self.df_country = df.set_index('ares').T.to_dict('list')
        for k, v in self.df_country.items():
            self.df_country[k] = v[0]
        # print(self.df_country)

    def trans_map(self, _data):
        try:
            return self.df_country[_data]
        except KeyError:
            return ''


if __name__ == '__main__':
    maps = MapAreas()
    print(maps.trans_map('北京市'))
