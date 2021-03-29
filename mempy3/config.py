"""Config file for Mempy3

Global setting for the project. Contains:
- Path globals
- Preprocess and tagging info (special chars, xml markup, tt tags, etc.)

Uses pathlib.Path
"""

from pathlib import Path

# Paths to various storage locations, both for base data and results
# By default all data is saved in the same base directory (BASE)STORAGE_PATH)

# Base corpus files can be stored in a different location (e.g external drive)
#   since they shouldn't be needed after initial extraction

# Base path to transformed data and results
BASE_STORAGE_PATH = Path('C:/Users/Sanchez/Desktop/m3data/')

# Path to corpus files
CORPUS_PATH = Path('D:/corpus/articles/')

# Paths to DocModel and corpusframes pickles
# docmodels dir contains pickled DocModel objects representing each doc in the corpus
# corpusframes contains various pickled Pandas DataFrames used in analysis
#   corpusframes are used to store intermediate results to avoid reading all DocModels for each analysis
DOCMODELS_PATH = BASE_STORAGE_PATH / 'docmodels'
CORPUSFRAMES_PATH = BASE_STORAGE_PATH / 'corpusframes'

# Analysis and results dir paths.
# Analysis is typically used for raw results and experiments.
# Results for clean results used for visualization
BASE_ANALYSIS_PATH = BASE_STORAGE_PATH / 'analysis'
BASE_RESULTS_PATH = BASE_STORAGE_PATH / 'results'

# Paths for lexical categories csvs
LEXCATS_FULL = BASE_STORAGE_PATH / 'csvs' / 'lexcats_full.csv'
LEXCATS_BASE = BASE_STORAGE_PATH / 'csvs' / 'lexcats_base.csv'
LEXCATS_3 = BASE_STORAGE_PATH / 'csvs' / 'lexcats_3.csv'
LEX_FULL = BASE_STORAGE_PATH / 'csvs' / 'lex_full.csv'

# Paths for metadata CSV mappings
DOCTYPE_CATS_CSV_PATH = BASE_STORAGE_PATH / 'csvs/doctype_cats.csv'
PRIMARY_SUBJECTS_CSV_PATH = BASE_STORAGE_PATH / 'csvs/primary_subjects.csv'
SECONDARY_SUBJECTS_CSV_PATH = BASE_STORAGE_PATH / 'csvs/secondary_subjects.csv'


######

MIN_PARA_LEN = 5

# Sections to ignore when reading texts and abstracts from html files
# These won't be extracted in DocModel text / tt_text variables
TRASH_SECTIONS = ('st', 'tbl', 'display-formula', 'fig', 'file', 'suppl', 'table', 'abbr', 'abbrgrp', 'sub', 'ext-link')

SPECIAL_CHARACTERS = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '\\', 'λ', 'β', 'μ', '°', '®',
                      '#', '@', '!', '"', '$', '%', '&', "'", '(', ')', '*', '+', ',', '.', '/', ':', ';',
                      '<', '=', '>', '?', '[', ']', '^', '_', '`', '{', '|', '}', '~']

