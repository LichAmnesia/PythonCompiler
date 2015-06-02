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
TOKEN_STYLE = ['keyword', 'identifier', 'number',
        'operator','limiter','CONSTANT']
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
            'function':'FUNCTION',
            'break':'BREAK',
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
        self.dtype = TOKEN_STYLE[type_index]
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
    print delimiters
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
            elif content[i].isdigit():
                temp = ''
                while i < len(content):
                    if content[i].isdigit() or (content[i] == '.' and content[i + 1].isdigit()):
                        temp += content[i]
                        i += 1
                    elif not content[i].isdigit():
                        if content[i] == '.':
                            print 'float number error!'
                            exit()
                        else: break
                self.print_log('常量',temp)
                self.tokens.append(Token(2,temp))
                i = self.skip_blank(i)
            # 如果是分隔符
            elif content[i] in delimiters:
                self.print_log('分隔符', content[i])
                self.tokens.append(Token(4, content[i]))
                # 如果是字符串常量
                if content[i] == '\"':
                    i += 1
                    temp = ''
                    while i < len(content):
                        if content[i] != '\"':
                            temp += content[i]
                            i += 1
                        else: break
                    else:
                        print 'error: lack of \"'
                        exit()
                    self.print_log('常量',temp)
                    self.tokens.append(Token(5,temp))
                    self.print_log('分隔符','\"')
                    self.tokens.append(Token(4,'\"'))
                i = self.skip_blank(i + 1)
            # 如果是運算符
            elif content[i] in operators:
                # 如果是 ++ 或者 --
                if (content[i] == '+' or content[i] == '_') and content[i + 1] == content[i]:
                    self.print_log('運算符', content[i] * 2)
                    self.tokens.append(Token(3,content[i] * 2))
                    i = self.skip_blank(i + 2)
                # 如果是>= 或者 <=
                elif (content[i] == '>' or content[i] == '<') and content[i + 1] == '=':
                    self.print_log('運算符',content[i] + '=')
                    self.tokens.append(Token(3,content[i] + '='))
                    i = self.skip_blank(i + 2)
                # 如果是 -2312
                elif (content[i-1] =='=' and content[i] == '-' and content[i + 1].isdigit()):
                    temp = '-'
                    i += 1
                    while i < len(content):
                        if content[i].isdigit() or (content[i] == '.' or content[i + 1].isdigit()):
                            temp += content[i]
                            i += 1
                        elif not content[i].isdigit():
                            if content[i] == '.':
                                print 'negative float number error!'
                                exit()
                            else: break
                    self.print_log('常量',temp)
                    self.tokens.append(Token(2,temp))
                    i = self.skip_blank(i)
                # 其他
                else:
                    self.print_log('運算符',content[i])
                    self.tokens.append(Token(3,content[i]))
                    i = self.skip_blank(i + 1)
def lexer():
    lexer = Lexer()
    lexer.main()
    for token in lexer.tokens:
        print '(%s, %s)' % (token.dtype, token.value)

class NFA(object):
    def __init__(self):
        self.name = None
        self.first = [0 for i in range(110)]
        self.follow = [0 for i in range(110)]
        self.edge = []
        self.to = {}
        self.production = []
        self.select = []


