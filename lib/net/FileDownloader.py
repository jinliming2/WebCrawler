#! python3
import os
import re
import requests
header_filename = re.compile(r'filename="?([^ ";]+?)"?')
header_ext_name = re.compile(r'/?[^/]+$')


def download(url, path='./download/', filename=None, header=None, cookie=None):
    header = header if header is not None else {}
    cookie = cookie if cookie is not None else {}
    path = path if path[-1] == '/' or path[-1] == '\\' else path + '/'
    try:
        r = requests.get(url, headers=header, cookies=cookie, stream=True)
        if filename is None:
            if 'Content-Disposition' in r.headers:
                _filename = header_filename.search(r.headers['Content-Disposition'])
                if _filename:
                    filename = _filename.group(0)
            if filename is None:
                import lib.util as util
                filename = util.url_filename(url)
                if filename is None:
                    filename = 'unnamed_file'
        ext_index = filename.rfind('.')
        file_name = filename
        ext_name = ''
        if ext_index >= 0:
            ext_name = filename[ext_index:]
            file_name = filename[:ext_index]
        elif 'Content-Type' in r.headers:
            _ext_name = header_ext_name.search(r.headers['Content-Type'])
            if _ext_name:
                ext_name = '.' + _ext_name.group(0)
                filename += ext_name
        if os.path.exists(path + filename):
            i = 2
            while os.path.exists('%s%s (%d)%s' % (path, file_name, i, ext_name)):
                i += 1
            filename = '%s (%d)%s' % (file_name, i, ext_name)
        with open(path + filename, 'wb') as file:
            for chunk in r.iter_content(10):
                file.write(chunk)
    except Exception as e:
        print(e)
        raise
