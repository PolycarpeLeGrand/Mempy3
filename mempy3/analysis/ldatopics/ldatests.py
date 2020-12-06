import pandas as pd
import pickle
import numpy as np
from umap import UMAP
from sklearn.decomposition import LatentDirichletAllocation
from mempy3.config import CORPUSFRAMES_PATH, BASE_ANALYSIS_PATH
from mempy3.utils.dftools import tfidf_docterm_df
from mempy3.utils.dispenser import filter_metadata_index_list, load_nva_abs_docterm_df
from mempy3.utils.timer import Timer


def print_top_topics(df, num_docs=20):
    df = df.sample(num_docs)

    for i in range(num_docs):
        print(df.iloc[i].nlargest(20))
        print()


def print_avg_value_per_top_topic(df):
    n_topics = len(df.columns)
    #print(df)
    df['main_topic'] = df.idxmax(axis=1)
    #print(df)
    print(df['main_topic'].value_counts()[:15])
    # print([top for top in df.columns if top not in df['main_topic'].value_counts().index])

    for i in range(n_topics):
        print(df.groupby('main_topic').mean().iloc[i].nlargest(20))
        print()


def top_bot_topics(df, n=15):
    df['main_topic'] = df.idxmax(axis=1)
    print(df['main_topic'].value_counts()[:n])
    print(df['main_topic'].value_counts()[-n:])


if __name__ == '__main__':
    working_dir = 'topics_80_2_02_100_3_50_2k'
    df_file_name = 'doc_topics_df.p'
    # df_file_name = 'doc_topics_df.p'
    df = pickle.load(open(BASE_ANALYSIS_PATH / 'LDA' / working_dir / df_file_name, 'rb'))

    # print_top_topics(df, 20)
    print('\n********\n')
    print_avg_value_per_top_topic(df)
    print('\n********\n')
    # top_bot_topics(df)

