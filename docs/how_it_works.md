Introduction
============


There are 5 components to the code. They are kept as separate files in the
html2text directory. This part of the documentation explains them bit by bit.


compat.py
---------

This part exists only to test compatibility with the available python standard libraries. Python3 relocated some libraries and so this file makes sure that everything has a common interface.

config.py
---------

Used to provide various configuration settings to the converter. They are as follows:

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

utils.py
--------

Used to provide utility functions to html2text
Some functions are:

    - name2cp                   :name to code point
    - hn                        :headings
    - dumb_property_dict        :hash of css attrs
    - dumb_css_parser           :returns a hash of css selectors, each
                                 containing a hash of css attrs
    - element_style             :hash of final style of element
    - google_list_style         :find out ordered?unordered
    - google_has_height         :does element have height?
    - google_text_emphasis      :a list of all emphasis modifiers
    - google_fixed_width_font   :check for fixed width font
    - list_numbering_start      :extract numbering from list elem attrs
    - skipwrap                  :skip wrap for give para or not?
    - escape_md                 :escape md sensitive within other md
    - escape_md_section         :escape md sensitive across whole doc


cli.py
------

Command line interface for the code.


| Option                                                 | Description
|--------------------------------------------------------|---------------------------------------------------
| `--version`                                            | Show program version number and exit
| `-h`, `--help`                                         | Show this help message and exit
| `--ignore-links`                                       | Do not include any formatting for links
|`--protect-links`                                       | Protect links from line breaks surrounding them "+" with angle brackets
|`--ignore-images`                                       | Do not include any formatting for images
|`--images-to-alt`                                       | Discard image data, only keep alt text
|`--images-with-size`                                    | Write image tags with height and width attrs as raw html to retain dimensions
|`--images-as-html`                                      | Always write image tags as raw html; preserves "height", "width" and "alt" if possible.
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

*A complete list is available [here](usage.md)*

__init__.py
-----------

This is where everything comes together. This is the glue for all the
things we have described above.

This file describes a single HTML2Text class which is itself a subclass of the HTMLParser in python

Upon initialization it sets various config variables necessary for
processing the given html in a certain manner necessary to create valid
markdown text.
The class defines methods:

    - feed
    - handle
    - outtextf
    - close
    - handle_charref
    - handle_entityref
    - handle_starttag
    - handle_endtag
    - previousIndex
    - handle_emphasis
    - handle_tag
    - pbr
    - p
    - soft_br
    - o
    - handle_data
    - charref
    - entityref
    - google_nest_count
    - optwrap

Besides this there are 2 more methods defined:

    - html2text     :calls the HTML2Text class with .handle() method
    - unescape      :calls the HTML2Text class with .unescape() method

What they do is provide methods to make the HTML parser in python
parse the HTML and convert to markdown.
