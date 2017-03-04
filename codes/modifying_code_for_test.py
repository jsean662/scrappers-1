# -*- coding: utf-8 -*-

import re
# import time
import nltk
# import json
# import pandas as pd
from datetime import datetime as dt


def listfinder(msg_list):
    print msg_list


def separator(msg_to_sep):
    print 'decide separator'
    msg_sep_list = msg_to_sep.split('\n\n')
    return msg_sep_list


def listmaker(orig_msg):
    print 'Original message >>>', orig_msg
    date = orig_msg.split(' - ', 1)[0]
    timestamp = dt.strptime(date, '%d/%m/%y, %H:%M').strftime('%s')
    # orig_date = dt.fromtimestamp(int(timestamp)).strftime('%d/%m/%Y %H:%M:%S')
    # print timestamp, orig_date

    p_n = orig_msg.split(' - ', 1)[-1].split(': ', 1)[0]
    phone_number = ''.join(re.findall('[0-9]+', p_n))
    # print phone_number

    orig_msg = orig_msg.split(' - ', 1)[-1].split(': ', 1)[-1]
    # print orig_msg
    orig_msg = re.sub('[0-9]+\)', '', orig_msg)
    orig_msg = orig_msg.replace('*', '').replace('@', '').replace('`', '')
    orig_msg = orig_msg.replace('(', ' ').replace(')', ' ')
    orig_msg = orig_msg.replace('_', '').replace('-', '')
    find_config = '([0-9]+(\.?[5]?) (B?b?)(?<=\S)[hHKkEeDdRrOoMm]+)|([0-9]+(\.?[5]?)(B|b)[hHKkEeDdRrOoMm]+)|([1] (R?r?)[Kk]+)|([1](R|r)[Kk])'
    count_bhk = re.findall(find_config, orig_msg)
    cnt_bhk_length = len(count_bhk)
    print count_bhk, len(count_bhk)
    print len(orig_msg), len(nltk.word_tokenize(orig_msg))
    if cnt_bhk_length > 2:
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

    with open('/home/karan/Nexchange/api_ai_whatsapp/whatsapp/textfiles/WhatsApp Chat with TRC Bandra to Scruz.txt') as f:
        for line in f:
            line = re.sub('[^\x00-\x7F]+', '', line)

            ignr = ['joined using', '<Media', 'changed this', 'removed ', 'added ', 'file attached',
                    'join my WhatsApp Group', 'left', 'chat.whatsapp.com', 'security code changed',
                    'secured with end-to-end encryption', 'created group', 'deleted this',
                    'changed the subject']
            if re.findall('^[0-9]+/[0-9]+/[0-9]+.', line):
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
                                    if (sent != '') and (not re.findall('\d{10}|\d{11}|\d{12}', sent)):
                                        sent = re.sub('[0-9]+\)', '', sent)
                                        sent = sent.replace('*', '').replace('@',
                                                                             '').replace('`', '')
                                        sent = sent.replace('(', ' ').replace(')', ' ')
                                        sent = sent.replace('_', '').replace('-', '')
                                        print count, '>>>>>>>', sent
                    msg_str = ''
                    msg_str = line
            else:
                msg_str += line
        print listmaker(msg_str)


if __name__ == '__main__':
    reading()
