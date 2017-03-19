# -*- coding: utf-8 -*-

import re
# import time
import nltk
# import json
# import pandas as pd
from datetime import datetime as dt


def listfinder(msg_):
    print 'Running listfinder >>>', msg_
    msg_ = re.split('[0-9]+\. |[0-9]+\)', msg_)
    print '>>>1', msg_
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
    print "+++++++++++++++++++++++++++++++++++++++"
    orig_msg = orig_msg.lower()
    print 'Original message >>>', orig_msg
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

    orig_msg = orig_msg.replace('*', '').replace('@', '').replace('`', '')
    orig_msg = orig_msg.replace('(', ' ')
    orig_msg = orig_msg.replace('_', '').replace('-', '').replace('~', '')
    find_config = '([0-9]+(\.?[5]?) (b)(h|e)(?<=\S)[kdrom]*)|([0-9]+(\.?[5]?)(b)(h|e)[kdrom]*)'
    find_config += '|([1] (r)[k])|([1](r)[k])'
    find_price = '([\d]+(\.?)[\d]*(\s?)(l|k)[ahcks]*)|([\d]+(\.?)[\d]*(\s?)(p)(k|c)[akgcin]*)'
    find_price += '|([\d]+(\.?)[\d]*(\s?)(c)(r)[ors]*)|([\d]+(\.?)[\d]*(\s?)(p)(a)(c)[kaing]*)'
    count_price = re.findall(find_price, orig_msg)
    cnt_prc_len = len(count_price)
    count_bhk = re.findall(find_config, orig_msg)
    cnt_bhk_length = len(count_bhk)
    print 'price >>>>>>>>', count_price, cnt_prc_len
    print count_bhk, len(count_bhk)
    print len(orig_msg), len(nltk.word_tokenize(orig_msg))
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


def reading():
    msg_str = ''
    count = 0
    base_path = '/home/karan/Nexchange/api_ai_whatsapp/whatsapp/textfiles/'
    with open(base_path + 'WhatsApp Chat with TRC Bandra to Scruz.txt') as f:
        for line in f:
            line = re.sub('[^\x00-\x7F]+', '', line)

            ignr = ['joined using', '<Media', 'changed this', 'removed ', 'added ', 'file attached',
                    'join my WhatsApp Group', 'left', 'chat.whatsapp.com', 'security code changed',
                    'secured with end-to-end encryption', 'created group', 'deleted this',
                    'changed the subject', 'You were added']
            if re.findall('^[0-9]+/[0-9]+/[0-9]+,.', line):
                if not any(x in line for x in ignr):
                    if not msg_str == '':
                        msg_list = listmaker(msg_str)
                        if msg_list:
                            msg_list = msg_list[:-2]
                            print 'multiple_list >>>', msg_list, '\n'
                            for msg in msg_list:
                                msg = msg.split('\n')
                                count = count + 1
                                print 'single_list >>>', msg, '\n'
                                for sent in msg:
                                    sent = sent.strip()
                                    if re.findall('\d{10}|\d{11}|\d{12}', sent) and len(sent) > 100:
                                        sent = re.sub('\d{10}|\d{11}|\d{12}', '', sent)
                                    if (sent != '') and (not re.findall('\d{10}|\d{11}|\d{12}',
                                                                        sent)):
                                        sent = re.sub('[0-9]+\)', '', sent)
                                        sent = sent.replace('*', '').replace('@',
                                                                             '').replace('`', '')
                                        sent = sent.replace('(', ' ').replace(')',
                                                                              ' ').replace('}', '')
                                        sent = sent.replace('_', '').replace('-',
                                                                             '').replace('{', '')
                                        print count, '>>>>>>>', sent
                                        with open(base_path + 'uploading.txt', 'ab') as storefile:
                                            storefile.write(sent + '\n')
                    msg_str = ''
                    msg_str = line
            else:
                msg_str += line
        print listmaker(msg_str)


if __name__ == '__main__':
    reading()
