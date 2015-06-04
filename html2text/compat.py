try:
    import urllib.parse as urlparse
    import html.entities as htmlentitydefs
    import html.parser as HTMLParser
except ImportError:  # Python2
    import htmlentitydefs
    import urlparse
    import HTMLParser
try:  # Python3
    import urllib.request as urllib
except ImportError:
    import urllib
