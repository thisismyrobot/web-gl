""" Basic doc-tests for Web-GL
"""
import doctest

doctest.testfile("tests.txt", verbose=True, optionflags=doctest.ELLIPSIS)

#hack to pause after running script - on windoze testfile causes a loss of focus for some reason...
raw_input("Focus this console and press Enter to close")