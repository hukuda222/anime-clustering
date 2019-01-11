# -*- coding: utf-8 -*-
import pandas as pd
import math

from sklearn.cluster import KMeans
from sklearn.decomposition import TruncatedSVD

import matplotlib.pyplot as plt
from matplotlib import cm

plt.rcParams["font.family"] = "IPAexGothic"


def read(i):
    po = pd.read_csv("sums/sum" + str(i) + ".csv", index_col=0)
    p = po.to_dict()
    for d in p:
        return p[d]


def get_list():
    frac = open('list.txt', 'rb')
    words = frac.readlines()
    for i, w in enumerate(words):
        words[i] = w.decode('utf-8').replace("\n", "")
    frac.close()
    return words

# {単語:{(出てきた文章番号):(出てきた数)}}の形式のdictを返す


def search(dics):
    big_dic = {}
    for i, dic in enumerate(dics):
        for l in dic:
            if big_dic.get(l) is None:
                big_dic[l] = {i: 1}
            else:
                if big_dic[l].get(i) is None:
                    big_dic[l][i] = 1
                else:
                    big_dic[l][i] += 1
    return big_dic


def get_tf(dics):
    all_sum = [0] * len(dics)
    all_cp = []
    for i, dic in enumerate(dics):
        for word in dic:
            all_sum[i] += dic[word]
    for i, dic in enumerate(dics):
        cp = {}
        for word in dic:
            cp[word] = (dic[word] / all_sum[i])
        all_cp.append(cp)
    return all_cp


def get_idf(big):
    out = {}
    for dic in big:
        count = len(dic) if len(big[dic]) < 20 else 0
        for i in big[dic]:
            count /= big[dic][i]
        out[dic] = math.log2(count) if count != 0 else 0
    return out


if __name__ == '__main__':
    dics = []
    new_dic = []
    for i in range(50):
        dics.append(read(i))
    big_dic = search(dics)
    tf = get_tf(dics)
    idf = get_idf(big_dic)

    word_dic = [0] * len(dics)

    for i, dic in enumerate(dics):
        new_dic.append({})
        word_dic[i] = []
        for word in dic:
            if tf[i][word] * idf[word] > 0.0003:
                new_dic[i][word] = dic[word]

    for i, d in enumerate(big_dic):
        for j, dic in enumerate(dics):
            word_dic[j].append({})
            if dic.get(d) is not None:
                word_dic[j][i] = dic[d]
            else:
                word_dic[j][i] = 0

    po = TruncatedSVD(2).fit_transform(word_dic)
    to = TruncatedSVD(30).fit_transform(word_dic)

    text_list = get_list()

    for i, nd in enumerate(new_dic):
        nd = pd.Series(nd)
        nd.to_csv("sums2/sum" + str(i) + ".csv")

    fig = plt.figure()
    axes = fig.add_subplot(111)
    # K-Meansのクラスタ分析クラス初期化
    km_model = KMeans(n_clusters=5)
    # ベクトル情報を食わせて、クラスタ分析を実行
    po2 = km_model.fit_predict(to)
    for i in range(50):
        if i != 2 and i != 5 and i != 21 and i != 39 and i != 38:
            axes.annotate(
                text_list[i], xy=(po[i][0], po[i][1]))
            axes.plot(po[i][0], po[i][1],
                      color=cm.hsv(float(po2[i]) / 5),
                      ms=6.0, zorder=3, marker="o")
    plt.axis('tight')
    plt.show()
