"""Tools used to build dataframes representing certain aspects of the corpus.

This is a collection of functions used to build various dataframes from the DocModels
The idea is to pre-build DFs that will be used a lot in order to avoid starting from scratch every time
This speeds up the process significantly, especially when testing, since we can just load the relevant df
    instead of getting the info from the DocModels

These dfs can be combined, filtered, etc. as needed.
We keep each one specific as to keep memory usage reasonable.

corpus frames:
Index only
Metadata (add doctype cats)
lexcounts (abs et txt)
docterm filtred abs
"""

import pandas as pd
from mempy3.config import DOCMODELS_PATH, CORPUSFRAMES_PATH, TT_EXCLUDED_TAGS, SPECIAL_CHARACTERS, TT_NOUN_TAGS, \
    TT_VERB_TAGS, TT_ADJ_TAGS, PRIMARY_SUBJECTS_CSV_PATH, SECONDARY_SUBJECTS_CSV_PATH, BASE_ANALYSIS_PATH, TT_BASE_TAGS
from mempy3.preprocess.docmodel import DocModel
from mempy3.utils.timer import Timer
import pickle
import csv
from collections import Counter
import numpy as np


def filter_tags_basic(tag_paras):
    """Takes a TT paras list, returns a lemma paras list of same dimension

    Filters words with pos tag in TT_EXCLUDED_TAGS (defined in config.py)
    Also filters words with special characters (see SPECIAL_CHARACTERS in config.py)
    """

    return [[tag.lemma for tag in para
             if (tag.pos not in TT_EXCLUDED_TAGS) and not(any(char in SPECIAL_CHARACTERS for char in tag.lemma))]
            for para in tag_paras]


def filter_tags_nva(tag_paras, min_lemma_len=3):
    """Takes a TT paras list, returns a lemma paras list of same dimension

    Keeps only words with tags in TT_NOUN_TAGS, TT_VERB_TAGS or TT_ADJ_TAGS (defined in config.py)
    Also filters out words with special characters (see SPECIAL_CHARACTERS in config.py) and shorter than min_lemma_len
    """

    return [[tag.lemma for tag in para
             if ((tag.pos in TT_NOUN_TAGS or tag.pos in TT_VERB_TAGS or tag.pos in TT_ADJ_TAGS)
                 and not(any(char in SPECIAL_CHARACTERS for char in tag.lemma)) and len(tag.lemma) >= min_lemma_len)]
            for para in tag_paras]


def filter_lemmas(lemma_list, accepted_lemmas):
    """Takes a list of words and returns a list keeping only words that are present in accepted_lemmas"""

    return [lem for lem in lemma_list if lem in accepted_lemmas]


def flatten_paras(paras):
    """Flattens a 2d list in a 1d list"""

    return sum((para for para in paras), [])


def load_doctype_cats():
    csvfile = open('data\\doctype_cats.csv', newline='')
    return {n[0]: n[1] for n in csv.reader(csvfile)}


def load_lexicon():
    csvfile = open('data\\lexicon_words.csv', newline='')
    return [n[0] for n in csv.reader(csvfile)]


def list_paragraphs(docmodels_path=DOCMODELS_PATH):
    """Returns a list of all paragraph names in the corpus, format: docid_paranum"""

    return [f'{dm.get_id()}_para{i}' for dm in DocModel.docmodel_generator(docmodels_path, vocal=True) for i in range(len(dm.get_text_tags()))]


def words_counts_old(docmodels_path=DOCMODELS_PATH, save_to='nva_counts_series.p'):
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


def word_counts(workon='texts', docmodels_path=DOCMODELS_PATH, min_token_len=1, id_list=None, tag_list=None):
    """Counts word occurrences in texts or abstracts.

    id_list: list of article ids, will skip ids not in the list. If no list is provided, will run on while corpus.
    tag_list: will only keep tokens with a TT tag in the list. If None, will keep all tags.

    Returns a df with 2 columns, words as index:
        total_occs: total occurences of each word in the parsed texts
        article_counts: number of docs where each words is found at least once
    """

    options = {'texts': DocModel.get_text_tags, 'abstracts': DocModel.get_abs_tags}
    assert workon in options, f'Error in word_counts(): "workon" param must be in {options.keys()}'
    fct = options[workon]

    total_occs = Counter()
    article_counts = Counter()

    for dm in DocModel.docmodel_generator(docmodels_path, vocal=True):
        if (id_list is not None) and (dm.get_id() not in id_list):
            continue
        words = [tag.lemma for tag in flatten_paras(fct(dm)) if len(tag.lemma) >= min_token_len and (tag_list is None or (tag.pos in tag_list))]
        total_occs.update(words)
        article_counts.update(set(words))

    total_occs_s = pd.Series(total_occs)
    article_counts_s = pd.Series(article_counts)

    return pd.DataFrame({'total_occs': total_occs_s, 'article_counts': article_counts_s})


