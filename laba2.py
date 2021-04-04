import re


def priority(priorities, x):
    for pr in priorities:
        if x in priorities[pr]:
            return pr
    return None


def check_if(s):
    if s.find('if') == 0 and len(s) > 2:
        return True
    else:
        return False


def description_var(block, outstr):
    i = 0
    count_var = 0
    while i != len(block) - 1:
        while block[i] != ':':
            if block[i] not in [',', ';']:
                outstr += block[i] + ' '
                count_var += 1
            i += 1
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
            outstr += '.. ' + str(z + 2) + ' АЭМ ' + block[i] + ' '
        else:
            outstr += str(count_var) + ' ' + block[i] + ' '
            count_var = 0
        i += 1
    return outstr


def main():
    priorities = {0: ['(', '[', 'if', 'while', 'for'], 1: [')', ']', ',', ';', 'then', 'else', 'do', 'to'], 2: [':=', 'goto'],
                  3: ['or'], 4: ['and'], 5: ['not'], 6: ['<', '>', '<=', '>=', '=', '<>'], 7: ['+', '-'], 8: ['*', '/'],
                  9: ['program', 'procedure', 'function', 'end', 'begin']}
    # examp = 'x := 3 + 4'
    examp = open('file_pascal.txt').read()
    # examp = 'x / y / (5 * z) + 10 * (97 + 12*2)'
    l = [el for el in re.split(r'(\.\.|\-?d+\.\d+|\-?\d+|\w+|;|:=|-|\+|\*|/|(|)|<|>|>=|<=|<>|=|[|]|,)', examp)
         if el not in ['', ' ', None, "\n"]]
    l = list(map(str.lower, l))

    print(l)
    count_aem = num_proc = level_proc = 1
    count_func = count_if = count_begin = count_end = count_while = count_for = 0
    check_if = False
    stack = []
    out_str = ''
    i = 0
    while i != len(l):
        p = priority(priorities, l[i])
        if p == 9:
            if l[i] == 'end':
                count_end += 1
                if check_if:
                    if l[i+1] == ';':
                        while not re.match(r'IF М\d+', stack[-1]):
                            out_str += stack.pop() + ' '
                        out_str += re.search(r'М\d+', stack[-1]).group(0) + ': '
                        stack.pop()
                        check_if = False
                        count_if = 0
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
                    count_for -= 1
                    i += 1
                else:
                    stack.append(l[i])
                    if count_begin == count_end:
                        num_proc += 1
                        level_proc = 1
            elif l[i] == 'begin':
                count_begin += 1
            else:
                if count_end != count_begin:
                    level_proc += 1
                    stack.append('PROC ' + str(num_proc) + ' ' + str(level_proc))
                else:
                    stack.append('PROC ' + str(num_proc) + ' ' + str(level_proc))
        elif l[i] == '.':
            stack.pop()
            out_str += 'КП '
        elif l[i] == ';':
            if re.match(r'PROC+', stack[-1]):
                dig = re.findall(r'\d+', stack[-1])
                out_str += str(dig[0]) + ' ' + str(dig[1]) + ' НП '
                stack.pop()
            elif stack[-1] == 'end':
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
        elif l[i] == 'goto':
            out_str += l[i+1] + ' БП '
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
            while not re.match(r'\d+Ф', stack[-1]) and stack[-1] != '(':
                out_str += stack.pop() + ' '
            if re.match(r'\d+Ф', stack[-1]):
                out_str += str(count_func+1) + 'Ф '
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

    print(out_str)


if __name__ == '__main__':
    main()
