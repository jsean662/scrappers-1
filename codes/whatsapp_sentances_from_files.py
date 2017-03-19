# -*- coding: utf-8 -*-

import os.path
import sys
import re
# import time
import nltk
import json
import pandas as pd
from datetime import datetime as dt
from .testing import TestListing

try:
    import apiai
except ImportError:
    sys.path.append(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir)
    )
    import apiai

CLIENT_ACCESS_TOKEN = '8f98e831118844ed84c7772121708a5d'


def listfinder(msg_):
    print 'Running listfinder >>>', msg_
    msg_ = re.split('[0-9]+\. |[0-9]+\)', msg_)
    # print '>>>1', msg_
    # print 'next splitting >>>', msg_list
    return msg_


def separator(msg_to_sep):
    print 'decide separator'
    form_msg_aftr_brk = []
    find_config = '([0-9]+(\.?[5]?) (b)(h|e)(?<=\S)[kdrom]*)|([0-9]+(\.?[5]?)(b)(h|e)[kdrom]*)'
    find_config += '|([1] (r)[k])|([1](r)[k])'
    msg_sep_list = msg_to_sep.split('\n\n')
    for single_sep_list in msg_sep_list:
        count_bhk = re.findall(find_config, single_sep_list)
        if len(count_bhk) > 1:
            get_sep_listing = listfinder(single_sep_list)
            form_msg_aftr_brk += get_sep_listing
        else:
            form_msg_aftr_brk += [single_sep_list]
    cmn_prt = []
    n_cmn_prt = []
    for one_msg in form_msg_aftr_brk:
        if re.findall(find_config, one_msg):
            n_cmn_prt += [one_msg]
        else:
            cmn_prt += [one_msg]
    print '>>>', cmn_prt, n_cmn_prt, '>>>'
    form_msg_wt_cmn = []
    form_list = ''
    for one in n_cmn_prt:
        form_list += one
        for one_ech in cmn_prt:
            one_ech = one_ech.replace('\n', ' ')
            form_list += '\n' + one_ech
        form_msg_wt_cmn += [form_list]
        form_list = ''
    return form_msg_wt_cmn


def listmaker(orig_msg):
    print "++++++++++++++++++++++++++++++++++++++++++"
    orig_msg = orig_msg.lower()
    print '\nOriginal Message >>>', orig_msg
    date = orig_msg.split(' - ', 1)[0]
    try:
        timestamp = dt.strptime(date, '%d/%m/%y, %H:%M').strftime('%s')
    except:
        date = date.replace('.', '')
        try:
            timestamp = dt.strptime(date, '%d/%m/%y, %H:%M %p').strftime('%s')
        except:
            try:
                timestamp = dt.strptime(date, '%m/%d/%y, %H:%M %p').strftime('%s')
            except:
                timestamp = dt.strptime(date, '%d/%m/%Y, %H:%M %p').strftime('%s')
    # orig_date = dt.fromtimestamp(int(timestamp)).strftime('%d/%m/%Y %H:%M:%S')
    # print timestamp, orig_date

    p_n = orig_msg.split(' - ', 1)[-1].split(': ', 1)[0]
    phone_number = ''.join(re.findall('[0-9]+', p_n))
    # print phone_number

    orig_msg = orig_msg.split(' - ', 1)[-1].split(': ', 1)[-1]
    # print orig_msg
    # orig_msg = re.sub('[0-9]+\)', '', orig_msg)
    orig_msg = orig_msg.replace('*', '').replace('@', '').replace('`', '')
    orig_msg = orig_msg.replace('(', ' ')
    orig_msg = orig_msg.replace('_', '').replace('-', '').replace('~', '')
    find_config = '([0-9]+(\.?[5]?) (b)(h|e)(?<=\S)[kdrom]*)|([0-9]+(\.?[5]?)(b)(h|e)[kdrom]*)'
    find_config += '|([1] (r)[k])|([1](r)[k])'
    count_bhk = re.findall(find_config, orig_msg)
    cnt_bhk_length = len(count_bhk)
    print '\nFind BHK and count >>>', count_bhk, len(count_bhk), '\n'
    print '\nCharacter and word >>>', len(orig_msg), len(nltk.word_tokenize(orig_msg)), '\n'

    if cnt_bhk_length > 1:
        msg_list = separator(orig_msg)
        msg_list.append(timestamp)
        msg_list.append(phone_number)
    elif cnt_bhk_length > 0:
        msg_list = [orig_msg]
        msg_list.append(timestamp)
        msg_list.append(phone_number)
    else:
        msg_list = []

    return msg_list


