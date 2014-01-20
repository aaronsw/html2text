content = """
<div style="text-align: center; width: 194px; font-family: arial,sans-serif; font-size: 83%;"><div><a href="http://picasaweb.google.com/moishel/StHelenS"><img height="160" src="http://lh4.google.com/moishel/RTmZ8ePCABE/AAAAAAAAAJk/fyPodYMRh6I/s160-c/StHelenS.jpg" style="border: medium none ; padding: 0px; margin-top: 16px;" width="160" /></a></div><a href="http://picasaweb.google.com/moishel/StHelenS"><div style="color: rgb(77, 77, 77); font-weight: bold; text-decoration: none;">St. Helen's</div></a><div style="color: rgb(128, 128, 128);"></div></div><br /><br />I climbed St. Helen's today.<br /><br />It turned out to be as close to perfect as I'd like.<br /><br />I'm going back to drinking beer and watching TV now.
"""

import html2text
h = html2text.HTML2Text()
h.body_width = 0
h.escape_snob = 1

print h.handle(content)
