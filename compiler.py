#!/usr/bin/env python

import sys
import argparse
import os

NUM, ID, INPUT, PRINT, LBRA, RBRA, LPAR, RPAR, PLUS, MINUS, LESS, \
EQUAL, SEMICOLON, MIN, MAX, WHILE, AND, IF, ELSE, STRING_LITERAL, \
FIND, POINT, NOT_EQUAL, MORE, COLON, REMAINS, MULTIPLICATION, DIVISION, COMMA, RSBRA, LSBRA, EXCLAM = range(32)

tokens = {
    0: "number",
    1: "operand",
    2: "identifier",
    3: "identifier",
    4: "l_brace",
    5: "r_brace",
    6: "l_paren",
    7: "r_paren",
    8: "operation",
    9: "operation",
    10: "logic operation",
    11: "operation",
    12: "semi",
    13: "function",
    14: "function",
    15: "cycle",
    16: "and",
    17: "if",
    18: "else",
    19: "string_literal",
    20: "function",
    21: "point",
    22: "logic operation",
    23: "logic operation",
    24: "colon",
    25: "operation",
    26: "operation",
    27: "operation",
    28: "comma",
    29: "rsbra",
    30: "lsbra",
    31: "logic operation"
}
SYMBOLS = {'{': LBRA, '}': RBRA, '=': EQUAL, ';': SEMICOLON, '(': LPAR,
           ')': RPAR, '+': PLUS, '-': MINUS, '<': LESS,
           '.': POINT, '>': MORE, ':': COLON, '%': REMAINS, '*': MULTIPLICATION,
           '/': DIVISION, ',': COMMA, '[': LSBRA, ']': RSBRA, '!': EXCLAM}
WORDS = {'input': INPUT, 'print': PRINT, 'min': MIN, 'max': MAX, 'while': WHILE, 'and': AND,
         'if': IF, 'else': ELSE, 'find': FIND}
SAVE = []  # Массив токенов
nesting = 0  # Вложенность для циклов и т.д.
lex_nesting = 0  # Вложенность для парсера
check = False  # Была ли проверка табуляций
TABLE = []  # Таблица символов


# Функция для вывода ошибок
def error(location: int, position: int, msg: str, value: str):
    print(f"-Loc<{location}:{position + 1}>".ljust(10) + f"{msg}".ljust(20) + f"'{value}'-")


# Функция для вывода токенов
def output(location: int, position: int, type: str, value: str):
    print(f"Loc<{location}:{position + 1}>".ljust(10) + f"{type}".ljust(20) + f"'{value}'")


