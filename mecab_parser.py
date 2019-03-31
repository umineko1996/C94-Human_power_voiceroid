#coding:utf-8
import MeCab
import codecs
import re
import pprint

#
# 用意した台詞データをmecabで解析し、情報を付加してテキストに出力します
# 出力後はコマンドからの入力により入力された文章に含まれるデータが何番目にあるかを出力します
#

input_file = 'kanata.txt'
output_file = 'parsed.txt'

def check_info(dict, info) :
    for i in dict[word] :
        if i["clazz"] == info["clazz"] and i["yomi"] == info["yomi"] and i["type"] == info["type"]:
            i["nums"].append(info["nums"][0])
            return True
    return False

f = codecs.open(input_file, 'r', 'utf-8')
data = f.read()
f.close()
lines = data.split("\n")
tagger = MeCab.Tagger("-u user.dic") #-Owakati")-Ochasen
f = codecs.open(output_file, 'w', 'utf-8')
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

        info = dict(clazz=clazz, yomi=yomi, type=type, nums=[num])

        if not words_dict.get(word, []) : # 初出単語
            words_dict.setdefault(word, []).append(info)
            continue
        if check_info(words_dict, info) : # 既知のパターン
            continue
        words_dict[word].append(info)     # 初出単語ではないが用法が違う


f.write(pprint.pformat(words_dict, compact=True))

tagger = MeCab.Tagger("-Owakati -u user.dic")
while True :
    in_str = input()
    if in_str == "0" :
        break
    result = tagger.parse(in_str)

    result = result.replace("。", "").replace("、", "").replace("「", "").replace("」", "").replace("『", "") \
    .replace("』", "").replace("！", "").replace("？", "").replace("　","").replace("―", "").strip()  # 記号削除
    if result == "":
        continue

    words = result.split()
    for word in words :
        infos = words_dict.get(word, [])
        nums = []
        for info in infos :
            nums.extend(info["nums"])

        str_nums =  str(nums)
        if len(nums) > 20 :
            str_nums = "more"
        elif not nums :
            str_nums = "non"

        print (word + " : " + str_nums)

