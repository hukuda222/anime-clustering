# anime-clustering
アニメのタイトルで検索し、ヒットしたサイトの記事の内容からアニメを分類しました。
特徴量はword2vecとtf-idfを、分類手法はK平均法と群平均法を用いました。

以下のグラフはword2vecの特徴量をもとにk-meansでクラスタリングし、ベクトルを二次元にしてt-SNEで平面にプロットしたものです。

![](https://raw.githubusercontent.com/hukuda222/anime-divide/master/all.png)

![](https://raw.githubusercontent.com/hukuda222/anime-divide/master/part.png)
