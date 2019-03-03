#coding: utf8
from flask import Flask, request, render_template
from data_helper import *
from es_helper import *
from model_helper import *

app = Flask(__name__)

database_cols = ["sr_no", "kwd_cust_origin", "kwd_cust_confirm", "kwd_gs_origin", "kwd_gs_confirm",
           "kwd_changed", "tag_first_name", "tag_first_prob", "tag_second_name", "tag_second_prob", "tag_third_name",
           "tag_third_prob", "tag_confirm", "tag_changed"]
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
    global df_database
    sr_no = request.data.decode('utf-8')
    print('sr_no', sr_no)

    any_dict = df_database.loc[df_database.sr_no == sr_no, :].to_dict(orient='record')[0]
    print('any_dict', json.dumps(any_dict, ensure_ascii=False))

    return json.dumps(any_dict, ensure_ascii=False)


@app.route('/upload', methods=['GET', 'POST'])
def upload():
    global df_database
    sr_cate_b_filter = ['교환/반품/AS관련', '상품품질관련', '상품관련']

    f = request.files['userfile']
    f.save('./data/'+f.filename)
    #
    #TODO './data/sample.dat'
    file_path = './data/'+f.filename
    print('''df_temp''')
    df_temp = raw_file_to_df(file_path, sr_cate_b_filter)

    df_temp.to_pickle('./data/df_temp.pkl')
    df_temp = pd.read_pickle('./data/df_temp.pkl')

    print('''df_es''')
    df_es = get_analysed_keywords(df_temp[['sr_no', 'customer_text', 'gs_text']])

    df_es.to_pickle('./data/df_es.pkl')
    df_es = pd.read_pickle('./data/df_es.pkl')

    print('''df_tags''')
    df_tags = get_tags_and_prob(df_es[['sr_no',  'customer_terms', 'gs_terms']])

    df_tags.to_pickle('./data/df_tags.pkl')
    df_tags = pd.read_pickle('./data/df_tags.pkl')
    #

    print('''df_merge''')
    df = df_es.merge(df_tags, on=['sr_no'])
    df["kwd_cust_confirm"] = df["kwd_cust_origin"]
    df["kwd_gs_confirm"] = df["kwd_gs_origin"]
    df["tag_confirm"] = df["tag_first_name"]
    df["kwd_changed"] = False
    df["tag_changed"] = False
    # TODO 추출결과 별도의 df에 저장 pk(index == sr_no)

    print('''df_database''')
    df_database = df_database.append(df)
    df_database.to_pickle('data/df_database/df_database_'+datetime.today().strftime('%Y%m%d')+".pkl")

    print('''df_datatable''')
    df_datatable = df_temp.loc[df_temp['sr_cate_b'].isin(['교환/반품/AS관련', '상품품질관련', '상품관련']), datatable_cols].reset_index(drop=True)
    df_datatable = df_datatable.merge(df_tags[['sr_no', 'tag_first_name', 'tag_second_name', 'tag_third_name']], on=['sr_no'])

    df_datatable.to_pickle('./data/df_datatable.pkl')
    df_datatable = pd.read_pickle('./data/df_datatable.pkl')

    html = df_datatable.to_html( )
    print(html[:1000])
    return html

if __name__ == '__main__':

    app.run()

