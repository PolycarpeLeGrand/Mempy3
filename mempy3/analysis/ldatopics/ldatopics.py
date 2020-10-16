import pandas as pd
import pickle
import numpy as np
from sklearn.decomposition import LatentDirichletAllocation
from mempy3.config import CORPUSFRAMES_PATH
from mempy3.utils.dftools import tfidf_docterm_df


def make_and_train_lda_model(docterm_df, n_topics, n_loops, learn_decay, a, b, learn_method, rnd_state):
    lda = LatentDirichletAllocation(n_components=n_topics, max_iter=n_loops, learning_decay=learn_decay,
                                    doc_topic_prior=a, topic_word_prior=b,
                                    learning_method=learn_method, random_state=rnd_state).fit(docterm_df)
    return lda


def lda_topics_main():
    topics = 12
    loops = 100
    decay = 0.9
    a = 0.1
    b = 0.6
    learn_method = 'batch'
    rnd = 2112
    min_tokens = 50  # remove docs with less than X tokens
    max_word_frequence = 0.4  # remove words that appear in more than X% of the docs

    # load docterm
    df = pickle.load(open(CORPUSFRAMES_PATH / 'abs_nva_docterm_corpusframe.p', 'rb'))
    df = df[df.sum(axis=1) >= min_tokens]
    print(df)

    word_occs = (df>0).sum() # Series avec le numbre de textes qui contiennent chaque mot
    df = df.drop(word_occs[word_occs>(max_word_frequence*len(df))].index, axis=1)
    print(df)

    # tfidf
    df = tfidf_docterm_df(df)
    print(df)

    # fit
    lda_model = make_and_train_lda_model(df, topics, loops, decay, a, b, learn_method, rnd)
    # transform
    topics_df = pd.DataFrame(lda_model.transform(df), columns=[f'topic_{i}' for i in range(topics)], index=df.index)

    # print and save results


if __name__ == '__main__':
    lda_topics_main()

