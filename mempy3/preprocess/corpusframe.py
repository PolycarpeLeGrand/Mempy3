import pandas as pd
from mempy3.config import DOCMODELS_PATH, CORPUSFRAMES_PATH, TT_EXCLUDED_TAGS, SPECIAL_CHARACTERS
from mempy3.preprocess.docmodel import DocModel
from mempy3.utils.timer import Timer
import pickle
import csv
'''
iter les dataframes
prendre les donnees qu'on veut (metas, txt & tags pour txt et abs)
les mettre dans un dataframe
ou un dict, qui apres devient un dataframe
genre big_dict[id] = {title:ad, text:dsfds, tt:sdfsd}
et dataframe from_dict

ensuite, ajouter keks colonnes genre doctype_cats et lens
    pourrait faire len(filtered tags) pour abs et txt et aussi len(paras) pour txt 
'''


def make_base_corpusframe(docmodels_path=DOCMODELS_PATH):
    dl = [dm.to_dict() for dm in DocModel.docmodel_generator(docmodels_path)]
    return pd.DataFrame(dl).set_index('id')


def make_corpusframe_from_docmodels(docmodels_path=DOCMODELS_PATH):
    d = {}
    for i, dm in enumerate(DocModel.docmodel_generator(docmodels_path)):
        d = dm.to_dict()
        #print(d[dm.get_id()])
        if (i + 1) % 10000 == 0:
            print(d)
            print(f'Processed {i + 1} docmodels...')
    return pd.DataFrame.from_dict(d, orient='index')


def make_std_corpusframe(file_path, col_structure):
    cf = pickle.load(open(file_path, 'rb'))
    doctype_cats = make_doctype_cats_dict()
    # cf.drop(columns=['raw_text_paragraphs', 'raw_abs_paragraphs'])
    cf['doctype_cat'] = doctype_cats[cf['doctype']]
    cf['abs_lemmas'] = [tag.lemma for tag in (sum(cf['tt_abs_paragraphs'])) if tag.pos not in TT_EXCLUDED_TAGS and
                        not any(sc in tag.lemma for sc in SPECIAL_CHARACTERS)]
    cf['text_lemmas'] = [tag.lemma for tag in (sum(cf['tt_text_paragraphs'])) if tag.pos not in TT_EXCLUDED_TAGS and
                         not any(sc in tag.lemma for sc in SPECIAL_CHARACTERS)]
    cf['num_abs_tokens'] = len(cf['abs_lemmas'])
    cf['num_text_tokens'] = len(cf['text_lemmas'])
    cf.drop(columns=['tt_abs_paragraphs', 'tt_text_paragraphs'])
    return cf


def make_doctype_cats_dict():
    csvfile = open('data\\docmodel_cats.csv', newline='')
    d = {n[0]: n[1] for n in csv.reader(csvfile)}
    print(d)
    return d


def flatten(paragraphs):
    return sum(paragraphs, [])


def filter_tags():
    pass


if __name__ == '__main__':
    print('Running corpusframe main')
    print('Will create base and std corpusframes')
    assert input('Enter \'Y\' to continue...').lower() == 'y'
    timer = Timer()

    '''
    df = pickle.load(open(CORPUSFRAMES_PATH / 'metadata_corpusframe.p', 'rb'))
    print(f'Using {df.memory_usage(index=True).sum()/(1024**2)} mbs')
    print(df.columns)
    '''

    print('\nStarting to work on base corpusframe...')
    cf = make_base_corpusframe()
    pickle.dump(cf, open(CORPUSFRAMES_PATH / 'base_corpusframe.p', 'wb'))
    print(cf)
    timer.step('First step done!')


    '''
    print('\nStarting to work on std corpusframe')
    std_cf = make_std_corpusframe(cf)
    pickle.dump(std_cf, open(CORPUSFRAMES_PATH / 'std_corpusframe.p', 'wb'))
    timer.step('Second step done!')
    print(f'Made std corpusframe with columns: {std_cf.columns}')
    print(std_cf)
    '''