# Лексер
def lexer(input_data: str, location: int, display: bool):
    global lex_nesting
    global check
    # текущее положение(курсор)
    current = 0

    # проверка табуляции в while, if, else
    if check:
        if lex_nesting != 0:
            if input_data.startswith("\t" * lex_nesting) or input_data.startswith(" " * lex_nesting * 4):
                check = False
            else:
                if display:
                    error(location, 0, "Invalid number of tabs:", "")
                check = False

    # Проход по строке и сбор токенов
    while current < len(input_data):
        # обрабатываемый символ
        symbol = input_data[current]

        # переменная для отслеживания начала символа(слова) для вывода позиции
        start_position = current
        # обработка комментариев
        if symbol == "#":
            break
        # обработка конца строки
        elif symbol == "\n":
            break
        # обработка пробелов
        elif symbol.isspace():
            current += 1
            continue
        # обработка различных небуквенных символов
        elif symbol in SYMBOLS:
            # Переменная для проверки !=, >=, <=
            # Сначала просмотр первого символа
            if current < len(input_data) - 1:
                # Если не конец строки, то смотрим следующий символ
                next_symbol = input_data[current + 1]
                # Если есть схожий с символами из таблицы. кроме скобок, то собираем в один токен
                if (next_symbol in SYMBOLS) and (next_symbol != "}" and next_symbol != "]" and next_symbol != ")"):
                    temporary = {tokens[SYMBOLS[symbol]]: symbol + next_symbol}
                    symbol_for_output = symbol + next_symbol
                    current += 1
                    SAVE.append(temporary)
                # Есои следующий символ не относится к таблице, то просто добавляем токен
                else:
                    temporary = {tokens[SYMBOLS[symbol]]: symbol}
                    symbol_for_output = symbol
                    SAVE.append(temporary)
            else:  # Конец строки(следующего символа нет), просто добавляем токен
                temporary = {tokens[SYMBOLS[symbol]]: symbol}
                symbol_for_output = symbol
                SAVE.append(temporary)
            # Для лексического анализа выводятся токены
            if display:
                output(location, start_position, tokens[SYMBOLS[symbol]], symbol_for_output)

            current += 1
            continue
        # обработка чисел
        elif symbol.isdigit():
            value = ""
            # Сбор больших цифр в один токен
            while symbol.isdigit():
                value += symbol
                current += 1
                if current < len(input_data):
                    symbol = input_data[current]
                else:
                    break

            temporary = {tokens[NUM]: value}
            SAVE.append(temporary)

            if display:
                output(location, start_position, tokens[NUM], value)

            continue
        # обработка строковых литералов
        elif symbol == "\"":
            literal = ""
            # Если нашли правую ковычку, то собираем все в один токен
            if input_data.rfind("\"") > current:
                current += 1
                symbol = input_data[current]

                while symbol != "\"":
                    literal += symbol
                    current += 1
                    if current < len(input_data):
                        symbol = input_data[current]
                    else:
                        break

                current += 1
                temporary = {tokens[STRING_LITERAL]: literal}
                SAVE.append(temporary)

                if display:
                    output(location, start_position, tokens[STRING_LITERAL], literal)

                continue
            else:  # Если не нашли правую ковычку, то до конца строки собираем все в один токен
                symbol = input_data[current]
                if input_data.rfind("\n") > 0:
                    while current < input_data.rfind("\n"):
                        literal += symbol
                        current += 1
                        if current < len(input_data):
                            symbol = input_data[current]
                        else:
                            break

                    error(location, start_position, "Unknown identifier:", literal)
                else:  # То же самое, только до конца файла(последняя строка)
                    while symbol != "":
                        literal += symbol
                        current += 1
                        if current < len(input_data):
                            symbol = input_data[current]
                        else:
                            break

                    error(location, start_position, "Unknown identifier:", literal)
        # обработка букв, названий переменных, функций и т.д.
        elif symbol.isalpha():
            value = ""
            # Сбор длинных слов в один токен
            while symbol.isalpha():
                value += symbol
                current += 1
                if current < len(input_data):
                    symbol = input_data[current]
                else:
                    break
            # Проверка на то, есть ли данное слово в таблице
            if value.lower() in WORDS:
                # Если да, то смотрим как оно выглядит, далее обрабока разных слов или ошибка
                if value.islower():
                    if value == "while" or value == "if":
                        if input_data[-2] == ":":
                            lex_nesting += 1
                            check = True
                            temporary = {tokens[WORDS[value]]: value}
                            SAVE.append(temporary)
                        else:
                            error(location, start_position, "'while' will not work", "")
                            temporary = {tokens[WORDS[value]]: value}
                            SAVE.append(temporary)
                    elif value == "else":
                        if input_data[-2] == ":":
                            check = True
                            temporary = {tokens[WORDS[value]]: value}
                            SAVE.append(temporary)
                        else:
                            error(location, start_position, "'else' will not work", "")
                            temporary = {tokens[WORDS[value]]: value}
                            SAVE.append(temporary)
                    else:
                        temporary = {tokens[WORDS[value]]: value}
                        SAVE.append(temporary)

                    if display:
                        output(location, start_position, tokens[WORDS[value]], value)

                    continue
                else:
                    error(location, start_position, "Need lower:", value)
            else:  # Просто символ, просто в токен
                temporary = {tokens[ID]: value}
                SAVE.append(temporary)

                if display:
                    output(location, start_position, tokens[ID], value)

                continue

        else:  # Ошибка, если неизвестный символ
            error(location, start_position, "Unknown symbol:", symbol)
            current += 1

            continue

    return SAVE