def sngl_list_qry(single_listing, count, make_dict, t_make_dict):
    ai = apiai.ApiAI(CLIENT_ACCESS_TOKEN)

    for sent in single_listing:
        sent = sent.strip()
        if re.findall('\d{10}|\d{11}|\d{12}', sent) and len(sent) > 100:
            sent = re.sub('\d{10}|\d{11}|\d{12}', '', sent)
        if (sent != '') and (not re.findall('\d{10}|\d{11}|\d{12}', sent)) and len(sent) < 256:
            print sent
            sent = re.sub('[0-9]+\)', '', sent)
            sent = sent.replace('*', '').replace('@', '').replace('`', '')
            sent = sent.replace('(', ' ').replace(')', ' ').replace('}', '')
            sent = sent.replace('_', '').replace('-', '').replace('{', '')

            request = ai.text_request()
            request.session_id = count
            request.query = sent
            # response = request.getresponse().read()
            response = json.loads(request.getresponse().read())
            print json.dumps(response, indent=2, sort_keys=True)
            para_dict = response['result']['parameters']

            # context_para_dict = response['result']['contexts'][0]['parameters']
            print "\nparametrs >>>"
            print json.dumps(para_dict, indent=2, sort_keys=True)

            try:
                print response['sessionId'], '--', response['result']['metadata']['intentName']
            except:
                print response['sessionId'], '-- No Intent'

            try:
                make_dict['Actual_msg'] += '|' + response['result']['resolvedQuery']
                t_make_dict['Actual_msg'] += '|' + response['result']['resolvedQuery']
            except KeyError:
                make_dict['Actual_msg'] = response['result']['resolvedQuery']
                t_make_dict['Actual_msg'] = response['result']['resolvedQuery']

            for key in para_dict.keys():
                try:
                    make_dict[key] += para_dict[key]
                    try:
                        if para_dict[key]:
                            t_make_dict[key] += para_dict[key] + \
                                [response['result']['metadata']['intentName']]
                        else:
                            t_make_dict[key] += ['not data'] + \
                                [response['result']['metadata']['intentName']]
                    except:
                        print 'No Intent Match'
                except KeyError:
                    make_dict[key] = para_dict[key]
                    try:
                        if para_dict[key]:
                            t_make_dict[key] = para_dict[key] + \
                                [response['result']['metadata']['intentName']]
                        else:
                            t_make_dict[key] = ['no data'] + \
                                [response['result']['metadata']['intentName']]
                    except:
                        print 'No Intent Match'
    return make_dict, t_make_dict


