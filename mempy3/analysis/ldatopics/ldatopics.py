"""Runs and saves lda models and results"""

import pandas as pd
import pickle
import numpy as np
from umap import UMAP
from sklearn.decomposition import LatentDirichletAllocation
from mempy3.config import CORPUSFRAMES_PATH, BASE_ANALYSIS_PATH
from mempy3.utils.dftools import tfidf_docterm_df
from mempy3.utils.timer import Timer


def make_and_train_lda_model(docterm_df, n_topics, n_loops, learn_decay, a, b, learn_method, rnd_state):
    return LatentDirichletAllocation(n_components=n_topics, max_iter=n_loops, learning_decay=learn_decay,
                                     doc_topic_prior=a, topic_word_prior=b,
                                     learning_method=learn_method, random_state=rnd_state).fit(docterm_df)


def topics_to_csv(df, num_words=15, param_dict=None):
    """Takes a topic words df, returns a csv (str) with 2 param rows and 2 rows per topic (words and weights)"""

    csv = ''
    if param_dict:
        csv += ', '.join(param for param in param_dict.keys()) + '\n'
        csv += ', '.join(str(param) for param in param_dict.values()) + '\n'

    for topic in df.index:
        csv += ', '.join([word for word in df.loc[topic].sort_values(ascending=False)[:num_words].keys()]) + '\n'
        csv += ', '.join([str(word) for word in df.loc[topic].sort_values(ascending=False)[:num_words].values]) + '\n'
    return csv


def update_folder_csv(path):
    topic_words_df = pickle.load(open(path / 'topic_words_df.p', 'rb'))
    with open(path / 'topic_probs.csv', 'wb') as f:
        f.write(topics_to_csv(topic_words_df, 10).encode('utf-8'))


def lda_topics_main(name, topics, a, b, min_tokens, max_word_frequence, min_word_occs, loops=100, decay=0.9,
                    rnd=2112, learn_method='batch'):
    timer = Timer()
    param_dict = {'name': name, 'n_topics': topics, 'a': a, 'b': b, 'min_tokens': min_tokens,
                  'max_word_freq': max_word_frequence, 'min_word_occ': min_word_occs, 'loops': loops, 'decay': decay}

    # Define the path where the model files will go
    # Creates a new file if it does not exist, else old files will be overwritten
    # Based on BASE_ANALYSIS_PATH, from config.
    path = BASE_ANALYSIS_PATH / 'LDA' / name
    path.mkdir(exist_ok=True)

    # Load docterm df
    df = pickle.load(open(CORPUSFRAMES_PATH / 'abs_nva_docterm_corpusframe.p', 'rb'))

    # Only keep docs with enough tokens
    df = df[(df.sum(axis=1) >= min_tokens)]

    # Remove words that occur in too few docs (by default, removes words that happen in less than 10 docs)
    # and
    # Remove words that are in more than x% of the docs (by default, remove words that are in more than 30% of docs)
    df = df.drop((df > 0).sum()[lambda x: (x < min_word_occs) | (x > max_word_frequence*len(df))].index, axis=1)

    # tfidf or log normalization, one or both can be commented out
    #df = tfidf_docterm_df(df)
    df = df.apply(lambda x: np.log(x + 1))

    # Fit model and save as pickle
    lda_model = make_and_train_lda_model(df, topics, loops, decay, a, b, learn_method, rnd)
    pickle.dump(lda_model, open(path / 'lda_model.p', 'wb'))
    # lda_model = pickle.load(open(path / 'lda_model.p', 'rb'))

    # Make topic words df (index = topics, cols = words)
    topic_words_df = pd.DataFrame(lda_model.components_, index=[f'topic_{i}' for i in range(topics)], columns=df.columns)

    # Transform to get doc x topic dist, normalized
    doc_topics_df = pd.DataFrame(lda_model.transform(df), columns=[f'topic_{i}' for i in range(topics)], index=df.index)

    # Normalize both, so that the sum of each row = 1. Can be commented out
    topic_words_df = topic_words_df.apply(lambda x: x / topic_words_df.sum(axis=1))
    doc_topics_df = doc_topics_df.apply(lambda x: x / doc_topics_df.sum(axis=1))


    # add col with main topic for each doc
    # add col with main word for each topic
    # doc_topics_df['main_topic'] = doc_topics_df.idxmax(axis=1)
    # topic_words_df['top_word'] = topic_words_df.idxmax(axis=1)

    # Reduce to 3d with umad and cols info to doc_topics_df
    # Reduce to 3d with umad and cols info to topics_words_df
    # reducer = UMAP(n_components=3)
    # doc_topics_df[['x', 'y', 'z']] = reducer.fit_transform(doc_topics_df)
    # topic_words_df[['x', 'y', 'z']] = reducer.fit_transform(topic_words_df)

    # Save results!
    pickle.dump(doc_topics_df, open(path / 'doc_topics_df.p', 'wb'))
    pickle.dump(topic_words_df, open(path / 'topic_words_df.p', 'wb'))

    res = lda_model.components_
    names = df.columns
    param_dict['log likelyhood'] = lda_model.score(df)
    param_dict['perplexity'] = lda_model.perplexity(df)

    # Print and save to txt top words for each topic
    # Does the same job as the csv thing but is uglier and clunkier
    # But it's nice to have the results printed and it works so who cares
    resdict = {}
    for num, topic in enumerate(res):
        features = [topic.argsort()[:-19:-1]]
        resdict[num] = [names[i] for i in features]
        # print([df.columns[topic.argsort()[i]] for i in range(10)])
    topics_str = '\n'.join([f'{key} - {", ".join(word for word in words[0])}' for key, words in resdict.items()])
    param_str = '\n'.join([f'{key} - {value}' for key, value in param_dict.items()])

    with open(path / 'topics.txt', 'wb') as f:
        f.write(topics_str.encode('utf-8'))

    with open(path / 'params.txt', 'wb') as f:
        f.write(param_str.encode('utf-8'))

    with open(path / 'topic_probs.csv', 'wb') as f:
        f.write(topics_to_csv(topic_words_df, 10, param_dict).encode('utf-8'))

    print(param_str)
    print('\n')
    print(topics_str)
    print(f'Done running lda main! Run time: {timer.get_run_time()}')
    print('\n\n\n')


