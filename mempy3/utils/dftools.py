"""Collection of tools, tests and shenanigans relative to dataframes"""

import pandas as pd
import numpy as np
import pickle
import csv
from mempy3.config import CORPUSFRAMES_PATH, LEXCATS_FULL, LEXCATS_BASE


def load_and_merge_dfs_from_pickles(path_list):
    """Loads and merges dfs from a list of Path objects

    Takes a list of Path objects pointing to pickled dfs
    Merges them horizontally according to the indexes of the first in the list
    Values in the other dfs that don't match any index will be discarded
    """

    return


def inspect_pickled_df(path):
    """Loads a pickled df from a Path obj and prints info"""
    df = pickle.load(open(path, 'rb'))
    print(df.index)
    print(list(df.columns))
    print(df.dtypes)
    print(f'Df using: {df.memory_usage(deep=True).sum() / (1024 ** 2)} mbs')
    print(df)


def tfidf_docterm_df(df):
    return (df.div(df.sum(axis=1), axis=0))*np.log(len(df)/(df > 0).sum())


def classify_lexical_occurences(df, cat_file):
    csvfile = open(cat_file, newline='')
    cat_dict = {n[0]: [n[i+1] for i in range(len(n)-1) if n[i+1] != ''] for n in csv.reader(csvfile)}
    for cat in cat_dict.keys():
        df[cat] = sum(df[w] for w in cat_dict[cat] if w in df.columns)
    return df.drop([col for col in df.columns if col not in cat_dict.keys()], axis=1)


if __name__ == '__main__':
    #inspect_pickled_df(CORPUSFRAMES_PATH / 'abs_nva_docterm_corpusframe.p')
    #print(classify_lexical_occurences(pickle.load(open(CORPUSFRAMES_PATH / 'lexicon_corpusframe.p', 'rb')), LEXCATS_BASE))
    print(tfidf_docterm_df(pd.DataFrame({'a': [1,0,0], 'b': [0,7,1]})))

