# coding:utf-8
# 根据反馈的Title列表，实时对Title分词、计算tf-idf特征，并计算文章之间的相似度
# 维护一个全量政策ID表，维护一个目前未爬起详细内容政策ID表
from LAC import LAC
from gensim import corpora, models, similarities


class MatchPolicy(object):

    def __init__(self, _text):
        self.match_count = 0
        self.no_count = 0
        self.no_match = set()  # 用来记录未匹配到的政策
        self.text = _text
        self.lac = LAC(mode='seg')  # 加载 lac 分词模型
        self.dictionary, self.corpus, self.features = self.gen_corpus()
        self.tf_idf_model, self.tf_idf_corpus = self.gen_tf_idf()
        self.sparse_matrix = similarities.SparseMatrixSimilarity(self.tf_idf_corpus, self.features)  # num_best=3 返回最相似的三个标题

    @staticmethod
    def load_word(_path):
        word = []
        with open(_path, encoding='utf-8', mode='r') as file:
            for lines in file.readlines():
                line = lines.strip('\n')
                if line == '':
                    continue
                else:
                    word.append(line)
        return word

    # 分词、取停用词、生成词典
    def gen_corpus(self):
        # 加载停用词
        stop_word = MatchPolicy.load_word('./file/stop_word.txt')
        doc = self.lac.run(self.text)  # 分词
        doc_filter = list()
        for words in doc:
            temp_words = [i for i in words if i not in stop_word]
            doc_filter.append(temp_words)
        _dictionary = corpora.Dictionary(doc_filter)  # 生成词典
        _features = len(_dictionary.token2id)
        _corpus = [_dictionary.doc2bow(text) for text in doc_filter]  # 生成词库,以(词, 词频)方式存储
        # dictionary.save('dict.txt')  # 保存生成的词典
        # dictionary = Dictionary.load('dict.txt')  # 加载词典
        # corpora.MmCorpus.serialize('corpus.mm',corpus)  # 保存生成的语料
        # corpus=corpora.MmCorpus('corpus.mm')  # 加载语料
        return _dictionary, _corpus, _features

    def gen_tf_idf(self):
        # 初始化tf-idf模型
        tf_idf = models.TfidfModel(self.corpus)
        # 装换整个词库
        corpus_tf_idf = tf_idf[self.corpus]
        # tf_idf.save("data.tfidf")  # 保存tf_idf模型
        # tf_idf = models.TfidfModel.load("data.tfidf")  # 加载tf_idf模型
        return tf_idf, corpus_tf_idf

    def return_no_match(self):
        print("一共包含政策数量:%d, 其中匹配到%d, 未匹配到:%d" % (self.match_count + self.no_count, self.match_count, self.no_count))
        res_no_match = list(set(self.no_match))
        res_no_match = sorted(res_no_match)  # key=lambda i: len(i)
        # print(len(res_no_match))
        return res_no_match  # .sort()

    def match(self, _data, flag=False, thread=0.5):  # flag 来控制是进行血缘匹配、还是推荐匹配相关政策
        if flag:  # 为真则进行血缘匹配
            res_list = list()
            for i in range(len(_data)):
                file = _data[i]
                print(file)
                _doc = self.lac.run(file)
                _corpus = self.dictionary.doc2bow(_doc)
                _tf_idf = self.tf_idf_model[_corpus]
                similarity = self.sparse_matrix.get_similarities(_tf_idf)
                sims = sorted(enumerate(similarity), key=lambda item: -item[1])[0]
                if sims[1] > thread:
                    print("******匹配到政策：******\n", file, self.text[sims[0]])
                    res_list.append(self.text[sims[0]])
                    self.match_count += 1
                else:
                    self.no_count += 1
                    res_list.append('')
                    self.no_match.add(file)
            return res_list
        else:
            res_list = list()
            _doc = self.lac.run(_data)
            _corpus = self.dictionary.doc2bow(_doc)
            _tf_idf = self.tf_idf_model[_corpus]
            similarity = self.sparse_matrix.get_similarities(_tf_idf)
            sims = sorted(enumerate(similarity), key=lambda item: -item[1])
            for var in sims:
                # print(var, type(var[1]))
                if var[1] >= thread:
                    res_list.append((self.text[var[0]], var[1]))
            return res_list
