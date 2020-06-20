#!/usr/bin/env python

import sys
import argparse
import sys


class Lexer:
    NUM, ID, INPUT, PRINT, LBRA, RBRA, LPAR, RPAR, PLUS, MINUS, LESS, \
    EQUAL, SEMICOLON, MIN, MAX, WHILE, AND, IF, ELSE, STRING_LITERAL, FIND, POINT, NOT_EQUAL, MORE, COLON, REMAINS, MULTIPLICATION, DIVISION, COMMA, RSBRA, LSBRA, EOF = range(32)

    tokens = {
        0 : "number",
        1 : "operand",
        2 : "identifier",
        3 : "identifier",
        4 : "l_brace",
        5 : "r_brace",
        6 : "l_paren",
        7 : "r_paren",
        8 : "operation",
        9 : "operation",
        10 : "logic operation",
        11 : "operation",
        12 : "semi",
        13 : "function",
        14 : "function",
        15 : "cycle",
        16 : "and",
        17 : "if",
        18 : "else",
        19 : "string_literal",
        20 : "function",
        21 : "point",
        22 : "logic operation",
        23 : "logic operation",
        24 : "colon",
        25 : "operation",
        26 : "operation",
        27 : "operation",
        28 : "comma",
        29 : "rsbra",
        30 : "lsbra"
    }

    SYMBOLS = {'{': LBRA, '}': RBRA, '=': EQUAL, ';': SEMICOLON, '(': LPAR,
               ')': RPAR, '+': PLUS, '-': MINUS, '<': LESS, ';': SEMICOLON,
               '.': POINT, '>': MORE, ':': COLON, '%':REMAINS, '*': MULTIPLICATION,
               '/': DIVISION, ',': COMMA, '[': LSBRA, ']': RSBRA}
    WORDS = {'input': INPUT, 'print': PRINT, 'min': MIN, 'max': MAX, 'while': WHILE, 'and': AND,
             'if': IF, 'else': ELSE, 'find': FIND}

    ch = ' '  # assume the first char is a space
    index_ch = 0
    new_index_ch = 0

    line_ = ''

    def __init__(self, line: str, location: int):
        index_ch = 0
        new_index_ch = 0
        self.location = location
        self.line_ = line
        while (self.index_ch < (len(self.line_)) and self.ch != "\n" and self.ch != ""):
            if self.line_.startswith("#"):
                break
            else:
                self.next_tok()

    def error(self, msg: str):
        print(f"{'|'*10}Loc<{self.location}:{self.index_ch + 1}>".ljust(20) + f"{msg} '{self.value}'{'|'*10}")

    def output(self):
        print(f"Loc<{self.location}:{self.index_ch + 1}>".ljust(20) + f"{self.tokens[self.sym]} '{self.ch}'")

    def w_output(self):
        print(f"Loc<{self.location}:{self.index_ch - len(str(self.value)) + 1}>".ljust(20) + f"{self.tokens[self.sym]} '{self.value}'")

    def getc(self):
        if self.index_ch < len(self.line_) and self.ch != "\0" and self.ch != "\n":
            self.index_ch = self.new_index_ch
            self.ch = self.line_[self.index_ch]
            self.new_index_ch += 1

    def next_tok(self):
        self.value = None
        self.sym = None
        while self.sym == None:
            if len(self.ch) == 0:
                self.sym = Lexer.EOF
            elif self.ch.isspace():
                self.getc()
            elif self.ch == "#":
                break
            elif self.ch == "\"":
                literal = ""
                if self.line_.rfind("\"") > self.index_ch:
                    while self.index_ch <= self.line_.rfind("\""):
                        literal += self.ch
                        self.getc()
                    self.sym = Lexer.STRING_LITERAL
                    self.value = literal
                    self.w_output()
                else:
                    if self.line_.rfind("\n") > 0:
                        while self.index_ch < self.line_.rfind("\n"):
                            literal += self.ch
                            self.getc()
                        self.sym = Lexer.STRING_LITERAL
                        self.value = literal
                        self.error('Unknown identifier: ')
                        self.getc()
                    else:
                        while self.index_ch < self.line_.rfind(""):
                            literal += self.ch
                            self.getc()
                        self.sym = Lexer.STRING_LITERAL
                        self.value = literal
                        self.error('Unknown identifier: ')
                        self.getc()

            elif self.ch in Lexer.SYMBOLS:
                self.sym = Lexer.SYMBOLS[self.ch]
                self.output()
                if self.index_ch == len(self.line_) - 1:
                    sys.exit(1)
                else:
                    self.getc()
            elif self.ch.isdigit():
                intval = 0
                while self.ch.isdigit():
                    intval = intval * 10 + int(self.ch)
                    self.getc()
                self.value = intval
                self.sym = Lexer.NUM
                self.w_output()
            elif self.ch.isalpha():
                ident = ''
                while self.ch.isalpha():
                    ident = ident + self.ch.lower()
                    if (self.index_ch == len(self.line_) - 1):
                        self.value = ident
                        self.error('Unknown identifier: ')
                        sys.exit(1)
                    else:
                        self.getc()
                if ident in Lexer.WORDS:
                    self.sym = Lexer.WORDS[ident]
                    self.value = ident
                    self.w_output()
                elif len(ident) == 1:
                    self.sym = Lexer.ID
                    self.value = ident
                    self.w_output()
                else:
                    self.value = ident
                    self.error('Unknown identifier: ')

            else:
                self.value = str(self.ch)
                self.error('Unknown symbol: ')
                self.getc()

