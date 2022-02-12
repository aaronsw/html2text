Usage
=====

The module is simple enough to use. This tutorial will get you started.

Installing
----------

These are the methods you can get the module installed:-

### PIP

For those who have pip, we got your back.

```
$ pip install html2text
```

### Clone from Git Repository

Clone the repository from https://github.com/Alir3z4/html2text

```
$ git clone --depth 1 https://github.com/Alir3z4/html2text.git
$ python setup.py build
$ python setup.py install
```



Basic Usage
-----------

Once installed the module can be used as follows.

    import html2text
    html = function_to_get_some_html()
    text = html2text.html2text(html)
    print(text)

This converts the provided html to text( Markdown text) with all the
options set to default.

Using Options
--------------

To customize the options provided by the module the usage is as follows:

    import html2text
    text_maker = html2text.HTML2Text()
    text_maker.ignore_links = True
    text_maker.bypass_tables = False
    html = function_to_get_some_html()
    text = text_maker.handle(html)
    print(text)


Available Options
-----------------

All options exist in the config.py file. A list is provided here with
simple indications of their function.


    - UNICODE_SNOB for using unicode
    - ESCAPE_SNOB for escaping every special character
    - LINKS_EACH_PARAGRAPH for putting links after every paragraph
    - BODY_WIDTH for wrapping long lines
    - SKIP_INTERNAL_LINKS to skip #local-anchor things
    - INLINE_LINKS for formatting images and links
    - PROTECT_LINKS protect from line breaks
    - GOOGLE_LIST_INDENT no of pixels to indent nested lists
    - IGNORE_ANCHORS
    - IGNORE_IMAGES
    - IMAGES_AS_HTML always generate HTML tags for images; preserves `height`, `width`, `alt` if possible.
    - IMAGES_TO_ALT
    - IMAGES_WITH_SIZE
    - IGNORE_EMPHASIS
    - BYPASS_TABLES format tables in HTML rather than Markdown
    - IGNORE_TABLES ignore table-related tags (table, th, td, tr) while keeping rows
    - SINGLE_LINE_BREAK to use a single line break rather than two
    - UNIFIABLE is a dictionary which maps unicode abbreviations to ASCII
                values
    - RE_SPACE for finding space-only lines
    - RE_ORDERED_LIST_MATCHER for matching ordered lists in MD
    - RE_UNORDERED_LIST_MATCHER for matching unordered list matcher in MD
    - RE_MD_CHARS_MATCHER for matching Md \,[,],( and )
    - RE_MD_CHARS_MATCHER_ALL for matching `,*,_,{,},[,],(,),#,!
    - RE_MD_DOT_MATCHER for matching lines starting with <space>1.<space>
    - RE_MD_PLUS_MATCHER for matching lines starting with <space>+<space>
    - RE_MD_DASH_MATCHER for matching lines starting with <space>(-)<space>
    - RE_SLASH_CHARS a string of slash escapeable characters
    - RE_MD_BACKSLASH_MATCHER to match \char
    - USE_AUTOMATIC_LINKS to convert <a href='http://xyz'>http://xyz</a> to <http://xyz>
    - MARK_CODE to wrap 'pre' blocks with [code]...[/code] tags
    - WRAP_LINKS to decide if links have to be wrapped during text wrapping (implies INLINE_LINKS = False)
    - WRAP_LIST_ITEMS to decide if list items have to be wrapped during text wrapping
    - WRAP_TABLES to decide if tables have to be wrapped during text wrapping
    - DECODE_ERRORS to handle decoding errors. 'strict', 'ignore', 'replace' are the acceptable values.
    - DEFAULT_IMAGE_ALT takes a string as value and is used whenever an image tag is missing an `alt` value. The default for this is an empty string '' to avoid backward breakage
    - OPEN_QUOTE is the character used to open a quote when replacing the `<q>` tag. It defaults to `"`.
    - CLOSE_QUOTE is the character used to close a quote when replacing the `<q>` tag. It defaults to `"`.

Options that are not in the config.py file:

    - emphasis_mark is the character used when replacing the `<em>` tag. It defaults to `_`.
    - strong_mark is the characer used when replacing the `<strong>` tag. It defaults to `**`.

To alter any option the procedure is to create a parser with
`parser = html2text.HTML2Text()` and to set the option on the parser.
example: `parser.unicode_snob = True` to set the UNICODE_SNOB option.


Command line options
--------------------


| Option                                                 | Description
|--------------------------------------------------------|---------------------------------------------------
| `--version`                                            | Show program version number and exit
| `-h`, `--help`                                         | Show this help message and exit
| `--ignore-links`                                       | Do not include any formatting for links
|`--protect-links`                                       | Protect links from line breaks surrounding them "+" with angle brackets
|`--ignore-images`                                       | Do not include any formatting for images
|`--images-as-html`                                      | Always write image tags as raw html; preserves "height", "width" and "alt" if possible.
|`--images-to-alt`                                       | Discard image data, only keep alt text
|`--images-with-size`                                    | Write image tags with height and width attrs as raw html to retain dimensions
|`-g`, `--google-doc`                                    | Convert an html-exported Google Document
|`-d`, `--dash-unordered-list`                           | Use a dash rather than a star for unordered list items
|`-b` `BODY_WIDTH`, `--body-width`=`BODY_WIDTH`          | Number of characters per output line, `0` for no wrap
|`-i` `LIST_INDENT`, `--google-list-indent`=`LIST_INDENT`| Number of pixels Google indents nested lists
|`-s`, `--hide-strikethrough`                            | Hide strike-through text. only relevant when `-g` is specified as well
|`--escape-all`                                          | Escape all special characters.  Output is less readable, but avoids corner case formatting issues.
| `--bypass-tables`                                      | Format tables in HTML rather than Markdown syntax.
| `--ignore-tables`                                      | Ignore table-related tags (table, th, td, tr) while keeping rows.
| `--single-line-break`                                  | Use a single line break after a block element rather than two.
| `--reference-links`                                    | Use reference links instead of inline links to create markdown
| `--ignore-emphasis`                                    | Ignore all emphasis formatting in the html.
| `-e`, `--asterisk-emphasis`                            | Use asterisk rather than underscore to emphasize text
| `--unicode-snob`                                       | Use unicode throughout instead of ASCII
| `--no-automatic-links`                                 | Do not use automatic links like <https://www.google.com/>
| `--no-skip-internal-links`                             | Turn off skipping of internal links
| `--links-after-para`                                   | Put the links after the paragraph and not at end of document
| `--mark-code`                                          | Mark code with [code]...[/code] blocks
| `--no-wrap-links`                                      | Do not wrap links during text wrapping. Implies `--reference-links`
| `--wrap-list-items`                                    | Wrap list items during text wrapping.
| `--wrap-tables`                                        | Wrap tables during text wrapping.
| `--decode-errors`=`HANDLER`                            | What to do in case an error is encountered. `ignore`, `strict`, `replace` etc.
| `--pad-tables`                                         | Use padding to make tables look good.
| `--default-image-alt`=`Image_Here`                     | Inserts the given `alt` text whenever images are missing `alt` values.
| `--open-quote`=`"`                                     | Inserts the given text when opening a quote. Defaults to `"`.
| `--close-quote`=`"`                                    | Inserts the given text when closing a quote. Defaults to `"`.
