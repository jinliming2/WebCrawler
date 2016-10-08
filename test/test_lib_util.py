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


if __name__ == '__main__':
    unittest.main()
