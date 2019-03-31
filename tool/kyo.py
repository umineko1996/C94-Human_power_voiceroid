#!/usr/bin/python
# coding: UTF-8
#coding:Shift_JIS

#
# 『かりぐらし恋愛』のシナリオデータから荒波 杏（あらなみ きょう）の台詞データを抜き出します
#

import re
import codecs
import os
import glob


out = []

files = glob.glob('karigurashi/*.ks')
print (files)
for file in files:
    #print (str(file)+"展開")
    f = codecs.open(file,"r","utf8")
    data = f.read()
    f.close()

    lines = data.split('[c]')
    #print type(lines)
    for line in lines:
        if("[杏" in line):
            #print (line)
            numline = re.findall('vo2_.*',line)
            #print(numline)
            num = re.findall('vo2_\d+',numline[0])[0].replace("vo2_","")
            words = (re.findall('\[>>\].+\[<<\]',line))[0].replace("[>>]","「").replace("[<<]","」")

            out.append([int(num),words])
out.sort()

f = codecs.open('kyo.txt','w',"utf-8")
for tmp in out:
    f.write(str(tmp[0])+":*:"+tmp[1]+'\n')
    print(str(tmp[0])+":"+tmp[1])
print('完了')