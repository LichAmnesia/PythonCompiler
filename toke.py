#!/usr/bin/env python
# encoding: utf-8
# @Author: Lich_Amnesia
#

'''
Compiler for C using python
Options:
        -h, --h         show help
        -s file         import the source file, required!
        -l              lexer
        -p              parser
Examples:
    python *.py -h
    python *.py -s source.c -l
    python *.py -s source.c -p

'''
import re
import sys
import getopt

# token 大分類
TOKEN_STYLE = ['KEY_WORD', 'IDENTIFIER', 'DIGIT_CONSTANT',
        'OPERATOR','SEPARATOR','STRING_CONSTANT']
# 關鍵字、運算符、分隔符（可以具體指定）進行具體化
DETAIL_TOKEN_STYLE = {
            'include': 'INCLUDE',
            'int': 'INT',
            'float': 'FLOAT',
            'char': 'CHAR',
            'double': 'DOUBLE',
            'void': 'VOID',
            'for': 'FOR',
            'if': 'IF',
            'else': 'ELSE',
            'while': 'WHILE',
            'return': 'RETURN',
            '=': 'ASSIGN',
            '&': 'ADDRESS',
            '<': 'LT',
            '>': 'GT',
            '++': 'SELF_PLUS',
            '--': 'SELF_MINUS',
            '+': 'PLUS',
            '-': 'MINUS',
            '*': 'MUL',
            '/': 'DIV',
            '>=': 'GET',
            '<=': 'LET',
            '(': 'LL_BRACKET',
            ')': 'RL_BRACKET',
            '{': 'LB_BRACKET',
            '}': 'RB_BRACKET',
            '[': 'LM_BRACKET',
            ']': 'RM_BRACKET',
            ',': 'COMMA',
            '\"': 'DOUBLE_QUOTE',
            ';': 'SEMICOLON',
            '#': 'SHARP'}
# 關鍵字 刪掉double
#keywords = [['int','float','double','char','void'],
#        ['if','for','while','else'],['include','return']]
keywords = []

# 運算符
#operators = ['=', '&', '<', '>', '++', '--',
#             '+', '-', '*', '/', '>=', '<=', '!=']
operators = []
# 分隔符
#delimiters = ['(',')','{','}','[',']',',','\"',';']
delimiters = []

# 文件名
file_name = None
# 文件內容
content = None

class Token(object):
    # 記錄分析出來的單詞
    def __init__(self, type_index, value):
        self.type = DETAIL_TOKEN_STYLE[value] if type_index == 0 or type_index == 3 or type_index == 4 else TOKEN_STYLE[type_index]
        self.value = value

def readin():
    # 讀入delimiters分隔符
    de_file = open("delimiters",'r')
    st = {}
    cnt = 0
    st['A'] = ''
    for line in de_file:
        #print(str(len(line)) + " "  + line)
        if len(line) == 5:
            now = st[line[0]] + line[3]
            delimiters.append(now)
        else:
            None
        cnt += 1
    #print delimiters
    del st
    de_file.close()

    # 讀入運算符
    op_file = open("operators",'r')
    st = {}
    cnt = 0
    st['A'] = ''
    for line in op_file:
        if len(line) == 5:
            now = st[line[0]] + line[3]
            operators.append(now)
        else:
            None
        cnt += 1
    print operators
    del st
    op_file.close()

    # 讀入關鍵詞（分三類）
    ke_file = open("keywords_1",'r')
    st = {}
    tmp = []
    cnt = 0
    st['A'] = ''
    for line in ke_file:
        if line[0] == '#': break
        if len(line) == 5:
            now = st[line[0]] + line[3]
            tmp.append(now)
        elif len(line) == 6:
            st[line[4]] = st[line[0]] + line[3]
        cnt += 1
    keywords.append(tmp)
    del st
    ke_file.close()

    ke_file = open("keywords_2",'r')
    st = {}
    tmp = []
    cnt = 0
    st['A'] = ''
    for line in ke_file:
        if line[0] == '#': break
        if len(line) == 5:
            now = st[line[0]] + line[3]
            tmp.append(now)
        elif len(line) == 6:
            st[line[4]] = st[line[0]] + line[3]
        cnt += 1
    keywords.append(tmp)
    del st
    ke_file.close()

    ke_file = open("keywords_3",'r')
    st = {}
    tmp = []
    cnt = 0
    st['A'] = ''
    for line in ke_file:
        if line[0] == '#': break
        if len(line) == 5:
            now = st[line[0]] + line[3]
            tmp.append(now)
        elif len(line) == 6:
            st[line[4]] = st[line[0]] + line[3]
        cnt += 1
    keywords.append(tmp)
    print keywords
    del st
    ke_file.close()


class Lexer(object):
    '''詞法分析器'''

    def __init__(self):
        # 保存分析出來的結果
        self.tokens = []

    # 判定是否是空白字符
    def is_blank(self,index):
        return content[index] == ' ' or content[index] == '\t' or content[index] == '\n' or content[index] == '\r'

    # 跳過空白字符
    def skip_blank(self,index):
        while index < len(content) and self.is_blank(index):
            index += 1
        return index

    # 打印
    def print_log(self, style, value):
        print '(%s, %s)' % (style, value)

    # 判定是否是關鍵字
    def is_keyword(self, value):
        for item in keywords:
            if value in item:
                return True
        return False

    # 詞法分析主程序
    def main(self):
        i = 0
        while i < len(content):
            i = self.skip_blank(i)

            if content[i] == '#':
                None
                #self.tokens.append(Token(4, content[i]))
                #i = self.skip_blank(i + 1)
                # 後面再寫
            # 字母或者數字開頭
            elif content[i].isalpha() or content[i] == '_':
                # 找到該字符串
                temp = ''
                while i < len(content) and (content[i].isalpha() or content[i] == '_' or content[i].isdigit()):
                    temp += content[i]
                    i += 1
                # 判斷該字符串
                if self.is_keyword(temp):
                    self.print_log('關鍵字',temp)
                    self.tokens.append(Token(0,temp))
                else:
                    self.print_log('標識符',temp)
                    self.tokens.append(Token(1,temp))
                i = self.skip_blank(i)
            # 如果數字開頭

def lexer():
    lexer = Lexer()
    lexer.main()
    for token in lexer.tokens:
        print '(%s, %s)' % (token.type, token.value)

def parser():
    parser = Parser()
    parser.main()
    parser.display(parser.tree.root)


if __name__ == '__main__':
    try:
        opts, argvs = getopt.getopt(sys.argv[1:], 's:lph', ['help'])
    except:
        print __doc__
        exit()
    readin()

    for opt, argv in opts:
        if opt in ['-h', '--h', '--help']:
            print __doc__
            exit()
        elif opt == '-s':
            file_name = argv.split('.')[0]
            source_file = open(argv, 'r')
            content = source_file.read()
        elif opt == '-l':
            lexer()
        #elif opt == '-p':
         #   parser()
