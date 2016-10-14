#! python3
from datetime import datetime
from sqlite3 import IntegrityError
import sys
import lib.util as util
import lib.db_helper as db
from lib.ThreadPool import ThreadPool
from lib.net.GetHTML import GetHTML
from lib.net.FileDownloader import download
arg = {
    'url': None,
    'unsafe': False,
    'deep': 5,
    'thread': 10,
    'parent': False,
    'timeout': 30,
    'download': False,
    'database': './crawler_{$Y}{$M}{$D}{$H}{$m}{$s}.db'
}
constant = {
}
start_deep = 0
max_deep = 0
pool = None
conn = None


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


def url_check(url, current):
    if url == '':
        return False
    a = url.find(':')
    if a >= 0:
        a = url[:a]
        if a != 'http' and a != 'https':
            return False
    deep = util.url_get_deep(url, current)
    if deep is None:
        return False
    if not deep['origin']:
        return False
    if deep['deep'] > max_deep:
        return False
    if deep['deep'] < start_deep and not arg['parent']:
        return False
    return True


def process_image(url, current):
    if not url_check(url, current):
        return
    url = util.make_url(url, current)
    print("Processing Image: " + url)
    try:
        db.insert_image(conn, url)
        if arg['download']:
            download(url, ssl=not arg['unsafe'])
    except IntegrityError:
        return


def runner_analyse_html(url, current):
    if not url_check(url, current):
        return
    url = util.make_url(url, current)
    if db.find_url(conn, url) is not None:
        return
    print("Processing URL: " + url)
    try:
        db.insert_url(conn, url)
    except IntegrityError:
        return
    html = GetHTML.get(url, ssl=not arg['unsafe'])
    links = GetHTML.get_links(html)
    list(map(lambda l: pool.add(runner_analyse_html, l, url), links['link']))
    list(map(lambda l: process_image(l, url), links['image']))
    list(map(lambda l: process_image(l, url), links['css_image']))

if __name__ == '__main__':
    generate_constant()
    try:
        arg.update(util.parse_args(sys.argv, constant, 'url'))
        util.args_constant(arg, constant)
        check_args()
        arg['deep'] = int(arg['deep'])
        arg['thread'] = int(arg['thread'])
        arg['timeout'] = int(arg['timeout'])
    except Exception as e:
        print(e)
        exit(-1)
    # Start
    # Database
    conn = db.connect(arg['database'])
    db.create_table(conn)

    start_deep = util.url_get_deep(arg['url'])['deep']
    max_deep = start_deep + arg['deep']
    pool = ThreadPool(arg['thread'], arg['timeout'], True)
    pool.add(runner_analyse_html, arg['url'], '/')
    pool.join()
    db.disconnect(conn)
