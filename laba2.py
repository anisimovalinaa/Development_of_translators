import re
import laba1


#определяет приоритет x
def priority(priorities, x):
    for pr in priorities:
        if x in priorities[pr]:
            return pr
    return None


# обработка описания переменных
def description_var(block, outstr):
    i = 0
    count_var = 0
    while i <= len(block) - 1:
        while i <= len(block) - 1 and block[i] != ':':
            if block[i] not in [',', ';', '\n']:
                outstr += block[i] + ' '
                count_var += 1
            elif block[i] == '\n':
                outstr += r'\n '
            i += 1
        if i >= len(block):
            continue
        i += 1
        if block[i] == 'array':
            i += 1
            z = 0
            while block[i] != ']':
                if block[i].isdigit():
                    outstr += block[i] + ' '
                elif block[i] == ',':
                    outstr += '.. '
                    z += 1
                i += 1
            i += 2
            outstr += '.. ' + str(z + 2) + 'АЭМ ' + str(count_var) + ' ' + block[i] + ' '
            count_var = 0
        else:
            outstr += str(count_var) + ' ' + block[i] + ' '
            count_var = 0
        i += 1
    return outstr


# перевод в обратную польскую запись
def rpn(text):
    priorities = {0: ['(', '[', 'if', 'while', 'for'], 1: [')', ']', ',', ';', 'then', 'else', 'do', 'to'],
                  2: [':=', 'goto'],
                  3: ['or'], 4: ['and'], 5: ['not'], 6: ['<', '>', '<=', '>=', '=', '<>'], 7: ['+', '-'], 8: ['*', '/'],
                  9: ['program', 'procedure', 'function', 'end', 'begin']}

    l = [el for el in re.split(r'(\-?\d+\.\d+|\-?\d+|\w+|;|\'.*\'|:=|<=|>=|-|\+|\*|/|(|)|<|>|<>|=|[|]|,)', text)
         if el not in ['', ' ', None]]
    l = list(map(str.lower, l))

    count_aem = num_proc = level_proc = 1
    count_func = count_if = count_begin = count_end = count_while = count_for = 0
    check_if = check_fun = False
    stack = []
    out_str = ''
    i = 0
    while i != len(l):
        p = priority(priorities, l[i])
        if p == 9:
            if l[i] == 'end':
                count_end += 1
                if check_if:
                    if l[i + 1] == ';':
                        while not re.match(r'IF М\d+', stack[-1]):
                            out_str += stack.pop() + ' '
                        out_str += re.search(r'М\d+', stack[-1]).group(0) + ': '
                        stack.pop()
                        check_if = False
                        count_if -= 1
                        i += 1
                    else:
                        pass
                elif count_while > 0:
                    while not re.match(r'WHILE П\d+', stack[-1]):
                        out_str += stack.pop() + ' '
                    out_str += re.search(r'П\d+', stack[-1]).group(0) + ': '
                    stack.pop()
                    count_while -= 1
                    i += 1
                elif count_for > 0:
                    while not re.match(r'FOR ЦФ\d+', stack[-1]):
                        out_str += stack.pop() + ' '
                    out_str += re.search(r'ЦФ\d+', stack[-1]).group(0) + ': '
                    stack.pop()
                    count_for = 0
                    i += 1
                else:
                    stack.append(l[i])
                    if count_begin == count_end:
                        num_proc += 1
                        level_proc = 1
            elif l[i] == 'begin':
                count_begin += 1
            else:
                if l[i] == 'function':
                    check_fun = True
                if count_end != count_begin:
                    level_proc += 1
                    stack.append('PROC ' + str(num_proc) + ' ' + str(level_proc))
                else:
                    stack.append('PROC ' + str(num_proc) + ' ' + str(level_proc))
        elif l[i] == '.':
            stack.pop()
            out_str += 'КП '
        elif l[i] == "\n":
            out_str += r'\n '
        elif l[i] == ';':
            if len(stack) > 0 and re.match(r'PROC+', stack[-1]):
                dig = re.findall(r'\d+', stack[-1])
                out_str += str(dig[0]) + str(dig[1]) + 'НП '
                stack.pop()
            elif len(stack) > 0 and stack[-1] == 'end':
                stack.pop()
                out_str += 'КП '
            elif check_if:
                while not re.match(r'IF М\d+', stack[-1]):
                    out_str += stack.pop() + ' '
            elif count_while > 0:
                while not re.match(r'WHILE П\d+', stack[-1]):
                    out_str += stack.pop() + ' '
            elif count_for > 0:
                while not re.match(r'FOR ЦФ\d+', stack[-1]):
                    out_str += stack.pop() + ' '
            else:
                while len(stack) != 0:
                    out_str += stack.pop() + ' '
        elif l[i] == ',':
            while not re.match(r'\d+АЭМ', stack[-1]) and not re.match(r'\d+Ф', stack[-1]):
                out_str += stack.pop() + ' '
            if re.match(r'\d+АЭМ', stack[-1]):
                stack.pop()
                count_aem += 1
                stack.append(str(count_aem) + 'АЭМ')
            if re.match(r'\d+Ф', stack[-1]):
                stack.pop()
                count_func += 1
                stack.append(str(count_func) + 'Ф')
        elif l[i] == 'var':
            block = []
            i += 1
            while l[i] not in ['begin', 'procedure', 'function']:
                block.append(l[i])
                i += 1
            i -= 1
            out_str = description_var(block, out_str)
            out_str += str(num_proc) + ' ' + str(level_proc) + ' КО '
        elif p is None:
            out_str += l[i] + ' '
            if check_fun and l[i + 1] == '(':
                i += 2
                desc = []
                while l[i] != ')':
                    desc.append(l[i])
                    i += 1
                out_str = description_var(desc, out_str)
                i -= 1
                check_fun = False
        elif l[i] == 'goto':
            out_str += l[i + 1] + ' БП '
            i += 2
        elif l[i] == 'while' or l[i] == 'for':
            stack.append(l[i].upper())
        elif l[i] == 'to' or l[i] == 'downto':
            while stack[-1] != 'FOR':
                out_str += stack.pop() + ' ' + l[i] + ' '
        elif l[i] == 'do':
            while stack[-1] not in ['WHILE', 'FOR']:
                out_str += stack.pop() + ' '
            if stack[-1] == 'WHILE':
                count_while += 1
                stack[-1] += ' П' + str(count_while)
                out_str += 'П' + str(count_while) + ' '
            else:
                count_for += 1
                stack[-1] += ' ЦФ' + str(count_for)
                out_str += 'ЦФ' + str(count_for) + ' '
        elif l[i] == 'else':
            while not re.match(r'IF М\d+', stack[-1]):
                out_str += stack.pop() + ' '
            stack.pop()
            count_if += 1
            stack.append('IF М' + str(count_if))
            out_str += 'М' + str(count_if) + ' БП М' + str(count_if - 1) + ': '
        elif l[i] == '[':
            count_aem += 1
            stack.append(str(count_aem) + 'АЭМ')
        elif l[i] == ']':
            while not re.match(r'\d+АЭМ', stack[-1]):
                out_str += stack.pop() + ' '
            out_str += stack.pop() + ' '
            count_aem = 1
        elif l[i] == '(':
            if re.match(r'\w+', l[i - 1]):
                count_func += 1
                stack.append(str(count_func) + 'Ф')
            else:
                stack.append(l[i])
        elif l[i] == ')':
            if l[i + 1] == ':':
                i += 2
                out_str += '1 ' + l[i] + ' КО '
            else:
                while not re.match(r'\d+Ф', stack[-1]) and stack[-1] != '(':
                    out_str += stack.pop() + ' '
                if re.match(r'\d+Ф', stack[-1]):
                    out_str += str(count_func + 1) + 'Ф '
                    count_func = 0
                stack.pop()
        elif l[i] == 'if':
            stack.append(l[i].upper())
            check_if = True
        elif l[i] == 'then':
            while stack[-1] != 'IF':
                out_str += stack.pop() + ' '
            count_if += 1
            stack[-1] += ' М' + str(count_if)
            out_str += 'М' + str(count_if) + ' УПЛ '
        elif len(stack) == 0 or priority(priorities, stack[-1]) is None or priority(priorities, stack[-1]) < p:
            stack.append(l[i])
        else:
            while len(stack) != 0 and priority(priorities, stack[-1]) >= p:
                out_str += stack.pop() + ' '
            stack.append(l[i])
        i += 1

    while len(stack) != 0:
        out_str += stack.pop() + ' '

    return out_str


def translate_to_symbol(rpn_str, dictionary):
    out_str = ''
    rpn_str = [el for el in re.split(r'(\s|\'.{, 20}\')', rpn_str) if el not in ['', ' ']]

    for el in rpn_str:
        code = laba1.find_code(el, dictionary)
        if code == '':
            out_str += el + ' '
        else:
            out_str += code + ' '

    return out_str


def main():
    text = open('file_pascal.txt', encoding='UTF-8').read().lower()
    dictionary = laba1.create_dict(text)
    rpn_str = rpn(text)
    out_seq = translate_to_symbol(rpn_str, dictionary)

    for el in dictionary.items():
        print(el)
    print(rpn_str)
    print(out_seq)

    out = open('reverse_Polish_notation.txt', 'w')
    out.write(out_seq)


if __name__ == '__main__':
    main()