SPECIAL_CHARACTERS_EXTENDED = ['□', '\u200b', '∓', 'ǖ', 'ứ', 'ί', '最', '西', 'η', '❿', '⊳', 'ℰ', '║', 'ྒྷ', '@', '࠷',
                               '➔', '⊤', 'ﬁ', '˚', 'ü', 'ė', '抱', '查', 'ł', 'ħ', '≺', '⋯', '制', '₦', '̄', '超', '휖',
                               '′', '管', '➩', '︸', '²', 'ị', '❹', '算', '‧', 'ϊ', 'α', '⊿', 'ˊ', '吃', 'è', 'ỉ', '≊',
                               '#', '⋅', '№', '、', 'ⓒ', '‸', '─', 'õ', 'ō', '‹', '¼', '步', '∀', 'à', 'ⅰ', '√', '对',
                               '助', 'к', '经', '⟧', 'œ', '事', 'ĸ', 'ⓡ', 'ǝ', '再', '⩾', '欢', '样', '希', '更', '⌣', '⊓',
                               'ι', 'ɧ', '″', 'ʹ', 'ờ', '讲', '后', '⅛', 'ǔ', '\uf8ef', '⊕', 'ó', 'ɥ', '\uf0ae', '·',
                               '∣', '│', 'ⅲ', 'ŕ', 'δ', '功', '™', '∕', '独', '‴', 'ϕ', 'ų', '\x81', '┐', '⊄', '直',
                               '⇀', '⇄', 'м', '˜', 'р', '\uf06d', 'ḡ', '∃', '↕', 'ẽ', '3', 'ȧ', '┌', 'č', '≤', 'ν',
                               '\x99', '’', 'û', '些', 'ư', '∅', 'ή', 'ß', '③', '΄', '↔', 'ź', '\u0fe0', 'ℜ', '●',
                               '父', '↪', 'ú', 'ӧ', 'ǫ', '⊢', '以', '∬', '系', '语', '害', '≪', '⟦', 'ì', 'é', '‡',
                               'ē', '畅', '⟩', '-', 'ф', 'ĩ', '旨', '⊣', '｀', '∄', '↓', 'ĵ', '\u202a', '›', '十', '安',
                               '自', '供', '一', 'ϋ', 'ℤ', '❽', '觉', 'ℬ', 'ⅅ', '持', '有', '‚', '∖', '〚', '⪯', '≫',
                               '_', '④', 'ỹ', 'ϰ', 'ᒭ', '话', '\uf062', '想', 'ž', 'ḣ', '很', '￣', 'ǻ', 'ξ', '⌈', 'έ',
                               'ب', '，', '少', '⊂', 'с', '草', 'ྜ', 'ℵ', 'ɨ', '≅', '∗', 'ẹ', '❼', '∫', '精', '我', '英',
                               'ẳ', '\u2061', '平', '孤', 'ɑ', 'ĝ', '口', 'ń', '⇑', 'ż', 'ĉ', '∞', 'š', '↦', 'ă', 'ņ',
                               'ِ', 'ʟ', 'ṙ', 'κ', '₤', '∇', '❾', '⇓', 'ầ', '黄', '⋃', '⇝', '¶', '人', '快', 'ụ', 'ت',
                               '̂', '9', '②', '入', '哭', 'ā', 'ự', '¹', 'ك', '̌', '¾', 'ệ', 'á', '劲', '您', 'г', '≃',
                               '感', '消', '計', '流', '统', 'ŝ', 'і', 'θ', '5', '东', '三', '⑦', '〈', 'в', '❷', 'ő', '∐',
                               '←', '⇌', 'ğ', '8', '内', '胃', '̃', '\xad', '⌉', '别', '每', '败', '‖', '≰', 'ά', 'ę', 'כ',
                               '¬', '∙', 'ẩ', 'ﬂ', 'ҳ', '键', 'а', '∠', '↑', '¢', '用', '≦', '÷', '⋮', 'х', '→', '得',
                               'β', '⊙', '℃', 'ä', '❶', '试', 'у', '∪', '帮', 'þ', 'ˆ', 'ο', '−', '\\', 'ُ', '家', 'ộ',
                               '≲', '≜', '‿', '‐', '〈', '―', 'đ', '⊴', '⃗', '̈', '̀', '^', '¡', 'н', '¯', 'ć', '⟨',
                               '心', 'є', '①', 'ḧ', 'μ', '译', '灵', '⌊', '体', '近', '↘', 'ṽ', 'ŷ', 'ε', 'ĺ', '∼', 'ƶ',
                               '∥', '就', '响', '○', 'ë', 'ø', '∨', 'ơ', 'ş', '⊲', '‟', '⑥', '̲', '≼', 'о', '≡', '≙',
                               '枢', 'ℒ', '日', 'ℓ', '\x7f', '请', '稳', '†', '„', '➝', '∑', 'い', 'ö', '٨', '照', 'ǎ',
                               '〛', 'ï', '烦', '⋍', 'π', '即', '◆', '友', 'ý', '过', 'ū', 'å', 'ྞ', 'ể', 'ℋ', '♀', '望',
                               'ς', '⊗', 'ò', '1', '◁', '清', '7', 'λ', '﹤', '▴', '•', 'ℏ', '的', 'ñ', '悲', 'ψ', '≧',
                               'ấ', '∩', '翻', '2', 'ĥ', 'ɳ', 'ℑ', '⊨', 'ℕ', '⑧', 'ϖ', 'ś', '⃦', 'ό', '▪', '沮', '复',
                               '劃', '≎', '≽', 'ρ', '▽', 'ê', '生', '⌢', '失', '⊊', '煙', 'ʼ', '\u206c', '睡', 'ợ', '¸',
                               '沉', 'ũ', 'ℛ', '好', 'ə', '◊', '们', 'ŵ', '∟', '⊃', 'ⅱ', '進', 'φ', '到', 'ã', '框', 'ẑ',
                               'ℚ', '·', '피', '提', '╀', '朋', 'ǐ', '▶', 'Ú', '♂', '士', 'ϐ', 'ð', '.', '§', '≯', '未',
                               '♦', 'е', '‑', '儿', '℗', '页', '⥄', '❖', '难', 'ϑ', '̇', '原', '∈', '⌴', '双', 'ř', 'ů',
                               '♢', 'ồ', '▷', 'ˠ', '♯', '═', 'ề', '❺', 'ϱ', 'ȳ', '+', '⊈', 'î', 'ω', '⌋', '来', '户',
                               '乐', '⑤', '∶', 'ϒ', '⇔', '⁄', 'ế', '在', '做', '线', 'ї', 'ϵ', '比', '使', 'į', 'Ö', '愉',
                               'ŋ', 'ắ', '地', 'ﬀ', '互', 'ζ', 'ġ', '親', '↖', '풯', '˙', 'υ', '͘', '⊥', 'µ', '≳', '⋆',
                               '己', '歉', '≥', '⅜', '풵', 'ả', 'ℇ', '丧', '二', '℘', 'ℳ', 'и', 'º', '伤', '结', "'",
                               '⊆', '⁰', '也', 'ℍ', 'æ', '½', '起', 'ˉ', '∉', '‵', '≻', '⇐', 'ą', '△', '果', 'ˋ', 'ℙ',
                               'ɠ', 'ŭ', '⋱', '╨', '验', '∭', '∏', '∊', '■', 'ℱ', 'ň', 'ű', 'â', '网', 'ặ', '看', 'ª',
                               'ℐ', '可', '✓', '0', '不', '풩', '⑨', '︷', '∂', 'ɛ', '帝', 'ĕ', 'ƒ', '≌', 'ç', '⋈', '∍',
                               '³', 'ΰ', '时', '∆', '❸', 'ı', '或', '⋂', '中', '加', '⤢', 'ớ', 'ℂ', '集', '∘', '℮',
                               '∧', '⃛', '明', '◯', '┴', 'í', 'ỏ', '稍', 'ώ', '❻', '►', '址', 'ī', '‘', 'ẋ', '输', '※',
                               '▵', '应', 'қ', '6', '怕', 'ө', 'ǿ', '‰', '̸', '⊔', '能', 'τ', '⇒', '‗', 'γ', 'ố', '〉',
                               'ɸ', 'ݼ', '力', '重', '4', '≠', '〉', 'ℝ', '支', '和', 'ƈ', '⅞', 'ṁ', '▲', '₂', '▮', 'χ',
                               'ù', 'َ', '▼', '活', '﹥', '׀', 'ύ', '∝', 'ӿ', 'ậ', '喜', '智', '费', '空', '都', '⊇', '́',
                               'σ', 'ě', '◦', 'ċ', '⊘', 'ạ', 'א', '件', '≈', 'ɗ', 'ô', '≮']


