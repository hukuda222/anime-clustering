from gensim.models import word2vec
import random
import matplotlib.pyplot as plt

from scipy.cluster.hierarchy import linkage, dendrogram

plt.rcParams['font.family'] = 'Arial Unicode MS'


def get_list():
    frac = open('list2.txt', 'rb')
    words = frac.readlines()
    for i, w in enumerate(words):
        words[i] = w.decode('utf-8').replace("\n", "")
    frac.close()
    return words


# 学習
sentences = word2vec.Text8Corpus("corpus_wakati2.txt")
model = word2vec.Word2Vec(sentences, size=100, min_count=20, window=5)
# モデルの保存と読込
model.save("sample2.model")

model = word2vec.Word2Vec.load("sample2.model")
if __name__ == '__main__':
    print("go")
    titles = get_list()
    vectors = list()  # 100はword2vecが返してくれるやつ
    for i, title in enumerate(titles):
        vectors.append(model[title])

    result1 = linkage(vectors, metric='chebyshev', method='average')
    dendrogram(result1, labels=titles, orientation='right')

    plt.show()
