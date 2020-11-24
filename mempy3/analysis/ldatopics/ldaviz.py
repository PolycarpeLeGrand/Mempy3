"""Tools for lda visualisation"""

import pandas as pd
import pickle
from mempy3.config import BASE_ANALYSIS_PATH
import plotly.express as px
from sklearn.manifold import TSNE
from umap import UMAP


def quick_scatter_viz(df, dims=2, mapping='tsne'):

    if mapping == 'tsne':
        reducer = TSNE(n_components=dims, random_state=0)
    elif mapping == 'umap':
        reducer = UMAP(n_components=dims)
    else:
        raise ValueError(f'Expected mapping to be tsne or umap, got {mapping} instead')

    projections = reducer.fit_transform(df)

    if dims == 2:
        df[['x', 'y']] = projections
        fig = px.scatter(df, x='x', y='y')
    elif dims == 3:
        df[['x', 'y', 'z']] = projections
        fig = px.scatter_3d(df, x='x', y='y', z='z')
    else:
        raise ValueError(f'Expected dims in (2, 3), got {dims} instead')

    fig.show()


if __name__ == '__main__':
    BASE_PATH = BASE_ANALYSIS_PATH / 'LDA'

    # Adjust settings here!
    working_dir = 'topics_96_1_02_100_3_50'
    df_file_name = 'doc_topics_df.p'
    dims = 2
    mapping = 'tsne'

    # Works here
    df = pickle.load(open(BASE_PATH / working_dir / df_file_name, 'rb'))
    quick_scatter_viz(df, dims=dims, mapping=mapping)

