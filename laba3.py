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
    sequence = 'C1 1 1 НП R1 I1 N1 N2 O2 2АЭМ 1 W5 R1 I2 I3 I4 I5 I6 5 W5 R1 1 1 КО R1 W8 ' \
               'C2 2Ф R1 I2 N1 O3 W10 N2 ЦФ1 R1 W12 I1 I2 2АЭМ 2Ф R1 ЦФ1: R1 I4 N1 O3 R1 I5 N1 O3 R1'
    sequence = [el for el in re.split(r'(\'.*\'|\s)', sequence) if el not in ['', ' ']]
    print(sequence)
    stack = []
    output = ''
    replace = {'integer': 'int', 'real': 'float', 'double': 'double', 'string': 'char', 'boolean': 'bool',
               'writeln': 'printf', 'readln': 'scanf', ':=': '='}
    count_tab = 0

    i = 0
    while i != len(sequence):
        name = find_name(sequence[i], dictionary)
        if name == '\\n':
            if output[-1] not in ['{', '}', '\n']:
                output += ';\n'
            elif len(stack) != 0:
                output += '\t' * count_tab + stack.pop() + ';\n'
            else:
                output += '\n'
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
            output += '\t' * count_tab + replace[name] + '('
        elif sequence[i].isdigit() and (sequence[i + 1] != 'НП' and sequence[i + 2] != 'НП' and sequence[i + 1] != 'КО'
                                        and sequence[i + 2] != 'КО'):
            output += '\t' * count_tab + find_name(sequence[i + 1], dictionary) + ' '
            dig = int(sequence[i])
            temps = []
            while dig != 0:
                temps.append(stack.pop())
                dig -= 1
            output += ', '.join(temps[::-1])
            i += 1
        elif re.match(r'.*НП', sequence[i]):
                output += 'int main(void) {'
                stack.pop()
                count_tab += 1
        elif re.match(r'.*Ф$', sequence[i]):
            count = int(sequence[i][0]) - 1
            mass = []
            while count != 0:
                mass.append(stack.pop())
                count -= 1
            output += ', '.join(mass[::-1]) + ')'
        elif re.match(r'.*АЭМ', sequence[i]):
            count = int(sequence[i][0])
            mass = []
            while count != 0:
                mass.append(stack.pop())
                count -= 1
            mass = mass[1] + '[' + mass[0] + ']'
            stack.append(mass)
        elif re.match(r'ЦФ.*:', sequence[i]):
            count_tab -= 1
            output += '\t' * count_tab + '}'
        elif re.match(r'ЦФ.*', sequence[i]):
            condition = stack.pop().split()
            temp = condition[0].split('=')[0]
            beg = int(condition[0].split('=')[1]) - 1
            iter = '++' if condition[1] == 'to' else '--'
            condition[0] = temp + '=' + str(beg)
            output += '\t' * count_tab + 'for(' + condition[0] + '; ' + temp + ' < ' + condition[2] + '; ' + temp + \
                      iter + ') {'
            count_tab += 1
        elif len(stack) > 0 and re.match(r'.*to.*', stack[-1]):
            stack[-1] += ' ' + name
        elif name != None:
            stack.append(name)
        i += 1

    while len(stack) != 0:
        output += stack.pop()
    # output += ';\n'

    print(output)
    out_file = open('file_c.txt', 'w')
    out_file.write(output)
    out_file.close()


if __name__ == '__main__':
    text = open('file_pascal.txt', encoding='UTF-8').read().lower()
    dictionary = laba1.create_dict(text)
    main(dictionary)
