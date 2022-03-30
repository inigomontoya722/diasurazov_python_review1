import sys
import argparse
import string
import pickle
from collections import Counter

alfavitUpper = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
alfavitLower = 'abcdefghijklmnopqrstuvwxyz'


def encode_vigenere(keyword, text):
    res = ''
    j = 0
    for i in text:
        if (keyword[j] in alfavitUpper):
            key = ord(keyword[j])-ord('A')
        if (keyword[j] in alfavitLower):
            key = ord(keyword[j])-ord('a')
        j += 1
        if(j == len(keyword)):
            j = 0
        mestou = alfavitUpper.find(i)
        new_mestou = (mestou + key) % 26
        mestol = alfavitLower.find(i)
        new_mestol = (mestol + key) % 26
        if i in alfavitUpper:
            res += alfavitUpper[new_mestou]
        elif i in alfavitLower:
            res += alfavitLower[new_mestol]
        else:
            res += i
    return res


def decode_vigenere(keyword, text):
    res = ''
    j = 0
    for i in text:
        if (keyword[j] in alfavitUpper):
            key = ord(keyword[j])-ord('A')
        if (keyword[j] in alfavitLower):
            key = ord(keyword[j])-ord('a')
        j += 1
        if(j == len(keyword)):
            j = 0
        mestou = alfavitUpper.find(i)
        new_mestou = mestou - key
        if (new_mestou < 0):
            new_mestou += 26
        mestol = alfavitLower.find(i)
        new_mestol = mestol - key
        if (new_mestol < 0):
            new_mestol += 26
        if i in alfavitUpper:
            res += alfavitUpper[new_mestou]
        elif i in alfavitLower:
            res += alfavitLower[new_mestol]
        else:
            res += i
    return res


def encode_caesar(key, text):
    res = ''
    for i in text:
        mestou = alfavitUpper.find(i)
        new_mestou = (mestou + key) % 26
        mestol = alfavitLower.find(i)
        new_mestol = (mestol + key) % 26
        if i in alfavitUpper:
            res += alfavitUpper[new_mestou]
        elif i in alfavitLower:
            res += alfavitLower[new_mestol]
        else:
            res += i
    return res


def decode_caesar(key, text):
    res = ''
    for i in text:
        mestou = alfavitUpper.find(i)
        new_mestou = mestou - key
        if(new_mestou < 0):
            new_mestou += 26
        mestol = alfavitLower.find(i)
        new_mestol = mestol - key
        if (new_mestol < 0):
            new_mestol += 26
        if i in alfavitUpper:
            res += alfavitUpper[new_mestou]
        elif i in alfavitLower:
            res += alfavitLower[new_mestol]
        else:
            res += i
    return res


def change_text(text):
    all_unnecess = string.whitespace + string.punctuation + string.digits
    for sym in all_unnecess:
        text = text.replace(sym, '')

    return text.lower()


def train(text):
    text = change_text(text)
    frictions = dict(Counter(text))

    for val in string.ascii_lowercase:
        if val not in frictions:
            frictions[val] = 0

    for val in frictions:
        frictions[val] = frictions[val] / (len(text) if len(text) else 1)
    return frictions


def eq_measure(dic1, dic2, sh_key = 0):

    res = 0.0
    sh = encode_caesar

    for val, key in dic2.items():
        res += (key - dic1[sh(sh_key, val)]) ** 2
    return res


def createParser():
    parser = argparse.ArgumentParser()
    parser.add_argument('--cipher')
    parser.add_argument('--key')
    parser.add_argument('--input-file')
    parser.add_argument('--output-file')
    parser.add_argument('--model-file')
    parser.add_argument('--text-file')

    return parser


def main():
    parser = createParser()
    namespace = parser.parse_args(sys.argv[2:])

    if (sys.argv[1] == 'decode'):
        key = namespace.key
        cipher = namespace.cipher
        input_file = namespace.input_file
        output_file = namespace.output_file
        if (input_file == None):
            s = input()
        else:
            f = open(input_file, 'r')
            s = f.read()
            f.close()
        if (cipher == 'caesar'):
            out = decode_caesar(int(key), s)
        if (cipher == 'vigenere'):
            out = decode_vigenere(str(key), s)

        if (output_file == None):
            print(out)
        else:
            f = open(output_file, 'w+')
            f.write(out)
            f.close()

    if (sys.argv[1] == 'encode'):
        key = namespace.key
        cipher = namespace.cipher
        input_file = namespace.input_file
        output_file = namespace.output_file
        if (input_file == None):
            s = input()
        else:
            f = open(input_file, 'r')
            s = f.read()
            f.close()
        if (cipher == 'caesar'):
            out = encode_caesar(int(key), s)
        if (cipher == 'vigenere'):
            out = encode_vigenere(str(key), s)

        if (output_file == None):
            print(out)
        else:
            f = open(output_file, 'w+')
            f.write(out)
            f.close()

    if (sys.argv[1] == 'train'):
        text_file = namespace.text_file
        model_file = namespace.model_file
        if (text_file == None):
            s = input()
        else:
            f = open(text_file, 'r')
            s = f.read()
            f.close()
        dic = train(s)
        with open(model_file, 'wb') as file:
            pickle.dump(dic, file)
    if (sys.argv[1] == 'hack'):
        input_file = namespace.input_file
        output_file = namespace.output_file
        model_file = namespace.model_file
        if (input_file == None):
            s = input()
        else:
            f = open(text_file, 'r')
            s = f.read()

        dic1 = train(s)
        with open(model_file, 'rb') as f:
            try:
                dic2 = pickle.load(f)
            except Exception as e:
                print(e)
                quit()

        eq_meas = {}

        for key, val in enumerate(dic1):
            eq_meas[key] = eq_measure(dic1, dic2, key)

        keys = list(eq_meas.items())
        keys.sort(key=lambda i: i[1])

        res = decode_caesar(keys[0][0], s)

        if (output_file == None):
            print(res)
        else:
            f = open(output_file, 'w+')
            f.write(res)
        f.close()



if __name__ == '__main__':
    main()
