"""File used to prototype and test whatever i'm working on at the moment. Will be messy."""

from sklearn.manifold import TSNE
import pickle
from mempy3.config import BASE_ANALYSIS_PATH
import plotly.express as px
import pandas as pd
import numpy as np
from umap import UMAP
from sklearn.decomposition import PCA
import plotly.graph_objects as go

pd.set_option('display.width', 230)
pd.set_option('display.max_columns', 15)
pd.set_option('min_rows', 15)


colors = px.colors.qualitative.Dark24

'''
lda = pickle.load(open(BASE_ANALYSIS_PATH / 'lda_abs.p', 'rb'))
tdf = pickle.load(open(BASE_ANALYSIS_PATH / 'lda_abs_topic_dist.p', 'rb'))

print(tdf)
# res = lda.components_
res = lda.components_ / lda.components_.sum(axis=1)[:, np.newaxis]
names = pickle.load(open(BASE_ANALYSIS_PATH / 'lda_features.p', 'rb'))
# print(res)
# print(names)

df = pd.DataFrame(res, index=[f'topic_{i}' for i in range(24)], columns=names)
print(df)
df = df.transpose()
# df['main_topic'] = df.index
df['main_topic'] = df.idxmax(axis=1)
tdf['main_topic'] = tdf.idxmax(axis=1)
tdf['color'] = tdf['main_topic'].map(lambda x: colors[tdf.columns.get_loc(x)])
print(tdf)
# ajouter colone pour nombre de txts avec le topic comme topic principal
'''

wdf = pickle.load(open(BASE_ANALYSIS_PATH / 'LDA' / 'topics_96_4_01_100_3_10' / 'doc_topics_df.p', 'rb')) # .drop(['main_topic'], axis=1)
# wdf = pickle.load(open(BASE_ANALYSIS_PATH / 'LDA' / 'topics_20_5_5' / 'topic_words_df.p', 'rb')).transpose()
# wdf = wdf / wdf.sum(axis=1)[:, np.newaxis]
# wdf['main_topic'] = wdf.idxmax(axis=1)

'''
df = px.data.iris()
features = df.loc[:, :'petal_width']
print(features)
print(features / features.sum(axis=1)[:, np.newaxis])
'''
print(wdf)
print(wdf.sum(axis=1))


#tsne = TSNE(n_components=2, random_state=0)
# projections = tsne.fit_transform(wdf.drop(['main_topic'], axis=1), )
#projections = tsne.fit_transform(wdf)

reducer = UMAP(n_components=2)
projections = reducer.fit_transform(wdf) # .drop(['main_topic'], axis=1)

# pca = PCA(n_components=2)
# projections = pca.fit_transform(wdf.drop('main_topic', axis=1))

wdf[['x', 'y']] = projections
#print(projections.shape)

# pca = PCA(n_components=3)
# projections = pca.fit_transform(tdf.drop('main_topic', axis=1))
# print(projections)

'''
fig = px.scatter_3d(
    wdf, x='x', y='y', z='z',
    hover_name=wdf.index, labels={'color': 'Main Topic'}, color_discrete_sequence=px.colors.qualitative.Dark24,) # color=wdf.columns
fig.update_traces(marker={'size': 5})
fig.show()
'''

fig = px.scatter(
    wdf, x='x', y='y', # color=wdf['main_topic'],
    hover_name=wdf.index, labels={'color': 'Main Topic'}, ) # color_continuous_scale='viridis') # color_continuous_scale='viridis')# color_discrete_sequence=px.colors.qualitative.Dark24,) # color=wdf.columns
fig.update_traces(marker={'size': 5})
fig.show()

'''
fig = go.Figure(data=[go.Scatter3d(
    x=[p[0] for p in projections],
    y=[p[1] for p in projections],
    z=[p[2] for p in projections],
    #colo=tdf.main_topic,
    hovertext=tdf.index,
    mode='markers',
    marker_color=tdf['color'],
    marker=dict(
        size=12,       # set color to an array/list of desired values
        #color=tdf['main_topic'],
        # colorscale='Viridis',   # choose a colorscale
        #opacity=0.8,
    ),
)])

# tight layout
fig.update_layout(title='allo')
fig.show()

'''