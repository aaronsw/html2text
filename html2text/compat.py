try:  # pragma: no cover
    import urllib.parse as urlparse
    import html.entities as htmlentitydefs
    import html.parser as HTMLParser
except ImportError:  # pragma: no cover
    import htmlentitydefs
    import urlparse
    import HTMLParser
try:  # pragma: no cover
    import urllib.request as urllib
except ImportError:  # pragma: no cover
    import urllib