def reading():
    test = TestListing()
    msg_str = ''
    count = 0
    make_dict = {}
    t_make_dict = {}
    dict_list = []
    t_dict_list = []
    crrct_dict = []

    textf_path = '/home/karan/Nexchange/api_ai_whatsapp/whatsapp/textfiles/'
    with open(textf_path + 'WhatsApp Chat with TRC Bandra to Scruz.txt') as f:
        for line in f:
            line = re.sub('[^\x00-\x7F]+', '', line)

            ignr = ['joined using', '<Media', 'changed this', 'removed ', 'added ', 'file attached',
                    'join my WhatsApp Group', 'left', 'chat.whatsapp.com', 'security code changed',
                    'secured with end-to-end encryption', 'created group', 'deleted this',
                    'changed the subject', 'You were added']
            if re.findall('^[0-9]+/[0-9]+/[0-9]+,.', line):
                if not any(x in line for x in ignr):
                    if not msg_str == '':
                        multiple_listing = listmaker(msg_str)
                        if multiple_listing:
                            listingdate = multiple_listing[-2]
                            phonenumber = multiple_listing[-1]
                            multiple_listing = multiple_listing[:-2]
                            print '\nmultiple_listing >>>', multiple_listing, '\n'
                            for single_listing in multiple_listing:
                                single_listing = single_listing.split('\n')
                                count = count + 1
                                make_dict = {'listing_date': [listingdate],
                                             'phone_number': [phonenumber]}
                                t_make_dict = {'listing_date': [listingdate],
                                               'phone_number': [phonenumber]}
                                print '\nsingle_listing >>>', single_listing, '\n'
                                make_dict, t_make_dict = sngl_list_qry(single_listing, count,
                                                                       make_dict, t_make_dict)

                                print "\nAfter API.AI call >>>"
                                print json.dumps(make_dict, indent=2, sort_keys=True), '\n'
                                print '\nFormatting the message >>>'
                                crrct_dict.append(test.checkListing(make_dict))

                                dict_list.append(make_dict)
                                t_dict_list.append(make_dict)
                                t_dict_list.append(t_make_dict)

                    msg_str = ''
                    msg_str = line
            else:
                msg_str += line
        print listmaker(msg_str)
        df = pd.DataFrame(dict_list)
        path = '/home/karan/Nexchange/api_ai_whatsapp/whatsapp/textfiles/store/' \
               + dt.now().strftime('%d-%m-%y,%H:%M:%S')
        os.makedirs(path)
        df.to_csv(path + '/apidict.csv', index=False, encoding='utf-8')
        df1 = pd.DataFrame(t_dict_list)
        df1.to_csv(path + '/apidict_wt_intent.csv', index=False, encoding='utf-8')
        df_frm = pd.DataFrame(crrct_dict)
        df_frm.to_csv(path + '/corrected.csv', index=False, encoding='utf-8')
        print 'Done .....'
        # print df
        # print df1
        # print df_frm


