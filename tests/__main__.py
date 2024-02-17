import sys
import pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / 'src'))

import unittest
import importlib


if __name__ == '__main__':
    excludes = []

    is_test_case = lambda v: isinstance(v, type) and issubclass(v, unittest.TestCase)

    py_items = pathlib.Path(__file__).resolve().parent.glob('test_*.py')
    testmodules = [importlib.import_module(str(i.stem)) for i in py_items if i.is_file()]
    testcases = [a for m in testmodules for a in [getattr(m, i) for i in dir(m)] if is_test_case(a)]

    suite = unittest.TestSuite([unittest.makeSuite(t) for t in set(testcases)])
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)
