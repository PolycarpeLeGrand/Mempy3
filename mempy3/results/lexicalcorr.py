import pandas as pd
import pickle

from mempy3.utils.dftools import classify_lexical_occurences
from mempy3.config import LEXCATS_3, CORPUSFRAMES_PATH, BASE_ANALYSIS_PATH


def classify():
    pass


if __name__ == '__main__':
    classification = LEXCATS_3
    df = pickle.load(open(CORPUSFRAMES_PATH / 'lexicon_paras_corpusframe.p', 'rb'))
    lexcats_df = classify_lexical_occurences(df, classification)
    print(lexcats_df.corr().applymap(lambda x: 0 if x == 1 else x))
    #save_dest = BASE_ANALYSIS_PATH / 'analysis/lexcats/lexcats_df_3.p'

    pickle.dump(lexcats_df, open(BASE_ANALYSIS_PATH / 'lexcats/lexcats_paras_3_df.p', 'wb'))