class Parser():
    def __init__(self):
        lexer = Lexer()
        lexer.main()
        self.tokens = lexer.tokens
        self.index = 0

        self.keyword = []
        self.vt = {}
        self.vn = {}
        self.nfa = [NFA() for i in range(105)]
        start = 0

    def read_grammar(self,filename):
        fin = open(filename,'r')
        lines = [line.strip() for line in fin.readlines()]
        allwords = []
        for i in lines:
            if i == '': continue
            word = i.split(' ')
            for j in word:
                if j == '': continue
                allwords.append(j)
        fin.close()
        self.keyword = []
        tmp = []
        self.vn = {}
        now = 0
        i = 0
        while i < len(allwords):
            s1 = allwords[i]
            #print i
            if i + 1 < len(allwords) and allwords[i + 1] == ':' :
                if self.vn.has_key(s1) == True:
                    now = self.vn[s1]
                else :
                    now += 1
                    self.vn[s1] = now
                    print now
                    self.nfa[now].name = s1
                    self.nfa[now].production = []
            else:
                tmp = []
                tmp.append(s1)

                while 1 :
                    if i + 1 >= len(allwords): break
                    if i + 1 < len(allwords) and (allwords[i + 1] == '|' or allwords[i + 1] == '\\' ):
                        break
                    tmp.append(allwords[i + 1])
                    i += 1
                    #print tmp
                self.nfa[now].production.append(tmp)
                #print self.nfa[now].production
            i += 2
        self.get_terminal()
        return

    def get_terminal(self):
        self.vt = {}
        #print len(self.vn)
        for i in range(1,len(self.vn) + 1):
            for j in range(len(self.nfa[i].production)):
                for k in range(len(self.nfa[i].production[j])):
                    s = self.nfa[i].production[j][k]
                    if self.isTerminal(s) and self.vt.has_key(s) == False:
                        tmp = len(self.vt)
                        self.vt[s] = tmp + 1
                        print tmp,s
        #print len(self.vn), len(self.vt)
        #print self.vn.keys()
        #for i in range(1,len(self.vn) + 1):

    def isTerminal(self,s):
        if self.vn.has_key(s) == False: return True
        return False


    def get_firstset(self):
        for i in range(1,len(self.vn) + 1):
            self.nfa[i].first = [0 for j in range(110)]
        tmp = [0 for i in range(110)]
        cnt = 0
        while True :
            flag = False
            cnt += 1
            #print cnt,'cnt'
            for i in range(1,len(self.vn) + 1):
                tmp = [0 for j in range(110)]
                for j in range(110):
                    tmp[j] = self.nfa[i].first[j]
                for j in range(len(self.nfa[i].production)):
                    k = 0
                    while k < len(self.nfa[i].production[j]) :
                        s = self.nfa[i].production[j][k]
                        #print cnt,k
                        #print cnt,s,k
                        if self.isTerminal(s):
                            self.nfa[i].first[self.vt[s]] = 1
                            break
                        else :
                            id = self.vn[s]

                            for l in range(110):
                                self.nfa[i].first[l] |= self.nfa[id].first[l]
                            #print self.nfa[i].first
                            #print tmp
                            if self.nfa[id].first[self.vt['$']]:
                                self.nfa[i].first[self.vt['$']] = 0
                            else: break
                        k += 1
                    if k == len(self.nfa[i].production[j]):
                        self.nfa[i].first[vt['$']] = 1
                #print tmp, self.nfa[i].first
                if flag == False and tmp != self.nfa[i].first:
                    flag = True
            if flag == False: break

    def get_followset(self):
        if self.get_firstset(): return False
        start = -1
        for i in range(1,len(self.vn) + 1):
            if self.nfa[i].name == 'start':
                start = i
                break

        if start == -1:
            print "Your grammer should have a non-ternimal 'start' as a start."
            return False
        #add @ of end
        for i in range(1,len(self.vn) + 1):
            self.nfa[i].follow = [0 for j in range(110)]
        sz = len(self.vt)
        #print sz
        self.vt['@'] = sz + 1
        self.nfa[start].follow[self.vt['@']] = 1

        tmp = [0 for i in range(110)]
        while True:
            flag = False
            for i in range(1,len(self.vn) + 1):
                for j in range(len(self.nfa[i].production)):
                    for k in range(len(self.nfa[i].production[j])):
                        s = self.nfa[i].production[j][k]
                        if self.isTerminal(s) == False:
                            id = self.vn[s];
                            for l in range(110):
                                tmp[l] = self.nfa[id].follow[l]

                            h = k + 1
                            while h < len(self.nfa[i].production[j]) :
                                s = self.nfa[i].production[j][h];
                                if self.isTerminal(s):
                                    self.nfa[id].follow[self.vt[s]] = 1
                                    break
                                else :
                                    kk = self.vn[s]
                                    for l in range(110):
                                        self.nfa[id].follow[l] |= self.nfa[kk].first[l]
                                    if self.nfa[kk].first[self.vt['$']]:
                                        self.nfa[id].follow[self.vt['$']] = 0
                                    else : break
                                h += 1
                            if h == len(self.nfa[i].production[j]):
                                for l in range(110):
                                    self.nfa[id].follow[l] |= self.nfa[i].follow[l]
                            if flag == False and self.nfa[id].follow != tmp:
                                flag = True
            if flag == False: break

        #for i in range(1,len(self.vn) + 1):
        #    a = 0
        #    b = 0
        #    for j in range(110):
        #        if self.nfa[i].first[j] == 1: a += 1
        #        if self.nfa[i].follow[j] == 1: b += 1
        #    print a,b
        return True


    def get_selectset(self):
        if self.get_followset() == False: return False
        tmp = [0 for i in range(110)]
        for i in range(1,len(self.vn) + 1):
            self.nfa[i].select = []

            for j in range(len(self.nfa[i].production)):
                k = 0
                tmp = [0 for l in range(110)]
                while k < len(self.nfa[i].production[j]):
                    s = self.nfa[i].production[j][k]
                    if s == '$':
                        None
                    elif self.isTerminal(s):
                        tmp[self.vt[s]] = 1
                        print tmp,self.nfa[i].select
                        self.nfa[i].select.append(tmp)
                        break
                    else:
                        id = self.vn[s]
                        for l in range(110):
                            tmp[l] |= self.nfa[id].first[l]
                        if self.nfa[id].first[self.vt['$']]:
                            tmp[self.vt['$']] = 0
                        else :
                            self.nfa[i].select.append(tmp)
                            break
                    k += 1
                if k == len(self.nfa[i].production[j]):
                    for l in range(110):
                        tmp[l] |= self.nfa[i].follow[l]
                    self.nfa[i].select.append(tmp)
        #for i in range(1,len(self.vn) + 1):
        #    a = 0
        #    b = 0
        #    for j in range(110):
        #        if self.nfa[i].first[j] == 1: a += 1
        #        if self.nfa[i].follow[j] == 1: b += 1
        #    print a,b
        return True

    def build_edge(self):
        if self.get_selectset() == False : return False
        tmp = [0 for i in range(110)]
        print "sss"
        for i in range(1,len(self.vn)+1):
            self.nfa[i].to = {}
            for j in range(len(self.nfa[i].production)):
                #print self.nfa[i].select[j],len(self.nfa[i].select[j]);
                for l in range(len(self.nfa[i].select[j])):
                    tmp[l] = self.nfa[i].select[j][l];
                for k in range(1,len(self.vt) + 1):
                        if tmp[k]:
                            if self.nfa[i].to.has_key(k) == True:
                                print "Not a LL(1) grammer"
                                print "Error in " , self.nfa[i].name
                                return False
                            self.nfa[i].to[k] = j
        return True

    def compile_lex_table(self):
        cnt = 0
        now = 0
        y = None
        x = None
        s1 = None
        s2 = None
        st = []
        st.append('@')
        st.append('start')
        while True:

            if now == len(self.tokens): y = '@'
            else :
                s1 = self.tokens[now].dtype
                s2 = self.tokens[now].value
                y = s1
                if y == 'keyword' or y == 'operator' or y == 'limiter':
                    y = s2
            x = st[len(st)-1]
            cnt += 1

            while True:
                x = st[len(st)-1]
                if self.isTerminal(x) :
                    if x == y:
                        st.pop()
                        break
                    else:
                        print 'Syntax Error with in',cnt,'line'
                        return False
                else:
                    id = self.vn[x]
                    print s1,s2,y,self.vt[y]
                    if self.nfa[id].to.has_key(self.vt[y]) == True:
                        k = self.nfa[id].to[self.vt[y]]
                        st.pop()
                        j = len(self.nfa[id].production[k]) - 1
                        while j >= 0:
                            if self.nfa[id].production[k][j] != '$':
                                st.append(self.nfa[id].production[k][j])
                            j -= 1
                    else :
                        print '2 Syntax Error with in',cnt,'line'
                        return False
                        #for j in range(len(self.nfa[id].production[k])):
            if y == '@': break
            now += 1
        print 'Compiling successfully.'


    def _init(self,s):
        if self.read_grammar(s) == False: return False
        if self.build_edge() == False: return False
        return True

    def syntax_grammar(self,s):
        if self._init(s) == False : return False
        if self.compile_lex_table() == False : return False
        return True

    # 主程序
    def main(self):
        # 根節點
        if self.syntax_grammar("syntax_grammar") == True :
            print "YES"
        else :
            print "NO"

def parser():
    parser = Parser()
    parser.main()

    #parser.display(parser.tree.root)


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
        elif opt == '-p':
            parser()
