from mempy3.preprocess.docmodel import DocModel
from mempy3.config import DOCMODELS_PATH, TT_ADJ_TAGS, TT_VERB_TAGS, TT_NOUN_TAGS, BASE_STORAGE_PATH, TT_EXCLUDED_TAGS
from spacy.lang.en import English
import pickle
from gensim.models import Word2Vec
from mempy3.utils.timer import Timer


def dm_from_id(ids):
    for id in ids:
        yield pickle.load(open(DOCMODELS_PATH / f'{id}.p', 'rb'))


def gen_text_list(ids):
    """2d list, text nva_tokens"""
    return [[tag.lemma for tag in para if (tag.pos not in TT_EXCLUDED_TAGS)]
            for dm in dm_from_id(ids) for para in dm.get_text_tags()]


def gen_text_list_old(ids):
    """2d list, text nva_tokens"""
    return [[tag.lemma for tag in sum(dm.get_text_tags(), []) if
                     (tag.pos in TT_NOUN_TAGS or tag.pos in TT_VERB_TAGS or tag.pos in TT_ADJ_TAGS)]
            for dm in dm_from_id(ids)]


def make_word_list(save_name, cluster_num):
    id_df = pickle.load(open(base_storage_path / 'analysis/LDA' / topic_model_name / 'reductions_df.p', 'rb'))
    filtered_ids = list(id_df[id_df['clustering_7'] == f'Cluster {cluster_num}'].index)
    word_list = gen_text_list(filtered_ids)
    pickle.dump(word_list, open(save_name, 'wb'))


if __name__ == '__main__':
    base_storage_path = BASE_STORAGE_PATH
    topic_model_name = 'topics_80_2_02_100_3_50_2k'

    cluster = 2
    w2c_words_filename = f'w2v_words_c{cluster}.p'

    timer = Timer()

    # make_word_list(w2c_words_filename, cluster)

    with open(w2c_words_filename, 'rb') as f:
        t = pickle.load(f)

    print(len(t))
    timer.step('Got texts!')

    vector_size = 300
    word_window = 15
    min_count = 30
    epochs = 10

    print(f'Starting word2vec on cluster {cluster}. {vector_size} dimensions, {word_window} window, {min_count} min count, {epochs} epochs')
    model = Word2Vec(sentences=t, size=vector_size, window=word_window, min_count=min_count, workers=4)
    model.train(t, total_examples=len(t), epochs=epochs)
    #model.save("word2vec.model")
    timer.step('Done!')

    print('Most similar')
    print(f'Model: {model.wv.most_similar(positive=["model"])}')
    print(f'Mechanism: {model.wv.most_similar(positive=["mechanism"])}')
    print(f'Explain: {model.wv.most_similar(positive=["explain"])}')
    print()
    print('Vector similarity')
    print(f'Model Explain:  {model.wv.similarity("model", "explain")}')
    print(f'Mechanism Explain:  {model.wv.similarity("mechanism", "explain")}')

    # antibio - bacterie + virus

    #test_1 = '1465-9921-8-16.p'
    # test_2 = '1297-9686-44-13.p'
    #dm = pickle.load(open(DOCMODELS_PATH / test_1, 'rb'))
    #raw_paras = dm.get_raw_text()
    #raw_text = '/n'.join(raw_paras)
    #nlp = English()
    #sentencizer = nlp.create_pipe("sentencizer")
    #nlp.add_pipe(sentencizer)



