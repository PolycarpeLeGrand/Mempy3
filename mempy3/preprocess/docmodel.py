"""Defines the DocModel class, used to represent docs.

Running parser.py will make a DocModel object for each doc (xml file) and pickle it.
These objects hold the metadata and text data for each doc, as to not rely on xml files.
Use getter functions to access instance variables.

DocModel functions must be adjusted depending on the xml format(s)
"""

import pickle
import os
import treetaggerwrapper
import itertools
from spacy.lang.en import English


class DocModel:
    def __init__(self, origin_file, tree, save_path, save_on_init=True, extract_metadata_on_init=True):
        # file data
        self.tree = tree
        self.origin_file = origin_file
        self.filename = origin_file[:-4] + '.p'
        self.file_path = save_path / self.filename

        # metadata
        self.id = origin_file[:-4]
        self.year = None
        self.title = None
        self.source = None
        self.doctype = None
        self.issn = None
        self.keywords = None

        self.doctype_cat = None
        self.primary_subjects = None
        self.secondary_subjects = None

        # text
        self.raw_text_paragraphs = None
        self.raw_abs_paragraphs = None

        # tt
        self.tt_text_paragraphs = None
        self.tt_abs_paragraphs = None

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

    def get_issn(self):
        return self.issn

    def get_keywords(self):
        return self.keywords

    def get_doctype_cat(self):
        return self.doctype_cat

    def get_primary_subjects(self):
        return self.primary_subjects

    def get_secondary_subjects(self):
        return  self.secondary_subjects

    def get_raw_text(self):
        """Get text as a list of paragraphs ['para1 text', 'para 2 text']"""

        return self.raw_text_paragraphs

    def get_raw_abs(self):
        """Get abstract text as a list of paragraphs ['para1 text', 'para 2 text']"""

        return self.raw_abs_paragraphs

    def get_text_tags(self):
        """Get text tags as 2d list [[para1 Tags], [para2 Tags], ...]"""

        return self.tt_text_paragraphs

    def get_abs_tags(self):
        """Get abstract tags as 2d list [[para1 Tags], [para2 Tags], ...]"""

        return self.tt_abs_paragraphs

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

    def extract_issn(self):
        try:
            d = self.tree.getroot()[2][1].find("issn").text
            self.issn = d.lower().strip()
        except:
            self.issn = 'error'
            print(f'Error updating issn on {self.id}')

    def extract_doctype_cat(self, doctype_cats_mapping):
        try:
            self.doctype_cat = doctype_cats_mapping[self.doctype]
        except:
            self.doctype_cat = 'error'
            print(f'Error updating doctype cat on {self.id}. Base doctype: {self.doctype}')

    def extract_primary_subjects(self, primary_subjects_mapping):
        try:
            self.primary_subjects = primary_subjects_mapping[self.source]
        except:
            self.primary_subjects = []
            print(f'Error updating primary subjects on {self.id}. Source: {self.source}. Issn: {self.issn}')

    def extract_secondary_subjects(self, secondary_subjects_mapping):
        try:
            self.secondary_subjects = secondary_subjects_mapping[self.source]
        except:
            self.secondary_subjects = []
            print(f'Error updating secondary subjects on {self.id}. Source: {self.source}. Issn: {self.issn}')

    def extract_keywords(self):
        try:
            self.keywords = [kwd.text.lower() for kwd in self.tree.getroot()[2].find('kwdg').iter('kwd')]
        except:
            self.keywords = []
            print(f'Error updating keywords on {self.id}')

    def extract_all_metadata(self):
        self.extract_id()
        self.extract_year()
        self.extract_title()
        self.extract_source()
        self.extract_doctype()
        self.extract_issn()
        self.extract_keywords()

    def extract_abstract(self, trash_sections):
        self.raw_abs_paragraphs = self.extract_content_paragraphs('.fm/abs', trash_sections)

    def extract_text(self, trash_sections):
        self.raw_text_paragraphs = self.extract_content_paragraphs('bdy', trash_sections)

    def treetag_abstract(self, tagger):
        self.tt_abs_paragraphs = self.treetag_paragraphs(self.raw_abs_paragraphs, tagger)

    def treetag_text(self, tagger):
        self.tt_text_paragraphs = self.treetag_paragraphs(self.raw_text_paragraphs, tagger)

    def extract_coocs(self):
        return ''

    ### work and process methods ###
    ### private ###

    # additional trash sections to consider: abbr, abbrgrp
    # work_section : bdy, abs
    def extract_content_paragraphs(self, work_section, trash_sections, min_para_len=5):
        bdy = self.tree.find(work_section)
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
        return para_list

    def to_viz_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'source': self.source,
            'doctype': self.doctype,
            'year': self.year,
            'abstract_paras': self.raw_abs_paragraphs,
            'text_paras': self.raw_text_paragraphs
        }

    def calc_coocs(self):
        self.get_text_tags()
        return

    ### TreeTagger preprocess and parse ###

    # Process chaque paragraphe avec TreeTagger pour les transformer en listes de tags
    # Prend une liste [str, str, str,str]
    # Retourne une liste [ [tag, tag, tag], [tag, tag, tag] ]
    def treetag_paragraphs(self, paragraphs, tagger):
        try:
            tt_tags = [treetaggerwrapper.make_tags(tagger.tag_text(para.lower()), exclude_nottags=True) for para in paragraphs]
        except:
            print(f'Treetagging error on id: {self.id}')
            tt_tags = []
        return tt_tags

    def save_to_pickle(self, destination=None):
        save_to = destination if destination else self.file_path
        pickle.dump(self, open(save_to, 'wb'))

    def __str__(self):
        return f'DocModel {self.id} - {self.title}'

    def __repr__(self):
        return {'id': self.id, 'title': self.title}

    @classmethod
    def load_from_pickle(cls, path, filename):
        return pickle.load(open(path / filename, 'rb'))

    @classmethod
    def docmodel_generator(cls, path, vocal=True, conditions=None):
        for i, filename in enumerate(os.listdir(path)):
            with open(path / filename, 'rb') as f:
                try:
                    dm = pickle.load(f)
                    if not conditions or conditions(dm):
                        yield dm
                except EOFError:
                    print(f'Generator error on file: {filename}')
            if vocal and i % 5000 == 0:
                print(f'Generating {i}th docmodel')


if __name__ == '__main__':
    # test_path = SUB_K_DOCMODELS_DIR
    # srs_path = SUB_K_CORPUS_DIR
    from mempy3.config import DOCMODELS_PATH
    # from mempy3.config import BASE_STORAGE_PATH
    # test_1 = '1465-9921-8-16.p'
    # test_1 = '1297-9686-44-13.p'
    #test_1 = '0778-7367-67-1-15.p'
    #dm = pickle.load(open(DOCMODELS_PATH / test_1, 'rb'))

    for dm in DocModel.docmodel_generator(DOCMODELS_PATH):
        dm.extract_issn()
        dm.extract_keywords()
        dm.save_to_pickle(DOCMODELS_PATH / dm.filename)

