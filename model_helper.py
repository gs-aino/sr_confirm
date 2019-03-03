import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from itertools import chain
import pickle
import numpy as np

model_dir = './data/model/'
model_config = {
    'cust_vectorizer_path' : model_dir + 'cust_vectorizer.pkl',
    'gs_vectorizer_path' : model_dir + 'gs_vectorizer.pkl',
    'vectorizer_path' : model_dir + 'vectorizer.pkl',
    'model_path' : model_dir + 'model.pkl',
}

y_dict = {
    0: '개수/중량문의',
    1: '맛 불만족',
    2: '변질불만',
    3: '보관방법 문의',
    4: '사과주스누락',
    5: '사이즈 문의',
    6: '사이즈작음불만',
    7: '외관불량'
}


def get_tags_and_prob(df):
    customer_corpus = df.customer_terms.tolist()
    gs_corpus = df.gs_terms.tolist()
    corpus = [x + y for x, y in zip(customer_corpus, gs_corpus)]

    cust_vectorizer, gs_vectorizer, vectorizer = _load_vectorizers()

    X_cust = cust_vectorizer.transform(customer_corpus).toarray()
    X_gs = gs_vectorizer.transform(gs_corpus).toarray()
    X = vectorizer.transform(corpus).toarray()

    cust_vocab = {v: k for k, v in cust_vectorizer.vocabulary_.items()}
    gs_vocab = {v: k for k, v in gs_vectorizer.vocabulary_.items()}

    model = _load_model()
    y_prob = model.predict_proba(X)
    result = _get_tags_and_prob(y_prob)

    df_tags = pd.DataFrame(df['sr_no'])
    df_tags["tag_first_name"] = result[:, 0]
    df_tags["tag_first_prob"] = result[:, 1]
    df_tags["tag_second_name"] = result[:, 2]
    df_tags["tag_second_prob"] = result[:, 3]
    df_tags["tag_third_name"] = result[:, 4]
    df_tags["tag_third_prob"] = result[:, 5]
    df_tags["kwd_cust_origin"] = _get_kwds(X_cust, cust_vocab)
    df_tags["kwd_gs_origin"] = _get_kwds(X_gs, gs_vocab)

    return df_tags


def _get_tags_and_prob(y_prob):
    y_pred = [y.argsort()[-3:][::-1] for y in y_prob]
    y = [[y_dict[l[0]], y_prob[i, l[0]], y_dict[l[1]], y_prob[i, l[1]], y_dict[l[2]], y_prob[i, l[2]]] for i, l in enumerate(y_pred)]
    return np.array(y, dtype=object)


def _load_vectorizers():
    with open(model_config['cust_vectorizer_path'], 'rb') as f:
        cust_vectorizer = pickle.load(f)
    with open(model_config['gs_vectorizer_path'], 'rb') as f:
        gs_vectorizer = pickle.load(f)
    with open(model_config['vectorizer_path'], 'rb') as f:
        vectorizer = pickle.load(f)

    return cust_vectorizer, gs_vectorizer, vectorizer


# def _make_dataset(df):
#     customer_corpus = df.customer_terms.tolist()
#     gs_corpus = df.gs_terms.tolist()
#     corpus = [x + y for x, y in zip(customer_corpus, gs_corpus)]
#
#     cust_vectorizer, gs_vectorizer, vectorizer = _load_vectorizers()
#     X_cust = cust_vectorizer.transform(customer_corpus)
#     X_gs = gs_vectorizer.transform(gs_corpus)
#     X = vectorizer.transform(corpus)
#     return X_cust.toarray(), X_gs.toarray(), X.toarray()


def _load_model():
    with open(model_config['model_path'], 'rb') as f:
        model = pickle.load(f)
    return model


def _get_kwds(x_vecs, vocab):
    kwds_list = []
    for x_vec in x_vecs:
        non_zero_cnt = np.count_nonzero(x_vec)
        num_alpha = min(int(2 * non_zero_cnt / 3) + 1, 10)
        kwds_list.append(" ".join([vocab[x] for x in x_vec.argsort()[-num_alpha:][::-1]]))
    return kwds_list