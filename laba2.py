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


def main():
    priorities = {0: ['(', '[', 'if'], 1: [')', ']', ',', 'then', 'else'], 2: [':='], 3: ['or'], 4: ['and'], 5: ['not'],
                  6: ['<', '>', '<=', '>=', '=', '<>'], 7: ['+', '-'], 8: ['*', '/']}
    # examp = 'x := 3 + 4'
    examp = 'if x=5 then x := x+1'
    # examp = 'x / y / (5 * z) + 10 * (97 + 12*2)'
    l = [el for el in re.split(r'(\d+\.\d+|\d+|\w+||:=|-|\+|\*|/|(|)|<|>|>=|<=|<>|=|[|]|,)', examp)
         if el not in ['', ' ', None]]

    print(l)
    m = 0
    count_aem = 1
    count_func = 0
    count_if = 0
    stack = []
    out_str = ''
    for el in enumerate(l):
        p = priority(priorities, el[1])
        if el[1] == ',':
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
        elif p is None:
            out_str += el[1] + ' '
        elif el[1] == '[':
            count_aem += 1
            stack.append(str(count_aem) + 'АЭМ')
        elif el[1] == ']':
            while not re.match(r'\d+АЭМ', stack[-1]):
                out_str += stack.pop() + ' '
            out_str += stack.pop() + ' '
            count_aem = 1
        elif el[1] == '(':
            if re.match(r'\w+', l[el[0] - 1]):
                count_func += 1
                stack.append(str(count_func) + 'Ф')
            else:
                stack.append(el[1])
        elif el[1] == ')':
            while not re.match(r'\d+Ф', stack[-1]) and stack[-1] != '(':
                out_str += stack.pop() + ' '
            if re.match(r'\d+Ф', stack[-1]):
                out_str += str(count_func+1) + 'Ф '
                count_func = 0
            stack.pop()
        elif el[1] == 'then':
            while stack[-1] != 'if':
                out_str += stack.pop() + ' '
            count_if += 1
            stack[-1] += ' М' + str(count_if)
            out_str += 'М' + str(count_if) + ' УПЛ '
        elif len(stack) == 0 or el[1] == 'if' or priority(priorities, stack[-1]) is None or priority(priorities, stack[-1]) < p:
            stack.append(el[1])
        else:
            while len(stack) != 0 and priority(priorities, stack[-1]) >= p:
                out_str += stack.pop() + ' '
            stack.append(el[1])

    while len(stack) != 0:
        out_str += stack.pop() + ' '

    print(out_str)


if __name__ == '__main__':
    main()