def create_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('name', type=str, nargs='?')
    parser.add_argument('fname', type=str, nargs='?')

    return parser

if __name__ == '__main__':
    parser = create_parser()
    option = parser.parse_args(sys.argv[1:])
    file_name = parser.parse_args(sys.argv[2:])

    if option.name == "/dump-tokens":
        file = open(file_name.name, 'r')
        try:
            for location, line in enumerate(file, 1):
                l = Lexer(line, location)
        finally:
            file.close()

    if file_name.name:
        pass
    else:
        print("Файл не указан.")
        sys.exit()

#Работа с файлом

# token_single = {
#           "a" : "operand",
#           "b" : "operand",
#           "c" : "operand",
#           "<" : "logic operation",
#           ">" : "logic operation",
#           "+" : "operation",
#           "-" : "operation",
#           "*" : "operation",
#           "/" : "operation",
#           ")" : "r_paren",
#           "(" : "l_paren",
#           "{" : "l_brace",
#           "}" : "r_brace",
#           ";" : "semi",
#           ":" : "colon",
#           "=" : "operation",
#           "," : "comma"
# }
# #Список функций
# token_other = {
#                 "print" : "identifier",
#                 "input" : "identifier",
#                 "while" : "cycle",
#                 "and" : "and",
#                 "if" : "if",
#                 "else" : "else",
#                 "!=" : "logic operation",
#                 "==" : "logic operation",
#                 "%=" : "operation",
#                 "array" : "operand",
#                 "return" : "return",
#                 "min" : "function",
#                 "max" : "function"
# }
# #Позиция функции из списка функций
# position = 0
#
# #Взаимодействие со строкой терминала
# def create_parser():
#     parser = argparse.ArgumentParser()
#     parser.add_argument('name', type=str, nargs='?')
#     parser.add_argument('fname', type=str, nargs='?')
#
#     return parser
#
# if __name__ == '__main__':
#     parser = create_parser()
#     option = parser.parse_args(sys.argv[1:])
#     file_name = parser.parse_args(sys.argv[2:])
#
#     if option.name == "/dump-tokens":
#         pass
#
#     if file_name.name:
#         pass
#     else:
#         print("Файл не указан.")
#         sys.exit()
#
# #Работа с файлом
# file = open(file_name.name, 'r')
# try:
#     for location, line in enumerate(file, 1):
#         # Налицие литерала в строке
#         literal = False
#         skip = False
#         error = False
#         n_skip = None
#         dict_of_token_position = {}
#
#         # Обработка комментария
#         if line.startswith("#"):
#             continue
#
#         # Поиск функции в строке
#         for key_t_o, value_t_o in token_other.items():
#             if line.find(key_t_o) != -1:
#                 dict_of_token_position[line.find(key_t_o)] = key_t_o
#                 if line.rfind(key_t_o) not in dict_of_token_position:
#                     dict_of_token_position[line.rfind(key_t_o)] = key_t_o
#
#         # Начало обработки каждого символа
#         for num_of_symbol in range(len(line)):
#             # Случай с функцией не в начале строки.
#             for key_p, value_p in dict_of_token_position.items():
#                 if num_of_symbol == key_p:
#                     print(f"Loc=<{location}:{num_of_symbol}> {token_other[value_p]} '{value_p}'")
#                     n_skip = len(value_p) + num_of_symbol
#                     skip = True
#                     break
#
#             if skip == True and num_of_symbol < n_skip:
#                 continue
#             else:
#                 skip = False
#
#
#             # Обработка строчных литералов
#             if line[num_of_symbol] == "\"" and literal == False:
#                 start = line.find("\"")
#                 if line.rfind("\"") > start:
#                     end = line.rfind("\"")
#                     print(f"Loc=<{location}:{num_of_symbol}> string_literal '{line[start:end + 1]}'")
#                     literal = True
#                 else:
#                     if line.rfind("\n") > 0:
#                         end = line.rfind("\n")
#                         print(f"<<Loc=<{location}:{num_of_symbol}> unknown '{line[start:end]}'>>")
#                         break
#                     else:
#                         end = line.rfind("")
#                         print(f"<<Loc=<{location}:{num_of_symbol}> unknown '{line[start:end]}'>>")
#                         break
#
#             if line[num_of_symbol] == "=" and line[num_of_symbol + 1] == " " and line[num_of_symbol + 2] == "[":
#                 start = line.find("[")
#                 end = line.rfind("]")
#                 print(f"Loc=<{location}:{num_of_symbol}> array '{line[start:end + 1]}'")
#                 break
#
#
#             if line[num_of_symbol] not in token_single and line[num_of_symbol] != "\n" and line[num_of_symbol] != " " and literal == False and line[num_of_symbol].isdigit() == False:
#                     if len(line) <= 2:
#                         print(f"<<Loc=<{location}:{num_of_symbol}> unknown '{line[num_of_symbol]}'>>")
#                         break
#                     else:
#                         print(f"<<Loc=<{location}:{num_of_symbol}> unknown '{line[num_of_symbol:len(line)]}'>>")
#                         break
#
#
#             # Вывод токенов
#             for key_ts, value_ts in token_single.items():
#                 if line[num_of_symbol] == key_ts:
#                     print(f"Loc=<{location}:{num_of_symbol}> {value_ts} '{key_ts}'")
#
#             # Вывод чисел
#             if line[num_of_symbol].isdigit():
#                 print(f"Loc=<{location}:{num_of_symbol}> number '{line[num_of_symbol]}'")
#
# finally:
#     file.close()