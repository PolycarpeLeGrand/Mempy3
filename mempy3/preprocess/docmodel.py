import pickle
import os
import treetaggerwrapper
from config import *
import pandas as pd
import csv


class DocModel:
    TAGGER = treetaggerwrapper.TreeTagger(TAGLANG='en')

    '''
    with open('data\\docmodel_cats.csv', newline='') as csvfile:
        DOCTYPE_CATS = {n[0]: n[1] for n in csv.reader(csvfile)}
    print('util globals loaded')
    '''
    def __init__(self, origin_file, tree, save_path, save_on_init=True, extract_metadata_on_init=True):
        # file data
        self.tree = tree
        self.origin_file = origin_file
        self.path = save_path
        self.filename = origin_file[:-4] + '.p'

        # metadata
        self.id = origin_file[:-4]
        self.year = None
        self.title = None
        self.source = None
        self.doctype = None
        self.doctype_cat = None

        # text
        self.raw_text_paragraphs = None
        self.raw_abstract_paragraphs = None
        self.has_text = False
        self.has_abstract = False

        # tt
        self.text_tt_paragraphs = None
        self.abstract_tt_paragraphs = None

        # others
        self.log = {}

        # extract and save on creation
        if extract_metadata_on_init:
            self.extract_all_metadata()
        if save_on_init:
            self.save_to_pickle()

    ### Getters ###
    def get_id(self):
        return self.id

    def get_year(self):
        return self.year

    def get_title(self):
        return self.title

    def get_source(self):
        return self.source

    def get_doctype(self):
        return self.doctype

    def get_doctype_cat(self):
        return self.doctype_cat

    def get_has_text(self):
        return self.has_text

    def get_has_abstract(self):
        return self.has_abstract

    def get_raw_text(self, splitter='\n'):
        return splitter.join(para for para in self.raw_text_paragraphs)

    def get_raw_abstract(self, splitter='\n'):
        return splitter.join(para for para in self.raw_abstract_paragraphs)

    def get_text_lemmas(self, filter_tags=True, flatten=True):
        return DocModel.format_tt_values(self.text_tt_paragraphs, attribute='lemma', filter_tags=filter_tags, flatten=flatten)

    def get_abstract_lemmas(self, filter_tags=True, flatten=True):
        return DocModel.format_tt_values(self.abstract_tt_paragraphs, attribute='lemma', filter_tags=filter_tags, flatten=flatten)

    def get_text_tags(self):
        return DocModel.format_tt_values(self.text_tt_paragraphs, filter_tags=True, flatten=True)

    def get_abstract_tags(self):
        return DocModel.format_tt_values(self.abstract_tt_paragraphs, filter_tags=True, flatten=True)

    def get_num_tokens(self):
        return len(self.get_text_lemmas())

    def get_num_uni_tokens(self):
        return len(set(self.get_text_lemmas()))

    def get_num_abstract_tokens(self):
        return len(self.get_abstract_lemmas())

    def get_lexical_counts(self, text=True, abstract=True):
        assert (text or abstract), "Why would you call this method with both params False???"
        r = []
        if text:
            r.append(pickle.load(open(DF_RESULTS_DIR+'lexicon_df.p', 'rb')).loc[[self.id]])
        if abstract:
            r.append(pickle.load(open(DF_RESULTS_DIR+'lexicon_abs_df.p', 'rb')).loc[[self.id]])
        return pd.concat(r, axis=1, sort=False)

    ### Extractors ###
    def extract_id(self):
        try:
            id = self.tree.getroot()[0].text
            if id != self.id:
                print(f'id mismatch on doc from {self.origin_file}, using xml id')
            self.id = id
        except:
            self.id = 'error'
            print(f'Error updating id on doc from {self.origin_file}')

    def extract_year(self):
        try:
            self.year = self.tree.getroot()[2][1].find("pubdate").text
        except:
            self.year = 'error'
            print(f'Error updating year on {self.id}')

    def extract_title(self):
        try:
            self.title = ''.join(self.tree.getroot()[2].find("bibl").find("title")[0].itertext())
        except:
            self.title = 'error'
            print(f'Error updating title on {self.id}')

    def extract_source(self):
        try:
            s = self.tree.getroot()[2][1].find("source").text
            self.source = s.lower().strip()
        except:
            self.source = 'error'
            print(f'Error updating source on {self.id}')

    def extract_doctype(self):
        try:
            d = self.tree.getroot()[2][0].text
            self.doctype = d.lower().strip()
        except:
            self.doctype = 'error'
            print(f'Error updating doctype on {self.id}')

    def extract_doctype_category(self):
        try:
            self.doctype_cat = DocModel.DOCTYPE_CATS[self.doctype]
        except:
            self.doctype_cat = 'error'
            print(f'Error updating doctype category on {self.id}')

    def extract_all_metadata(self):
        self.extract_id()
        self.extract_year()
        self.extract_title()
        self.extract_source()
        self.extract_doctype()

    def extract_abstract(self):
        self.raw_abstract_paragraphs, self.has_abstract = self.extract_content_paragraphs('.fm/abs')

    def extract_text(self):
        self.raw_text_paragraphs, self.has_text = self.extract_content_paragraphs('bdy')

    def treetag_abstract(self):
        self.abstract_tt_paragraphs = self.treetag_paragraphs(self.raw_abstract_paragraphs)

    def treetag_text(self):
        self.text_tt_paragraphs = self.treetag_paragraphs(self.raw_text_paragraphs)

    ### work and process methods ###
    ### private ###

    # additional trash sections to consider: abbr, abbrgrp
    # work_section : bdy, abs
    def extract_content_paragraphs(self, work_section, min_para_len=5, trash_sections=('st', 'tbl', 'display-formula', 'fig', 'file', 'suppl', 'table')):
        bdy = self.tree.find(work_section)
        success = True
        try:
            for sec in trash_sections:
                for ele in bdy.iter(sec):
                    ele.clear()
            para_list = list(filter(lambda x: len(x) > min_para_len, [''.join(t for t in para.itertext()) for para in bdy.iter('p')]))
        except:
            print(f'Error processing {work_section} on {self.filename}')
            para_list = ['error']
            success = False
        if len(para_list) == 0:
            print(f'No {work_section} for file {self.id}')
            para_list = ['no text']
            success = False
        return para_list, success

    ### TreeTagger preprocess and parse ###

    # Process chaque paragraphe avec TreeTagger pour les transformer en listes de tags
    # Prend une liste [str, str, str,str]
    # Retourne une liste [ [tag, tag, tag], [tag, tag, tag] ]
    def treetag_paragraphs(self, paragraphs):
        try:
            tt_tags = [treetaggerwrapper.make_tags(DocModel.TAGGER.tag_text(para.lower()), exclude_nottags=True) for para in paragraphs]
        except:
            print(f'Treetagging error on id: {self.id}')
            tt_tags = []
        return tt_tags

    # attributes: 'lemma', 'pos', 'word'
    # Prend une liste 2d de paragraphes tt tags et applique les filtres specifies
    # Call d'autres fcts selong les params
    # Retourne une liste paragraphes 2d avec les specs demandees
    # TODO add split sentences
    @staticmethod
    def format_tt_values(paragraphs, attribute=None, filter_tags=True, flatten=False):
        if filter_tags:
            paragraphs = DocModel.filter_tt_tags(paragraphs)
        if attribute:
            paragraphs = DocModel.select_tt_attributes(paragraphs, attribute)
        if flatten:
            paragraphs = DocModel.flatten_paragraphs(paragraphs)
        return paragraphs

    # Prend une liste 2d de paragraphes de tt tags et filtre selon excluded tags et special chars
    # Retourne une liste sans les tags avec POS exclus ou special chars dans le lemma
    @staticmethod
    def filter_tt_tags(paragraphs, excluded_tags=TT_EXCLUDED_TAGS, special_chars=SPECIAL_CHARACTERS):
        return [[tag for tag in para if tag.pos not in excluded_tags and not any(sc in tag.lemma for sc in special_chars)] for para in paragraphs]

    # Prend une liste 2d de paragraphes de tt tags et extrait un element
    # Retourne liste avec meme format et dimensions, mais lemma (ou autre element) a la place de Tag complet
    # lemma, pos, word
    @staticmethod
    def select_tt_attributes(paragraphs, attribute):
        return [[getattr(tag, attribute) for tag in para] for para in paragraphs]

    # Prend une liste 2d et la reduit a 1d en sommant les elements
    # Utile pour reduire les listes separees en paragraphes en liste pour le texte complet
    @staticmethod
    def flatten_paragraphs(paragraphs):
        return sum(paragraphs, [])

    def save_to_pickle(self, path=None, filename=None):
        if not path:
            path = self.path
        if not filename:
            filename = self.filename
        pickle.dump(self, open(path + filename, 'wb'))

    def __str__(self):
        return f'DocModel {self.id} {self.title}'

    def __repr__(self):
        return {'title': self.title}

    @classmethod
    def load_from_pickle(cls, path, filename):
        return pickle.load(open(path + filename, 'rb'))

    @classmethod
    def docmodel_generator(cls, path, conditions=None):
        for filename in os.listdir(path):
            try:
                dm = pickle.load(open(path + filename, 'rb'))
                if not conditions or conditions(dm):
                    yield dm
            except EOFError:
                print(f'Generator error on file: {filename}')


if __name__ == '__main__':
    test_path = SUB_K_DOCMODELS_DIR
    srs_path = SUB_K_CORPUS_DIR
    test_1 = '1465-9921-8-16.p'
    test_2 = '1297-9686-44-13.p'
    dm = pickle.load(open(test_path + test_1, 'rb'))
    # TAGGER = treetaggerwrapper.TreeTagger(TAGLANG='en')
    # dm.treetag_text()
    print(dm.get_lexical_counts())


