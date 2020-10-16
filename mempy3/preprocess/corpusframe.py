import pandas as pd
from mempy3.config import DOCMODELS_PATH, CORPUSFRAMES_PATH, TT_EXCLUDED_TAGS, SPECIAL_CHARACTERS, TT_NOUN_TAGS, TT_VERB_TAGS, TT_ADJ_TAGS
from mempy3.preprocess.docmodel import DocModel
from mempy3.utils.timer import Timer
import pickle
import csv
from collections import Counter
import numpy as np
import gc
'''
This module builds and saves pd dataframes representing different aspects of the corpus.

This allows to run different preprocess steps and save the results in an easily accessible way.
Since not everything can be loaded to memory at once, specific parts can be loaded and combined.
These dfs can also be combined with the result dfs of various analysis
TODO naming conventions

corpus frames:
Index only
Metadata (add doctype cats)
lexcounts (abs et txt)
docterm filtred abs
'''


def filter_tags_basic(tag_paras):
    return [[tag.lemma for tag in para
             if (tag.pos not in TT_EXCLUDED_TAGS) and not(any(char in SPECIAL_CHARACTERS for char in tag.lemma))]
            for para in tag_paras]


def filter_tags_nva(tag_paras):
    return [[tag.lemma for tag in para
             if (tag.pos in TT_NOUN_TAGS or tag.pos in TT_VERB_TAGS or tag.pos in TT_ADJ_TAGS)
             and not(any(char in SPECIAL_CHARACTERS for char in tag.word))]
            for para in tag_paras]


def filter_lemmas(lemma_list, accepted_lemmas):
    return [lem for lem in lemma_list if lem in accepted_lemmas]


def flatten_paras(paras):
    return sum((para for para in paras), [])


def load_doctype_cats():
    csvfile = open('data\\doctype_cats.csv', newline='')
    return {n[0]: n[1] for n in csv.reader(csvfile)}


def load_lexicon():
    csvfile = open('data\\lexicon_words.csv', newline='')
    return [n[0] for n in csv.reader(csvfile)]


def words_counts(docmodels_path=DOCMODELS_PATH, save_to='nva_counts_series.p'):
    c = Counter()
    for dm in DocModel.docmodel_generator(docmodels_path, vocal=True):
        c.update(flatten_paras(filter_tags_nva(dm.get_abs_tags())))
    c = pd.Series(c)
    pickle.dump(c, open(f'data\\{save_to}', 'wb'))
    print(c)
    print(f'len: {len(c)}')
    print((c >= 5).value_counts())
    print((c >= 10).value_counts())
    print((c >= 20).value_counts())


def make_lexical_counts_corpusframe(docmodels_path=DOCMODELS_PATH):
    lexicon_words = load_lexicon()
    print(lexicon_words)
    df = pd.DataFrame(np.float32(0.0), index=lexicon_words, columns=pickle.load(open(CORPUSFRAMES_PATH / 'metadata_corpusframe.p', 'rb')).index) # .astype(np.uint8)
    for dm in DocModel.docmodel_generator(docmodels_path):
        cnt = Counter(flatten_paras([[tag.lemma for tag in para if tag.word in lexicon_words] for para in dm.get_text_tags()]))
        df[dm.get_id()].update(pd.Series(cnt, dtype=np.float32))
    return df.transpose()


def make_abs_nva_docterm_corpusframe(docmodels_path=DOCMODELS_PATH):
    accepted_lemmas = pickle.load(open('data\\nva_counts_series.p', 'rb'))
    accepted_lemmas = list(accepted_lemmas[accepted_lemmas >= 10].index)
    df = pd.DataFrame(np.float32(0.0), index=accepted_lemmas, columns=pickle.load(open(CORPUSFRAMES_PATH / 'metadata_corpusframe.p', 'rb')).index) # .astype(np.uint8)
    for dm in DocModel.docmodel_generator(docmodels_path):
        cnt = Counter(filter_lemmas(flatten_paras(filter_tags_nva(dm.get_abs_tags())), accepted_lemmas))
        df[dm.get_id()].update(pd.Series(cnt, dtype=np.float32))
    return df.transpose()


def make_metadata_corpusframe(docmodels_path=DOCMODELS_PATH):
    doctype_cats = load_doctype_cats()
    return pd.DataFrame.from_records([{'id': dm.get_id(),
                                       'title': dm.get_title(),
                                       'year': dm.get_year(),
                                       'source': dm.get_source(),
                                       'doctype': dm.get_doctype(),
                                       'doctype_cat': doctype_cats[dm.get_doctype()],
                                       'abs_tokens': len(flatten_paras(filter_tags_basic(dm.get_abs_tags()))),
                                       'text_tokens': len(flatten_paras(filter_tags_basic(dm.get_text_tags())))}
                                      for dm in DocModel.docmodel_generator(docmodels_path)], index='id')


def corpusframe_wrapper(func, save_name):
    return


def docterm_wrapper():
    # wordlist ou criteres
    # id list a partir de meta_cf_filtered.index
    # bref, on fait un wrapper pour faire des docterms en instanciant un df init avec les bons axes/dims et des 0
    return

if __name__ == '__main__':
    #corpusframe_fct = words_counts
    corpusframe_fct = make_lexical_counts_corpusframe
    save_name = 'lexicon_corpusframe.p'

    print('Running corpusframe main.')
    print(f'Making corpusframe with dict {corpusframe_fct.__name__}, saving as {save_name} ')
    assert input('Enter \'Y\' to continue...').lower() == 'y'

    timer = Timer()
    df = corpusframe_fct()
    pickle.dump(df, open(CORPUSFRAMES_PATH / save_name, 'wb'))
    print(f'Done pickling! Run time: {timer.get_run_time()}')
    print(f'Df using: {df.memory_usage(deep=True).sum() / (1024 ** 2)} mbs')
    print(df)
