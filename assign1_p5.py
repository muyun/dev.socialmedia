#!/usr/bin/python3
# -*- coding: utf-8 -*-
''' Name:     anayChinese.py
    Function: 
    
'''
#import nltk
#import operator
from __future__ import division
#ch_punctuation = ["。", "，", "、", "·", "！", "？", "[", "]", "（", "）", "："]

def get_chinese_character(src_file):
    #load the data from the source file
    text_file = open(src_file,"r")
    text = text_file.read()
    
    text_file.close()

    import re
    # remove the chinese punctuations
    text1 = re.sub(r"：|。|，|\[|\]|\？|！|\（|\）|、", "",text)
    #print(text1)
    # remove any alphanumeric character
    text2 = re.sub(r"[a-zA-Z0-9_]" , "",text1)
    #print(text2)
    new_text = re.sub(r"\n" , "", text2)
    #print(new_text)

    # get the chinese list
    ch_list = [ ch for ch in new_text]

    return ch_list

def list_2_freq(mylist):
    mydict = dict()
    # add one if the chinese character exists in the dict
    for ch in mylist:
        mydict[ch] = mydict.get(ch,0) + 1

    #print(mydict) 
    # sort the value in the dict according to the decreasing 
    import operator
    ch_freq_sorted = sorted(mydict.items(), key=operator.itemgetter(1),reverse= True)

    return ch_freq_sorted

def list_2_bigram(mylist):
     return [mylist[i:i+2] for i in range(0,len(mylist)-1)]

def bigram_2_freq_dict(mybigram):
    mydict = dict()
    for (ch1,ch2) in mybigram:
        mydict[(ch1,ch2)] = mydict.get((ch1,ch2),0) + 1

    #sort
    import operator
    bigram_freq_sorted = sorted(mydict.items(), key=operator.itemgetter(1),reverse= True)
    
    return bigram_freq_sorted

def cal_probability(mylist,str1,mybigram,str2):
    x, y = int(0), int(1)
    # get the number of str1 in mylist
    for (ch, num) in mylist:
        if ch == str1:
            y = num
            break
    #print("y is:")
    #print(y)

    #get the number of str2 in mybigram
    chs=str()
    
    for (token, num) in  mybigram:
        for ch in token:
            chs = chs + ch
            
        if chs == str2:
                             
            x = num
            chs=''
            break
        else:
            chs=''
        

    #print("xy is:")
    #print(x)

    #value=print("%.2f" % p )
    return x/y

def get_character_bigram(mybigram,str1):
    mydict = dict()
    
    for (ch1,ch2) in mybigram:
          # 
           if ch1 == str1:
                 mydict[(ch1,ch2)] = mydict.get((ch1,ch2),0) + 1
    #sort
    import operator
    character_bigram_freq_sorted = sorted(mydict.items(), key=operator.itemgetter(1),reverse= True)
    
    return character_bigram_freq_sorted


def main():
    src_file="/home/zhaowenlong/workspace/lib/nltk_data/corpora/custombook/wikipedia_hongkong.txt"
    
    mylist = get_chinese_character(src_file)
    #print(mylist)

    ### get the number of times a chinese character appear in dictionary ch_freq_dict
    #  p(y) * N, like '香'
    ch_freq_dict = list_2_freq(mylist)
    #print(ch_freq_dict)

    ###the number of times a bigram
    # get the list about bigram
    ch_bigram = list_2_bigram(mylist) 
    #  the number of times a bigram in dictionary ch_bigram_freq_dict
    #  p(xy) * N, like '香港'
    ch_bigram_freq_dict = bigram_2_freq_dict(ch_bigram)
    
    ###bigram['香']['港'] = p('港'|'香') = p('香港') / p('香') = xy / x
    p=cal_probability(ch_freq_dict,'香',ch_bigram_freq_dict,'香港')
    print("The probability is: %.4f" % p)
    print('--------------------')
    ###print the top 10 words following ['中'] along with the probabilities
    #the bigram including the first character is '中'
    character_bigram_freq_sorted = get_character_bigram(ch_bigram,'中')
    #get the top 10 words following '中'
    #print(character_bigram_freq_sorted[:10])
    
    chs=str()
    print('Char(s)\tProbability')
    print('--------------------') 
    for (token,num) in character_bigram_freq_sorted[:10]:
        for ch in token:
            #every words
            chs=chs + ch
            #the related probability
        ch_p = cal_probability(ch_freq_dict,'中',ch_bigram_freq_dict,chs)
        
        print(chs,'\t',ch_p)
        chs='' 
    
if __name__ == "__main__":
    main()    