# WARNING: check if fct is abs or text
# fait un df index=ids et cols=mots du lexique, data est le nombre d'occurence de chaque mot
# pour rien manquer et etre plus simple, check si tag.word est dans le lexique, mais ajoute tag.lemma au df
# probablement des cols qui vont etre a 0, mais on travaille avec des categories alors c'est pas grave
def make_lexical_counts_corpusframe(docmodels_path=DOCMODELS_PATH):

    tag_fct = DocModel.get_abs_tags
    lexicon_words = load_lexicon()

    # Creates a df with right dims by loading doc ids from metadata corpusframe. Is faster than building as we go
    with open(CORPUSFRAMES_PATH / 'metadata_corpusframe.p', 'rb') as meta_df:
        df = pd.DataFrame(np.float32(0.0), index=lexicon_words, columns=pickle.load(meta_df).index) # .astype(np.uint8)

    for dm in DocModel.docmodel_generator(docmodels_path):
        cnt = Counter(flatten_paras([[tag.lemma for tag in para if tag.word in lexicon_words] for para in tag_fct(dm)]))
        df[dm.get_id()].update(pd.Series(cnt, dtype=np.float32))

    return df.transpose()


# WARNING: check if fct is abs or text.
def make_lexical_counts_paras_corpusframe(docmodels_path=DOCMODELS_PATH):
    lexicon_words = load_lexicon()
    cols = []
    for dm in DocModel.docmodel_generator(docmodels_path):
        for i, para in enumerate(dm.get_text_tags()):
            cols.append(f'{dm.get_id()}_para{i}')

    df = pd.DataFrame(np.float32(0.0), index=lexicon_words, columns=cols)  # .astype(np.uint8)
    for dm in DocModel.docmodel_generator(docmodels_path):
        for i, para in enumerate(dm.get_text_tags()):
            cnt = Counter([tag.lemma for tag in para if tag.word in lexicon_words])
            df[f'{dm.get_id()}_para{i}'].update(pd.Series(cnt, dtype=np.float32))
    '''
    df = pd.DataFrame(index=lexicon_words, dtype=np.float32)
    for dm in DocModel.docmodel_generator(docmodels_path):
        for i, para in enumerate(dm.get_text_tags()):
            df[f'{dm.get_id()}_para{i}'] = df.index.map(Counter([tag.lemma for tag in para if tag.word in lexicon_words]))
    '''
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
    #doctype_cats = load_doctype_cats()
    return pd.DataFrame.from_records([{'id': dm.get_id(),
                                       'title': dm.get_title(),
                                       'year': dm.get_year(),
                                       'source': dm.get_source(),
                                       'issn': dm.get_issn(),
                                       'doctype': dm.get_doctype(),
                                       'doctype_cat': dm.get_doctype_cat(),
                                       'primary_subjects': dm.get_primary_subjects(),
                                       'secondary_subjects': dm.get_secondary_subjects(),
                                       'abs_tokens': len(flatten_paras(filter_tags_basic(dm.get_abs_tags()))),
                                       'text_tokens': len(flatten_paras(filter_tags_basic(dm.get_text_tags())))}
                                      for dm in DocModel.docmodel_generator(docmodels_path)], index='id')


def make_source_subjects_df(subjects_mapping_csv_path):
    """From a subjects csv path, makes a True/False source x subjects df"""

    with open(subjects_mapping_csv_path, newline='') as cd_csv:
        subjects_mapping = {n[0]: [n[i] for i in range(1, len(n)) if n[i] != ''] for n in csv.reader(cd_csv)}
    subjects = set(pd.core.common.flatten(subjects_mapping.values()))
    return pd.DataFrame.from_records([{subject: subject in source_subjects for subject in subjects}
                                      for source_subjects in subjects_mapping.values()],
                                     index=subjects_mapping.keys())



def corpusframe_wrapper(func, save_name):
    return


def docterm_wrapper():
    # wordlist ou criteres
    # id list a partir de meta_cf_filtered.index
    # bref, on fait un wrapper pour faire des docterms en instanciant un df init avec les bons axes/dims et des 0
    return


if __name__ == '__main__':


    index = pickle.load(open(BASE_ANALYSIS_PATH / 'LDA/topics_80_2_02_100_3_50_2k/reductions_df.p', 'rb')).index
    print(index)
    wc = word_counts(id_list=list(index))
    print(wc)
    print(wc['total_occs'].nlargest(30))
    print(wc['total_occs'].nsmallest(30))
    print(wc['article_counts'].nlargest(30))
    print(wc['article_counts'].nsmallest(30))

    print('******')
    print(wc[wc['article_counts'] <= 5])
    print()
    pickle.dump(wc, open(CORPUSFRAMES_PATH / 'text_word_counts_filtered_ids_df.p', 'wb'))

    # tf = df['primary_subjects'].apply(pd.Series)
    # print(tf.unique())

    # pf = make_source_subjects_df(PRIMARY_SUBJECTS_CSV_PATH)
    # sf = make_source_subjects_df(SECONDARY_SUBJECTS_CSV_PATH)
    # pickle.dump(pf, open(CORPUSFRAMES_PATH / 'primary_subjects_df.p', 'wb'))
    # pickle.dump(sf, open(CORPUSFRAMES_PATH / 'secondary_subjects_df.p', 'wb'))

    assert False
    corpusframe_fct = make_metadata_corpusframe
    save_name = 'metadata_corpusframe_2.p'

    print('Running corpusframe main.')
    print(f'Making corpusframe with dict {corpusframe_fct.__name__}, saving as {save_name} ')
    assert input('Enter \'Y\' to continue...').lower() == 'y'

    timer = Timer()
    df = corpusframe_fct()
    pickle.dump(df, open(CORPUSFRAMES_PATH / save_name, 'wb'))
    print(f'Done pickling! Run time: {timer.get_run_time()}')
    print(f'Df using: {df.memory_usage(deep=True).sum() / (1024 ** 2)} mbs')
    print(df.dtypes)
    print(df)

