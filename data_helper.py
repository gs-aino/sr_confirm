import pandas as pd
import re
import os.path
from os import listdir
from os.path import isfile, join

act_cate_list = ['고객 Outbound', '모바일 Outbound', 'SMS발송', '메일 Outbound', 'Email - Outbound', '기타 Outbound',
                 '채널 자동답변(OB)']
sr_act_dict = {}


def load_stored_df(df_cols):

    df_path = './data/df_database/'
    # df_file_names = [f for f in listdir(df_path) if isfile(join(df_path, f))]
    df_file_names = [f for f in listdir(df_path)]
    if df_file_names:
        sorted(df_file_names)
        df_file_name = df_file_names[-1]
        df = pd.read_pickle(df_path+df_file_name)
    else:
        df = pd.DataFrame(columns=df_cols)
    return df


def raw_file_to_df(file_path):
    global sr_act_dict
    df = pd.read_csv(file_path, sep='\t')

    #TODO 모든 column명 특히 한글에 대응하도록 reindex로 추후 바꿔야함
    # print(df.head())
    print(df.columns.tolist())

    df.columns = ['sr_no', 'sr_area', 'sr_channel', 'sr_cate_b', 'sr_cate_m', 'sr_cate_s', 'sr_text', 'ord_status', 'act_no',
     'act_text', 'act_status', 'act_cate', 'supp_ques', 'prd_cd', 'prd_nm', 'prd_desc', 'ord_cd', 'ord_date', 'supp_cd',
     'supp_nm']


    df = df[['sr_no', 'sr_area', 'sr_channel', 'sr_cate_b', 'sr_cate_m', 'sr_cate_s', 'sr_text', 'ord_status',
             'act_no', 'act_text', 'act_status', 'act_cate', 'supp_ques',
             'prd_cd', 'prd_nm', 'prd_desc', 'ord_cd', 'ord_date', 'supp_cd', 'supp_nm']]

    df['sr_no'] = df['sr_no'].apply(lambda string: _remove_single_quotation(string))
    df['sr_area'] = df['sr_area'].apply(lambda string: _remove_single_quotation(string))
    df['sr_channel'] = df['sr_channel'].apply(lambda string: _remove_single_quotation(string))
    df['sr_cate_b'] = df['sr_cate_b'].apply(lambda string: _remove_single_quotation(string))
    df['sr_cate_m'] = df['sr_cate_m'].apply(lambda string: _remove_single_quotation(string))
    df['sr_cate_s'] = df['sr_cate_s'].apply(lambda string: _remove_single_quotation(string))
    df['sr_text'] = df['sr_text'].apply(lambda string: _remove_single_quotation(string))
    #TODO ord_status call sr의 경우에는 뽑는 방식으로 변경
    df['ord_status'] = df['ord_status'].apply(lambda string: _remove_single_quotation(string))
    df['act_no'] = df['act_no'].apply(lambda string: _remove_single_quotation(string))
    df['act_text'] = df['act_text'].apply(lambda string: _remove_single_quotation(string))
    df['act_status'] = df['act_status'].apply(lambda string: _remove_single_quotation(string))
    df['act_cate'] = df['act_cate'].apply(lambda string: _remove_single_quotation(string))
    df['prd_nm'] = df['prd_nm'].apply(lambda string: _remove_single_quotation(string))
    df['prd_desc'] = df['prd_desc'].apply(lambda string: _remove_single_quotation(string))
    df['ord_date'] = df['ord_date'].apply(lambda string: _remove_single_quotation(string))
    df['supp_nm'] = df['supp_nm'].apply(lambda string: _remove_single_quotation(string))
    df['supp_ques'] = df['supp_ques'].apply(lambda string: _remove_single_quotation(string))

    df['sr_cate'] = None
    df['sr_cate'] = df.apply(lambda row: _make_sr_cate(row), axis=1)


    #TODO 활동번호가 아니라 활동시간으로 변경
    df = df.sort_values(['sr_no', 'act_no']).reset_index(drop=True)

    df['sr_start_type'] = df.sr_text.apply(lambda x: _sr_start_type(x))

    df["customer_text"] = ""
    df["gs_text"] = ""

    df = df.apply(lambda row: _extract_customer_text_from_question_ver3(row), axis=1)
    df = df.apply(lambda row: _extract_gs_text_from_question_ver2(row, df), axis=1)

    df['customer_text'] = df.customer_text.apply(lambda x: _cleansing_raw_text_by_char_ver2(x))
    df['gs_text'] = df.gs_text.apply(lambda x: _cleansing_raw_text_by_char_ver2(x))

    del sr_act_dict

    return df


