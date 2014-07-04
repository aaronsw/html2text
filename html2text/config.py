# Use Unicode characters instead of their ascii psuedo-replacements
import re

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

# Number of pixels Google indents nested lists
GOOGLE_LIST_INDENT = 36

IGNORE_ANCHORS = False
IGNORE_IMAGES = False
IGNORE_EMPHASIS = False

### Entity Nonsense ###
# For checking space-only lines on line 771
SPACE_RE = re.compile(r'\s\+')



unifiable = {'rsquo': "'", 'lsquo': "'", 'rdquo': '"', 'ldquo': '"',
             'copy': '(C)', 'mdash': '--', 'nbsp': ' ', 'rarr': '->',
             'larr': '<-', 'middot': '*', 'ndash': '-', 'oelig': 'oe',
             'aelig': 'ae', 'agrave': 'a', 'aacute': 'a', 'acirc': 'a',
             'atilde': 'a', 'auml': 'a', 'aring': 'a', 'egrave': 'e',
             'eacute': 'e', 'ecirc': 'e', 'euml': 'e', 'igrave': 'i',
             'iacute': 'i', 'icirc': 'i', 'iuml': 'i', 'ograve': 'o',
             'oacute': 'o', 'ocirc': 'o', 'otilde': 'o', 'ouml': 'o',
             'ugrave': 'u', 'uacute': 'u', 'ucirc': 'u', 'uuml': 'u',
             'lrm': '', 'rlm': ''}
