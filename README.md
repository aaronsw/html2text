# html2text

[![Build Status](https://secure.travis-ci.org/Alir3z4/html2text.png)](https://travis-ci.org/Alir3z4/html2text)
[![Coverage Status](https://coveralls.io/repos/Alir3z4/html2text/badge.png)](https://coveralls.io/r/Alir3z4/html2text)
[![Downloads](http://badge.kloud51.com/pypi/d/html2text.png)](https://pypi.org/project/html2text/)
[![Version](http://badge.kloud51.com/pypi/v/html2text.png)](https://pypi.org/project/html2text/)
[![Wheel?](http://badge.kloud51.com/pypi/wheel/html2text.png)](https://pypi.org/project/html2text/)
[![Format](http://badge.kloud51.com/pypi/format/html2text.png)](https://pypi.org/project/html2text/)
[![License](http://badge.kloud51.com/pypi/license/html2text.png)](https://pypi.org/project/html2text/)


html2text is a Python script that converts a page of HTML into clean, easy-to-read plain ASCII text. Better yet, that ASCII also happens to be valid Markdown (a text-to-HTML format).


Usage: `html2text [filename [encoding]]`

| Option                                                 | Description
|--------------------------------------------------------|---------------------------------------------------
| `--version`                                            | Show program's version number and exit
| `-h`, `--help`                                         | Show this help message and exit
| `--ignore-links`                                       | Don't include any formatting for links
|`--escape-all`                                          | Escape all special characters.  Output is less readable, but avoids corner case formatting issues.
| `--reference-links`                                    | Use reference links instead of links to create markdown
| `--mark-code`                                          | Mark preformatted and code blocks with [code]...[/code]

For a complete list of options see the [docs](https://github.com/Alir3z4/html2text/blob/master/docs/usage.md)


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
>>> print h.handle("<p>Hello, <a href='https://www.google.com/earth/'>world</a>!")
Hello, world!

>>> print(h.handle("<p>Hello, <a href='https://www.google.com/earth/'>world</a>!"))

Hello, world!

>>> # Don't Ignore links anymore, I like links
>>> h.ignore_links = False
>>> print(h.handle("<p>Hello, <a href='https://www.google.com/earth/'>world</a>!"))
Hello, [world](https://www.google.com/earth/)!

```

*Originally written by Aaron Swartz. This code is distributed under the GPLv3.*


## How to install

`html2text` is available on pypi
https://pypi.org/project/html2text/

```
$ pip install html2text
```


## How to run unit tests

    tox

To see the coverage results:

    coverage html

then open the `./htmlcov/index.html` file in your browser.

## Documentation

Documentation lives [here](https://github.com/Alir3z4/html2text/blob/master/docs/usage.md)
