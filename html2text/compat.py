try:
    import htmlentitydefs
    import urlparse
    import HTMLParser
except ImportError:  # Python3
    import html.entities as htmlentitydefs
    import urllib.parse as urlparse
    import html.parser as HTMLParser
try:  # Python3
    import urllib.request as urllib
except ImportError:
    import urllib
