import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from itertools import chain
import pickle

# df_y = pd.read_csv('./y_0301.dat', sep='\t')
# df_y.columns = ['sr_media', 'cust_no', 'sr_no', 'sr_month', 'sr_type', 'sr_b', 'sr_b_cd', 'sr_m', 'prd_cate_m','sr_m_cd', 'sr_s', 'sr_s_cd',
#               'prd_cd', 'prd_nm', 'prd_item', 'supp_cd', 'supp_nm', 'num_inq', 'sr_text', 'y_val', 'etc']

# df_y = df_y[['sr_no','sr_type', 'sr_m', 'sr_m_cd', 'sr_s', 'sr_s_cd', 'supp_cd', 'supp_nm', 'sr_text', 'y_val']]
# df_y['prd_cate_m'].unique()

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
    X_cust, X_gs, X = _make_dataset(df)
    model = _load_model()
    y_prob = model.predict_proba(X)

    df_tags = pd.DataFrame(df['sr_no'])
    df_tags["tag_first_name"] = None
    df_tags["tag_first_prob"] = None
    df_tags["tag_second_name"] = None
    df_tags["tag_second_prob"] = None
    df_tags["tag_third_name"] = None
    df_tags["tag_third_prob"] = None
    df_tags[["tag_first_name", "tag_first_prob", "tag_second_name", "tag_second_prob", "tag_third_name", "tag_third_prob"]] = _get_tags_and_prob(y_prob)
    return df_tags


def _get_tags_and_prob(y_prob):
    y_pred = [y.argsort()[-3:][::-1] for y in y_prob]
    y = [(y_dict[l[0]], y_prob[l[0]], y_dict[l[1]], y_prob[l[1]], y_dict[l[2]], y_prob[l[2]]) for l in y_pred]
    return y


def _load_vectorizers():
    with open(model_config['cust_vectorizer_path']) as f:
        cust_vectorizer = pickle.load(f)
    with open(model_config['gs_vectorizer_path']) as f:
        gs_vectorizer = pickle.load(f)
    with open(model_config['vectorizer_path']) as f:
        vectorizer = pickle.load(f)

    return cust_vectorizer, gs_vectorizer, vectorizer


def _make_dataset(df):
    customer_corpus = df.customer_terms.tolist()
    gs_corpus = df.gs_terms.tolist()
    corpus = [x + y for x, y in zip(customer_corpus, gs_corpus)]

    cust_vectorizer, gs_vectorizer, vectorizer = _load_vectorizers()
    X_cust = cust_vectorizer.transform(customer_corpus)
    X_gs = gs_vectorizer.transform(gs_corpus)
    X = vectorizer.transform(corpus)
    return X_cust, X_gs, X


def _load_model():
    with open(model_config['model_path']) as f:
        model = pickle.load(f)
    return model