import re


# проверяет содержится ли value в классе лексем class_lex
def check(class_lex, dictionary, value):
    if value not in dictionary[class_lex]:
        dictionary[class_lex][value] = len(dictionary[class_lex]) + 1


# производит считывание всех переменных в программе
def read_temps_var(description, dictionary):
    var_array = list(
                map(lambda x: x.strip(), description.split(';'))
                )[0:-1:]

    dictionary['R'][';'], dictionary['O'][':'] = len(dictionary['R']) + 1, len(dictionary['O']) + 1
    for array_el in var_array:
        temps, type_var = map(lambda x: x.strip(), array_el.split(':'))
        temps = list(map(lambda x: x.strip(), temps.split(',')))
        if len(temps) > 1:
            check('R', dictionary, ',')
        for el in temps:
            check('I', dictionary, el)
        arr_type_var = type_var.split()
        if len(arr_type_var) == 1:
            check('W', dictionary, type_var)
        else:
            check('W', dictionary, arr_type_var[0])
            check('W', dictionary, arr_type_var[2])
            check('W', dictionary, arr_type_var[3])
            check('W', dictionary, array_el[0])
            list_const = re.findall(r'\d+', arr_type_var[1])
            check('R', dictionary, '[')
            check('R', dictionary, ']')
            check('N', dictionary, list_const[0])
            check('N', dictionary, list_const[1])


# разделяет строку по операторам
def split_operations(current_str, list_operations, dictionary):
    for operation in list_operations:
        str_split = current_str.split(operation)
        if len(str_split) > 1:
            check('O', dictionary, operation)
            if str_split[0] not in dictionary['I'] and str_split[0] != '':
                if str_split[0].isdigit():
                    check('N', dictionary, str_split[0])
                else:
                    split_operations(str_split[0], list_operations, dictionary)
            if str_split[1] not in dictionary['I'] and str_split[1] != '':
                if str_split[1].isdigit():
                    check('N', dictionary, str_split[1])
                else:
                    split_operations(str_split[1], list_operations, dictionary)
            break


# создание словаря классов лексем
def create_dict(text):
    d = {'W': {}, 'I': {}, 'O': {}, 'R': {}, 'N': {}, 'C': {}}

    name_blocks = ['program', 'function', 'procedure']
    spec_words = ['begin', 'end', 'write', 'goto', 'writeln', 'readln', 'read', 'for', 'to', 'do', 'if', 'then', 'else', 'while']
    operators = [':=', '+', '-', '*', '/', 'mod', 'div', '=', '<', '>', '<=', '>=']

    current_str = str()
    i = 0
    while i != len(text):
        if text[i] == '\'':
            current_str = text[i]
            i += 1
            while text[i] != '\'':
                current_str += text[i]
                i += 1
            current_str += '\''
            check('C', d, current_str)
            current_str = ''
        elif text[i] not in [' ', '\n', '\t', '(', ')', ';', ',', '.']:
            current_str = current_str + text[i]
        elif current_str not in [' ', ''] or text[i] in ['(', ')', ';', ',']:
            if text[i] in ['(', ')', ';', ',', '.']:
                check('R', d, text[i])
            if current_str in d['I']:
                pass
            elif current_str in name_blocks:
                check('W', d, current_str)
                name_str = ''
                i += 1
                while text[i] != '\n':
                    name_str += text[i]
                    i += 1
                check('C', d, name_str)
            elif current_str == 'var':
                check('W', d, current_str)
                ind = text[i::].find('begin') + i
                description_temps = text[i:ind:].strip()

                read_temps_var(description_temps, d)
                i = ind - 1
            elif current_str in spec_words:
                check('W', d, current_str)
            elif current_str in operators:
                check('O', d, current_str)
            elif current_str.isdigit():
                check('N', d, current_str)
            else:
                split_operations(current_str, operators + [':'], d)
            current_str = ''
        i += 1
    return d


# поиск кода лексемы
def find_code(lexeme, dictionary):
    class_lex = num = str()
    for key in dictionary.keys():
        if lexeme in dictionary[key]:
            class_lex = key
            num = str(dictionary[key][lexeme])
    return class_lex + num


def to_share(string, dictionary):
    separators = [',', ':', ';', '(', ')', '+', '-', '/', '*', '=', '<', '>', '.', '[', ']']
    word = str()
    seq = []
    if (len(string) > 0 and string[0] == '\'') or string in [':=', '<=', '>=', '<>', 'mod', 'div']:
        code = find_code(string, dictionary)
        seq.append(code)
    else:
        for i in range(len(string)):
            if string[i] not in separators:
                word += string[i]
                if i + 1 == len(string):
                    code = find_code(word, dictionary)
                    seq += [code]
            else:
                code_sep = find_code(string[i], dictionary)
                if word != '':
                    code = find_code(word, dictionary)
                    seq += [code, code_sep]
                else:
                    seq += [code_sep]
                word = ''
    return seq


def split(text):
    l = []
    word = str()
    check = False
    i = 0
    while i != len(text):
        if not check:
            if text[i] == '\'':
                l.append(word)
                word = text[i]
                check = True
            elif text[i:i+2] in [':=', '<=', '>=', '<>']:
                l.append(word)
                l.append(text[i:i+2])
                word = ''
                i += 1
            elif text[i:i+3] in ['div', 'mod']:
                l.append(word)
                l.append(text[i:i+3])
                word = ''
                i += 2
            elif text[i] != ' ':
                word += text[i]
                if i + 1 == len(text):
                    l.append(word)
            elif word != '':
                l.append(word)
                word = ''
        else:
            word += text[i]
            if text[i] == '\'':
                l.append(word)
                word = ''
                check = False
        i += 1
    return l


# формирование выходной последовательности
def create_output_sequence(text, dictionary):
    text = text.split('\n')
    sequence = []
    for text_str in text:
        seq = []
        text_str = split(text_str)
        for lex in text_str:
            seq += to_share(lex, dictionary)
        sequence.append(seq)
    # for seq in sequence:
    #     print(seq)
    return sequence


# вывод словаря в файл
def output_table(class_lit):
    text = str()
    if class_lit == 'W':
        text += 'Специальные слова' + '\n'
    elif class_lit == 'I':
        text += 'Идентификаторы' + '\n'
    elif class_lit == 'O':
        text += 'Операции' + '\n'
    elif class_lit == 'R':
        text += 'Разделители' + '\n'
    elif class_lit == 'N':
        text += 'Числовые константы' + '\n'
    else:
        text += 'Символьные константы' + '\n'
    text += 'Лексема\tКод'
    return text


def main():
    file_pascal = open('file_pascal.txt', encoding='UTF-8')
    text = file_pascal.read()
    file_pascal.close()

    dictionary = create_dict(text)

    file_dict = open('dictionary.txt', 'w')
    for key in dictionary.keys():
        hat = output_table(key)
        file_dict.write(hat + '\n')
        for couple in dictionary[key].items():
            file_dict.write(couple[0] + '\t' + str(couple[1]) + '\n')
        file_dict.write('\n')

    file_dict.close()


    for key in dictionary.keys():
        print(key, dictionary[key])

    sequence = create_output_sequence(text, dictionary)

    out = open('output_sequence.txt', 'w')

    for seq in sequence:
        for word in seq:
            out.write(word + ' ')
        out.write('\n')
    out.close()


if __name__ == '__main__':
    main()
