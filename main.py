#! python3
from datetime import datetime
import sys
import lib.util as util
arg = {
    'url': None,
    'deep': 0,
    'parent': False,
    'download': False,
    'database': './crawler_{$Y}{$M}{$D}{$H}{$m}{$s}.db'
}
constant = {
}


def generate_constant():
    date = datetime.now()
    constant.update({
        'Y': util.format_width(date.year, 4),
        'M': util.format_width(date.month, 2),
        'D': util.format_width(date.day, 2),
        'H': util.format_width(date.hour, 2),
        'm': util.format_width(date.minute, 2),
        's': util.format_width(date.second, 2)
    })


def check_args():
    if arg['url'] is None:
        raise Exception("url is required!")


if __name__ == '__main__':
    generate_constant()
    try:
        arg.update(util.parse_args(sys.argv, constant, 'url'))
        check_args()
    except Exception as e:
        print(e)
        exit(-1)
    print(arg)
    print(constant)
