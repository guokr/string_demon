#!/usr/bin/env python
# encoding: utf-8

import regex as re
import commons as comm
from wu_manber import WuManber

# Chinese repeation
def repeat_content(text_list):
    text = ""
    for ele in text_list:
        text += ele

    #  que = list(text)
    return float(len(set(text)))/len(text) #0.35

# Chinese & English break
def break_check(text):
    text = unicode(text,'utf8')

    en_length, en_breaks = findPart(u"[\u0001-\u007F]+", text, "en") # "acsii"
    cn_length, cn_repeat = findPart(u"[\u4e00-\u9fa5]+", text, "cn") # "unicode chinese"
    #  print findPart(u"[\uac00-\ud7ff]+", text) # "unicode korean"
    #  print findPart(u"[\u30a0-\u30ff]+", text) # "unicode japanese katakana"
    #  findPart(u"[\u3040-\u309f]+", usample) # "unicode japanese hiragana"
    cn_punc = findPart(u"[\u3000-\u303f\ufb00-\ufffd]+", text, "punc") # "unicode cjk Punctuation"


    if en_length == 0:
        en_div, cn_en_ratio = 0, 1
    elif cn_length == 0:
        cn_div, cn_en_ratio = 0, 0
    else:
        cn_en_ratio = float(cn_length)/en_length


    en_div = float(en_length) / (en_breaks+1)
    cn_div = float(cn_length) / (cn_punc+en_breaks+0.001)
    return cn_repeat, cn_div, en_div, cn_en_ratio
# lcs
def lcs_info(text):
    suffix = comm.suffix_array(text)
    lcp = comm.longest_common_prefix(suffix, text)
    count = comm.suffix_counts(suffix, lcp)
    max_lcp, i = comm.max_value_and_index(lcp)
    phrase = suffix[i][:lcp[i]]
    return count[i], phrase, len(phrase)/3

def findPart(regex, text, dec_type):
    res=re.findall(regex, text)
    if dec_type == "en":
        text_length_all = 0
        break_times = 0
        for i in res:
            text_length_all += len(i)
            for j in i:
                if j == ' ':
                    break_times += 1
        return text_length_all, break_times

    elif dec_type == "cn":
        #  print repeat_content(res)
        text_length_all = 0
        for i in res:
            text_length_all += len(i)
        return text_length_all, repeat_content(res)

    elif dec_type == "punc":
        punc_length_all = 0
        for i in res:
            punc_length_all += 1
        return punc_length_all

# spam check
def spam_check(string_content):
    return break_check(string_content)

def lcs_check(string_content):
    return lcs_info(string_content)

# blacklist check
def blacklist_check(v_list, n_list, string_content):
    length = len(string_content)
    w_v = WuManber()
    w_v.InitPattern(v_list)
    _, ix_verb = w_v.Search(string_content)
    if ix_verb:
        w_n = WuManber()
        w_n.InitPattern(n_list)
        _, ix_noun = w_n.Search(string_content)
        if ix_noun:
            def get_min_distance():
                temp = length
                for i in ix_verb:
                    for j in ix_noun:
                        temp = min(temp, abs(i-j))
                return temp
            return [get_min_distance(),
                    length,
                    len(ix_noun),
                    len(ix_verb)]
