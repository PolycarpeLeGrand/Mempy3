"""Config file for Mempy3

Global setting for the project. Contains:
- Path globals
- Preprocess and tagging info (special chars, xml markup, tt tags, etc.)

Uses pathlib.Path
"""

from pathlib import Path


BASE_STORAGE_PATH = Path('C:/Users/Sanchez/Desktop/m3data/')
CORPUS_PATH = Path('D:/corpus/articles/')

BASE_ANALYSIS_PATH = BASE_STORAGE_PATH / 'analysis'
BASE_RESULTS_PATH = BASE_STORAGE_PATH / 'results'

DOCMODELS_PATH = BASE_STORAGE_PATH / 'docmodels'
CORPUSFRAMES_PATH = BASE_STORAGE_PATH / 'corpusframes'

LEXCATS_FULL = BASE_STORAGE_PATH / 'csvs' / 'lexcats_full.csv'
LEXCATS_BASE = BASE_STORAGE_PATH / 'csvs' / 'lexcats_base.csv'

######

MIN_PARA_LEN = 5
TRASH_SECTIONS = ('st', 'tbl', 'display-formula', 'fig', 'file', 'suppl', 'table')

SPECIAL_CHARACTERS = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '\\', 'λ', 'β', 'μ', '°', '®',
                      '#', '@', '!', '"', '$', '%', '&', "'", '(', ')', '*', '+', ',', '.', '/', ':', ';',
                      '<', '=', '>', '?', '[', ']', '^', '_', '`', '{', '|', '}', '~']


TT_TAGLIST_UNLISTED = [',', '(', ')', "''", '``', '#']

TT_TAGLIST = ['CC', 'CD', 'DT', 'EX', 'FW', 'IN', 'IN/that', 'JJ', 'JJR', 'JJS', 'LS', 'MD', 'NN', 'NNS', 'NP',
                    'NPS', 'PDT', 'POS', 'PP', 'PP$', 'RB', 'RBR', 'RBS', 'RP', 'SENT', 'SYM', 'TO', 'UH', 'VB', 'VBD',
                    'VBG', 'VBN', 'VBP', 'VBZ', 'VD', 'VDD', 'VDG', 'VDN', 'VDZ', 'VDP', 'VH', 'VHD', 'VHG', 'VHN',
                    'VHZ', 'VHP', 'VV', 'VVD', 'VVG', 'VVN', 'VVP', 'VVZ', 'WDT', 'WP', 'WP$', 'WRB',
                    ':', '$'] + TT_TAGLIST_UNLISTED

TT_EXCLUDED_TAGS = TT_TAGLIST_UNLISTED + [':', '$', 'SYM', 'SENT']

TT_VERB_TAGS = ['VV', 'VVD', 'VVG', 'VVN', 'VVP', 'VVZ']
TT_ADJ_TAGS = ['JJ', 'JJR', 'JJS']
TT_NOUN_TAGS = ['NN', 'NNS', 'NP', 'NPS']


if __name__ == '__main__':
    # tests
    print(f'Base storage path: {BASE_STORAGE_PATH}')
    print(f'Docmodels path: {DOCMODELS_PATH}')

    for p in (CORPUS_PATH, BASE_ANALYSIS_PATH, BASE_RESULTS_PATH, DOCMODELS_PATH, CORPUSFRAMES_PATH):
        if not p.is_dir():
            print(f'The following dir is defined in config but cannot be found {p}')
