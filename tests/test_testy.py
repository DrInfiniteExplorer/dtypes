import unittest
import doctest
import dtypes
import dtypes.structify
import dtypes.fwd
import dtypes.voidy
import dtypes.typedefs


def load_tests(loader, tests, ignore):
    tests.addTests(doctest.DocTestSuite(dtypes          , optionflags = doctest.ELLIPSIS))
    tests.addTests(doctest.DocTestSuite(dtypes.structify, optionflags = doctest.ELLIPSIS))
    tests.addTests(doctest.DocTestSuite(dtypes.fwd      , optionflags = doctest.ELLIPSIS))
    tests.addTests(doctest.DocTestSuite(dtypes.voidy    , optionflags = doctest.ELLIPSIS))
    tests.addTests(doctest.DocTestSuite(dtypes.typedefs , optionflags = doctest.ELLIPSIS))
    return tests
