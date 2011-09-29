#!/usr/bin/env python
import sys
sys.path.append('..')

import html2text

if __name__ == "__main__":
    # process input
    args = sys.argv[1:]
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
