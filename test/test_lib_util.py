#! python3
import unittest

if __name__ == '__main__':
    import sys

    sys.path.append("..")
import lib.util as util


class TestLibUtil(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    @staticmethod
    def dictCompare(question, answer=None):
        if answer is None:
            return question is None
        return [k for k in set(answer) if k not in question or question[k] != answer[k]] == []

    def test_parse_args(self):
        assert self.dictCompare(util.parse_args(
            [
                'F:/Git/WebCrawler/main.py',
                '1',
                '-a', '2',
                '--b', '3',
                '/c', '4',
                '-download',
                '-e',
                '-database', './crawler_{$Y}{$M}{$D}{$H}{$m}{$s}.db'
            ], {
                'Y': 2016,
                'M': 10,
                'D': '07',
                'H': 14,
                'm': 49,
                's': '00'
            }, 'url'
        ), {
            'url': '1',
            'a': '2',
            'b': '3',
            'c': '4',
            'download': True,
            'e': True,
            'database': './crawler_20161007144900.db'
        })

    def test_args_constant(self):
        arg = {
            'url': '1',
            'a': '2',
            'b': '3',
            'c': '4',
            'download': True,
            'e': True,
            'database': './crawler_{$Y}{$M}{$D}{$H}{$m}{$s}.db'
        }
        util.args_constant(arg, {
            'Y': 2016,
            'M': 10,
            'D': '07',
            'H': 14,
            'm': 49,
            's': '00'
        })
        assert self.dictCompare(arg, {
            'url': '1',
            'a': '2',
            'b': '3',
            'c': '4',
            'download': True,
            'e': True,
            'database': './crawler_20161007144900.db'
        })

    def test_format_width(self):
        assert util.format_width(1, 2) == "01"
        assert util.format_width(12, 2) == "12"
        assert util.format_width(2016, 2) == "2016"
        assert util.format_width(0, 3) == "000"
        assert util.format_width(66, 3) == "066"
        assert util.format_width(789, 3) == "789"
        assert util.format_width('', 3) == "000"

    def test_url_filename(self):
        assert self.dictCompare(util.url_filename('http://www.example.com/file/path/test.php'), {
            'filename': 'test.php',
            'path': 'file/path/'
        })
        assert self.dictCompare(util.url_filename('http://www.example.com/file/path/test'), {
            'filename': 'test',
            'path': 'file/path/'
        })
        assert self.dictCompare(util.url_filename('http://www.example.com/file'), {
            'filename': 'file',
            'path': '/'
        })
        assert self.dictCompare(util.url_filename('http://www.example.com/'))
        assert self.dictCompare(util.url_filename('http://www.example.com'))
        assert self.dictCompare(util.url_filename('http://www.example.com/download.php?filename=a.jpg'), {
            'filename': 'a.jpg',
            'path': 'download.php/'
        })

    def test_url_get_deep(self):
        assert self.dictCompare(util.url_get_deep('/test', 'https://www.example.com'), {
            'deep': 1,
            'origin': True
        })
        assert self.dictCompare(util.url_get_deep('/test/456', 'https://www.example.com/'), {
            'deep': 2,
            'origin': True
        })
        assert self.dictCompare(util.url_get_deep('/test?test/test#test', 'https://www.example.com'), {
            'deep': 1,
            'origin': True
        })
        assert self.dictCompare(util.url_get_deep('/test/test#test', 'https://www.example.com'), {
            'deep': 2,
            'origin': True
        })
        assert self.dictCompare(util.url_get_deep('test2/test3', 'https://www.example.com/test1'), {
            'deep': 2,
            'origin': True
        })
        assert self.dictCompare(util.url_get_deep('/', 'https://www.example.com/test/test'), {
            'deep': 1,
            'origin': True
        })
        assert self.dictCompare(util.url_get_deep('https://www.example.com/test/test2', 'https://www.example.com'), {
            'deep': 2,
            'origin': True
        })
        assert self.dictCompare(util.url_get_deep('https://www.example.com/', 'https://www.example.com'), {
            'deep': 1,
            'origin': True
        })
        assert self.dictCompare(util.url_get_deep('https://www.example.com', 'https://www.example.com'), {
            'deep': 1,
            'origin': True
        })
        assert self.dictCompare(util.url_get_deep('https://www.example2.com/test/test2', 'https://www.example.com'), {
            'deep': 2,
            'origin': False
        })
        assert self.dictCompare(util.url_get_deep('https://www.example2.com/test/test2/', 'https://www.example.com'), {
            'deep': 2,
            'origin': False
        })
        assert self.dictCompare(util.url_get_deep('https://www.example2.com/', 'https://www.example.com'), {
            'deep': 1,
            'origin': False
        })
        assert self.dictCompare(util.url_get_deep('https://www.example2.com', 'https://www.example.com'), {
            'deep': 1,
            'origin': False
        })
        assert self.dictCompare(util.url_get_deep('?a=1&b=2#3', 'https://www.example.com'))
        assert self.dictCompare(util.url_get_deep('#3', 'https://www.example.com'))
        assert self.dictCompare(util.url_get_deep('//www.example.com/test/test2', 'https://www.example.com'), {
            'deep': 2,
            'origin': True
        })
        assert self.dictCompare(util.url_get_deep('//www.example.com/', 'https://www.example.com'), {
            'deep': 1,
            'origin': True
        })
        assert self.dictCompare(util.url_get_deep('//www.example.com', 'https://www.example.com'), {
            'deep': 1,
            'origin': True
        })
        assert self.dictCompare(util.url_get_deep('//www.example2.com/test/test2', 'https://www.example.com'), {
            'deep': 2,
            'origin': False
        })
        assert self.dictCompare(util.url_get_deep('//www.example2.com/', 'https://www.example.com'), {
            'deep': 1,
            'origin': False
        })
        assert self.dictCompare(util.url_get_deep('//www.example2.com', 'https://www.example.com'), {
            'deep': 1,
            'origin': False
        })

    def test_make_url(self):
        assert util.make_url('/test', 'https://www.example.com') == 'https://www.example.com/test'
        assert util.make_url('/test/456', 'https://www.example.com/') == 'https://www.example.com/test/456'
        assert util.make_url('/test?test/test#test',
                             'https://www.example.com') == 'https://www.example.com/test?test/test#test'
        assert util.make_url('test2/test3', 'https://www.example.com/test1') == 'https://www.example.com/test2/test3'
        assert util.make_url('/', 'https://www.example.com/test/test') == 'https://www.example.com/'
        assert util.make_url('https://www.example.com/test/test2',
                             'https://www.example.com') == 'https://www.example.com/test/test2'
        assert util.make_url('https://www.example.com/', 'https://www.example.com') == 'https://www.example.com/'
        assert util.make_url('https://www.example.com', 'https://www.example.com') == 'https://www.example.com'
        assert util.make_url('https://www.example2.com/test/test2',
                             'https://www.example.com') == 'https://www.example2.com/test/test2'
        assert util.make_url('https://www.example2.com/', 'https://www.example.com') == 'https://www.example2.com/'
        assert util.make_url('https://www.example2.com', 'https://www.example.com') == 'https://www.example2.com'
        assert util.make_url('//www.example.com/test/test2',
                             'https://www.example.com') == 'https://www.example.com/test/test2'
        assert util.make_url('//www.example.com/', 'https://www.example.com') == 'https://www.example.com/'
        assert util.make_url('//www.example.com', 'https://www.example.com') == 'https://www.example.com'
        assert util.make_url('//www.example2.com/test/test2',
                             'https://www.example.com') == 'https://www.example2.com/test/test2'
        assert util.make_url('//www.example2.com/', 'https://www.example.com') == 'https://www.example2.com/'
        assert util.make_url('//www.example2.com', 'https://www.example.com') == 'https://www.example2.com'
        assert util.make_url('//www.example.com/test/test2',
                             'http://www.example.com') == 'http://www.example.com/test/test2'
        assert util.make_url('//www.example.com/', 'http://www.example.com') == 'http://www.example.com/'
        assert util.make_url('//www.example.com', 'http://www.example.com') == 'http://www.example.com'
        assert util.make_url('//www.example2.com/test/test2',
                             'http://www.example.com') == 'http://www.example2.com/test/test2'
        assert util.make_url('//www.example2.com/', 'http://www.example.com') == 'http://www.example2.com/'
        assert util.make_url('//www.example2.com', 'http://www.example.com') == 'http://www.example2.com'


if __name__ == '__main__':
    unittest.main()
