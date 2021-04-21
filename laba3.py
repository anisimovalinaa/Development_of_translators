import laba1
import laba2
import re


def find_name(code, dictionary):
    class_lex = code[0]
    if class_lex in dictionary:
        for item in dictionary[class_lex].items():
            if item[1] == int(code[1:]):
                return item[0]
    return None



def main(dictionary):
    sequence = 'I2 N1 O3 W10 N2 ЦФ1 R1 W12 I1 I2 2АЭМ 2Ф R1 ЦФ1: R1 I4 N1 O3 R1 I5 N1 O3'.split()
    stack = []
    output = ''
    replace = {'integer': 'int', 'real': 'float', 'double': 'double', 'string': 'char', 'boolean': 'bool',
               'writeln': 'printf', 'readln': 'scanf', ':=': '='}

    i = 0
    while i != len(sequence):
        name = find_name(sequence[i], dictionary)
        if name == '\\n':
            while len(stack) != 0:
                if stack[-1] == 'Ф':
                    output += ')'
                    stack.pop()
                else:
                    output += stack.pop()
            output += ';\n'
        elif name == '..':
            size = int(stack.pop()) - int(stack.pop()) + 1
            stack.append(str(size))
        elif sequence[i][0] == 'O':
            operator = replace[name]
            operands = []
            operands.append(stack.pop())
            operands.append(stack.pop())
            stack.append(operator.join(operands[::-1]))
        elif name == 'to':
            stack[-1] += ' ' + name
        elif name in ['writeln', 'readln', 'read', 'write']:
            output += replace[name] + '('
            stack.append('Ф')
        elif sequence[i].isdigit():
            output += '\n\t' + find_name(sequence[i + 1], dictionary) + ' '
            dig = int(sequence[i])
            temps = []
            while dig != 0:
                temps.append(stack.pop())
                dig -= 1
            output += ', '.join(temps[::-1]) + ';'
            i += 1
        elif re.match(r'.*НП', sequence[i]):
                output += 'int main(void) {'
                stack.pop()
        elif re.match(r'.*АЭМ', sequence[i]):
            count = int(sequence[i][0])
            mass = []
            while count != 0:
                mass.append(stack.pop())
                count -= 1
            mass = mass[1] + '[' + mass[0] + ']'
            stack.append(mass)
        elif re.match(r'ЦФ.*:', sequence[i]):
            output += '}'
        elif re.match(r'ЦФ.*', sequence[i]):
            condition = stack.pop().split()
            temp = condition[0].split('=')[0]
            iter = '++' if condition[1] == 'to' else '--'
            output += 'for(' + condition[0] + '; ' + temp + ' < ' + condition[2] + '; ' + temp + iter + ') {'
        elif len(stack) > 0 and re.match(r'.*to.*', stack[-1]):
            stack[-1] += ' ' + name
        elif name != None:
            stack.append(name)
        i += 1

    while len(stack) != 0:
        if stack[-1] == 'Ф':
            output += ')'
            stack.pop()
        else:
            output += stack.pop()
    output += ';\n'

    print(output)
    out_file = open('file_c.txt', 'w')
    out_file.write(output)
    out_file.close()


if __name__ == '__main__':
    text = open('file_pascal.txt', encoding='UTF-8').read().lower()
    dictionary = laba1.create_dict(text)
    main(dictionary)
