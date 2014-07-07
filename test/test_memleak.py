import sys
if sys.version_info[:2] < (2, 7):
    import unittest2 as unittest
else:
    import unittest
import logging
logging.basicConfig(format='%(levelname)s:%(funcName)s:%(message)s',
                    level=logging.DEBUG)

import html2text


class TestMemleak(unittest.TestCase):
    """
    See https://github.com/Alir3z4/html2text/issues/13 for more
    information on this.
    """

    def setUp(self):
        self.instr = 'miow '

    def test_same_string(self):
        h2t = html2text.HTML2Text()
        result = h2t.handle(self.instr)
        # Now, we shouldn't get leak of the previous run to the new one
        self.assertEqual(h2t.handle(self.instr), result)

    def test_empty_string(self):
        h2t = html2text.HTML2Text()
        h2t.handle(self.instr)
        # And even less when the input is empty
        self.assertEqual(h2t.handle(''), '\n\n')
