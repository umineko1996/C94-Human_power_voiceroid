#coding:utf-8
import MeCab
import codecs
import re
import sqlite3

#
# 用意した台詞データをmecabで解析し、情報を付加してデータベースに格納します
#

input_file = "kyo.txt"
output_db= "Human_power_voiceroid.db"

def check_info(dict, info) :
    for i in dict[word] :
        if i["clazz"] == info["clazz"] and i["yomi"] == info["yomi"] and i["type"] == info["type"]:
            i["num"].append(info["num"][0])
            return True
    return False

f = codecs.open(input_file, 'r', 'utf-8')
data = f.read()
f.close()
lines = data.split("\n")
tagger = MeCab.Tagger("-u user.dic")
words_dict = {}

for line in lines:
    section = line.split(":")
    if len (section) < 2 :
        continue
    num = section[0]    # 先頭数字
    type = section[1]   # 属性
    sentence = section[2]  # 台詞

    result = tagger.parseToNode(sentence)
    while result:
        word = result.surface
        r = result.feature.split(",")
        result = result.next
        word = word.replace("。", "").replace("、", "").replace("「", "").replace("」", "").replace(":", "").replace("『", "").replace("』", "").replace("！", "").replace("？", "").replace("　","").replace("―", "").strip()  # 記号削除

        if word == "":
            continue

        clazz = r[0]
        yomi = ""
        if len(r) > 7 :
            yomi = r[7]

        info = dict(clazz=clazz, yomi=yomi, type=type, num=[num])

        if not words_dict.get(word, []) : # 初出単語
            words_dict.setdefault(word, []).append(info)
            continue
        if check_info(words_dict, info) : # 既知のパターン
            continue
        words_dict[word].append(info)     # 初出単語ではないが用法が違う


conn = sqlite3.connect(output_db)
c = conn.cursor()

# テーブルの作成
try :
    c.execute("create table words_data(id INTEGER PRIMARY KEY, word text, clazz text, yomi text, type text, nums text, label text)")
except :
    pass

label = input_file.replace(".txt", "")
insert = "insert into words_data(word, clazz, yomi, type, nums, label) values(?, ?, ?, ?, ?, ?)"

for key in words_dict :
    word = key
    for info in words_dict[key] :
        nums = ','.join(info["num"])
        clazz = info["clazz"]
        yomi  = info["yomi"]
        type = info["type"]

        word_data = (word, clazz, yomi, type, nums, label)

        try :
            c.execute(insert, word_data)
        except :
            print(word_data)


conn.commit()
c.close()
conn.close()