def lda_run(n_t, a, b, min_tokens, max_freq, min_occs):
    """Calls LDA main, but builds file name from params. Useful to chain tests."""

    name = f'topics_{n_t}_{str(a)[2:]}_{str(b)[2:]}_{min_tokens}_{str(max_freq)[2:]}_{min_occs}'
    lda_topics_main(name, n_t, a, b, min_tokens, max_freq, min_occs)


if __name__ == '__main__':
    loops = 100 # Def 100
    decay = 0.9 # Def 0.9
    a = 0.1  # 0.1
    b = 0.01  # 0.01
    learn_method = 'batch' # Def batch, can change but online but doesnt seem to work as good
    rnd = 2112 # Def 2112
    min_tokens = 100  # Def 100, remove docs with less than X tokens
    max_word_frequence = 0.3  # Def 0.3, remove words that appear in more than X% of the docs
    min_word_occs = 10  # Def 10, min number of docs with word

    # fast test setup
    # lda_run(n_t=10, a=0.1, b=0.01, min_tokens=250, max_freq=0.3, min_occs=50, learn_method='batch')

    # 128, varier b, 100 min occs
    # Monter b pour voir si ça étend le tsne
    # Chain tests here. It might be nice to consider using a loop or something.

    lda_run(n_t=96, a=0.1, b=0.01, min_tokens=100, max_freq=0.3, min_occs=50)

    lda_run(n_t=96, a=0.1, b=0.02, min_tokens=100, max_freq=0.3, min_occs=50)
    # lda_run(n_t=96, a=0.2, b=0.02, min_tokens=100, max_freq=0.3, min_occs=50)

    # lda_run(n_t=96, a=0.4, b=0.01, min_tokens=100, max_freq=0.3, min_occs=10, learn_method='online')
    # lda_run(n_t=32, a=0.4, b=0.01, min_tokens=100, max_freq=0.3, min_occs=10)







