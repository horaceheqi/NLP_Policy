# 根据加载文件格式自动调用相应的读取代码
import pandas as pd


class LoadData:
    def __init__(self):
        self.file = ''
        self.df = pd.DataFrame()

    def set_file(self, _file):
        self.file = _file

    def read_file(self):
        if self.file.endswith('xlsx'):
            self.df = pd.read_excel(self.file, encoding='utf-8')
        elif self.file.endswith('csv'):
            self.df = pd.read_csv(self.file, encoding='utf-8')
        elif self.file.endswith('txt'):
            self.df = pd.read_table(self.file, encoding='utf-8', sep='\u0007', header=None, dtype=str)
            if self.df.shape[1] == 1:
                self.df = pd.read_table(self.file, encoding='utf-8', sep='\t', header=None, dtype=str)
        print("加载数据格式：", self.df.shape)

    def set_columns(self):
        if self.df.shape[1] == 17:
            self.df.columns = ['title', 'start_time', 'end_time', 'source', 'power', 'scope', 'province', 'city', 'county',
                               'content', 'set', 'funds', 'level', 'txt_id', 'cityid', 'provinceid', 'originalLink']
        elif self.df.shape[1] == 2:
            self.df.columns = ['id', 'title']
        elif self.df.shape[1] == 4:
            self.df.columns = ['id', 'title', 'content', 'originalLink']
        elif self.df.shape[1] == 10:
            self.df.columns = ['id', 'title', 'content', '政策背景', '支持内容', '申报条件', '申报材料', '申报方式', '其他内容', 'link']
        elif self.df.shape[1] == 11:
            self.df.columns = ['title', 'start_time', 'end_time', 'source', 'power', 'scope', 'province', 'city', 'county', 'content', 'set']
        elif self.df.shape[1] == 14:
            self.df.columns = ['id', 'title', 'state', 'level', 'type', 'scope', 'source', 'province', 'city', 'county', 'power', 'amount',
                               'start_time', 'end_time']

    def del_repeat(self, _col):
        self.df.loc[:, _col] = self.df[_col].apply(lambda x: x.strip())
        self.df.drop_duplicates([_col], keep='first', inplace=True)

    @staticmethod
    def save_data(_df, _name,  seg='\t'):
        _df.to_csv(_name, index=False, header=None, encoding='utf_8_sig', sep=seg)

    def load_data(self, _file, _cols=''):
        self.set_file(_file)
        self.read_file()
        self.set_columns()
        if _cols:
            self.del_repeat(_cols)
        return self.df
