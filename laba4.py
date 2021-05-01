import laba1
import sys

program_text = open("file_pascal.txt").read().lower()
dictionary = laba1.create_dict(program_text)
program_text = laba1.create_output_sequence(program_text, dictionary)
program_text = [item for sublist in program_text for item in sublist]
current_symbol = object
i = 0


def find_name():
    if i > len(program_text): error()
    class_lex = current_symbol[0]
    if class_lex in dictionary:
        for item in dictionary[class_lex].items():
            if item[1] == int(current_symbol[1:]):
                return item[0]
    return None


def error():
    print('Ошибка')
    sys.exit(0)


def scan():
    global current_symbol, i
    if i >= len(program_text): error()
    current_symbol = program_text[i]
    i += 1


def const():
    return True if (current_symbol[0] in ['C', 'N']) else False


def program():
    lex = find_name()
    if lex != 'program': error()
    scan()
    if not const(): error()
    scan()
    if find_name() != ';': error()
    scan()
    declare()
    if find_name() != 'begin': error()
    scan()
    text()
    if find_name() != 'end': error()
    scan()
    if find_name() != '.': error()


def text():
    while find_name() != 'end':
        sep_oper()


def sep_oper():
    if find_name() == 'if': if_oper()
    elif find_name() == 'for': for_oper()
    elif find_name() == 'while': while_oper()
    elif find_name() in ['write', 'writeln', 'read', 'readln']: func_oper()
    else:
        if not ident(): error()
        scan()
        if find_name() == ':=':
            scan()
            expression()
            scan()
        else:
            error()


def while_oper():
    scan()
    condition()
    if find_name() != 'do': error()
    else:
        scan()
        if find_name() != 'begin': error()
        scan()
        text()
        if find_name() != 'end': error()
        scan()
        if find_name() != ';': error()
        scan()


def func_oper():
    scan()
    if find_name() != '(': error()
    scan()
    if find_name() == ')':
        scan()
        if find_name() != ';': error()
        scan()
        return
    expression()
    while find_name() == ',':
        scan()
        expression()
    if find_name() != ')': error()
    scan()
    if find_name() != ';': error()
    scan()


def for_oper():
    scan()
    if not ident(): error()
    scan()
    if find_name() == ':=':
        scan()
        expression()
    else:
        error()
    if find_name() not in ['to', 'downto']: error()
    scan()
    expression()
    if find_name() != 'do': error()
    scan()
    if find_name() != 'begin': error()
    scan()
    text()
    if find_name() != 'end': error()
    scan()
    if find_name() != ';': error()
    scan()


def if_oper():
    scan()
    condition()
    if find_name() != 'then': error()
    else:
        scan()
        if find_name() != 'begin': error()
        scan()
        text()
        if find_name() != 'end': error()
        scan()
        if find_name() != ';': error()
        scan()


def condition():
    expression()
    if find_name() not in ['<', '>', '<>', '<=', '>=', '==']: error()
    scan()
    expression()


def expression():
    term()
    while find_name() in ['+', '-'] and find_name() not in [';']:
        scan()
        term()


def term():
    factor()
    while find_name() in ['*', '/'] and find_name() not in [';']:
        scan()
        factor()


def factor():
    if find_name() == '(':
        scan()
        expression()
        if find_name() != ')': error()
        else:
            scan()
    else:
        argument()


def argument():
    if not const() and not ident(): error()
    scan()
    if find_name() == '[':
        scan()
        argument()
        if find_name() != ']': error()
        scan()


def ident():
    return True if current_symbol[0] == 'I' else False


def declare():
    if find_name() != 'var': error()
    scan()
    while i < len(program_text) and find_name() != 'begin':
        if not ident(): error()
        scan()
        while find_name() == ',':
            scan()
            if not ident(): error()
            scan()
        if find_name() != ':': error()
        scan()
        if find_name() == 'array':
            scan()
            declare_array()
        if find_name() not in ['integer', 'real', 'string', 'byte', 'boolean']: error()
        scan()
        if find_name() != ';': error()
        scan()


def declare_array():
    if find_name() != '[': error()
    scan()
    if not const(): error()
    scan()
    if find_name() != '..': error()
    scan()
    if not const(): error()
    scan()
    if find_name() != ']': error()
    scan()
    if find_name() != 'of': error()
    scan()


if __name__ == '__main__':
    scan()
    program()
