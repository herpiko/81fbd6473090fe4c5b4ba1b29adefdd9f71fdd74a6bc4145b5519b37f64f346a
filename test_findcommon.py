#!/usr/bin/env python

import imp
import unittest
import os

path = os.path.abspath(__file__)
dir_path = os.path.dirname(path)
findcommon_module_path =  os.path.join(os.path.expanduser(dir_path), "findcommon.py")

findcommon = imp.load_source("findcommon", findcommon_module_path)

class FindCommonTestCase(unittest.TestCase):

    def testFindCommon(self):
        assert findcommon.find_common(os.path.join(os.path.expanduser(dir_path), "test_assets/original_case")) == "abcdef 4"

    def testFindCommonBinary(self):
        assert findcommon.find_common(os.path.join(os.path.expanduser(dir_path), "test_assets/binary_case")) == "ad8d9a23fdfbf399464a5471a47860f906702d5d2883d8718626c47ce59a4dcc 5"

    def testFindCommonMixed(self):
        assert findcommon.find_common(os.path.join(os.path.expanduser(dir_path), "test_assets/mixed_case")) == "abcdef 6"

    def testFindCommonUsrBin(self):
        # I'm sure there are common files in our /usr/bin
        assert int(findcommon.find_common("/usr/bin").split(" ")[1]) > 1
