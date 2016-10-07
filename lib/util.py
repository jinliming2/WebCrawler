#! python3
import re
str_constant = re.compile(r'\{\$(\w+)\}')


def parse_args(args, constant, default_key=''):
    """
    :param args: {List[String]}
    :param constant: {Dictionary}
    :param default_key: {String}
    :return: {Dictionary}
    """
    arg = {}
    key = default_key
    for i in range(1, len(args)):
        if args[i][:2] == '--':
            key = args[i][2:]
            arg[key] = True
        elif args[i][0] == '-' or args[i][0] == '/':
            key = args[i][1:]
            arg[key] = True
        else:
            if key == '':
                raise Exception('Unsolved argument: ' + args[i])
            rep = str_constant.findall(args[i])
            for r in rep:
                if r in constant:
                    args[i] = args[i].replace('{$' + r + '}', str(constant[r]))
            arg[key] = args[i]
    return arg


def format_width(string, width, character='0'):
    """
    :param string: {String|Number}
    :param width: {Number}
    :param character: {Char}
    :return: {String}
    """
    string = str(string)
    if width <= len(string):
        return string
    l = []
    for i in range(width):
        l.append(character)
    l.append(string)
    return ''.join(l)[-width:]
