#! python3
import re
str_constant = re.compile(r'\{\$(\w+)\}')
filename = re.compile(r'(?<!/)((/(\w+(\.[a-zA-Z0-9]+)?))|(=(\w+\.[a-zA-Z0-9]+)))')


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


def args_constant(args, constant):
    """
    :param args: {Dictionary}
    :param constant: {Dictionary}
    """
    for key in args:
        if isinstance(args[key], str):
            rep = str_constant.findall(args[key])
            for r in rep:
                if r in constant:
                    args[key] = args[key].replace('{$' + r + '}', str(constant[r]))


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


def url_filename(url):
    """
    :param url: {String}
    :return: {String}
    """
    rep = filename.findall(url)
    if len(rep) > 0:
        return {
            'filename': rep[-1][2] if rep[-1][2] != '' else rep[-1][5],
            'path': '/'.join([path[2] if path[2] != '' else path[5] for path in rep[:-1]]) + '/'
        }
    else:
        return None


def url_get_deep(url, current='/'):
    """
    :param url: {String}
    :param current: {String}
    :return: {Dictionary}
    """
    s = url.find('?')
    if s >= 0:
        url = url[:s]
    s = url.find('#')
    if s >= 0:
        url = url[:s]

    if url == '':
        return None

    same_origin = False

    if url[:2] == '//':
        if current[:7].lower() == 'http://' or current[:8].lower() == 'https://':
            s = current.find('//')
            url = current[:s] + url
        else:
            url = 'http:' + url

    if url[0] != '/' and url[:7].lower() != 'http://' and url[:8].lower() != 'https://':
        s = current.rfind('/') + 1
        current = current[:s]
        url = current + url
        same_origin = True

    if url[0] == '/' or current[0] == '/':
        same_origin = True
    if url[:7].lower() == 'http://' or url[:8].lower() == 'https://':
        s = url.find('/', 9)
        if s == -1:
            if url == current:
                same_origin = True
            return {
                'origin': same_origin,
                'deep': 1
            }
        if url[:s] == current[:s]:
            same_origin = True
        url = url[s:]

    if url == '/':
        return {
            'origin': same_origin,
            'deep': 1
        }

    if url[-1] == '/':
        url = url[:-1]

    deep = 0
    s = url.find('/')
    while s >= 0:
        deep += 1
        s = url.find('/', s + 1)

    return {
        'origin': same_origin,
        'deep': deep
    }


def make_url(url, current):
    if url[:7].lower() == 'http://' or url[:8].lower() == 'https://':
        return url
    if url[0] != '/':
        s = current.rfind('/') + 1
        current = current[:s]
        return current + url
    if url[:2] == '//':
        if current[:7].lower() == 'http://' or current[:8].lower() == 'https://':
            s = current.find('//')
            return current[:s] + url
        else:
            return 'http:' + url
    current += '/'
    s = current.find('/', 9)
    return current[:s] + url