# Функция вывода ast-дерева
def output_ast(ast):
    global nesting
    for key, value in ast.items():
        if isinstance(value, list):
            print("\t" * nesting + f"'{key}' : " + "[")
            nesting += 1
            # Присваивается список со словарём(-ями) для обработки
            list_of_dict = ast[key]
            for i in range(len(list_of_dict)):
                print("\t" * nesting + "{")
                # Присваивается один из словарей в list_of_dict
                dict_in_list = list_of_dict[i]
                output_ast(dict_in_list)
                print("\t" * nesting + "}")
            nesting -= 1
        else:
            print("\t" * nesting + f"'{key}' : '{value}'")


# Парсер
def parser(tokens_arr, display: bool):
    current = 0
    next_token = 0
    okay = False

    def LL1_walk():  # Функция для прохода по токенам
        nonlocal current
        nonlocal next_token

        if current < len(tokens_arr):  # Если токены есть
            token = tokens_arr[current]

            if current < len(tokens_arr) - 1:  # Если следующий токен есть
                next_token = tokens_arr[current + 1]
            else:
                next_token = {'none': 'none'}

            if "operand" in token.keys():
                if "operation" in next_token.keys():
                    current += 2
                    return {'type': 'Operation',
                            'value': next_token.get("operation"),
                            'params': [{'type': 'Operand',
                                        'value': token.get("operand")},
                                       LL1_walk()]
                            }
                elif "logic operation" in next_token.keys():
                    current += 2
                    return {'type': 'LogicOperation',
                            'value': next_token.get("logic operation"),
                            'params': [{'type': 'Operand',
                                        'value': token.get("operand")},
                                       LL1_walk()]
                            }
                elif "comma" in next_token.keys():
                    current += 2
                    return {'type': 'Operand',
                            'value': token.get("operand")}
                elif "point" in next_token.keys():
                    current += 2

                    return {'type': 'Operand',
                            'value': token.get("operand"),
                            'params': [LL1_walk()]}
                else:
                    current += 1
                    return {'type': 'Operand',
                            'value': token.get("operand")}

            elif "identifier" in token.keys():
                if "l_paren" in next_token.keys():
                    node = {'type': 'Function',
                            'value': token.get("identifier"),
                            'params': []}
                    current += 2
                    token = tokens_arr[current]

                    while "r_paren" not in token.keys():
                        node['params'].append(LL1_walk())
                        token = tokens_arr[current]
                    current += 1

                    return node
                else:
                    current += 1
                    if display:
                        error(-1, -1, " misuse", token.get("identifier"))

            elif "r_paren" in token.keys():
                current += 1

            elif "number" in token.keys():
                if "operation" in next_token.keys():
                    current += 2

                    return {'type': 'Operation',
                            'value': next_token.get("operation"),
                            'params': [{'type': 'Number',
                                        'value': token.get("number")},
                                       LL1_walk()]
                            }
                else:
                    current += 1

                    return {'type': 'Number',
                            'value': token.get("number")}

            elif "string_literal" in token.keys():
                current += 1

                return {'type': 'StringLiteral',
                        'value': token.get("string_literal")}

            elif "lsbra" in token.keys():
                temporary_list = []

                while "rsbra" not in token.keys():
                    current += 1
                    token = tokens_arr[current]
                    if "number" in token.keys():
                        temporary_list.append(token["number"])
                    elif "string_literal" in token.keys():
                        temporary_list.append(token["string_literal"])
                current += 1

                return {'type': 'Array',
                        'value': temporary_list}

            elif "function" in token.keys():
                if "l_paren" in next_token.keys():
                    node = {'type': 'Method',
                            'value': token.get("function"),
                            'params': []}
                    current += 2
                    token = tokens_arr[current]
                    while "r_paren" not in token.keys():
                        node['params'].append(LL1_walk())
                        token = tokens_arr[current]
                    current += 1

                    return node

            elif "cycle" in token.keys():
                node = {'type': 'Cycle',
                        'value': token.get("cycle"),
                        'params': []}
                current += 1
                token = tokens_arr[current]
                while "colon" not in token.keys():
                    node['params'].append(LL1_walk())
                    token = tokens_arr[current]

                current += 1

                return node

            elif "and" in token.keys():
                node = {'type': 'And',
                        'value': token.get("and"),
                        'params': []}
                current += 1
                token = tokens_arr[current]
                while ("and" not in token.keys()) and ("colon" not in token.keys()):
                    node['params'].append(LL1_walk())
                    token = tokens_arr[current]

                return node

            elif "if" in token.keys():
                node = {'type': 'СonditionalOperator',
                        'value': token.get("if"),
                        'params': []}
                current += 1
                token = tokens_arr[current]
                while "colon" not in token.keys():
                    node['params'].append(LL1_walk())
                    token = tokens_arr[current]

                current += 1

                return node

            elif "else" in token.keys():
                current += 2

                return {'type': 'Else',
                        'value': token.get("else")}

    # Основное аст-дерево
    ast = {'type': 'Program',
           'body': list()}

    # Цикл для запуска прохода по токенам и добавления их в дерево
    while current < len(tokens_arr):
        ast['body'].append(LL1_walk())

    if okay:
        visitor(ast)

    # print(ast)  # Вывод дерева в строчку для отладки
    # print(TABLE)  # Вывод таблицы символов и типов

    # Вывод дерева
    if display:
        output_ast(ast)

    return ast


