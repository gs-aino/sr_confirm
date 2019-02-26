from flask import Flask, request, render_template
import json
import pandas as pd
app = Flask(__name__)

@app.route('/')
def hello_world():
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload():
    f = request.files
    json_array_str = [{"sr_no":"S079670023","sr_cate_b":"이벤트\/프로모션관련","sr_cate_m":"TV쇼핑3회사은품문의","sr_cate_s":"TV쇼핑3회사은품문의","sr_text":"@접수시간 : 2016\/05\/02 13:59:51@주문상태 : <입금확인>@문의유형 : <상품>@내용 : 4개상품 20만원 이사민데 폴라로이드 카메라 받을수있나요?!","act_no":"A084665817","act_text":"네고객님!취소 상품으로 확인되며, 5월 3회&amp; 20만원 이상 구매시 이벤트는동일 상품으로 3회이상 &amp; 20만원 이상 구매에도 해당되며,단, 5월에 방송된 상품으로만 진행됩니다.  기온의 변덕으로 감기 조심하세요~@12@.","prd_cd":18492958,"prd_nm":"산지애 미시마 10.5kg","prd_desc":"공통,공통,공통,공통","ord_cd":764226793,"ord_date":"20160502","ord_status":"입금확인후취소","cust_no":111111},{"sr_no":"S098157204","sr_cate_b":"상품품질관련","sr_cate_m":"상품품질불만족","sr_cate_s":"기타상품불만족","sr_text":"@접수시간 : 2017\/07\/28 15:45:35@주문상태 : <배송완료>@문의유형 : <기타 문의>@내용 : 시골에 계신 엄마께 보내드렸는데, 딸이 보내준거라 아무 말씀 없으시다가 아제야 말씀하시네요. 처음에 6개가 썩어서 왔고, 사이즈 작은거는 제가 잘못 선택한거겠죠? 그런데 단맛이 하나도 없다고 하시네요. 딸이 보내준거라 맛 없어도 썩었어도 아까워서 그냥 드신다구요. 날이 너무 더우니 돌아다니시는것도 힘드실것 같아 보내드힘 건데 너무 속상합니다. 7\/22일 843054089 ★처리방법 알려주세요  ★반품처리가능한지... 썩은  6개  재발송가능한지요  ?","act_no":"A108280437","act_text":"송금처리하였습니다","prd_cd":21279613,"prd_nm":"딱딱이복숭아 1kg x 4팩","prd_desc":"공통,공통,공통,공통","ord_cd":843054089,"ord_date":"20170722","ord_status":"배송완료","cust_no":111111},{"sr_no":"S081356695","sr_cate_b":"상품품질관련","sr_cate_m":"상품불량","sr_cate_s":"변질","sr_text":"@접수시간 : 2016\/06\/12 14:05:03@주문상태 : <배송완료>@문의유형 : <반품교환수거>@내용 : 상한 산지애 사과 문의한 사람입니다. 사진 올립니다 빠른 연락바랍니다.","act_no":"A086765855","act_text":"@GS : @고객 : @연락처 : 0113412743  고객님 상품은 18과 보관중 \/ 2과는 사진 보냈음 (추가 발송)동생꺼도 확인해 보겠음","prd_cd":18538055,"prd_nm":"산지애10.5kg(미시마)+주스9팩","prd_desc":"공통,공통,공통,공통","ord_cd":768485395,"ord_date":"20160525","ord_status":"배송완료","cust_no":111111},{"sr_no":"S096390052","sr_cate_b":"배송관련","sr_cate_m":"배송기사(택배,업체)문의","sr_cate_s":"배송기사문의-고객확인","sr_text":"@고객 : <배송출발><직택배-직반>■택배기사 IN 01051001095 : 방문\/ 연락부재-. 보류 01086373772 : 2회부재@GS : 경비실요청","act_no":"A105698369","act_text":"@GS : @고객 : 목요일날 온다더니 벌써 도착했냐. 가서 찾아오겠음.@GS : 금요일 수령확인차 연락드려도 될지?@고객 : 경비실에 맡겼다면서? 지금 가서 찾아오면 됨.@GS : 알겠음. @연락처 : 01086373772@협력사문의\/요구사항 :","prd_cd":25499462,"prd_nm":"D_홀베리 애플망고10팩+10팩+3팩","prd_desc":"공통,공통,공통,공통","ord_cd":835774330,"ord_date":"20170612","ord_status":"배송완료","cust_no":111111},{"sr_no":"S114756675","sr_cate_b":"상품품질관련","sr_cate_m":"상품불량","sr_cate_s":"외관불량","sr_text":"@고객 : 고급스러운 포장으로 되어 있어 선물용으로 구입했는데 까만 상처도 있고, 겉부분 흠집도 있고 띠도 없고 이미지처럼 비단천도 없음.  * 불량사진 1688-4549 로 받기로함@GS : 업체로 처리방안 확인후 오늘 18시까지 연락이나 문자@연락처 : 01094479460@협력사문의사항 : 주문번호 918275411- 반품처리방안 답변부탁드립니다","act_no":"A129843457","act_text":"- 업체 02-949-1693 박은미씨 : 부재[12:09][15:18]","prd_cd":15300778,"prd_nm":"나주배 7.5kg 알찬 선물세트","prd_desc":"공통,공통,공통,공통","ord_cd":918275411,"ord_date":"20180916","ord_status":"배송완료","cust_no":111111}]
    cols = ["sr_no", "sr_cate_b", "sr_cate_m", "sr_cate_s", "sr_text", "act_no", "act_text",
                      "prd_cd", "prd_nm", "prd_desc", "ord_cd", "ord_date", "ord_status", "cust_no"]
    df = pd.DataFrame(json_array_str)
    df = df[cols]
    return df.to_json(orient='records')


@app.route('/sr_analysis_info', methods=['GET'])
def upload():
    any_json = {
        "sr_act_text": "고객 : \nGS: ",
        "kwd_cust_origin": [],
        "kwd_cust_confirm": [],
        "kwd_gs_origin": [],
        "kwd_gs_confirm": [],
        "kwd_changed": False,
        "tag_first_name": "",
        "tag_first_prob": 25.6,
        "tag_second_name": "",
        "tag_second_prob": 2.3,
        "tag_third_name": "",
        "tag_third_prob": 0.1,
        "tag_confirm": 0.1,
        "tag_changed": False,
    }
    return any_json


if __name__ == '__main__':
    app.run()
