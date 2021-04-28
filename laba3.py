import laba1
import laba2
import re


# поиск записи лексемы по таблице
def find_name(code, dictionary):
    class_lex = code[0]
    if class_lex in dictionary:
        for item in dictionary[class_lex].items():
            if item[1] == int(code[1:]):
                return item[0]
    return None


# генерация кода на языке си
def generation_code(dictionary, sequence):
    # sequence = "I2 N3 O3 П1 R1 I1 I1 I2 O4 O2 R1 I2 I2 N4 O4 O2 R1 П1:"
    sequence = [el for el in re.split(r'(\'.*\'|\s)', sequence) if el not in ['', ' ']]
    stack = []
    output = ''
    replace = {'integer': 'int', 'real': 'float', 'double': 'double', 'string': 'char', 'boolean': 'bool',
               'writeln': 'printf', 'write': 'printf', 'readln': 'scanf', 'read': 'scanf', ':=': '=', '=': '=='}
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
            operator = replace[name] if name in replace else name
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
            type = find_name(sequence[i + 1], dictionary)
            output += '\t' * count_tab + replace[type] + ' '
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
        elif re.match(r'М.*:', sequence[i]) or re.match(r'ЦФ.*:', sequence[i]) or re.match(r'П.*:', sequence[i]) or \
                sequence[i] == 'КП':
            count_tab -= 1
            output += '\t' * count_tab + '}'
        elif re.match(r'М.*', sequence[i]):
            output += '\t' * count_tab + 'if (' + stack.pop() + ') '
        elif re.match(r'П.*', sequence[i]):
            output += '\t' * count_tab + 'while (' + stack.pop() + ') {'
            count_tab += 1
        elif sequence[i] == 'УПЛ':
            output += '{'
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

    return output


if __name__ == '__main__':
    text = open('file_pascal.txt', encoding='UTF-8').read().lower()
    dictionary = laba1.create_dict(text)
    rpn = laba2.rpn(text)
    sequence = laba2.translate_to_symbol(rpn, dictionary)
    code_c = generation_code(dictionary, sequence)
    out_file = open('file_c.txt', 'w')
    out_file.write(code_c)
    out_file.close()
