"""Use this to pre-run tsne and umap  dim reductions on topic models to speed up visualisations

Saves a new df with cols for x, y and z* values for umap and tsne reductions
Also adds title, source and main_topic cols
Saves results as reductions_df.p in the topic model folder
"""

import pickle
from mempy3.config import BASE_ANALYSIS_PATH, CORPUSFRAMES_PATH
from mempy3.analysis.kmeans.kmeansclusters import kmeans_main
import plotly.express as px
from sklearn.manifold import TSNE
from umap import UMAP
import pandas as pd


def map_cluster_str(clusters):
    return list(map(lambda x: f'Cluster {x}', clusters))


def reduce(df):
    rdf = pd.DataFrame(index=df.index)
    mdf = pickle.load(open(CORPUSFRAMES_PATH / 'metadata_corpusframe.p', 'rb'))

    rdf['title'] = mdf['title'].loc[rdf.index]
    rdf['source'] = mdf['source'].loc[rdf.index]
    rdf['main_topic'] = df.idxmax(axis=1)

    rdf[['umap_2d_x', 'umap_2d_y']] = UMAP(n_components=2, random_state=211).fit_transform(df)
    rdf[['umap_3d_x', 'umap_3d_y', 'umap_3d_z']] = UMAP(n_components=3, random_state=211).fit_transform(df)

    rdf[['tsne_2d_x', 'tsne_2d_y']] = TSNE(n_components=2, random_state=211).fit_transform(df)
    rdf[['tsne_3d_x', 'tsne_3d_y', 'tsne_3d_z']] = TSNE(n_components=3, random_state=211).fit_transform(df)

    for c in [5, 7, 10, 15, 20, 25, 40]:
        rdf[f'clustering_{c}'] = map_cluster_str(kmeans_main(c, df))

    return rdf


if __name__ == '__main__':
    BASE_PATH = BASE_ANALYSIS_PATH / 'LDA'

    # Adjust settings here!
    working_dir = 'topics_80_2_02_100_3_50_2k'
    doc_topics_file_name = 'doc_topics_df.p'

    df = pickle.load(open(BASE_PATH / working_dir / doc_topics_file_name, 'rb'))
    df2 = reduce(df)
    print(df2)
    pickle.dump(df2, open(BASE_PATH / working_dir / 'reductions_df.p', 'wb'))