# Таблица символов и проверка соответствия типов
def table(left_parameter, operation, right_parameter=None):
    def table_insert(left_parameter, operation, right_parameter=None):
        left_type = None
        right_type = None

        if operation == "=":  # Если присваивание
            if left_parameter['type'] == "Operand":  # Операнде присваивается a = ...
                declared = False
                if len(TABLE) > 0:  # Если в таблице что-то есть
                    current = 0
                    while current < len(TABLE):  # Поиск в таблице
                        if left_parameter['value'] in TABLE[current]:
                            declared = True
                            break
                        else:
                            current += 1
                else:  # Если таблица пустая
                    TABLE.append({left_parameter['value']: 'None'})
                    declared = True

                if not declared:
                    TABLE.append({left_parameter['value']: 'None'})

            if right_parameter['type'] == "Number":  # Что присваивается ... = 2
                current = 0
                while current < len(TABLE):  # Поиск в таблице
                    if left_parameter['value'] in TABLE[current]:
                        TABLE[current][left_parameter['value']] = 'int'
                    current += 1
            elif right_parameter['type'] == "Operand":   # Что присваивается ... = b
                declared = False
                if 'params' in right_parameter:   # Если присутствуют методы у операнды, например, строковый метод find
                    current = 0
                    while current < len(TABLE):  # Поиск в таблице
                        if right_parameter['value'] in TABLE[current]:
                            if TABLE[current][right_parameter['value']] == 'string':  # Если найденный операнд строка,
                                _current = 0                                          # то все хорошо, иначе ошибка
                                while _current < len(TABLE):
                                    if left_parameter['value'] in TABLE[_current]:
                                        TABLE[_current][left_parameter['value']] = 'string'
                                        break
                                    else:
                                        _current += 1
                            else:
                                print("ERROR: Available only for strings")
                            declared = True
                            break
                        else:
                            current += 1
                else:  # Если обычный операнд
                    current = 0
                    while current < len(TABLE):
                        if right_parameter['value'] in TABLE[current]:
                            declared = True
                            _type = TABLE[current][right_parameter['value']]
                            current_ = 0
                            while current < len(TABLE):
                                if left_parameter['value'] in TABLE[current_]:
                                    if TABLE[current_][left_parameter['value']] == _type:
                                        break
                                    else:
                                        TABLE[current_][left_parameter['value']] = _type
                                    break
                                else:
                                    current_ += 1
                        else:
                            current += 1

                if not declared:
                    print(f"ERROR: Operand {right_parameter['value']} is not declared")
                    sys.exit()
            elif right_parameter['type'] == "Function":   # Что присваивается ... = input()
                if right_parameter['value'] == "input":
                    current = 0
                    while current < len(TABLE):
                        if left_parameter['value'] in TABLE[current]:
                            TABLE[current][left_parameter['value']] = 'input'
                        current += 1
            elif right_parameter['type'] == "StringLiteral":  # Что присваивается ... = "hello"
                current = 0
                while current < len(TABLE):
                    if left_parameter['value'] in TABLE[current]:
                        TABLE[current][left_parameter['value']] = 'string'
                    current += 1
            elif right_parameter['type'] == "Operation":   # Что присваивается ... = ... + ...
                _type = table_insert(right_parameter.get('params')[0], right_parameter['value'],
                                     right_parameter.get('params')[1])
                current = 0
                while current < len(TABLE):
                    if left_parameter['value'] in TABLE[current]:
                        TABLE[current][left_parameter['value']] = _type
                        break
                    else:
                        current += 1
            elif right_parameter['type'] == "Array":   # Что присваивается ... = [..., ..., ...]
                current = 0
                while current < len(TABLE):
                    if left_parameter['value'] in TABLE[current]:
                        TABLE[current][left_parameter['value']] = 'list'
                        break
                    else:
                        current += 1
            elif right_parameter['type'] == "Method":   # Что присваивается ... = string.find(...)
                if right_parameter['value'] == "min" or right_parameter['value'] == "max":
                    current = 0
                    while current < len(TABLE):
                        if left_parameter['value'] in TABLE[current]:
                            TABLE[current][left_parameter['value']] = 'int'
                            break
                        else:
                            current += 1
        elif operation == "+" or operation == "-" or operation == "*" or operation == "/" or operation == "%":
            if left_parameter['type'] == "Operand":
                current = 0
                declared = False
                while current < len(TABLE):
                    if left_parameter['value'] in TABLE[current]:
                        left_type = TABLE[current][left_parameter['value']]
                        declared = True
                        break
                    else:
                        current += 1

                if not declared:
                    print(f"ERROR: Operand {left_parameter['value']} is not declared")
                    sys.exit()
            elif left_parameter['type'] == "Number":
                left_type = 'int'
            elif left_parameter['type'] == "StringLiteral":
                left_type = 'string'

            if right_parameter['type'] == "Operand":
                current = 0
                declared = False
                while current < len(TABLE):
                    if right_parameter['value'] in TABLE[current]:
                        right_type = TABLE[current][right_parameter['value']]
                        declared = True
                        break
                    else:
                        current += 1

                if not declared:
                    print(f"ERROR: Operand {right_parameter['value']} is not declared")
                    sys.exit()
            elif right_parameter['type'] == "Number":
                right_type = 'int'
            elif right_parameter['type'] == "StringLiteral":
                right_type = 'string'

            # Проверка соотвествия типов
            if left_type == right_type:
                return left_type
            elif left_type == 'input':
                return right_type
            elif right_type == 'input':
                return left_type
            else:
                print(f"ERROR: Unsupported operand type(s) for {operation}: {left_type} and {right_type}")
        elif operation == "<" or operation == ">" or operation == "<=" or operation == ">=" or operation == "==" or \
                operation == "!=":
            if left_parameter['type'] == "Operand":
                current = 0
                declared = False
                while current < len(TABLE):
                    if left_parameter['value'] in TABLE[current]:
                        left_type = TABLE[current][left_parameter['value']]
                        declared = True
                        break
                    else:
                        current += 1

                if not declared:
                    print(f"ERROR: Operand {left_parameter['value']} is not declared")
                    sys.exit()
            elif left_parameter['type'] == "Number":
                left_type = 'int'

            if right_parameter['type'] == "Operand":
                current = 0
                declared = False
                while current < len(TABLE):
                    if right_parameter['value'] in TABLE[current]:
                        right_type = TABLE[current][right_parameter['value']]
                        declared = True
                        break
                    else:
                        current += 1

                if not declared:
                    print(f"ERROR: Operand {right_parameter['value']} is not declared")
                    sys.exit()
            elif right_parameter['type'] == "Number":
                right_type = 'int'

            if left_type == right_type:
                return left_type
            elif left_type == 'input':
                return right_type
            elif right_type == 'input':
                return left_type
            else:
                print(f"ERROR: Unsupported operand type(s) for {operation}: {left_type} and {right_type}")
        elif operation == "print":
            if left_parameter['type'] == "Operand":
                current = 0
                declared = False
                while current < len(TABLE):
                    if left_parameter['value'] in TABLE[current]:
                        declared = True
                        break
                    else:
                        current += 1

                if not declared:
                    print(f"ERROR: Operand '{left_parameter['value']}' is not declared")
                    sys.exit()
        elif operation == "while" or operation == "if":
            if left_parameter['type'] == "LogicOperation":
                table_insert(left_parameter.get('params')[0], left_parameter['value'],
                             left_parameter.get('params')[1])
            elif left_parameter['type'] == "And":
                table_insert(left_parameter.get('params')[0], operation)

    table_insert(left_parameter, operation, right_parameter)


