#coding:utf-8
import MeCab
import codecs
import re
import jaconv

#
# 用意した台詞データをmecabで解析し、カタカナ読みデータとして１台詞１ファイルで出力します（音素変換用）
#

f = codecs.open('kanata.txt', 'r', 'utf-8')
data = f.read()
f.close()
lines = data.split("\n")
tagger = MeCab.Tagger("-u user.dic -Oyomi")
#f = codecs.open("out_oyomi.txt", 'w', 'utf-8')
filename_tmp = "./yomi/Kanata_XXXX.txt"

def zeroPad(num, padLen):
    while (len(num) < padLen):
        num = "0" + num
    return num


for line in lines:
    result = tagger.parse(line)
    result = result.strip("\n").strip("\r").strip() #後方空白、改行削除
    result = result.replace("―", "").replace("…", "").replace("。", "").replace("、", "").replace("「", "").replace("」", "").replace("『", "").replace("』", "").replace("！", "").replace("？", "").replace("　","")  # 記号削除
    if result == "":
        continue
    words = result.split(":") #数字と文章で分割
    num = words.pop(0)  # 数字
    filename = filename_tmp.replace("XXXX", zeroPad(num, 4))
    f = codecs.open(filename, 'w', 'utf-8')
    words = jaconv.kata2hira(words[0])
    print(num + ":" + words)
    f.write(words)
    f.close()

    # for word in words:
    #     d.setdefault(word, []).append(num)

f.close()
# f = codecs.open("list.txt", 'w', 'utf-8')
# f.write(str(d))
# f.close()
