#! python3
import unittest


def suite():
    test_suite = unittest.TestSuite()
    return test_suite

unittest.main(defaultTest='suite')