# Посетитель
def visitor(ast):
    parent = ast
    ast_type = parent['type']

    def passage(ast_type, parent):
        if ast_type == "Program":
            child = parent.get('body')
            current = 0
            while current < len(child):
                block = child[current]
                current += 1
                ast_type = block.get('type')
                passage(ast_type, block)
        elif ast_type == "Operation":
            operation_value = parent.get('value')
            child = parent.get('params')
            if len(child) == 2:
                left_parameter = child[0]
                right_parameter = child[1]
                table(left_parameter, operation_value, right_parameter)
        elif ast_type == "Function":
            current = 0
            operation_value = parent.get('value')
            child = parent.get('params')
            while current < len(child):
                table(child[current], operation_value)
                current += 1
        elif ast_type == "Cycle":
            current = 0
            operation_value = parent.get('value')
            child = parent.get('params')
            while current < len(child):
                table(child[current], operation_value)
                current += 1
        elif ast_type == "СonditionalOperator":
            current = 0
            operation_value = parent.get('value')
            child = parent.get('params')
            while current < len(child):
                table(child[current], operation_value)
                current += 1

    passage(ast_type, parent)


intro = ".intel_syntax noprefix\n.global main\n.LC0:\n.string \"%d\\n\"\nmain:\npush rbp\n" \
        "mov rbp, rsp\n"
