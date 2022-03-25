import sys
import argparse

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


def createParser():
    parser = argparse.ArgumentParser()
    parser.add_argument('--cipher')
    parser.add_argument('--key')
    parser.add_argument('--input-file')
    parser.add_argument('--output-file')
    parser.add_argument('--model-file')

    return parser


if __name__ == '__main__':
    parser = createParser()
    namespace = parser.parse_args(sys.argv[2:])

    if(sys.argv[1] == 'decode'):
        key = namespace.key
        cipher = namespace.cipher
        input_file = namespace.input_file
        output_file = namespace.output_file
        if (input_file == None):
            s = input()
        else:
            f = open(input_file)
            s = f.read()
            f.close()
        if (cipher == 'caesar'):
            out = decode_caesar(int(key), s)
        if (cipher == 'vigenere'):
            out = decode_vigenere(str(key), s)

        if (output_file == None):
            print(out)
        else:
            f = open(output_file)
            f.write(out)
            f.close()

    if(sys.argv[1] == 'encode'):
        key = namespace.key
        cipher = namespace.cipher
        input_file = namespace.input_file
        output_file = namespace.output_file
        if(input_file == None):
            s = input()
        else:
            f = open(input_file)
            s = f.read()
            f.close()
        if(cipher == 'caesar'):
            out = encode_caesar(int(key), s)
        if(cipher == 'vigenere'):
            out = encode_vigenere(str(key), s)

        if(output_file == None):
            print(out)
        else:
            f = open(output_file)
            f.write(out)
            f.close()
