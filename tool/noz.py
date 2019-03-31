#!/usr/bin/puthon
# coding: UTF-8
#coding:Shift_JIS

#
# 『PRETTY×CATION』のシナリオデータから朝霧 希美（あさぎり のぞみ）の台詞データを抜き出します
#

import re
import codecs
import os
import glob

out = []


files = glob.glob('puretycation/*.ks')
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
        if("noz" in line) :
            try:
                #print line
                #fi.write(str(line.encode("UTF-8"))+"\n\n")

                #line = line.encode('Shift_JIS')
                #data = line.split('\n')
                #print(data)
                numline = re.findall('noz_.*\d',line)
                #print(numline)
                num = re.findall('\d+',numline[0])[0]
                #print (line)
                words = (re.findall('「.+」',line,re.DOTALL))[0].replace("[r]\r\n","")

                out.append([int(num),words])
                print(str(num)+":"+words)
                #fi.write(str(num)+":"+words.encode('UTF-8')+"\n\n\n")
            except :
                pass
out.sort()

f = codecs.open('nozomi.txt','w','utf-8')
for tmp in out:
    f.write(str(tmp[0])+":"+tmp[1]+'\n')
    #print(str(tmp[0])+":"+tmp[1].encode('Shift_JIS'))
f.close()
print('完了')




