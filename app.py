#coding: utf8
from flask import Flask, request, render_template
import json
import pandas as pd
import sys
import os.path
from data_helper import *
from es_helper import *
from model_helper import *

app = Flask(__name__)

database_cols = ["sr_no", "sr_act_text", "kwd_cust_origin", "kwd_cust_confirm", "kwd_gs_origin", "kwd_gs_confirm",
           "kwd_changed", "tag_first_name", "tag_first_prob", "tag_second_name", "tag_second_prob", "tag_third_name",
           "tag_third_prob", "tag_confirm", "tag_changed"]

#TODO consider stored date
df_database = load_stored_df(database_cols)

datatable_cols = ["sr_no", "sr_cate_b", "sr_cate_m", "sr_cate_s", "sr_text", "act_no", "act_text",
        "prd_cd", "prd_nm", "prd_desc", "ord_cd", "ord_date", "ord_status", "cust_no"]


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/upload', methods=['GET', 'POST'])
def upload():
    f = request.files['userfile']
    f.save('./'+f.filename)

    #TODO './data/sample.dat'
    file_path = './data/sample.dat'

    df_temp = raw_file_to_df(file_path)
    #TODO './sample.dat'
    df_datatable = df_temp[datatable_cols]

    # df_db
    # TODO df 키워드 추출
    # TODO df tag 추출
    # TODO 추출결과 별도의 df에 저장 pk(index == sr_no)

    df_es = get_analysed_keywords(df_temp['sr_no', 'customer_text', 'gs_text'])


    return df_datatable.to_html()


@app.route('/sr_analysis_info', methods=['GET', 'POST'])
def sr_analysis_info():
    # sr_no = request.json['sr_no']

    #TODO df에서 해당 sr찾는 작업

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


if __name__ == '__main__':
    app.run()
