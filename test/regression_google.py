#!/usr/bin/env python

__version__ = "0.1"

import sys
sys.path.append('..')

import optparse
import html2text

# Wrap long lines at position. 0 for no wrapping. (Requires Python 2.3.)
BODY_WIDTH = 78

# Number of pixels Google indents nested lists
GOOGLE_LIST_INDENT = 36

if __name__ == "__main__":
    p = optparse.OptionParser('%prog [(filename|url) [encoding]]',
                              version='%prog ' + __version__)
    p.add_option("-g", "--google-doc", action="store_true", dest="google_doc",
        default=False, help="convert an html-exported Google Document")
    p.add_option("-d", "--dash-unordered-list", action="store_true", dest="ul_style_dash",
        default=False, help="use a dash rather than a star for unordered list items")
    p.add_option("-b", "--body-width", dest="body_width", action="store", type="int",
        default=78, help="number of characters per output line, 0 for no wrap")
    p.add_option("-i", "--google-list-indent", dest="list_indent", action="store", type="int",
        default=GOOGLE_LIST_INDENT, help="number of pixels Google indents nested lists")
    p.add_option("-s", "--hide-strikethrough", action="store_true", dest="hide_strikethrough",
        default=False, help="hide strike-through text. only relevent when -g is specified as well")
    (options, args) = p.parse_args()

    # handle options
    if options.ul_style_dash:
        options.ul_item_mark = '-'
    else:
        options.ul_item_mark = '*'

    html2text.BODY_WIDTH = options.body_width
    html2text.GOOGLE_LIST_INDENT = options.list_indent
    html2text.options = options

    # process input
    if len(args) > 0:
        file_ = args[0]
        encoding = None
        if len(args) == 2:
            encoding = args[1]
        if len(args) > 2:
            p.error('Too many arguments')

        data = open(file_, 'rb').read()
        if encoding is None:
            try:
                from chardet import detect
            except ImportError:
                detect = lambda x: {'encoding': 'utf-8'}
            encoding = detect(data)['encoding']
        data = data.decode(encoding)
    else:
        data = sys.stdin.read()
    html2text.wrapwrite(html2text.html2text(data, ''))