def _remove_single_quotation(string):
    new_string = string
    try:
        new_string = re.sub(pattern = "(^'|'$)", repl="", string=string)
    except TypeError:
        new_string = re.sub(pattern = "(^'|'$)", repl="", string=str(string))
    finally:
        return new_string.strip()


def _make_sr_cate(row):
    row['sr_cate'] = 'b : ' + row['sr_cate_b'] + '\nm : ' + row['sr_cate_m'] + '\ns : ' + row['sr_cate_s']
    return row['sr_cate']


def _check_start_with_ver2(x, compare_string_list: list):
    if not x:
        return False

    for string in compare_string_list:
        if x.startswith(string):
            return True

    return False


def _sr_start_type(sr_text):
    if not sr_text:
        return False

    if sr_text.startswith("@고객"):
        return 'call_type_customer'

    if sr_text.startswith("@GS"):
        return 'call_type_gs'

    if sr_text.startswith("@접수시간"):
        return 'mobile_type'

    return 'other_type'


def _extract_customer_text_from_question_ver3(row):
    string = row['sr_text']
    if row['sr_start_type'] == 'call_type_customer':
        try:
            if '@GS' in string:
                found = re.search(pattern='@고객(.+)@GS', string=string).group(1)
            else:
                found = re.search(pattern='@고객(.+)$', string=string).group(1)
            row['customer_text'] = found
        except AttributeError:
            print("call : ", string)
            row['customer_text'] = string

    elif row['sr_start_type'] == 'call_type_gs':
        try:
            if '@고객' in string:
                found = re.search(pattern='@고객(.+)$', string=string).group(1)
            else:
                found = ""
            row['customer_text'] = found
        except AttributeError:
            print("call : ", string)
            row['customer_text'] = string
    elif row['sr_start_type'] == 'mobile_type':
        try:
            found = re.search(pattern='@(문의)*내용 : (.+?)$', string=string).group(2)
            row['customer_text'] = found
        except AttributeError:
            print("mob : ", string)
            row['customer_text'] = string
    else:
        #         print(row)
        row['customer_text'] = string
    return row


def _extract_gs_text_from_question_ver2(row, df):
    global sr_act_dict
    string = row['sr_text']
    if row['sr_start_type'] == 'call_type_customer':
        try:
            if '@GS' in string:
                found = re.search(pattern='@GS(.+)$', string=string).group(1)
            else:
                found = ""
            row['gs_text'] = found
        except AttributeError:
            print("call : ", string)
    elif row['sr_start_type'] == 'call_type_gs':
        try:
            if '@고객' in string:
                found = re.search(pattern='@GS(.+)@고객', string=string).group(1)
            else:
                found = re.search(pattern='@GS(.+)$', string=string).group(1)
            row['gs_text'] = found
        except AttributeError:
            print("call : ", string)
    elif row['sr_start_type'] == 'mobile_type':
        sr_no = row['sr_no']
        if sr_no in sr_act_dict.keys():
            row['gs_text'] = sr_act_dict[sr_no]
        else:
            df_temp = df.loc[df.sr_no == sr_no, ['act_no', 'act_cate', 'act_text']]
            for i, v in df_temp.iterrows():
                if v['act_cate'] in act_cate_list:
                    row['gs_text'] = v['act_text']
                    sr_act_dict[sr_no] = v['act_text']
                    break
            if row['gs_text'] == "":
                idx = df_temp.index.tolist()[0]
                row['gs_text'] = df_temp.loc[idx, 'act_text']
                sr_act_dict[sr_no] =  df_temp.loc[idx, 'act_text']
    return row


def _cleansing_raw_text_by_char_ver2(text):
    text = re.sub(pattern=r'\n|\t|ㆍ|\r|,|;|:|<|>|-|_|=|\+|/|@|\(|\)|\*|&|\^|#|\$|~|◈|★|■|●|\[|\]|\"', repl=" ", string=text)
    text = re.sub(pattern=r'( )+', repl=' ', string=text)

    text = re.sub(pattern=r'(\.)+', repl='.', string=text)
    text = re.sub(pattern=r'(\?)+', repl='?', string=text)
    text = re.sub(pattern=r'(\!)+', repl='!', string=text)
    text = re.sub(pattern=r'(ㅎ)+', repl='ㅎ', string=text)
    text = re.sub(pattern=r'(ㅋ)+', repl='ㅋ', string=text)
    text = re.sub(pattern=r'(ㅠ|ㅜ)+', repl='ㅠ', string=text)
    text = re.sub(pattern=r'(♡|♥)+', repl='♥', string=text)

    return text