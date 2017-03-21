# -*- coding: utf-8 -*-

import os.path
import sys
import re
# import time
import nltk
import json
import pandas as pd
from datetime import datetime as dt

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


class TestListing():
    final_dict = {}

    def checkFurnishing(self, furnishing_list, dict_):
        print 'Running checkFurnishing >>>', furnishing_list
        if furnishing_list:
            self.final_dict['furnishing'] = furnishing_list
        else:
            self.final_dict['furnishing'] = 'None'

    def checkTt(self, tt_list, dict_):
        print 'Running checkTt >>>', tt_list
        if tt_list:
            self.final_dict['tt'] = tt_list[0]
        else:
            self.final_dict['tt'] = 'None'

    def checkPt(self, pt_list, dict_):
        print 'Running checkPt >>>', pt_list
        if pt_list:
            self.final_dict['property_type'] = pt_list[0]
        elif 'BHK' in dict_['config'] or 'bhk' in dict_['config']:
            self.final_dict['property_type'] = 'Home'
        else:
            self.final_dict['property_type'] = 'None'

    def checkDeal(self, deal_list, dict_):
        print 'Running checkDeal >>>', deal_list
        if deal_list:
            self.final_dict['req_avl'] = deal_list[0]
        else:
            self.final_dict['req_avl'] = 'test'

    def checkConfig(self, config_list, dict_):
        print 'Running checkConfig >>>', config_list
        if len(config_list) == 1:
            self.final_dict['config'] = config_list[0]
        if len(config_list) > 1:
            self.final_dict['config'] = config_list[0]
        # set default as 2 bhk if config list empty
        if not config_list:
            self.find_config['config'] = 'None'

    def getPrice(self, price):
        print price

    def checkPrice(self, price_dict, dict_):
        print 'Running checkPrice >>>', price_dict
        p_key = price_dict.keys()

        if 'composite_price' in p_key:
            if price_dict['composite_price']:
                for prc in price_dict['composite_price']:
                    try:
                        price_dict['price'] += [prc['price']]
                        price_dict['label_amt_units'] += [prc['label_amt_units']]
                    except:
                        price_dict['price'] = [prc['price']]
                        price_dict['label_amt_units'] = [prc['label_amt_units']]

        p_key = price_dict.keys()
        if 'label_amt_units' in p_key:
            if price_dict['label_amt_units']:
                for n, elemnt in enumerate(price_dict['label_amt_units']):
                    if 'k' in elemnt or 'pkg' in elemnt:
                        price_dict['label_amt_units'][n] = 1000
                    if 'lac' in elemnt:
                        price_dict['label_amt_units'][n] = 100000
                    if 'cr' in elemnt:
                        price_dict['label_amt_units'][n] = 10000000
                if len(price_dict['label_amt_units']) == 1:
                    price_dict['label_amt_units'] += [1]

        if 'price' in p_key and len(price_dict['price']) <= 2:
            p_list = []
            if price_dict['price']:
                if ('label_amt_units' in price_dict.keys()) and price_dict['label_amt_units']:
                    if len(price_dict['price']) == 1:
                        price_dict['price'] += [1]
                    for r_elmnt in price_dict['price']:
                        if len(price_dict['label_amt_units']) >= 1:
                            for c_elmnt in price_dict['label_amt_units']:
                                p_list.append(int(r_elmnt*c_elmnt))
                        else:
                            p_list.append(int(r_elmnt))
                else:
                    p_list = price_dict['price']
            print 'After label to price >>>', price_dict
            print 'all price figures >>>', p_list
            fmtd_price = []

            if not fmtd_price:
                # for one value in price and label
                for dr in p_list:
                    if [nr/dr for nr in p_list] == [1, 0, 0, 0]:
                        fmtd_price = [(p_list[0], 0)]
                        print fmtd_price

            if not fmtd_price:
                # for Range case
                c = 0
                for dr in p_list:
                    if [nr/dr for nr in p_list] in [[1, 1, 1, 1], [0, 0, 1, 1]]:
                        c += 1
                    if c > 3:
                        fmtd_price = [((p_list[1]+p_list[2])/2, 0)]
                        print fmtd_price

            if not fmtd_price:
                # for two price and one label
                for dr in p_list:
                    if [nr/dr for nr in p_list] == [1, 0, 1, 0]:
                        fmtd_price = [((p_list[0]+p_list[2])/2, 0)]
                        print fmtd_price

            if not fmtd_price:
                # for rental+deposite case
                if 'LL' in dict_['tt'] or 'L/L' in dict_['tt']:
                    fmtd_price = [(dr, nr) for dr in p_list
                                  for nr in p_list if nr/dr >= 2 and nr/dr <= 10]
                    print fmtd_price

            if not fmtd_price:
                # only habing price not label
                fmtd_price = [(p_list[0], 0)]
                print fmtd_price

        if 'LL' in dict_['tt']:
            self.final_dict['price'] = fmtd_price[0][0]
            if fmtd_price[0][1] == 0:
                self.final_dict['deposit'] = fmtd_price[0][0]*3
            else:
                self.final_dict['deposit'] = fmtd_price[0][1]

        if 'OR' in dict_['tt']:
            self.final_dict['price'] = fmtd_price[0][0]
            self.final_dict['deposit'] = 0

    def checkArea(self, area_dict):
        print area_dict

    def checkLocality(self, loc_list, dict_):
        print 'Running checkLoc >>>', loc_list
        if loc_list:
            self.final_dict['locality'] = loc_list
        else:
            self.final_dict['locality'] = ['None']

    def checkPark(self, park_dict, dict_):
        print 'Running checkPark >>>', park_dict
        if 'no' in park_dict.keys():
            if park_dict['no']:
                self.final_dict['parking'] = park_dict['no'][0]

    def checkListing(self, make_dict_chk):
        self.final_dict = {}
        print "Running checkList >>>"
        price_keys = ['label_amt_units', 'composite_price', 'label_deposit', 'price',
                      'label_currency_Rs']
        # area_keys = ['composite_area', 'label_area', 'label_area_units', 'sqft']
        park_keys = ['composite_parking', 'label_park', 'no']

        try:
            self.final_dict['Actual_msg'] = make_dict_chk['Actual_msg']
        except:
            print 'No actual mesg'
        self.final_dict['phonenumber'] = make_dict_chk['phone_number'][0]
        self.final_dict['listing_date'] = make_dict_chk['listing_date'][0]
        try:
            self.checkDeal(make_dict_chk['req_avail'], self.final_dict)
        except:
            self.checkDeal(['Default'], self.final_dict)
        try:
            self.checkConfig(make_dict_chk['config'], self.final_dict)
        except:
            self.checkConfig(['None'], self.final_dict)
        print self.final_dict
        try:
            self.checkTt(make_dict_chk['transaction_type'], self.final_dict)
        except:
            self.checkTt(['None'], self.final_dict)
        print self.final_dict
        try:
            self.checkPt(make_dict_chk['property_type'], self.final_dict)
        except KeyError:
            self.checkPt([], self.final_dict)
        print self.final_dict
        try:
            self.checkPrice({key: make_dict_chk[key]
                            for key in price_keys if key in make_dict_chk.keys()},
                            self.final_dict)
        except:
            self.checkPrice({'price': [1]}, self.final_dict)
        print self.final_dict
        # self.checkArea({key: make_dict_chk[key]
        #                 for key in area_keys if key in make_dict_chk.keys()},
        #                self.final_dict)
        try:
            self.checkLocality(make_dict_chk['label_locality_mum'], self.final_dict)
        except:
            self.checkLocality([], self.final_dict)
        print self.final_dict
        try:
            self.checkFurnishing(make_dict_chk['furnishing'], self.final_dict)
        except:
            self.checkFurnishing([], self.final_dict)
        print self.final_dict
        self.checkPark({key: make_dict_chk[key]
                        for key in park_keys if key in make_dict_chk.keys()},
                       self.final_dict)
        print "\nAfter Preparing final dict >>>"
        print self.final_dict
        return self.final_dict


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
