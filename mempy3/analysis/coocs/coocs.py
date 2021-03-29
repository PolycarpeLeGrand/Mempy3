from collections import defaultdict, Counter
from mempy3.preprocess.docmodel import DocModel
import pandas as pd
from mempy3.config import DOCMODELS_PATH, BASE_ANALYSIS_PATH, SPECIAL_CHARACTERS_EXTENDED, TT_BASE_TAGS, LEX_FULL
import pickle
import numpy as np
import string
import csv
from pathlib import Path

from mempy3.preprocess.corpusframe import word_counts

ta = 'allo je suis un gros legume et je suis tres gentil'.split(' ')
tb = 'bonjour je mappelle gentil et je suis un tres gros legume'.split(' ')


def make_coocs_df_3(lexicon, window=5, id_list=None, tag_list=None):
    d = defaultdict(Counter)
    for dm in DocModel.docmodel_generator(DOCMODELS_PATH):
        if (id_list is not None) and (dm.get_id() not in id_list):
            continue
        for para in dm.get_text_tags():
            # para = [tag for tag in para if tag.pos in tag_list]
            para = list(filter(lambda x: x.pos in tag_list, para))
            for i, tag in enumerate(para):
                # if tag.pos in tag_list:
                beg = max(i - window, 0)
                end = i + window + 1
                    #if len(tag.lemma) > 2 and not(any(char in SPECIAL_CHARACTERS_EXTENDED for char in tag.lemma)):
                d[tag.lemma].update(map(lambda x: x.lemma, para[beg:end]))
                    #d[tag.lemma].update([tag.lemma for tag in para[beg:end] if len(tag.lemma) > 2 and not(any(char in SPECIAL_CHARACTERS_EXTENDED for char in w))])
                    #d[tag.lemma].update([tag.lemma for tag in para[beg:end] if tag.lemma in lexicon])

    d = dict(d)
    print(len(d.keys()))
    print(len(lexicon))
    return pd.DataFrame(d, index=lexicon, columns=lexicon)


def filter_coocs_from_lex(lex_csv_path):
    csvfile = open(lex_csv_path, newline='')
    lexicon = [r[0] for r in csv.reader(csvfile)]
    #lexicon = [r[i+1] for r in csv.reader(csvfile) for i in range(len(r)-1) if r[i+1] != '']
    return lexicon


def calc_coocs_on_docs(index, group_name, tag_list=None):

    save_path = Path(BASE_ANALYSIS_PATH / f'coocs/{group_name}')
    save_path.mkdir(exist_ok=True)

    # Can comment out once ran once if settings remaine the same, will greatly reduce run time
    # word_counts_df = word_counts(min_token_len=3, id_list=index, tag_list=tag_list)
    # word_counts_df.to_pickle(save_path / 'filtered_word_counts_df.p')
    word_counts_df = pd.read_pickle(save_path / 'filtered_word_counts_df.p')

    cooc_lexicon = word_counts_df[word_counts_df['article_counts'] >= 50].index
    cooc_lexicon = [w for w in cooc_lexicon if
                    (len(w) > 2) and not (any(char in SPECIAL_CHARACTERS_EXTENDED for char in w))]

    df = make_coocs_df_3(lexicon=cooc_lexicon, id_list=index, tag_list=tag_list)
    # stop = ['the', 'and', 'for', 'with', 'that', 'have', 'use', 'from', 'not', 'these', 'all', 'also']
    # df.drop(stop, inplace=True)

    # Normalize
    #word_counts_df = word_counts_df.loc[df.index]
    #df = df / word_counts_df['total_occs']

    target_words = filter_coocs_from_lex(LEX_FULL)
    df = df[[w for w in target_words if w in df.columns]]
    print(df)
    df.to_pickle(save_path / 'coocs_corpus_lexicon_df.p')


def iter_clusters_for_coocs(cluster_name):

    with open(BASE_ANALYSIS_PATH / 'LDA/topics_80_2_02_100_3_50_2k/reductions_df.p', 'rb') as f:
        tdf = pickle.load(f)
        index = list(tdf[(tdf['clustering_7'] == cluster_name)].index)
        del tdf

    calc_coocs_on_docs(index, cluster_name.replace(' ', '_').lower(), tag_list=TT_BASE_TAGS)


if __name__ == '__main__':

    for i in range(7):
        iter_clusters_for_coocs(f'Cluster {i}')
        print('*********')
        print(f'Done with Cluster {i}')
        print('*********')

    calc_coocs_on_docs(None, 'corpus', tag_list=TT_BASE_TAGS)

    assert False

    calc_ccocs_on_cluster('Cluster 1')
    df = pd.read_pickle(BASE_ANALYSIS_PATH / 'coocs/full_corpus/coocs_full_df.p')
    wd_df = pickle.load(open(CORPUSFRAMES_PATH / 'text_word_counts_filtered_ids_df.p', 'rb'))

    lex = filter_coocs_from_lex(LEXCATS_FULL)
    print(len(lex))

    stop = ['the', 'and', 'for', 'with', 'that', 'have', 'use', 'from', 'not', 'these', 'all', 'also']
    df.drop(stop, inplace=True)
    wd_df = wd_df.loc[df.index]
    df = df / wd_df['total_occs']

    words = ['model', 'explain', 'mechanism', 'see']
    df = df[[w for w in lex if w in df.columns]]

    print(df)
    print(df['model'].nlargest(30))
    print(df['mechanism'].nlargest(30))
    print(df['explain'].nlargest(30))

    pickle.dump(df, open(BASE_ANALYSIS_PATH / 'coocs/full_corpus/coocs_corpus_lexicon_df.p', 'wb'))
    print(df.sum().nlargest(30))
    print(df.sum())
    assert False

    index = list(pickle.load(open(BASE_ANALYSIS_PATH / 'LDA/topics_80_2_02_100_3_50_2k/reductions_df.p', 'rb')).index)
    lexicon = wd_df[wd_df['article_counts'] >= 50].index
    lexicon = [w for w in lexicon if (len(w) > 2) and not(any(char in SPECIAL_CHARACTERS_EXTENDED for char in w))]
    print(lexicon)
    print(len(lexicon))
    df = make_coocs_df_3(lexicon=lexicon, id_list=index)

    #rf = wd_df.loc[df.index]
    #print(rf)
    #df = df / rf['total_occs']

    print(df)
    print(df['model'].nlargest(10))
    print(df['mechanism'].nlargest(10))
    print(df['explain'].nlargest(10))

    pickle.dump(df, open(BASE_ANALYSIS_PATH / 'coocs_full_df.p', 'wb'))

    #f = a.reindex_like(b).fillna(0) + b.fillna(0).fillna(0)
    #g = b.reindex_like(a).fillna(0) + a.fillna(0).fillna(0)
    #print(f)
    #print(g)


    #print(d)
    #df = pd.DataFrame(d, index=d.keys(), columns=d.keys())
    #print(df)



