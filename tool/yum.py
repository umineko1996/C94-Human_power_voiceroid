#!/usr/bin/puthon
# coding: UTF-8
#coding:Shift_JIS

#
# 『できない私が、くり返す。』のシナリオデータから栗原 ゆめ（くりはら ゆめ）の台詞データを抜き出します
#

import re
import codecs
import os
import glob

out = []

files = glob.glob('kurikaesu/*.ks')
#print files
for file in files:
    print (str(file)+"展開")
    f = codecs.open(file,'r','UTF-16')
    data = f.read()
    f.close()
    #data = data.decode('UTF-16')
    lines = data.split('[np]')
    #print type(lines)
    for line in lines:
        #line = line.decode("UTF-16")
        #try :
        #except :
        #   pass
        if("yum" in line) :
            try:
                #print line
                #fi.write(str(line.encode("UTF-8"))+"\n\n")

                #line = line
                #data = line.split('\n')
                #print(data)
                numline = re.findall('yum_.*\d',line)
                #print(numline)
                num = re.findall('\d+',numline[0])[0]
                #print (line)
                words = (re.findall('「.+」',line,re.DOTALL))[0]

                out.append([int(num),words])
                print(str(num)+":"+words)
                #fi.write(str(num)+":"+words.encode('UTF-8')+"\n\n\n")
            except :
                pass
out.sort()

f = codecs.open('yume.txt','w','utf-8')
for tmp in out:
    f.write(str(tmp[0])+":"+tmp[1]+'\n')
    #print(str(tmp[0])+":"+tmp[1])
f.close()
print('完了')




