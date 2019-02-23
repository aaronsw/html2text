import sys


if sys.version_info[0] == 2:
    import htmlentitydefs
    import urlparse
    import HTMLParser
    from cgi import escape as html_escape
else:
    import urllib.parse as urlparse
    import html.entities as htmlentitydefs
    import html.parser as HTMLParser
    from html import escape

    def html_escape(s):
        return escape(s, quote=False)


__all__ = ['HTMLParser', 'html_escape', 'htmlentitydefs', 'urlparse']
