from gensim.models import word2vec
import random
from sklearn.decomposition import TruncatedSVD
import matplotlib.pyplot as plt
from matplotlib import cm

plt.rcParams['font.family'] = 'Arial Unicode MS'


# vectorは一つ、center_vectorsは複数


def near(vector, center_vectors):
    def euclid_dist(vector1, vector2): return (
        sum([(vec[0] - vec[1])**2 for vec
             in list(zip(vector1, vector2))]))**0.5
    d = [euclid_dist(vector, center_vector)
         for center_vector in center_vectors]
    return d.index(min(d))


def clustering(vectors, label_count, learning_count_max=1000):
    # 各vectorに割り当てられたクラスタラベルを保持するvector
    label_vector = [random.randint(0, label_count - 1)for i in vectors]
    # 一つ前のラベル
    old_label_vector = list()
    # 各クラスタの重心の初期化
    center_vectors = [[0] * len(vectors[0])] * label_count

    for step in range(learning_count_max):
        # 各重心のベクトルを作る
        for vec, label in zip(vectors, label_vector):
            # それぞれcenterに加算して行ってる
            center_vectors[label] = [c + v for c,
                                     v in zip(center_vectors[label], vec)]
        for i, center_vector in enumerate(center_vectors):
            center_vectors[i] = [
                v / label_vector.count(i) if label_vector.count(i) != 0 else 0 for v in center_vector]
        # 各ベクトルのラベルの再割当て
        for i, vec in enumerate(vectors):
            label_vector[i] = near(vec, center_vectors)
        # 前Stepと比較し、ラベルの割り当てに変化が無かったら終了
        if old_label_vector == label_vector:
            break
        # ラベルのベクトルを保持
        old_label_vector = [l for l in label_vector]
    return center_vectors


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
# model.save("sample2.model")
# 単語間の類似度計算

model = word2vec.Word2Vec.load("sample2.model")
if __name__ == '__main__':
    print("go")
    titles = get_list()
    vectors = list()  # 100はword2vecが返してくれるやつ
    for i, title in enumerate(titles):
        vectors.append(model[title])

    po = TruncatedSVD(2).fit_transform(vectors)
    centers = clustering(vectors, 5)

    fig = plt.figure()
    axes = fig.add_subplot(111)
    for i in range(34):
        if i != 2:
            axes.annotate(
                titles[i], xy=(po[i][0], po[i][1]))
            axes.plot(po[i][0], po[i][1],
                      color=cm.hsv(float(near(vectors[i], centers)) / 5),
                      ms=6.0, zorder=3, marker="o")
    plt.axis('tight')
    plt.show()
