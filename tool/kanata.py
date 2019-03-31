#!/usr/bin/python
# coding: UTF-8
#coding:Shift_JIS
import re
import codecs
import os
import glob

#
# 『紙の上の魔法使い』のシナリオデータから日向 かなた（ひむかい かなた）の台詞データを抜き出します
#

out = []

files = glob.glob('./../scenario/kamimaho/*.ks')
print (files)
for file in files:
    #print (str(file)+"展開")
    f = codecs.open(file,"r","shift_jis")
    data = f.read()
    f.close()

    lines = data.split('[ps]')
    #print type(lines)
    for line in lines:
        if('char=\"kanata\"' in line):
            print (line)
            numline = re.findall('kanata_.*ogg',line)
            #print(numline)
            num = re.findall('\d+',numline[0])[0]
            words = (re.findall('「.+」',line))[0]

            out.append([int(num),words])

out.sort()

f = codecs.open('kanata.txt','w',"utf-8")
for tmp in out:
    f.write(str(tmp[0])+":*:"+tmp[1]+'\n')
    print(str(tmp[0])+":"+tmp[1])
print('完了')