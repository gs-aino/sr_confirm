import pandas as pd
from elasticsearch import Elasticsearch
from elasticsearch.client import IndicesClient
import json
from itertools import chain

dt = '190301'

es_config = {
  "ES_INDEX_NAME": "sr_confirm_"+dt,
  "FIELDS": ['sr_no', 'customer_text', 'gs_text']
}

es = Elasticsearch(timeout=30)
ic = IndicesClient(es)

def get_analysed_keywords(df_raw):
    df = df_raw[es_config['FIELDS']]
    body_list = [_gen_bulk(row) for i, row in df.iterrows()]

    count_list = [x for x in range(0, len(df), 5000)]
    count_list.append(len(df))

    for i in range(len(count_list) - 1):
        prev_i = count_list[i]
        next_i = count_list[i + 1]
        print(prev_i)

        body = [_ for _ in chain(*(body_list[prev_i:next_i]))]
        body = "\n".join(body)
        es.bulk(body=body)

    count = es.count(index=es_config['ES_INDEX_NAME'])['count']

    count_list = [x for x in range(0, count, 5000)]
    count_list.append(count)
    print("count: {}".format(count))

    customer_morphs_result_list = _get_morphs_result(df.customer_text.tolist())
    gs_morphs_result_list = _get_morphs_result(df.gs_text.tolist())

    df_es = pd.DataFrame()
    df_es['sr_no'] = df.sr_no

    df_es['customer_terms'] = _get_terms_list(customer_morphs_result_list)
    df_es['gs_terms'] = _get_terms_list(gs_morphs_result_list)

    def morph_results_to_dhub():
        return

    #
    #
    # results = list()
    # results.append(es.search(index=es_config['ES_INDEX_NAME'], size=10000, scroll='1m'))
    # scroll_id = results[0]['_scroll_id']
    # data = [_get_necessary_data(result['_source']) for result in results[0]['hits']['hits']]
    # del results
    #
    # print('''search data''')
    # for _ in range(count // 10000):
    #     print('searching idx : {}'.format(_))
    #     results = es.scroll(scroll_id=scroll_id, scroll='1m')['hits']['hits']
    #     results = [_get_necessary_data(result['_source']) for result in results]
    #     data.extend(results)
    #     del results
    #
    # print("data: {}".format(len(data)))
    #
    # print('''convert to dataframe''')
    # df_es = pd.DataFrame(data)
    # del data
    #
    # df_es.sr_no = df_es.sr_no.astype('str')
    # # df.to_pickle('df_temp_text.pkl')
    #
    # # df = pd.read_pickle('df_temp_text.pkl')
    # df_es['customer_terms'] = None
    # df_es['gs_terms'] = None
    # df_es = df_es.set_index('sr_no')
    #
    # print('''get_mtermvectors''')
    # for idx in range(len(count_list) - 1):
    #     print('idx : {}'.format(count_list[idx]))
    #     ids = df_es.iloc[count_list[idx]:count_list[idx + 1]].index.tolist()
    #     term_list = _get_mtermvectors(ids)
    #     ids = []
    #
    #     temp_customer = []
    #     for x in term_list:
    #         ids.append(x['_id'])
    #         if 'customer_text' in x['term_vectors'].keys():
    #             temp_customer.append([x['term_vectors']['customer_text']['terms']])
    #         else:
    #             temp_customer.append(None)
    #     df_es.loc[ids, 'customer_terms'] = temp_customer
    #     df_es.loc[ids, 'customer_terms'] = df_es.loc[ids, 'customer_terms'].apply(lambda x: _sort_terms_vector_ver2(x))
    #     del temp_customer
    #
    #     temp_gs = []
    #     for x in term_list:
    #         if 'gs_text' in x['term_vectors'].keys():
    #             temp_gs.append([x['term_vectors']['gs_text']['terms']])
    #         else:
    #             temp_gs.append(None)
    #     df_es.loc[ids, 'gs_terms'] = temp_gs
    #     df_es.loc[ids, 'gs_terms'] = df_es.loc[ids, 'gs_terms'].apply(lambda x: _sort_terms_vector_ver2(x))
    #     del term_list, temp_gs, ids
    #
    #     print('''reset_index df''')
    #     df_es = df_es.reset_index()
    #     print("df: {}".format(len(df_es)))
    #
    #     df_es.customer_terms = df_es.customer_terms.apply(lambda l: " ".join(l) if l is not None else None)
    #     df_es.gs_terms = df_es.gs_terms.apply(lambda l: " ".join(l) if l is not None else None)

        return df_es


def _gen_bulk(row):
    '''
    { "update" : {"_id" : message_id, "_type" : "_doc", "_index" : index_name, "retry_on_conflict" : 3} }
    { "doc" : {"field" : "value"} }
    '''

    _head = {
        "update": {
            "_id": row['sr_no'],
            "_type": "_doc",
            "_index": es_config["ES_INDEX_NAME"],
            "retry_on_conflict": 3
        }
    }

    _body = dict()
    _body["doc_as_upsert"] = True
    _body['doc'] = row.to_dict()

    return [json.dumps(_head), json.dumps(_body)]


def _get_mtermvectors(ids):
    body = dict()
    body["ids"] = ids
    body["parameters"] = {"fields": ["sr_no", "customer_text", "gs_text"]}

    res = es.mtermvectors(index=es_config['ES_INDEX_NAME'], doc_type='_doc', body=body, realtime=False)['docs']
    return res


def _sort_terms_vector_ver2(term_vectors):
    if not term_vectors:
        return ""
    term_dict = {}
    for term, val in term_vectors[0].items():
        for pos_info in val['tokens']:
            term_dict[str(pos_info['position']).zfill(5) + str(pos_info['end_offset']).zfill(5)] = term

    sorted_terms = sorted(term_dict.items())
    sorted_terms = [tup[1] for tup in sorted_terms]
    return sorted_terms


def _get_necessary_data(result):
    data = {}
    data["sr_no"] = result["sr_no"]
    data["gs_text"] = result["gs_text"]
    data["customer_text"] = result["customer_text"]
    return data


def _get_morphs_result(text_list):
    morphs_result_list = []
    body = {
        "analyzer": "nori",
        "explain": True
    }
    for text in text_list:
        temp = []
        body['text'] = text
        result = ic.analyze(es_config['ES_INDEX_NAME'], body=body)
        try:
            temp = result['detail']['tokenfilters'][-1]['tokens']
        except:
            print(result)
        finally:
            morphs_result_list.append(temp)
    return morphs_result_list


def _get_terms_list(morphs_result_list):
    return [" ".join([morph['token'] for morph in morphs if morph['posType'] in ['COMPOUND', None, 'MORPHEME']])
            for morphs in morphs_result_list]