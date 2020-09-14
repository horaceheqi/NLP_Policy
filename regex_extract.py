# coding:utf-8
# 提取文章中父政策并进行血缘图构建
import re
import copy
import html


def regex_policy(_data):  # _df 列数为3
    regex = '《[^》]+》'
    res_policy = set()
    results = re.findall(regex, _data)
    for result in results:
        res_policy.add(filter_title(result))
    return filter_repeat(list(res_policy))


def regex_policy2(_arr):  # _df 列数为5
    regex = '《[^》]+》'
    res_policy = set()
    for i in range(_arr.shape[0]):
        if _arr[i] and _arr[i] != 'null':
            results = re.findall(regex, _arr[i])
        else:
            continue
        for result in results:
            res_policy.add(filter_title(result))
    return filter_repeat(list(res_policy))


def filter_title(_text):  # 清洗title中html标签
    _text = _text.replace('"', '')
    _text = re.sub('<[^<]+?>', '', _text).replace('\n', '').strip()
    _text = html.unescape(_text)
    return _text


def remove_symbol(_data):  # 只提取书名号中的文字
    regex = '《(.*)》'
    return re.findall(regex, _data)[0]


def filter_repeat(_list):
    res_list = []
    for x in range(len(_list)):
        flag = 0
        temp_x = remove_symbol(_list[x])
        temp_list = copy.deepcopy(_list)
        temp_list.remove(_list[x])
        for y in temp_list:
            temp_y = remove_symbol(y)
            # print(temp_x, temp_y)
            if temp_x in temp_y:
                flag = 1
                break
            else:
                continue
        if flag == 0:
            res_list.append(_list[x])
    return res_list


# 提取文章中的政策
def extract_policy(_df):
    if _df.shape[1] == 3:
        _df['content'] = _df['content'].fillna('null')  # 过滤掉 content 为 nan
        _df_temp = _df[~_df['content'].isin(['null'])]
        print('过滤content为空：', _df_temp.shape)
        # 逐行遍历对 content 进行截取
        _df_temp['contain_policy'] = _df_temp['content'].apply(lambda x: regex_policy(x))
        _df_temp = _df_temp[~_df_temp['contain_policy'].apply(lambda x: len(x) == 0)]
        print('过滤没有父政策：', _df_temp.shape)
        return _df_temp
    elif _df.shape[1] == 5:
        _df = _df.fillna('null')
        _df_temp = _df[~_df['content'].isin(['null'])]
        _df_temp['contain_policy'] = _df_temp[['政策背景', '支持内容']].apply(regex_policy2, axis=1)
        _df_temp = _df_temp[~_df_temp['contain_policy'].apply(lambda x: len(x) == 0)]
        print('过滤没有父政策后剩余：', _df_temp.shape)
        return _df_temp
    else:
        print('extract_policy 中df传输格式有问题')