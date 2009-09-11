""" Doc-tests for Web-GL
"""
import doctest

tests = (
    "tests/pages.txt",
    "tests/interfaces.txt"
    )

for test in tests:
    doctest.testfile(test, optionflags=doctest.ELLIPSIS)

#"pauses" after finish - in a cross-platform manner - pressing enter will close the open script.
raw_input("If no output above, everything passed!\nFocus this console and press Enter to close")