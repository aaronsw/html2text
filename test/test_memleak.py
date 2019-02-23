import html2text
import unittest


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
