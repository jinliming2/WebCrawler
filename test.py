#! python3
import unittest
from test.test_lib_util import TestLibUtil


def suite():
    test_suite = unittest.TestSuite()
    test_suite.addTest(unittest.makeSuite(TestLibUtil))
    return test_suite

unittest.main(defaultTest='suite')
