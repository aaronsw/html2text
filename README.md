# html2text

[![Build Status](https://secure.travis-ci.org/Alir3z4/html2text.png)](http://travis-ci.org/Alir3z4/html2text)
[![Coverage Status](https://coveralls.io/repos/Alir3z4/html2text/badge.png)](https://coveralls.io/r/Alir3z4/html2text)
[![Downloads](https://pypip.in/d/html2text/badge.png)](https://pypi.python.org/pypi/html2text/)
[![Version](https://pypip.in/v/html2text/badge.png)](https://pypi.python.org/pypi/html2text/)
[![Egg?](https://pypip.in/egg/html2text/badge.png)](https://pypi.python.org/pypi/html2text/)
[![Wheel?](https://pypip.in/wheel/html2text/badge.png)](https://pypi.python.org/pypi/html2text/)
[![Format](https://pypip.in/format/html2text/badge.png)](https://pypi.python.org/pypi/html2text/)
[![License](https://pypip.in/license/html2text/badge.png)](https://pypi.python.org/pypi/html2text/)


html2text is a Python script that converts a page of HTML into clean, easy-to-read plain ASCII text. Better yet, that ASCII also happens to be valid Markdown (a text-to-HTML format).


Usage: `html2text [(filename|url) [encoding]]`


| Option                                                 | Description
|--------------------------------------------------------|---------------------------------------------------
| `--version`                                            | Show program's version number and exit
| `-h`, `--help`                                         | Show this help message and exit
| `--ignore-links`                                       | Don't include any formatting for links
|`--protect-links`                                       | Protect links from line breaks surrounding them "+" with angle brackets
|`--ignore-images`                                       | Don't include any formatting for images
|`--images-to-alt`                                       | Discard image data, only keep alt text
|`--images-with-size`                                    | Write image tags with height and width attrs as raw html to retain dimensions
|`-g`, `--google-doc`                                    | Convert an html-exported Google Document
|`-d`, `--dash-unordered-list`                           | Use a dash rather than a star for unordered list items
|`-b` `BODY_WIDTH`, `--body-width`=`BODY_WIDTH`          | Number of characters per output line, `0` for no wrap
|`-i` `LIST_INDENT`, `--google-list-indent`=`LIST_INDENT`| Number of pixels Google indents nested lists
|`-s`, `--hide-strikethrough`                            | Hide strike-through text. only relevent when `-g` is specified as well
|`--escape-all`                                          | Escape all special characters.  Output is less readable, but avoids corner case formatting issues.
| `--bypass-tables`                                      | Format tables in HTML rather than Markdown syntax.
| `--single-line-break`                                  | Use a single line break after a block element rather than two.
| `--reference-links`                                    | Use reference links instead of links to create markdown
| `--mark-code`                                          | Mark preformatted and code blocks with [code]...[/code]



Or you can use it from within `Python`:

```
>>> import html2text
>>>
>>> print(html2text.html2text("<p><strong>Zed's</strong> dead baby, <em>Zed's</em> dead.</p>"))
**Zed's** dead baby, _Zed's_ dead.

```


Or with some configuration options:
```
>>> import html2text
>>>
>>> h = html2text.HTML2Text()
>>> # Ignore converting links from HTML
>>> h.ignore_links = True
>>> print h.handle("<p>Hello, <a href='http://earth.google.com/'>world</a>!")
Hello, world!

>>> print(h.handle("<p>Hello, <a href='http://earth.google.com/'>world</a>!"))

Hello, world!

>>> # Don't Ignore links anymore, I like links
>>> h.ignore_links = False
>>> print(h.handle("<p>Hello, <a href='http://earth.google.com/'>world</a>!"))
Hello, [world](http://earth.google.com/)!

```

*Originally written by Aaron Swartz. This code is distributed under the GPLv3.*


## How to install

`html2text` is available on pypi
https://pypi.python.org/pypi/html2text

```
$ pip install html2text
```


## How to run unit tests

    PYTHONPATH=$PYTHONPATH:. coverage run --source=html2text setup.py test -v

To see the coverage results:
    
    coverage combine
    coverage html

then open the `./htmlcov/index.html` file in your browser.

## Documentation

Documentation lives [here](docs/index.md)
