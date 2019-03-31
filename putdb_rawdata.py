#coding:utf-8
import MeCab
import codecs
import re
import sqlite3

#
# 用意した台詞データをデータベースに格納します
#

input_file = "kyo.txt"
output_db= "Human_power_voiceroid.db"

f = codecs.open(input_file, 'r', 'utf-8')
data = f.read()
f.close()
lines = data.split("\n")
sentence_list = []

for line in lines:
    section = line.split(":")
    if len (section) < 2 :
        continue
    num = section[0]    # 先頭数字
    type = section[1]   # 属性
    sentence = section[2]  # 台詞
    sentence_list.append(dict(num=num, type=type, sentence=sentence))


conn = sqlite3.connect(output_db)
c = conn.cursor()

# テーブルの作成
try :
    c.execute("create table sentences_data(label text, num int, type text, sentence text, PRIMARY KEY(label,num))")
except :
    pass

label = input_file.replace(".txt", "")
insert = "insert into sentences_data(label, num, type, sentence ) values(?, ?, ?, ?)"

for s in sentence_list :
    num = s["num"]
    type = s["type"]
    sentence = s["sentence"]

    sentence_data = (label, num, type, sentence)

    try :
        c.execute(insert, sentence_data)
    except :
        print(sentence_data)


conn.commit()
c.close()
conn.close()
