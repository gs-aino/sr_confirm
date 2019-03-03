#coding: utf8
from flask import Flask, request, render_template
import json
import pandas as pd
import sys
import os.path
from datetime import datetime
from data_helper import *
from es_helper import *
from model_helper import *

app = Flask(__name__)

database_cols = ["sr_no", "sr_text", "act_text", "kwd_cust_origin", "kwd_cust_confirm", "kwd_gs_origin", "kwd_gs_confirm",
           "kwd_changed", "tag_first_name", "tag_first_prob", "tag_second_name", "tag_second_prob", "tag_third_name",
           "tag_third_prob", "tag_confirm", "tag_changed"]
# sr_no --> index
pd.set_option('display.max_colwidth', -1)


#TODO consider stored date
df_database = load_stored_df(database_cols)

datatable_cols = ["sr_no", "sr_cate_b", "sr_cate_m", "sr_cate_s", "sr_text", # "act_text",
        "prd_cd", "prd_nm", "prd_desc", "ord_cd", "ord_date", "ord_status"]

old_width = pd.get_option('display.max_colwidth')

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/sr_analysis_info', methods=['GET', 'POST'])
def sr_analysis_info():
    # sr_no = request.json['sr_no']

    # TODO df에서 해당 sr찾는 작업

    any_dict = {
        "sr_no": "",
        "sr_act_text": "고객 : abc\nGS: 123",
        "kwd_cust_origin": ["a", "b", "c"],
        "kwd_cust_confirm": ["a", "b", "c"],
        "kwd_gs_origin": ["1", "2", "3"],
        "kwd_gs_confirm": ["1", "2", "3"],
        "kwd_changed": False,
        "tag_first_name": "111",
        "tag_first_prob": 25.6,
        "tag_second_name": "222",
        "tag_second_prob": 2.3,
        "tag_third_name": "333",
        "tag_third_prob": 0.1,
        "tag_confirm": 0.1,
        "tag_changed": False
    }
    return json.dumps(any_dict)


@app.route('/upload', methods=['GET', 'POST'])
def upload():
    global df_database
    f = request.files['userfile']
    f.save('./data/'+f.filename)
    #
    #TODO './data/sample.dat'

    # file_path = './data/sample.dat'
    # print('''df_temp''')
    # df_temp = raw_file_to_df(file_path)
    # print('''df_temp pickling''')
    # df_temp.to_pickle('./data/df_temp.pkl')

    print('''read df_temp pickling''')
    df_temp = pd.read_pickle('./data/df_temp.pkl')
    #
    # print('''df_es''')
    # df_es = get_analysed_keywords(df_temp[['sr_no', 'customer_text', 'gs_text']])
    # print(df_es.head())
    #
    # print('''df_es pickling''')
    # df_es.to_pickle('./data/df_es.pkl')


    print('''read df_es pickling''')
    df_es = pd.read_pickle('./data/df_es.pkl')

    print('''df_tags''')
    df_tags = get_tags_and_prob(df_es['sr_no',  'customer_terms', 'gs_terms'])

    print('''df_tags pickling''')
    df_tags.to_pickle('./data/df_tags.pkl')



    # rename_dict = {
    #     "customer_terms": "kwd_cust_origin",
    #     "gs_terms": "kwd_gs_origin"
    # }

    # df = df_es.merge(df_tags, on=['sr_no'])
    # df = df.rename(rename_dict)

    # df["kwd_cust_confirm"] = df["kwd_cust_origin"]
    # df["kwd_gs_confirm"] = df["kwd_gs_origin"]
    # df["tag_confirm"] = df["tag_first_name"]
    # df["kwd_changed"] = False
    # df["tag_changed"] = False
    # df = df.set_index(['sr_no'])
    #
    # # TODO 추출결과 별도의 df에 저장 pk(index == sr_no)

    # df_database = df_database.append(df)
    # df_database.to_pickle('df_database_'+datetime.today().strftime('%Y%m%d')+".pkl")
    #
    # TODO append ml result
    df_datatable = df_temp[datatable_cols]

    html = df_datatable.to_html(classes=['table', 'display', 'table-striped', 'table-bordered'])
    # pd.set_option('display.max_colwidth', old_width)
    print(html[:1000])
    return html
    # return any_html
# df.loc[df.sr_no == 'S074784807', 'sr_text']

if __name__ == '__main__':

    app.run()