displace = 4
asm_container = ""
def assembler(ast):
    parent = ast
    ast_type = parent['type']

    def asm_passage(childs):
        global asm_container
        global displace
        global intro

        for node in childs:
            if node['type'] == "Operation":
                operation_value = node.get('value')
                parameters = node.get('params')

                if operation_value == "=":
                    if len(parameters) == 2:
                        left_parameter = parameters[0]
                        right_parameter = parameters[1]

                        if left_parameter['type'] == "Operand":
                            for temp in childs:
                                if temp['type'] == "Operation" and temp['value'] == "=":
                                    if temp['params'][0]['type'] == "Operand" and temp['params'][0]['value'] == left_parameter['value']:
                                        if "displace" in temp['params'][0]:
                                            print("I'm here")
                                            break
                                        else:
                                            print("i'm here 3")
                                            if right_parameter['type'] != "Operation":
                                                asm_container += f"mov DWORD PTR [rbp-{displace}], "
                                            left_parameter["displace"] = displace
                                            displace += 4
                                            break
                        print(node)
                        if right_parameter['type'] == "Number":
                            asm_container += f"{right_parameter['value']}" + "\n"
                        elif right_parameter['type'] == "Operand":
                            for temp in childs:
                                if temp['type'] == "Operation" and temp['value'] == "=":
                                    if temp['params'][0]['type'] == "Operand" and temp['params'][0]['value'] == right_parameter['value']:
                                        print(temp['params'][0]['value'])
                                        asm_container += f"mov edx, DWORD PTR [rbp-{temp['params'][0]['displace']}]\n"
                                        break

                            for temp in childs:
                                if temp['type'] == "Operation" and temp['value'] == "=":
                                    if temp['params'][0]['type'] == "Operand" and temp['params'][0]['value'] == left_parameter['value']:
                                        asm_container += f"mov DWORD PTR [rbp-{temp['params'][0]['displace']}], edx\n"
                                        break
                        elif right_parameter['type'] == "Operation":
                            if right_parameter['value'] == "+":
                                left = right_parameter['params'][0]
                                right = right_parameter['params'][1]

                                if left['type'] == "Operand":
                                    for temp in childs:
                                        if temp['type'] == "Operation" and temp['value'] == "=":
                                            if temp['params'][0]['type'] == "Operand" and temp['params'][0]['value'] == left['value']:
                                                asm_container += f"mov edx, DWORD PTR [rbp-{temp['params'][0]['displace']}]\n"
                                                break
                                elif left['type'] == "Number":
                                    asm_container += f"mov edx, {left['value']}\n"

                                if right['type'] == "Operand":
                                    for temp in childs:
                                        if temp['type'] == "Operation" and temp['value'] == "=":
                                            if temp['params'][0]['type'] == "Operand" and temp['params'][0]['value'] == right['value']:
                                                asm_container += f"add edx, DWORD PTR [rbp-{temp['params'][0]['displace']}]\nmov DWORD PTR [rbp-{left_parameter['displace']}], edx\n"
                                                break
                                elif right['type'] == "Number":
                                    asm_container += f"add edx, {right['value']}\nmov DWORD PTR [rbp-{left_parameter['displace']}], edx\n"
                            elif right_parameter['value'] == "-":
                                left = right_parameter['params'][0]
                                right = right_parameter['params'][1]

                                if left['type'] == "Operand":
                                    for temp in childs:
                                        if temp['type'] == "Operation" and temp['value'] == "=":
                                            if temp['params'][0]['type'] == "Operand" and temp['params'][0]['value'] == \
                                                    left['value']:
                                                asm_container += f"mov edx, DWORD PTR [rbp-{temp['params'][0]['displace']}]\n"
                                                break
                                elif left['type'] == "Number":
                                    asm_container += f"mov edx, {left['value']}\n"

                                if right['type'] == "Operand":
                                    for temp in childs:
                                        if temp['type'] == "Operation" and temp['value'] == "=":
                                            if temp['params'][0]['type'] == "Operand" and temp['params'][0]['value'] == \
                                                    right['value']:
                                                asm_container += f"sub edx, DWORD PTR [rbp-{temp['params'][0]['displace']}]\nmov DWORD PTR [rbp-{left_parameter['displace']}], edx\n"
                                                break
                                elif right['type'] == "Number":
                                    asm_container += f"sub edx, {right['value']}\nmov DWORD PTR [rbp-{left_parameter['displace']}], edx\n"
                            elif right_parameter['value'] == "*":
                                left = right_parameter['params'][0]
                                right = right_parameter['params'][1]

                                if left['type'] == "Operand":
                                    for temp in childs:
                                        if temp['type'] == "Operation" and temp['value'] == "=":
                                            if temp['params'][0]['type'] == "Operand" and temp['params'][0]['value'] == \
                                                    left['value']:
                                                asm_container += f"mov edx, DWORD PTR [rbp-{temp['params'][0]['displace']}]\n"
                                                break
                                elif left['type'] == "Number":
                                    asm_container += f"mov edx, {left['value']}\n"

                                if right['type'] == "Operand":
                                    for temp in childs:
                                        if temp['type'] == "Operation" and temp['value'] == "=":
                                            if temp['params'][0]['type'] == "Operand" and temp['params'][0]['value'] == \
                                                    right['value']:
                                                asm_container += f"imul edx, DWORD PTR [rbp-{temp['params'][0]['displace']}]\nmov DWORD PTR [rbp-{left_parameter['displace']}], edx\n"
                                                break
                                elif right['type'] == "Number":
                                    asm_container += f"imul edx, {right['value']}\nmov DWORD PTR [rbp-{left_parameter['displace']}], edx\n"
                            elif right_parameter['value'] == "/":
                                left = right_parameter['params'][0]
                                right = right_parameter['params'][1]

                                if left['type'] == "Operand":
                                    for temp in childs:
                                        if temp['type'] == "Operation" and temp['value'] == "=":
                                            if temp['params'][0]['type'] == "Operand" and temp['params'][0]['value'] == \
                                                    left['value']:
                                                asm_container += f"mov eax, DWORD PTR [rbp-{temp['params'][0]['displace']}]\ncdq\n"
                                                break
                                elif left['type'] == "Number":
                                    asm_container += f"mov eax, {left['value']}\ncdq\n"

                                if right['type'] == "Operand":
                                    for temp in childs:
                                        if temp['type'] == "Operation" and temp['value'] == "=":
                                            if temp['params'][0]['type'] == "Operand" and temp['params'][0]['value'] == \
                                                    right['value']:
                                                asm_container += f"mov ebx, DWORD PTR [rbp-{temp['params'][0]['displace']}]\nidiv ebx\nmov DWORD PTR [rbp-{left_parameter['displace']}], eax\n"
                                                break
                                elif right['type'] == "Number":
                                    asm_container += f"mov ebx, {right['value']}\nidiv ebx\nmov DWORD PTR [rbp-{left_parameter['displace']}], eax\n"
                            elif right_parameter['value'] == "%":
                                left = right_parameter['params'][0]
                                right = right_parameter['params'][1]

                                if left['type'] == "Operand":
                                    for temp in childs:
                                        if temp['type'] == "Operation" and temp['value'] == "=":
                                            if temp['params'][0]['type'] == "Operand" and temp['params'][0]['value'] == \
                                                    left['value']:
                                                asm_container += f"mov eax, DWORD PTR [rbp-{temp['params'][0]['displace']}]\ncdq\n"
                                                break
                                elif left['type'] == "Number":
                                    asm_container += f"mov eax, {left['value']}\ncdq\n"

                                if right['type'] == "Operand":
                                    for temp in childs:
                                        if temp['type'] == "Operation" and temp['value'] == "=":
                                            if temp['params'][0]['type'] == "Operand" and temp['params'][0]['value'] == \
                                                    right['value']:
                                                asm_container += f"mov ebx, DWORD PTR [rbp-{temp['params'][0]['displace']}]\nidiv ebx\nmov DWORD PTR [rbp-{left_parameter['displace']}], edx\n"
                                                break
                                elif right['type'] == "Number":
                                    asm_container += f"mov ebx, {right['value']}\nidiv ebx\nmov DWORD PTR [rbp-{left_parameter['displace']}], edx\n"

            elif node['type'] == "Function":
                operation_value = node.get('value')
                parameters = node.get('params')

                if operation_value == "print":
                    for param in parameters:
                        if param['type'] == "Operand":
                            for temp in childs:
                                if temp['type'] == "Operation" and temp['value'] == "=":
                                    for i in range(2):
                                        if temp['params'][i]['type'] == "Operand" and temp['params'][i]['value'] == param['value']:
                                            asm_container += f"mov edx, DWORD PTR [rbp-{temp['params'][i]['displace']}]\nmov esi, edx\nmov edi, OFFSET FLAT:.LC0\nmov edx, 0\ncall printf\nmov edx, 0\n"
                                            break
                        elif param['type'] == "StringLiteral":
                            intro = ".intel_syntax noprefix\n.global main\n.LC0:\n.string \"%d\\n\"\n" + f".OUTPUT:\n.string \"{param['value']}\\n\"\n" + "main:\npush rbp\nmov rbp, rsp\n"
                            asm_container += f"mov edi, OFFSET FLAT:.OUTPUT\nmov eax, 0\ncall printf\nmov eax, 0\n"
        print(intro + asm_container + "nop\npop rbp \nret\n")

    if ast_type == "Program":
        child = parent.get('body')
        asm_passage(child)


