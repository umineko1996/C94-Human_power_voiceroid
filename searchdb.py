#coding:utf-8
import MeCab
import codecs
import re
import sqlite3

#
# putdb_XXX.pyで格納したデータを検索して出力します
#

input_db= "Human_power_voiceroid.db"

word_sql = "SELECT * FROM words_data WHERE word=?"
yomi_sql = "SELECT * FROM words_data WHERE yomi=?"
num_sql = "SELECT * FROM sentences_data WHERE num=?"
num_label_sql = "SELECT * FROM sentences_data WHERE label=? AND num=?"

flag ={"word" : True, "yomi" : True, "label" : ""}

def sentence_search(num) :
    if not flag["label"] :
        for row in c.execute(num_sql, (num,)) :
            print(row["label"] + ":" + row["sentence"])
    else :
        for row in c.execute(num_label_sql, (flag["label"],num)) :
            print(row["sentence"])
    return

def remove_symbol(string) :
    return string.replace("。", "").replace("、", "").replace("「", "").replace("」", "").replace("『", "") \
                 .replace("』", "").replace("！", "").replace("？", "").replace("　","").replace("―", "").strip()  # 記号削除

def create_key_num(words_info) :
    if len(words_info) == 1 : # １単語の時は省略しない用自分自身を返す
        return words_info[0]["nums"]

    cnt = {"word" : {}, "yomi" : {}}
    key_num = {"word" : {}, "yomi" : {}}
    for word_info in words_info :
        for key in word_info["nums"] :
            for label in word_info["nums"][key] :
                for n in word_info["nums"][key][label] :
                    cnt[key].setdefault(label, {})
                    cnt[key][label].setdefault(n, 0)
                    cnt[key][label][n] += 1
    for key in cnt :
        for label in cnt[key] :
            for k,_ in sorted(cnt[key][label].items(), key=lambda x: -x[1]) : # 降順ソート
                key_num[key].setdefault(label, [])
                key_num[key][label].append(k)
                if len(key_num[key][label]) >= 10 : # 降順上位10個までをキー番号とする
                    break
    return key_num

def check_key_word(nums) :
    for label in nums["word"] :
        if len(nums["word"][label]) > 10 :
            return False
    return True

def update_key_words_num(key_words_num, nums) :
    # 全てのラベルにおいて出現10回以下の単語の数字番号の論理和をとる
    for key in nums :
        for label in nums[key] :
            key_words_num[key].setdefault(label, [])
            key_words_num[key][label].extend(nums[key][label])
            key_words_num[key][label] = list(set(key_words_num[key][label]))

def print_label_nums(label, nums, key_words_num) :
    back_str = ""
    num_str = ""
    if len(nums) > 20 :
        nums = list(set(nums) & set(key_words_num)) # キーワードと同じ番号のみ残す
        back_str = " and more..."
    if set(nums) == set(key_words_num) : # 入力1単語の時
        back_str = ""
    if not nums :
        back_str = "more..."
    else :
        num_str = ",".join(nums)
    print(label + " : " + num_str + back_str)



def sentence_analyz(sentence) :
    words_info = []
    key_words_num = {"word" : {}, "yomi" : {}}
    result = tagger.parseToNode(sentence)
    while result:
        word = result.surface
        r = result.feature.split(",")
        result = result.next
        word = remove_symbol(word)
        if word == "":
            continue

        yomi = ""
        if len(r) > 7 :
            yomi = r[7]

        nums = {"word" : {}, "yomi" : {}}
        for row in c.execute(word_sql, (word,)) :
            nums["word"].setdefault(row["label"], [])
            ns = row["nums"].split(",")
            for n in ns :
                nums["word"][row["label"]].append(n)

        if yomi :
            for row in c.execute(yomi_sql, (yomi,)) :
                nums["yomi"].setdefault(row["label"], [])
                ns = row["nums"].split(",")
                for n in ns :
                    nums["yomi"][row["label"]].append(n)

        words_info.append({"word" : word, "yomi" : yomi, "nums" : nums})

        if check_key_word(nums) :
            update_key_words_num(key_words_num, nums)

        continue

    if not key_words_num["word"] and not key_words_num["yomi"] : # キーワードが無い
        key_words_num = create_key_num(words_info)

    for word_info in words_info :
        for key in word_info["nums"] :
            if not flag[key] :
                continue
            print(word_info[key])
            if not word_info["nums"][key] :
                print("non")
            for label in word_info["nums"][key] :
                if flag["label"] and label != flag["label"]:
                    continue
                print_label_nums(label, word_info["nums"][key][label], key_words_num.get(key, []).get(label, []))
        print()


def option_conf(c) :
    if c == "w" :
        flag["word"] = not flag["word"]
        if flag["word"] :
            print("単語の出現位置を表示します")
        else :
            print("単語の出現位置を表示しません")
    elif c == "y" :
        flag["yomi"] = not flag["yomi"]
        if flag["yomi"] :
            print("読みの出現位置を表示します")
        else :
            print("読みの出現位置を表示しません")
    elif c == "l" :
        while True :
            print("ラベル名を入力してください")
            label = input()
            if not in_str :
                continue
            else :
                flag["label"] = label
                print(flag["label"] + "で登録しました")
                break
    else :
        print("無効なオプションです")


conn = sqlite3.connect(input_db)
conn.row_factory = sqlite3.Row
c = conn.cursor()
tagger = MeCab.Tagger("-u user.dic")

if __name__ == "__main__":
    while True :
        in_str = input()
        if not in_str :
            continue
        elif in_str == "0" :
            break
        elif in_str[0] == "-"  and len(in_str) >= 2:
            option_conf(in_str[1])
            in_str = in_str[2:].strip()

        if in_str.isdecimal() :
            sentence_search(in_str)
        else :
            sentence_analyz(in_str)

c.close()
conn.close()
