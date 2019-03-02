import sys

if sys.version_info[0] == 2:
    import htmlentitydefs
    import urlparse
    import HTMLParser
else:
    import urllib.parse as urlparse
    import html.entities as htmlentitydefs
    import html.parser as HTMLParser

__all__ = ["HTMLParser", "htmlentitydefs", "urlparse"]
