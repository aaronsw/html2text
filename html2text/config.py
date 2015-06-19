import re

# Use Unicode characters instead of their ascii psuedo-replacements
UNICODE_SNOB = 0

# Escape all special characters.  Output is less readable, but avoids
# corner case formatting issues.
ESCAPE_SNOB = 0

# Put the links after each paragraph instead of at the end.
LINKS_EACH_PARAGRAPH = 0

# Wrap long lines at position. 0 for no wrapping. (Requires Python 2.3.)
BODY_WIDTH = 78

# Don't show internal links (href="#local-anchor") -- corresponding link
# targets won't be visible in the plain text file anyway.
SKIP_INTERNAL_LINKS = True

# Use inline, rather than reference, formatting for images and links
INLINE_LINKS = True

# Protect links from line breaks surrounding them with angle brackets (in
# addition to their square brackets)
PROTECT_LINKS = False

# Number of pixels Google indents nested lists
GOOGLE_LIST_INDENT = 36

IGNORE_ANCHORS = False
IGNORE_IMAGES = False
IMAGES_TO_ALT = False
IMAGES_WITH_SIZE = False
IGNORE_EMPHASIS = False
MARK_CODE = False

# Convert links with same href and text to <href> format if they are absolute links
USE_AUTOMATIC_LINKS = True

# For checking space-only lines on line 771
RE_SPACE = re.compile(r'\s\+')

RE_UNESCAPE = re.compile(r"&(#?[xX]?(?:[0-9a-fA-F]+|\w{1,8}));")
RE_ORDERED_LIST_MATCHER = re.compile(r'\d+\.\s')
RE_UNORDERED_LIST_MATCHER = re.compile(r'[-\*\+]\s')
RE_MD_CHARS_MATCHER = re.compile(r"([\\\[\]\(\)])")
RE_MD_CHARS_MATCHER_ALL = re.compile(r"([`\*_{}\[\]\(\)#!])")
RE_MD_DOT_MATCHER = re.compile(r"""
    ^             # start of line
    (\s*\d+)      # optional whitespace and a number
    (\.)          # dot
    (?=\s)        # lookahead assert whitespace
    """, re.MULTILINE | re.VERBOSE)
RE_MD_PLUS_MATCHER = re.compile(r"""
    ^
    (\s*)
    (\+)
    (?=\s)
    """, flags=re.MULTILINE | re.VERBOSE)
RE_MD_DASH_MATCHER = re.compile(r"""
    ^
    (\s*)
    (-)
    (?=\s|\-)     # followed by whitespace (bullet list, or spaced out hr)
                  # or another dash (header or hr)
    """, flags=re.MULTILINE | re.VERBOSE)
RE_SLASH_CHARS = r'\`*_{}[]()#+-.!'
RE_MD_BACKSLASH_MATCHER = re.compile(r'''
    (\\)          # match one slash
    (?=[%s])      # followed by a char that requires escaping
    ''' % re.escape(RE_SLASH_CHARS),
    flags=re.VERBOSE)

UNIFIABLE = {
    'rsquo': "'",
    'lsquo': "'",
    'rdquo': '"',
    'ldquo': '"',
    'copy': '(C)',
    'mdash': '--',
    'nbsp': ' ',
    'rarr': '->',
    'larr': '<-',
    'middot': '*',
    'ndash': '-',
    'oelig': 'oe',
    'aelig': 'ae',
    'agrave': 'a',
    'aacute': 'a',
    'acirc': 'a',
    'atilde': 'a',
    'auml': 'a',
    'aring': 'a',
    'egrave': 'e',
    'eacute': 'e',
    'ecirc': 'e',
    'euml': 'e',
    'igrave': 'i',
    'iacute': 'i',
    'icirc': 'i',
    'iuml': 'i',
    'ograve': 'o',
    'oacute': 'o',
    'ocirc': 'o',
    'otilde': 'o',
    'ouml': 'o',
    'ugrave': 'u',
    'uacute': 'u',
    'ucirc': 'u',
    'uuml': 'u',
    'lrm': '',
    'rlm': ''
}

BYPASS_TABLES = False

# Use a single line break after a block element rather an two line breaks.
# NOTE: Requires body width setting to be 0.
SINGLE_LINE_BREAK = False