# Treetagger POS tags

# Tags unlisted in doc but found in results
TT_TAGLIST_UNLISTED = [',', '(', ')', "''", '``', '#']

# Treetagger taglist (From doc + unlisted)
TT_TAGLIST = ['CC', 'CD', 'DT', 'EX', 'FW', 'IN', 'IN/that', 'JJ', 'JJR', 'JJS', 'LS', 'MD', 'NN', 'NNS', 'NP',
                    'NPS', 'PDT', 'POS', 'PP', 'PP$', 'RB', 'RBR', 'RBS', 'RP', 'SENT', 'SYM', 'TO', 'UH', 'VB', 'VBD',
                    'VBG', 'VBN', 'VBP', 'VBZ', 'VD', 'VDD', 'VDG', 'VDN', 'VDZ', 'VDP', 'VH', 'VHD', 'VHG', 'VHN',
                    'VHZ', 'VHP', 'VV', 'VVD', 'VVG', 'VVN', 'VVP', 'VVZ', 'WDT', 'WP', 'WP$', 'WRB',
                    ':', '$'] + TT_TAGLIST_UNLISTED

# Base excluded tags list (non-words)
TT_EXCLUDED_TAGS = TT_TAGLIST_UNLISTED + [':', '$', 'SYM', 'SENT']

# Liste francis
# ['FW','MD','VVPRHASAL','VV.?','JJ.?','NN.?','NP.?','RB.?']

# Tag categories
TT_VERB_TAGS = ['VV', 'VVD', 'VVG', 'VVN', 'VVP', 'VVZ']
TT_ADJ_TAGS = ['JJ', 'JJR', 'JJS']
TT_NOUN_TAGS = ['NN', 'NNS', 'NP', 'NPS']

TT_BASE_TAGS = TT_NOUN_TAGS + TT_VERB_TAGS + TT_ADJ_TAGS #+ ['MD', 'RB', 'RBR', 'RBS']


if __name__ == '__main__':
    # tests
    print(f'Base storage path: {BASE_STORAGE_PATH}')
    print(f'Docmodels path: {DOCMODELS_PATH}')

    for p in (CORPUS_PATH, BASE_ANALYSIS_PATH, BASE_RESULTS_PATH, DOCMODELS_PATH, CORPUSFRAMES_PATH):
        if not p.is_dir():
            print(f'The following dir is defined in config but cannot be found {p}')
