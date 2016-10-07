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

    def test_parse_args(self):
        result = util.parse_args(
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
        )
        answer = {
            'url': '1',
            'a': '2',
            'b': '3',
            'c': '4',
            'download': True,
            'e': True,
            'database': './crawler_20161007144900.db'
        }
        assert [k for k in set(answer) if k not in result or result[k] != answer[k]] == []

    def test_format_width(self):
        assert util.format_width(1, 2) == "01"
        assert util.format_width(12, 2) == "12"
        assert util.format_width(2016, 2) == "2016"
        assert util.format_width(0, 3) == "000"
        assert util.format_width(66, 3) == "066"
        assert util.format_width(789, 3) == "789"
        assert util.format_width('', 3) == "000"


if __name__ == '__main__':
    unittest.main()
