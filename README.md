# [html2text](http://www.aaronsw.com/2002/html2text/)

html2text is a Python script that converts a page of HTML into clean, easy-to-read plain ASCII text. Better yet, that ASCII also happens to be valid Markdown (a text-to-HTML format).

Usage: `html2text.py [(filename|url) [encoding]]`

    Options:
      --version             show program's version number and exit
      -h, --help            show this help message and exit
      --ignore-links        don't include any formatting for links
      --ignore-images       don't include any formatting for images
      -g, --google-doc      convert an html-exported Google Document
      -d, --dash-unordered-list
                            use a dash rather than a star for unordered list items
      -b BODY_WIDTH, --body-width=BODY_WIDTH
                            number of characters per output line, 0 for no wrap
      -i LIST_INDENT, --google-list-indent=LIST_INDENT
                            number of pixels Google indents nested lists
      -s, --hide-strikethrough
                            hide strike-through text. only relevent when -g is
                            specified as well

Or you can use it from within Python:

    import html2text
    print html2text.html2text("<p>Hello, world.</p>")

Or with some configuration options:

    import html2text
    h = html2text.HTML2Text()
    h.ignore_links = True
    print h.handle("<p>Hello, <a href='http://earth.google.com/'>world</a>!")

_Originally written by Aaron Swartz. This code is distributed under the GPLv3._


## How to do a release

1. Update the version in `html2text.py`
2. Update the version in `setup.py`
3. Run `python setup.py sdist upload`

## How to run unit tests

    cd test/
    python run_tests.py

[![Build Status](https://secure.travis-ci.org/aaronsw/html2text.png)](http://travis-ci.org/aaronsw/html2text)
