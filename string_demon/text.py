#!/usr/bin/env python
# encoding: utf-8

import regex as re
import commons as comm

# Chinese repeation
def repeat_content(text):
    que = list(text)
    if float(len(set(que)))/len(que) < 0.35:
        return True
    return False

# Chinese & English break
def break_check(text):
    text = unicode(text,'utf8')

    en_length, en_breaks = findPart(u"[\u0001-\u007F]+", text, "en") # "acsii"
    cn_length = findPart(u"[\u4e00-\u9fa5]+", text, "cn") # "unicode chinese"
    #  print findPart(u"[\uac00-\ud7ff]+", text) # "unicode korean"
    #  print findPart(u"[\u30a0-\u30ff]+", text) # "unicode japanese katakana"
    #  findPart(u"[\u3040-\u309f]+", usample) # "unicode japanese hiragana"
    cn_punc = findPart(u"[\u3000-\u303f\ufb00-\ufffd]+", text, "punc") # "unicode cjk Punctuation"

    if float(cn_punc)/cn_length < 0.05:
        return True
    return False

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
        text_length_all = 0
        for i in res:
            text_length_all += len(i)
        return text_length_all

    elif dec_type == "punc":
        punc_length_all = 0
        for i in res:
            punc_length_all += len(i)
        return punc_length_all

#get each language parts:
def spam_check(string_content):
    print repeat_content(string_content)
    print break_check(string_content)
    print lcs_info(string_content)

def blacklist_check(string_content):
    pass