'''def main():
    test = TestListing()
    ai = apiai.ApiAI(CLIENT_ACCESS_TOKEN)
    count = 0
    make_dict = {}
    t_make_dict = {}
    dict_list = []
    crrct_dict = []

    with open('/home/karan/Nexchange/api_ai_whatsapp/textfiles/test.txt') as f:
        for sent in f.readlines():
            sent = re.sub('[^\x00-\x7F]+', '', sent)

            if (sent != '') and (not re.findall('\d{10}|\d{11}|\d{12}', sent)):

                request = ai.text_request()

                if re.findall('^[0-9]+/[0-9]+/[0-9]+.', sent):
                    if count != 0:
                        dict_list.append(make_dict)
                        # dict_list.append(t_make_dict)
                        crrct_dict.append(test.checkListing(make_dict))
                        # test.checkListing(t_make_dict)

                        time.sleep(3)

                    count = count + 1
                    request.session_id = count
                    make_dict = {}
                    t_make_dict = {}

                    date = sent.split(' - ', 1)[0]
                    make_dict['listing-date'] = dt.strftime(dt.strptime(date, '%d/%m/%y, %H:%M'),
                                                            '%m/%d/%Y %H:%M:%S')
                    t_make_dict['listing-date'] = dt.strftime(dt.strptime(date, '%d/%m/%y, %H:%M'),
                                                              '%m/%d/%Y %H:%M:%S')

                    p_n = sent.split(' - ', 1)[-1].split(': ', 1)[0]
                    make_dict['phone-number'] = [''.join(re.findall('[0-9]+', p_n))]
                    t_make_dict['phone-number'] = [''.join(re.findall('[0-9]+', p_n))]

                    sent = sent.split(' - ', 1)[-1].split(': ', 1)[-1]
                    sent = re.sub('[0-9]+\)', '', sent)
                    sent = sent.replace('*', '').replace('@', '').replace('`', '')
                    sent = sent.replace('(', ' ').replace(')', ' ')

                    print sent

                else:
                    request.session_id = count

                    sent = re.sub('[0-9]+\)', '', sent)
                    sent = sent.replace('*', '').replace('@', '').replace('`', '')
                    sent = sent.replace('(', ' ').replace(')', ' ')

                    print sent

                request.query = sent
                # response = request.getresponse().read()
                response = json.loads(request.getresponse().read())
                # print json.dumps(response,indent=2,sort_keys=True)
                para_dict = response['result']['parameters']
                # context_para_dict = response['result']['contexts'][0]['parameters']
                print ">>>>>>>>"
                print json.dumps(para_dict, indent=2, sort_keys=True)

                try:
                    print response['sessionId'], '--', response['result']['metadata']['intentName']
                except:
                    print response['sessionId'], '-- No Intent'

                try:
                    make_dict['Actual_msg'] += '|' + response['result']['resolvedQuery']
                    t_make_dict['Actual_msg'] += '|' + response['result']['resolvedQuery']
                except KeyError:
                    make_dict['Actual_msg'] = response['result']['resolvedQuery']
                    t_make_dict['Actual_msg'] = response['result']['resolvedQuery']

                for key in para_dict.keys():
                    try:
                        make_dict[key] += para_dict[key]
                        try:
                            if para_dict[key]:
                                t_make_dict[key] += para_dict[key] + \
                                    [response['result']['metadata']['intentName']]
                            else:
                                t_make_dict[key] += ['not data'] + \
                                    [response['result']['metadata']['intentName']]
                        except:
                            print 'No Intent Match'
                    except KeyError:
                        make_dict[key] = para_dict[key]
                        try:
                            if para_dict[key]:
                                t_make_dict[key] = para_dict[key] + \
                                    [response['result']['metadata']['intentName']]
                            else:
                                t_make_dict[key] = ['no data'] + \
                                    [response['result']['metadata']['intentName']]
                        except:
                            print 'No Intent Match'

                time.sleep(3)

            elif re.findall('\d{10}|\d{11}|\d{12}', sent):
                numbers = re.findall('\d{10}|\d{11}|\d{12}', sent)
                # print numbers
                name = re.findall('[a-zA-Z]+', sent)
                print name

                make_dict['Actual_msg'] += '|' + sent
                t_make_dict['Actual_msg'] += '|' + sent

                make_dict['phone-number'] += numbers
                t_make_dict['phone-number'] += numbers

                time.sleep(3)

    dict_list.append(make_dict)
    # dict_list.append(t_make_dict)
    crrct_dict.append(test.checkListing(make_dict))
    # test.checkListing(t_make_dict)

    df = pd.DataFrame(dict_list)
    df1 = pd.DataFrame(crrct_dict)
    print df1
    # df = df.fillna('[]')
    # columns = list(df)
    # required_clmn = ['Actual_msg', 'config', 'furnishing', 'req_avail',
    #                  'property_type', 'transaction_type', 'phone-number',
    #                  'listing-date', 'label_locality_mum',
    #                  'composite_location',
    #                  'label_area', 'sqft', 'label_area_units',
    #                  'composite_area', 'price', 'label_amt_units',
    #                  'label_deposit', 'composite_price', 'label_customer_type',
    #                  'no', 'label_park', 'composite_parking']

    # arrng_clmn = []
    # arrng_clmn1 = []
    # for i in columns:
    #     if i in required_clmn:
    #         arrng_clmn.append(i)
    #     else:
    #         arrng_clmn1.append(i)

    # df = df[arrng_clmn+arrng_clmn1]
    df.to_csv(
            '/home/karan/Nexchange/api_ai_whatsapp/textfiles/' +
            'file_aftr_testcorrection_test_price.csv',
            header=True, index=False, encoding='utf-8')
    # print df
'''

if __name__ == '__main__':
    reading()
