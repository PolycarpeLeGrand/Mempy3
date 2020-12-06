"""Tools to filter corpusframes"""

import pandas as pd
import numpy as np
import pickle
from mempy3.config import CORPUSFRAMES_PATH


def filter_metadata_index_list(min_text_tokens=None, min_abs_tokens=None, min_year=None, doctype_cats=None):
    m_df = pickle.load(open(CORPUSFRAMES_PATH / 'metadata_corpusframe.p', 'rb'))

    if min_text_tokens:
        m_df = m_df[m_df['text_tokens'] >= min_text_tokens]
    if min_abs_tokens:
        m_df = m_df[m_df['abs_tokens'] >= min_abs_tokens]
    if min_year:
        m_df = m_df[m_df['year'] >= min_abs_tokens]
    if doctype_cats:
        m_df = m_df[m_df['doctype_cat'].isin(doctype_cats)]

    return list(m_df.index)


def load_nva_abs_docterm_df(filtered_index_list=None, min_tokens=None, min_word_occs=1, max_word_freq=1.0, log_norm=True):
    df = pickle.load(open(CORPUSFRAMES_PATH / 'abs_nva_docterm_corpusframe.p', 'rb'))

    if filtered_index_list:
        df = df.loc[filtered_index_list]
    if min_tokens:
        df = df[(df.sum(axis=1) >= min_tokens)]

    # df = df.loc[:, min_word_occs <= (df > 0).sum() <= max_word_freq*len(df)]
    df = df.drop((df > 0).sum()[lambda x: (x < min_word_occs) | (x > max_word_freq * len(df))].index, axis=1)

    if log_norm:
        df = df.apply(lambda x: np.log(x + 1))

    return df


if __name__ == '__main__':
    ind = filter_metadata_index_list(min_text_tokens=2000)
    # df = load_nva_abs_docterm_df(filtered_index_list=ind, min_tokens=100, min_word_occs=50, max_word_freq=0.3)
    df = load_nva_abs_docterm_df(filtered_index_list=ind, min_tokens=100, min_word_occs=10, max_word_freq=0.3, log_norm=False)
    print(df)
    print(df.sum().sum())
    print(load_nva_abs_docterm_df(filtered_index_list=ind, min_tokens=100, min_word_occs=50, max_word_freq=0.3, log_norm=False).sum().sum())


