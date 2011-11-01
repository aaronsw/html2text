# [html2text](http://www.aaronsw.com/2002/html2text/)

html2text is a Python script that converts a page of HTML into clean, easy-to-read plain ASCII text. Better yet, that ASCII also happens to be valid Markdown (a text-to-HTML format).

Usage: `python html2text.py [(filename|url) [encoding]]`

_Originally written by Aaron Swartz. This code is distributed under the GPLv3._


## How to do a release

1. Update the version in `html2text.py`
2. Update the version in `setup.py`
3. Run `python setup.py sdist upload`
