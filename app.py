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

#TODO consider stored date
df_database = load_stored_df(database_cols)

datatable_cols = ["sr_no", "sr_cate_b", "sr_cate_m", "sr_cate_s", "sr_text", "act_no", "act_text",
        "prd_cd", "prd_nm", "prd_desc", "ord_cd", "ord_date", "ord_status", "cust_no"]
any_html = '''
    <table id="example" class="table display table-striped table-bordered" style="width:100%">
        <thead>
            <tr>
                <td>customer_no</td>
                <td>category_b</td>
                <td>category_m</td>
                <td>category_s</td>
                <td>sr_no</td>
                <td>sr_text</td>
                <td>category_ml</td>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td>24778209</td>
                <td>상품관련</td>
                <td>상품문의</td>
                <td>사이즈문의</td>
                <td>S116324802</td>
                <td>@고객 : &lt;출고완료&gt;&lt;입고택배-택배&gt;&lt;완전매입상품&gt;사이즈문의@GS : 남여공용으로 여유있게 출시 되었으니 중간 사이즈인 경우 크게 선택해주세요@연락처 : 01082662114</td>
                <td>사이즈 선택문의</td>
            </tr>
            <tr>
                <td>22375339</td>
                <td>상품관련</td>
                <td>상품문의</td>
                <td>사이즈문의</td>
                <td>S115060297</td>
                <td>@고객 : &lt;입금확인&gt;&lt;입고택배-택배&gt;&lt;완전매입상품&gt;남자 쇼호스트가 입는 상품사이즈/키@GS : 100사이즈이고 177CM임</td>
                <td>SH착용사이즈</td>
            </tr>
            <tr>
                <td>6617289</td>
                <td>상품관련</td>
                <td>상품문의</td>
                <td>사이즈문의</td>
                <td>S115456369</td>
                <td>@고객 : &lt;입금확인&gt;&lt;입고택배-택배&gt;&lt;완전매입상품&gt;정사이즈하라고했는데 넉넉하게나온건지@GS : 정사이즈입니다 / 중간사이즈인 경우에도 정사이즈 권장합니다※ 치코트 자체가 넉넉하게
                    입는 </td>
                <td>사이즈 선택문의</td>
            </tr>
            <tr>
                <td>20181015</td>
                <td>상품관련</td>
                <td>상품문의</td>
                <td>사이즈문의</td>
                <td>S115764493</td>
                <td>@고객 : 키160 중학생여아 착용가능한지문의/국민카드 즉시할인문의@GS : 사이즈선택:85(44), 90(55) 사이즈 안내■착용 전 일 경우 수령 후 15일 이내 반품 가능■외부착용/ 세탁/
                    수선 후 반품 불가"
                </td>
                <td>성인이 아닌경우 사이즈문의</td>
            </tr>
            <tr>
                <td>20181021</td>
                <td>상품관련</td>
                <td>상품문의</td>
                <td>사이즈문의</td>
                <td>S116027595</td>
                <td>@고객 : 사이즈가 몇까지나오죠 / 네@GS : 85 110입니다.</td>
                <td>가장 큰/작은 사이즈</td>
            </tr>
            <tr>
                <td>33710984</td>
                <td>상품관련</td>
                <td>상품문의</td>
                <td>사이즈문의</td>
                <td>S115457699</td>
                <td>@고객 : &lt;입금확인&gt;&lt;입고택배-택배&gt;&lt;완전매입상품&gt;사이즈문의/ 정사이즈인지문의@GS : 정사이즈입니다 / ※ 치코트 자체가 넉넉하게 입는 옷이기도하고, 겨울철 두꺼운 이너와
                    함께 입기도하여엀</td>
                <td>사이즈 선택문의</td>
            </tr>
            <tr>
                <td>33728577</td>
                <td>상품관련</td>
                <td>상품문의</td>
                <td>사이즈문의</td>
                <td>S115456452</td>
                <td>@고객 : &lt;입금확인&gt;&lt;입고택배-택배&gt;&lt;완전매입상품&gt;사이즈 문의@GS : 정사이즈나 본인취향에 따라 크게 입을수도 있으니 보시고 판단안내/ 수긍@연락처 : 01091633245</td>
                <td>사이즈 선택문의</td>
            </tr>
            <tr>
                <td>33981722</td>
                <td>상품관련</td>
                <td>상품문의</td>
                <td>사이즈문의</td>
                <td>S116187470</td>
                <td>@고객 : 177cm 95kg 평소 105와 110사이즈 입음@GS : 정사이즈입니다 / 중간사이즈인 경우에도 정사이즈 권장합니다※ 치코트 자체가 넉넉하게 입는 옷이기도하고, 겨울철 두꺼운 이너와
                    함께 입기돀</td>
                <td>키/몸무게/허리 사이즈로 문의</td>
            </tr>
            <tr>
                <td>34184827</td>
                <td>상품관련</td>
                <td>상품문의</td>
                <td>사이즈문의</td>
                <td>S115290868</td>
                <td>@고객 : 사이즈가 공용으로 나와있는데 / 어디부터가 남성사이즈인가. 공용이라고 말만하지말고 / 상세적으로 확인해달라 요구@GS : 내일 18시까지 전화요청하시어 전화드림 @연락처 : 01033715675
                    @</td>
                <td>사이즈 선택문의</td>
            </tr>
            <tr>
                <td>34184827</td>
                <td>상품관련</td>
                <td>상품문의</td>
                <td>사이즈문의</td>
                <td>S115454967</td>
                <td>@고객 : 남여 공용으로 다 입을수있는지 @GS : 가능 안내</td>
                <td>사이즈 선택문의</td>
            </tr>
            <tr>
                <td>34184827</td>
                <td>상품관련</td>
                <td>상품문의</td>
                <td>사이즈문의</td>
                <td>S115455005</td>
                <td>@고객 : 01042093463인입//핑크색상 XL 면99사이즈인지?@GS : 88사이즈 안내드림//수긍</td>
                <td>사이즈 표기 문의</td>
            </tr>
            <tr>
                <td>34184827</td>
                <td>상품관련</td>
                <td>상품문의</td>
                <td>사이즈문의</td>
                <td>S115455171</td>
                <td>@고객 : 평소 55-66 착용함 // 사이즈문의 남성 쇼호스트 착용사이즈 문의드립니다@GS : 치코트 자체가 넉넉하게 입는 옷이기도하고, 겨울철 두꺼운 이너와 함께 입기도하여여유있게 나옴 90으례</td>
                <td>SH착용사이즈</td>
            </tr>
            <tr>
                <td>34184827</td>
                <td>상품관련</td>
                <td>상품문의</td>
                <td>사이즈문의</td>
                <td>S115455181</td>
                <td>@고객 : 사이즈 문의@GS : 블랙,네이비,화이트 선택시:85(XS),90(S),95(M),100(L),105(XL),110(2XL)└핑크 선택시:85(XS),90(S),95(M),100(L),105(XL)</td>
                <td>사이즈 선택문의</td>
            </tr>
            <tr>
                <td>34184827</td>
                <td>상품관련</td>
                <td>상품문의</td>
                <td>사이즈문의</td>
                <td>S115455264</td>
                <td>@고객 : 남/여공용인가요?정사이즈인지?남성 쇼호스트/모델 사이즈 몇 인가요?@GS : 남/여공용정사이즈입니다 / 중간사이즈인 경우에도 정사이즈 권장합니다남성 쇼호스트/모델 사이즈 몇 인가쀀</td>
                <td>사이즈 선택문의</td>
            </tr>
            <tr>
                <td>34184827</td>
                <td>상품관련</td>
                <td>상품문의</td>
                <td>사이즈문의</td>
                <td>S115455279</td>
                <td>@GS : 정사이즈입니다 / 중간사이즈인 경우에도 정사이즈 권장합니다</td>
                <td>사이즈 선택문의</td>
            </tr>
            <tr>
                <td>34184827</td>
                <td>상품관련</td>
                <td>상품문의</td>
                <td>사이즈문의</td>
                <td>S115455328</td>
                <td>@GS : 남녀공용</td>
                <td>사이즈 선택문의</td>
            </tr>
            <tr>
                <td>34184827</td>
                <td>상품관련</td>
                <td>상품문의</td>
                <td>사이즈문의</td>
                <td>S115455345</td>
                <td>@고객 : 55사이즈가 뭔지 문의 /쇼호스트 여자 사이즈문의 @GS : 90 사이즈 안내 // 90안내</td>
                <td>SH착용사이즈</td>
            </tr>
            <tr>
                <td>34184827</td>
                <td>상품관련</td>
                <td>상품문의</td>
                <td>사이즈문의</td>
                <td>S115455356</td>
                <td>@고객 : 상세 사이즈문의@GS : 안내 / 수긍</td>
                <td>상세 사이즈 문의</td>
            </tr>
            <tr>
                <td>34184827</td>
                <td>상품관련</td>
                <td>상품문의</td>
                <td>사이즈문의</td>
                <td>S115455365</td>
                <td>@고객 : 여성 쇼호스트가 착용한 핑크색 사이즈문의@GS : 90</td>
                <td>SH착용사이즈</td>
            </tr>
            <tr>
                <td>34184827</td>
                <td>상품관련</td>
                <td>상품문의</td>
                <td>사이즈문의</td>
                <td>S115455472</td>
                <td>@고객 : 사이즈 55인데 90으로 주문하면 맞는지지@GS : 정사이즈입니다 / 중간사이즈인 경우에도 정사이즈 권장합니다※ 치코트 자체가 넉넉하게 입는 옷이기도하고, 겨울철 두꺼운 이너와 함께 </td>
                <td>사이즈 표기 문의</td>
            </tr>
            <tr>
                <td>34184827</td>
                <td>상품관련</td>
                <td>상품문의</td>
                <td>사이즈문의</td>
                <td>S115455595</td>
                <td>@고객 : 170키 착용 사이즈 문의@GS : 확인 어려움</td>
                <td>키/몸무게/허리 사이즈로 문의</td>
            </tr>
            <tr>
                <td>34184827</td>
                <td>상품관련</td>
                <td>상품문의</td>
                <td>사이즈문의</td>
                <td>S115455721</td>
                <td>@고객 : 가격문의 사이즈문의 남자키가 184-190 사이 몸무게 80 키로 면 사이즈 뭘하면좋나요?@GS : 생방송협력사(C,D)[-] 님의 말 (오후 9:17) : 105요289000안내</td>
                <td>키/몸무게/허리 사이즈로 문의</td>
            </tr>
            <tr>
                <td>34184827</td>
                <td>상품관련</td>
                <td>상품문의</td>
                <td>사이즈문의</td>
                <td>S115455723</td>
                <td>@고객 : 사이즈문의/ 남여 기장이 다른지문의@GS : 남여공용이라 사이즈 같음 안내함.</td>
                <td>상세 사이즈 문의</td>
            </tr>
            <tr>
                <td>34184827</td>
                <td>상품관련</td>
                <td>상품문의</td>
                <td>사이즈문의</td>
                <td>S115455845</td>
                <td>@고객 : 키 153정도. 55사이즈 입으면 어떤사이즈 입어야되는지문의@GS : 개인에 따라 다르지만 작은것보단 넉넉하게 입으시길 권장 참고하여 부탁드림</td>
                <td>키/몸무게/허리 사이즈로 문의</td>
            </tr>
            <tr>
                <td>34184827</td>
                <td>상품관련</td>
                <td>상품문의</td>
                <td>사이즈문의</td>
                <td>S115455886</td>
                <td>@고객 : 여성쇼핑호스트 착용사이즈,키가 어떻게 되나요여성 키가 161cm/ 몸무게 68일경우 사이즈 어떻게 선택하면 될까요@GS : APP(MC/PC)할인:10%(28,900원),생방송협력사(C,D)[-]
                    님의 말 (오후 9:21) : 90</td>
                <td>SH착용사이즈</td>
            </tr>
            <tr>
                <td>34184827</td>
                <td>상품관련</td>
                <td>상품문의</td>
                <td>사이즈문의</td>
                <td>S115455909</td>
                <td>@고객 : 윤찬종(U3764)[상담원] 님의 말 (오후 9:23) : 158 / 60 kg 아이라는대 ...어떤걸 권해드려야할까요 생방송협력사(C,D)[-] 님의 말 (오후 9:23) : 95요...</td>
                <td>성인이 아닌경우 사이즈문의</td>
            </tr>
            <tr>
                <td>34184827</td>
                <td>상품관련</td>
                <td>상품문의</td>
                <td>사이즈문의</td>
                <td>S115455931</td>
                <td>@고객 : 1. 중3이 착용할 만한 사이즈문의@GS : 정사이즈 주문/착용하실 분 사이즈 확인후 주문안내-수긍@연락처 : 07042159116</td>
                <td>성인이 아닌경우 사이즈문의</td>
            </tr>
            <tr>
                <td>34184827</td>
                <td>상품관련</td>
                <td>상품문의</td>
                <td>사이즈문의</td>
                <td>S115455986</td>
                <td>@고객 : M 총길이@GS : 108</td>
                <td>상세 사이즈 문의</td>
            </tr>
            <tr>
                <td>34184827</td>
                <td>상품관련</td>
                <td>상품문의</td>
                <td>사이즈문의</td>
                <td>S115456051</td>
                <td>@고객 : 사이즈문의@GS : ※ 치코트 자체가 넉넉하게 입는 옷이기도하고, 겨울철 두꺼운 이너와 함께 입기도하여여유있게 나옴</td>
                <td>사이즈 선택문의</td>
            </tr>
            <tr>
                <td>34184827</td>
                <td>상품관련</td>
                <td>상품문의</td>
                <td>사이즈문의</td>
                <td>S115456084</td>
                <td>@고객 : 사이즈문의@GS : 정사이즈입니다 / 중간사이즈인 경우에도 정사이즈 권장합니다</td>
                <td>사이즈 선택문의</td>
            </tr>
        </tbody>
        <tfoot>
            <tr>
                <td>customer_no</td>
                <td>category_b</td>
                <td>category_m</td>
                <td>category_s</td>
                <td>sr_no</td>
                <td>sr_text</td>
                <td>category_ml</td>
            </tr>
        </tfoot>
    </table>
'''


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

    #TODO './data/sample.dat'
    file_path = './data/sample.dat'

    df_temp = raw_file_to_df(file_path)
    #TODO './sample.dat'
    df_datatable = df_temp[datatable_cols]

    df_es = get_analysed_keywords(df_temp['sr_no', 'customer_text', 'gs_text'])
    df_tags = get_tags_and_prob(df_es['sr_no',  'customer_terms', 'gs_terms'])

    rename_dict = {
        "customer_terms": "kwd_cust_origin",
        "gs_terms": "kwd_gs_origin"
    }

    df = df_es.merge(df_tags, on=['sr_no'])
    df = df.rename(rename_dict)

    df["kwd_cust_confirm"] = df["kwd_cust_origin"]
    df["kwd_gs_confirm"] = df["kwd_gs_origin"]
    df["tag_confirm"] = df["tag_first_name"]
    df["kwd_changed"] = False
    df["tag_changed"] = False
    df = df.set_index(['sr_no'])

    # TODO 추출결과 별도의 df에 저장 pk(index == sr_no)
    df_database = df_database.append(df)
    df_database.to_pickle('df_database_'+datetime.today().strftime('%Y%m%d')+".pkl")

    # return df_datatable.to_html()
    return any_html


if __name__ == '__main__':

    app.run()

