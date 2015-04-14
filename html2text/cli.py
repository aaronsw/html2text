import optparse

from html2text.compat import urllib
from html2text import HTML2Text, config, __version__
from html2text.utils import wrapwrite, wrap_read


def main():
    baseurl = ''

    p = optparse.OptionParser('%prog [(filename|url) [encoding]]',
                              version='%prog ' + __version__)
    p.add_option(
        "--ignore-emphasis",
        dest="ignore_emphasis",
        action="store_true",
        default=config.IGNORE_EMPHASIS,
        help="don't include any formatting for emphasis"
    )
    p.add_option(
        "--ignore-links",
        dest="ignore_links",
        action="store_true",
        default=config.IGNORE_ANCHORS,
        help="don't include any formatting for links")
    p.add_option(
        "--protect-links",
        dest="protect_links",
        action="store_true",
        default=config.PROTECT_LINKS,
        help=("protect links from line breaks surrounding them " +
              "with angle brackets"))
    p.add_option(
        "--ignore-images",
        dest="ignore_images",
        action="store_true",
        default=config.IGNORE_IMAGES,
        help="don't include any formatting for images"
    )
    p.add_option(
        "--images-to-alt",
        dest="images_to_alt",
        action="store_true",
        default=config.IMAGES_TO_ALT,
        help="Discard image data, only keep alt text"
    )
    p.add_option(
        "--images-with-size",
        dest="images_with_size",
        action="store_true",
        default=config.IMAGES_WITH_SIZE,
        help="Write image tags with height and width attrs as raw html to "
             "retain dimensions"
    )
    p.add_option(
        "-g", "--google-doc",
        action="store_true",
        dest="google_doc",
        default=False,
        help="convert an html-exported Google Document"
    )
    p.add_option(
        "-d", "--dash-unordered-list",
        action="store_true",
        dest="ul_style_dash",
        default=False,
        help="use a dash rather than a star for unordered list items"
    )
    p.add_option(
        "-e", "--asterisk-emphasis",
        action="store_true",
        dest="em_style_asterisk",
        default=False,
        help="use an asterisk rather than an underscore for emphasized text"
    )
    p.add_option(
        "-b", "--body-width",
        dest="body_width",
        action="store",
        type="int",
        default=config.BODY_WIDTH,
        help="number of characters per output line, 0 for no wrap"
    )
    p.add_option(
        "-i", "--google-list-indent",
        dest="list_indent",
        action="store",
        type="int",
        default=config.GOOGLE_LIST_INDENT,
        help="number of pixels Google indents nested lists"
    )
    p.add_option(
        "-s", "--hide-strikethrough",
        action="store_true",
        dest="hide_strikethrough",
        default=False,
        help="hide strike-through text. only relevant when -g is "
             "specified as well"
    )
    p.add_option(
        "--escape-all",
        action="store_true",
        dest="escape_snob",
        default=False,
        help="Escape all special characters.  Output is less readable, but "
             "avoids corner case formatting issues."
    )
    p.add_option(
        "--bypass-tables",
        action="store_true",
        dest="bypass_tables",
        default=config.BYPASS_TABLES,
        help="Format tables in HTML rather than Markdown syntax."
    )
    p.add_option(
        "--single-line-break",
        action="store_true",
        dest="single_line_break",
        default=config.SINGLE_LINE_BREAK,
        help=(
            "Use a single line break after a block element rather than two "
            "line breaks. NOTE: Requires --body-width=0"
        )
    )
    (options, args) = p.parse_args()

    # process input
    encoding = "utf-8"
    if len(args) > 0 and args[0] != '-':
        file_ = args[0]
        if len(args) == 2:
            encoding = args[1]
        if len(args) > 2:
            p.error('Too many arguments')

        if file_.startswith('http://') or file_.startswith('https://'):
            baseurl = file_
            j = urllib.urlopen(baseurl)
            data = j.read()
            if encoding is None:
                try:
                    from feedparser import _getCharacterEncoding as enc
                except ImportError:
                    enc = lambda x, y: ('utf-8', 1)
                encoding = enc(j.headers, data)[0]
                if encoding == 'us-ascii':
                    encoding = 'utf-8'
        else:
            data = open(file_, 'rb').read()
            if encoding is None:
                try:
                    from chardet import detect
                except ImportError:
                    detect = lambda x: {'encoding': 'utf-8'}
                encoding = detect(data)['encoding']
    else:
        data = wrap_read()

    if hasattr(data, 'decode'):
        data = data.decode(encoding)

    h = HTML2Text(baseurl=baseurl)
    # handle options
    if options.ul_style_dash:
        h.ul_item_mark = '-'
    if options.em_style_asterisk:
        h.emphasis_mark = '*'
        h.strong_mark = '__'

    h.body_width = options.body_width
    h.list_indent = options.list_indent
    h.ignore_emphasis = options.ignore_emphasis
    h.ignore_links = options.ignore_links
    h.protect_links = options.protect_links
    h.ignore_images = options.ignore_images
    h.images_to_alt = options.images_to_alt
    h.images_with_size = options.images_with_size
    h.google_doc = options.google_doc
    h.hide_strikethrough = options.hide_strikethrough
    h.escape_snob = options.escape_snob
    h.bypass_tables = options.bypass_tables
    h.single_line_break = options.single_line_break

    wrapwrite(h.handle(data))
