"""Tools for lda visualisation"""

import pandas as pd
import pickle
from mempy3.config import BASE_ANALYSIS_PATH
import plotly.express as px
from sklearn.manifold import TSNE
from umap import UMAP
from sklearn.cluster import MiniBatchKMeans


def scatter_from_reductions():
    pass


def quick_scatter_viz(df, dims=2, mapping='tsne', n_clusters=1):
    clusters = MiniBatchKMeans(n_clusters=n_clusters, random_state=2112).fit_predict(df)

    if mapping == 'tsne':
        reducer = TSNE(n_components=dims, random_state=0)
    elif mapping == 'umap':
        reducer = UMAP(n_components=dims)
    else:
        raise ValueError(f'Expected mapping to be tsne or umap, got {mapping} instead')

    projections = reducer.fit_transform(df)

    if dims == 2:

        df[['x', 'y']] = projections
        df['cluster'] = clusters
        df['cluster'] = df['cluster'].apply(str)
        print(df)
        # CHANGER DTYPE CLUSER COL PR DISCRETE
        fig = px.scatter(df, x='x', y='y', color=df['cluster'], color_discrete_sequence=px.colors.qualitative.Dark24)
        # color_discrete_sequence=px.colors.qualitative.Alphabet
    elif dims == 3:
        df[['x', 'y', 'z']] = projections
        df['cluster'] = clusters
        df['cluster'] = df['cluster'].apply(str)
        fig = px.scatter_3d(df, x='x', y='y', z='z', color=df['cluster'], color_discrete_sequence=px.colors.qualitative.Dark24)
        fig.update_traces(marker={'size': 3})
    else:
        raise ValueError(f'Expected dims in (2, 3), got {dims} instead')

    return fig


if __name__ == '__main__':
    BASE_PATH = BASE_ANALYSIS_PATH / 'LDA'

    # Adjust settings here!
    working_dir = 'topics_80_2_02_100_3_50_2k'
    df_file_name = 'doc_topics_df.p'
    dims = 2
    mapping = 'tsne'  # 'tsne' or 'umap'
    n_clusters = 32
    # Works here
    df = pickle.load(open(BASE_PATH / working_dir / df_file_name, 'rb'))
    fig = quick_scatter_viz(df, dims=dims, mapping=mapping, n_clusters=n_clusters)
    fig.show()