# Считывание аргументов из терминала
def arg_input():
    arg = argparse.ArgumentParser()
    arg.add_argument('name', type=str, nargs='?')
    arg.add_argument('fname', type=str, nargs='?')

    return arg


if __name__ == '__main__':
    argument = arg_input()
    option = argument.parse_args(sys.argv[1:])
    file_name = argument.parse_args(sys.argv[2:])

    display = False
    Lexer = None

    if option.name == "/dump-tokens":  # Лексер
        file = open(file_name.name, 'r')
        display = True
        try:
            for location, line in enumerate(file, 1):
                Lexer = lexer(line, location, display)
        finally:
            file.close()
    elif option.name == "/dump-ast":  # Парсер
        file = open(file_name.name, 'r')
        try:
            for location, line in enumerate(file, 1):
                Lexer = lexer(line, location, display)
            display = True
            Parser = parser(Lexer, display)
        finally:
            file.close()
    elif option.name == "/dump-asm":
        file = open(file_name.name, 'r')
        try:
            for location, line in enumerate(file, 1):
                Lexer = lexer(line, location, display)
            Parser = parser(Lexer, display)
            assembler(Parser)

            asm_out = intro + asm_container + "nop\npop rbp \nret\n"

            with open("asm_output.s", "w") as file_output:
                file_output.write(asm_out)
                file_output.close()
            os.system(f"gcc -Wall -no-pie asm_output.s -o program")
        finally:
            file.close()

    if file_name.name:
        pass
    else:
        print("Файл не указан.")
        sys.exit()
