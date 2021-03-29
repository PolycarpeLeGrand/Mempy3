"""Build DocModels from XML files and extract base data

Run as main or call parser_main()
Unless changes are made to the corpus or DocModel functions, this should only be ran once.
Be sure to set paths in config.py beforehand.
"""

from mempy3.config import CORPUS_PATH, DOCMODELS_PATH, TRASH_SECTIONS, DOCTYPE_CATS_CSV_PATH, PRIMARY_SUBJECTS_CSV_PATH, SECONDARY_SUBJECTS_CSV_PATH
from mempy3.utils.timer import Timer
from mempy3.preprocess.docmodel import DocModel
from mempy3.utils.utils import yn_input
import os
import xml.etree.ElementTree as ET
import treetaggerwrapper
import csv


def create_docmodels_from_xml_corpus(srs_path, save_path, extract_metadata=True):
    """Reads XMLs and create DocModel objects. Extracts metadata if asked to, which should usually be the case."""

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


def generate_metadata_from_mappings(docmodels_path, generate_doctype_cats=True,
                                    generate_primary_subjects=True, generate_secondary_subjects=True):
    """Generate 'subjects' and 'doctype cats' metadata from mappings loaded from CSV"""

    timer = Timer()

    if generate_doctype_cats:
        with open(DOCTYPE_CATS_CSV_PATH, newline='') as cd_csv:
            doctype_cats_mapping = {n[0]: n[1] for n in csv.reader(cd_csv)}
            print(doctype_cats_mapping)
    if generate_primary_subjects:
        with open(PRIMARY_SUBJECTS_CSV_PATH, newline='') as cd_csv:
            primary_subjects_mapping = {n[0]: [n[i] for i in range(1, len(n)) if n[i] != ''] for n in csv.reader(cd_csv)}
            print(primary_subjects_mapping)
    if generate_secondary_subjects:
        with open(SECONDARY_SUBJECTS_CSV_PATH, newline='') as cd_csv:
            secondary_subjects_mapping = {n[0]: [n[i] for i in range(1, len(n)) if n[i] != ''] for n in csv.reader(cd_csv)}
            print(secondary_subjects_mapping)

    for dm in DocModel.docmodel_generator(docmodels_path):
        if generate_doctype_cats:
            dm.extract_doctype_cat(doctype_cats_mapping)
        if generate_primary_subjects:
            dm.extract_primary_subjects(primary_subjects_mapping)
        if generate_secondary_subjects:
            dm.extract_secondary_subjects(secondary_subjects_mapping)
        dm.save_to_pickle(docmodels_path / dm.filename)
    print(f'Done extracting metadata from csvs. Parsing time: {timer.get_run_time()}')


def extract_and_tag_docmodel_texts(path):
    """Loads and updates all DocModels in a dir by extracting and tagging abstracts and texts"""

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


def parser_main():
    """Main fct for parser. Will create DocModels and/or extract/treetag texts based on input."""

    c_path = CORPUS_PATH
    dm_path = DOCMODELS_PATH

    print('Preprocessing corpus with parser.py')
    print(f'Working on corpus at: {c_path}')
    print(f'Storing DocModels at: {dm_path}')
    print()
    print('Do you want to run "create_docmodels_from_xml_corpus"?')
    print('This will create a DocModel object and save it as a pickle for each document in the corpus.')
    print('Metadata will also be extracted')
    run_create_docmodels = yn_input('Enter y to run this step, n to skip... ')
    print()

    print('Do you want to run "generate_metadata_from_mappings"?')
    print('This will update DocModels by extracting additional metadata from CSVs')
    print('Make sure that base metadata values are already extracted and that CSV files are available.')
    run_generate_from_csvs = yn_input('Enter y to run this step, n to skip... ')
    print()

    print('Run "extract_and_tag_docmodel_texts"?')
    print('This will extract texts and abstracts from DocModels and TreeTag them.')
    run_extract_and_tag = yn_input('Enter y to run this step, n to skip... ')
    print()

    if run_create_docmodels:
        create_docmodels_from_xml_corpus(c_path, dm_path)

    if run_generate_from_csvs:
        generate_metadata_from_mappings(dm_path)

    if run_extract_and_tag:
        extract_and_tag_docmodel_texts(dm_path)

    print()
    print('Corpus preprocessing done, have a good day!')


if __name__ == '__main__':
    parser_main()

