import html2text

# See https://github.com/Alir3z4/html2text/issues/13 for more information.

INSTR = "miow "


def test_same_string():
    h2t = html2text.HTML2Text()
    result = h2t.handle(INSTR)
    # Now, we shouldn't get leak of the previous run to the new one.
    assert h2t.handle(INSTR) == result


def test_empty_string():
    h2t = html2text.HTML2Text()
    h2t.handle(INSTR)
    # And even less when the input is empty.
    assert h2t.handle("") == "\n\n"
