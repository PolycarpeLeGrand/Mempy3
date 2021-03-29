from sklearn.cluster import MiniBatchKMeans
import numpy as np
import pickle
from mempy3.utils.timer import Timer

from mempy3.config import BASE_ANALYSIS_PATH


def kmeans_main(n_clusters, df, name=''):
    # path = BASE_ANALYSIS_PATH / 'LDA' / name
    # path.mkdir(exist_ok=True)

    # timer = Timer()
    clusters = MiniBatchKMeans(n_clusters=n_clusters, random_state=2112).fit_predict(df)
    # timer.step()

    # print(clusters)
    # print(len(clusters))

    # ca chie tt pcque ca modifie la ref
    # df['cluster'] = clusters

    # print(df.groupby('cluster').mean())
    # marche pas
    # for i in range(n_clusters):
    #    print(df.groupby('cluster').mean().iloc[i].nlargest(10))

    return clusters


def kmeans_run():
    pass


if __name__ == '__main__':
    working_dir = 'topics_80_2_02_100_3_50_2k'
    df_file_name = 'doc_topics_df.p'
    df = pickle.load(open(BASE_ANALYSIS_PATH / 'LDA' / working_dir / df_file_name, 'rb'))

    # ecart type, mediane
    clusters = kmeans_main(8, df, 'kmeans_64_80')
    print(type(clusters))

