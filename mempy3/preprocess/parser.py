from mempy3.config import CORPUS_PATH, DOCMODELS_PATH, TRASH_SECTIONS
from mempy3.utils.timer import Timer
from mempy3.preprocess.docmodel import DocModel
import os
import xml.etree.ElementTree as ET
import treetaggerwrapper


def create_docmodels_from_xml_corpus(srs_path, save_path, extract_metadata=True):
    timer = Timer()
    print(f'Starting to parse xml files at {srs_path}...')
    for i, filename in enumerate(os.listdir(srs_path)):
        try:
            DocModel(filename, ET.parse(srs_path / filename), save_path, extract_metadata_on_init=extract_metadata)
        except:
            print(f'Error on {filename}')
        if (i+1) % 10000 == 0: print(f'Parsed {i+1} files...')
    print(f'Done! Parsing time: {timer.get_run_time()}')
    print("Save path : {}".format(save_path))


def extract_and_tag_docmodel_texts(path):
    timer = Timer()
    tagger = treetaggerwrapper.TreeTagger(TAGLANG='en')
    print(f'Starting to extract and tag texts from docmodels at {path}...')
    for i, dm in enumerate(DocModel.docmodel_generator(path)):
        dm.extract_abstract(TRASH_SECTIONS)
        dm.extract_text(TRASH_SECTIONS)
        dm.treetag_abstract(tagger)
        dm.treetag_text(tagger)
        dm.save_to_pickle()
        if (i+1) % 10000 == 0: print(f'Processed {i+1} docmodels...')
    print(f'Done! Processing time: {timer.get_run_time()}')


if __name__ == '__main__':
    c_path = CORPUS_PATH
    dm_path = DOCMODELS_PATH

    print('Preprocessing corpus with parser.py')
    print('For each document in the corpus, this will create a DocModel object and save it as a pickle.')
    print('Texts and abstracts will then be extracted and tagged for each DocModel.')
    print(f'Working on corpus at: {c_path}')
    print(f'Storing DocModels at: {dm_path}')
    assert input('Enter \'Y\' to continue... ').lower() == 'y'
    print('\n')

    create_docmodels_from_xml_corpus(c_path, dm_path)
    print('\n')
    extract_and_tag_docmodel_texts(dm_path)

    print('Corpus preprocessing done, have a good day!')

