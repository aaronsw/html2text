import html2text

# See https://github.com/Alir3z4/html2text/issues/163 for more information.


def test_newline_on_multiple_calls():
    h = html2text.HTML2Text()
    html = "<p>test</p>"
    md1 = h.handle(html)
    md2 = h.handle(html)
    md3 = h.handle(html)
    assert md1 == md2 == md3
