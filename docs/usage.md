Usage
=====

The module is simple enough to use. This tutorial will get you started.

Installing
----------

These are the methods you can get the module installed:-

    1. `pip install html2text` for those who have pip
    2. Clone the repository from `https://github.com/Alir3z4/html2text.git`
        1. `git clone https://github.com/Alir3z4/html2text`
        2. `python setup build`
        3. `python setup install`


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
    - INLNE_LINKS for formatting images and links
    - PROTECT_LINKS protect from line breaks
    - GOOGLE_LIST_INDENT no of pixels to indent nested lists
    - IGNORE_ANCHORS
    - IGNORE_IMAGES
    - IMAGES_TO_ALT
    - IMAGES_WITH_SIZE
    - IGNORE_EMPHASIS
    - BYPASS_TABLES
    - SINGLE_LINE_BREAK to use a single line break rather than two
    - UNIFIABLE is a dictionary which maps unicode abbrevations to ASCII
                values
    - RE_SPACE for finding space-only lines
    - RE_UNESCAPE for finding html entities like &nbsp;
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

To alter any option the procedure is to create a parser with
`parser = html2text.HTML2Text()` and to set the option on the parser.
example: `parser.unicode_snob = True` to set the UNICODE_SNOB option.
