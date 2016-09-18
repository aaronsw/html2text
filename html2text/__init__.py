#!/usr/bin/env python
# coding: utf-8
"""html2text: Turn HTML into equivalent Markdown-structured text."""
from __future__ import division
import re
import sys

try:
    from textwrap import wrap
except ImportError:  # pragma: no cover
    pass

from html2text.compat import urlparse, HTMLParser, html_escape
from html2text import config

from html2text.utils import (
    name2cp,
    unifiable_n,
    google_text_emphasis,
    google_fixed_width_font,
    element_style,
    hn,
    google_has_height,
    escape_md,
    google_list_style,
    list_numbering_start,
    dumb_css_parser,
    escape_md_section,
    skipwrap,
    pad_tables_in_text
)

__version__ = (2016, 9, 19)


# TODO:
# Support decoded entities with UNIFIABLE.


class HTML2Text(HTMLParser.HTMLParser):
    def __init__(self, out=None, baseurl='', bodywidth=config.BODY_WIDTH):
        """
        Input parameters:
            out: possible custom replacement for self.outtextf (which
                 appends lines of text).
            baseurl: base URL of the document we process
        """
        kwargs = {}
        if sys.version_info >= (3, 4):
            kwargs['convert_charrefs'] = False
        HTMLParser.HTMLParser.__init__(self, **kwargs)

        # Config options
        self.split_next_td = False
        self.td_count = 0
        self.table_start = False
        self.unicode_snob = config.UNICODE_SNOB  # covered in cli
        self.escape_snob = config.ESCAPE_SNOB  # covered in cli
        self.links_each_paragraph = config.LINKS_EACH_PARAGRAPH
        self.body_width = bodywidth  # covered in cli
        self.skip_internal_links = config.SKIP_INTERNAL_LINKS  # covered in cli
        self.inline_links = config.INLINE_LINKS  # covered in cli
        self.protect_links = config.PROTECT_LINKS  # covered in cli
        self.google_list_indent = config.GOOGLE_LIST_INDENT  # covered in cli
        self.ignore_links = config.IGNORE_ANCHORS  # covered in cli
        self.ignore_images = config.IGNORE_IMAGES  # covered in cli
        self.images_to_alt = config.IMAGES_TO_ALT  # covered in cli
        self.images_with_size = config.IMAGES_WITH_SIZE  # covered in cli
        self.ignore_emphasis = config.IGNORE_EMPHASIS  # covered in cli
        self.bypass_tables = config.BYPASS_TABLES  # covered in cli
        self.ignore_tables = config.IGNORE_TABLES  # covered in cli
        self.google_doc = False  # covered in cli
        self.ul_item_mark = '*'  # covered in cli
        self.emphasis_mark = '_'  # covered in cli
        self.strong_mark = '**'
        self.single_line_break = config.SINGLE_LINE_BREAK  # covered in cli
        self.use_automatic_links = config.USE_AUTOMATIC_LINKS  # covered in cli
        self.hide_strikethrough = False  # covered in cli
        self.mark_code = config.MARK_CODE
        self.wrap_links = config.WRAP_LINKS  # covered in cli
        self.pad_tables = config.PAD_TABLES  # covered in cli
        self.default_image_alt = config.DEFAULT_IMAGE_ALT  # covered in cli
        self.tag_callback = None

        if out is None:  # pragma: no cover
            self.out = self.outtextf
        else:  # pragma: no cover
            self.out = out

        # empty list to store output characters before they are "joined"
        self.outtextlist = []

        self.quiet = 0
        self.p_p = 0  # number of newline character to print before next output
        self.outcount = 0
        self.start = 1
        self.space = 0
        self.a = []
        self.astack = []
        self.maybe_automatic_link = None
        self.empty_link = False
        self.absolute_url_matcher = re.compile(r'^[a-zA-Z+]+://')
        self.acount = 0
        self.list = []
        self.blockquote = 0
        self.pre = 0
        self.startpre = 0
        self.code = False
        self.br_toggle = ''
        self.lastWasNL = 0
        self.lastWasList = False
        self.style = 0
        self.style_def = {}
        self.tag_stack = []
        self.emphasis = 0
        self.drop_white_space = 0
        self.inheader = False
        self.abbr_title = None  # current abbreviation definition
        self.abbr_data = None  # last inner HTML (for abbr being defined)
        self.abbr_list = {}  # stack of abbreviations to write later
        self.baseurl = baseurl

        try:
            del unifiable_n[name2cp('nbsp')]
        except KeyError:
            pass
        config.UNIFIABLE['nbsp'] = '&nbsp_place_holder;'

    def feed(self, data):
        data = data.replace("</' + 'script>", "</ignore>")
        HTMLParser.HTMLParser.feed(self, data)

    def handle(self, data):
        self.feed(data)
        self.feed("")
        markdown = self.optwrap(self.close())
        if self.pad_tables:
            return pad_tables_in_text(markdown)
        else:
            return markdown

    def outtextf(self, s):
        self.outtextlist.append(s)
        if s:
            self.lastWasNL = s[-1] == '\n'

    def close(self):
        HTMLParser.HTMLParser.close(self)

        try:
            nochr = unicode('')
            unicode_character = unichr
        except NameError:
            nochr = str('')
            unicode_character = chr

        self.pbr()
        self.o('', 0, 'end')

        outtext = nochr.join(self.outtextlist)

        if self.unicode_snob:
            nbsp = unicode_character(name2cp('nbsp'))
        else:
            nbsp = unicode_character(32)
        try:
            outtext = outtext.replace(unicode('&nbsp_place_holder;'), nbsp)
        except NameError:
            outtext = outtext.replace('&nbsp_place_holder;', nbsp)

        # Clear self.outtextlist to avoid memory leak of its content to
        # the next handling.
        self.outtextlist = []

        return outtext

    def handle_charref(self, c):
        charref = self.charref(c)
        if not self.code and not self.pre:
            charref = html_escape(charref)
        self.handle_data(charref, True)

    def handle_entityref(self, c):
        entityref = self.entityref(c)
        if (not self.code and not self.pre
                and entityref != '&nbsp_place_holder;'):
            entityref = html_escape(entityref)
        self.handle_data(entityref, True)

    def handle_starttag(self, tag, attrs):
        self.handle_tag(tag, attrs, 1)

    def handle_endtag(self, tag):
        self.handle_tag(tag, None, 0)

    def previousIndex(self, attrs):
        """
        :type attrs: dict

        :returns: The index of certain set of attributes (of a link) in the
        self.a list. If the set of attributes is not found, returns None
        :rtype: int
        """
        if 'href' not in attrs:  # pragma: no cover
            return None
        i = -1
        for a in self.a:
            i += 1
            match = 0

            if ('href' in a) and a['href'] == attrs['href']:
                if ('title' in a) or ('title' in attrs):
                    if (('title' in a) and ('title' in attrs) and
                                a['title'] == attrs['title']):
                        match = True
                else:
                    match = True

            if match:
                return i

    def handle_emphasis(self, start, tag_style, parent_style):
        """
        Handles various text emphases
        """
        tag_emphasis = google_text_emphasis(tag_style)
        parent_emphasis = google_text_emphasis(parent_style)

        # handle Google's text emphasis
        strikethrough = 'line-through' in \
                        tag_emphasis and self.hide_strikethrough
        bold = 'bold' in tag_emphasis and not 'bold' in parent_emphasis
        italic = 'italic' in tag_emphasis and not 'italic' in parent_emphasis
        fixed = google_fixed_width_font(tag_style) and not \
            google_fixed_width_font(parent_style) and not self.pre

        if start:
            # crossed-out text must be handled before other attributes
            # in order not to output qualifiers unnecessarily
            if bold or italic or fixed:
                self.emphasis += 1
            if strikethrough:
                self.quiet += 1
            if italic:
                self.o(self.emphasis_mark)
                self.drop_white_space += 1
            if bold:
                self.o(self.strong_mark)
                self.drop_white_space += 1
            if fixed:
                self.o('`')
                self.drop_white_space += 1
                self.code = True
        else:
            if bold or italic or fixed:
                # there must not be whitespace before closing emphasis mark
                self.emphasis -= 1
                self.space = 0
            if fixed:
                if self.drop_white_space:
                    # empty emphasis, drop it
                    self.drop_white_space -= 1
                else:
                    self.o('`')
                self.code = False
            if bold:
                if self.drop_white_space:
                    # empty emphasis, drop it
                    self.drop_white_space -= 1
                else:
                    self.o(self.strong_mark)
            if italic:
                if self.drop_white_space:
                    # empty emphasis, drop it
                    self.drop_white_space -= 1
                else:
                    self.o(self.emphasis_mark)
            # space is only allowed after *all* emphasis marks
            if (bold or italic) and not self.emphasis:
                self.o(" ")
            if strikethrough:
                self.quiet -= 1

    def handle_tag(self, tag, attrs, start):
        # attrs is None for endtags
        if attrs is None:
            attrs = {}
        else:
            attrs = dict(attrs)

        if self.tag_callback is not None:
            if self.tag_callback(self, tag, attrs, start) is True:
                return

        # first thing inside the anchor tag is another tag that produces some output
        if (start and not self.maybe_automatic_link is None
                and tag not in ['p', 'div', 'style', 'dl', 'dt']
                and (tag != "img" or self.ignore_images)):
            self.o("[")
            self.maybe_automatic_link = None
            self.empty_link = False

        if self.google_doc:
            # the attrs parameter is empty for a closing tag. in addition, we
            # need the attributes of the parent nodes in order to get a
            # complete style description for the current element. we assume
            # that google docs export well formed html.
            parent_style = {}
            if start:
                if self.tag_stack:
                    parent_style = self.tag_stack[-1][2]
                tag_style = element_style(attrs, self.style_def, parent_style)
                self.tag_stack.append((tag, attrs, tag_style))
            else:
                dummy, attrs, tag_style = self.tag_stack.pop() if self.tag_stack else (None, {}, {})
                if self.tag_stack:
                    parent_style = self.tag_stack[-1][2]

        if hn(tag):
            self.p()
            if start:
                self.inheader = True
                self.o(hn(tag) * "#" + ' ')
            else:
                self.inheader = False
                return  # prevent redundant emphasis marks on headers

        if tag in ['p', 'div']:
            if self.google_doc:
                if start and google_has_height(tag_style):
                    self.p()
                else:
                    self.soft_br()
            else:
                self.p()

        if tag == "br" and start:
            if self.blockquote > 0:
                self.o("  \n> ")
            else:
                self.o("  \n")

        if tag == "hr" and start:
            self.p()
            self.o("* * *")
            self.p()

        if tag in ["head", "style", 'script']:
            if start:
                self.quiet += 1
            else:
                self.quiet -= 1

        if tag == "style":
            if start:
                self.style += 1
            else:
                self.style -= 1

        if tag in ["body"]:
            self.quiet = 0  # sites like 9rules.com never close <head>

        if tag == "blockquote":
            if start:
                self.p()
                self.o('> ', 0, 1)
                self.start = 1
                self.blockquote += 1
            else:
                self.blockquote -= 1
                self.p()

        if tag in ['em', 'i', 'u'] and not self.ignore_emphasis:
            self.o(self.emphasis_mark)
        if tag in ['strong', 'b'] and not self.ignore_emphasis:
            self.o(self.strong_mark)
        if tag in ['del', 'strike', 's']:
            if start:
                self.o('~~')
            else:
                self.o('~~')

        if self.google_doc:
            if not self.inheader:
                # handle some font attributes, but leave headers clean
                self.handle_emphasis(start, tag_style, parent_style)

        if tag in ["code", "tt"] and not self.pre:
            self.o('`')  # TODO: `` `this` ``
            self.code = not self.code
        if tag == "abbr":
            if start:
                self.abbr_title = None
                self.abbr_data = ''
                if ('title' in attrs):
                    self.abbr_title = attrs['title']
            else:
                if self.abbr_title is not None:
                    self.abbr_list[self.abbr_data] = self.abbr_title
                    self.abbr_title = None
                self.abbr_data = ''

        if tag == "a" and not self.ignore_links:
            if start:
                if ('href' in attrs) and \
                        (attrs['href'] is not None) and \
                        not (self.skip_internal_links and
                                 attrs['href'].startswith('#')):
                    self.astack.append(attrs)
                    self.maybe_automatic_link = attrs['href']
                    self.empty_link = True
                    if self.protect_links:
                        attrs['href'] = '<'+attrs['href']+'>'
                else:
                    self.astack.append(None)
            else:
                if self.astack:
                    a = self.astack.pop()
                    if self.maybe_automatic_link and not self.empty_link:
                        self.maybe_automatic_link = None
                    elif a:
                        if self.empty_link:
                            self.o("[")
                            self.empty_link = False
                            self.maybe_automatic_link = None
                        if self.inline_links:
                            try:
                                title = escape_md(a['title'])
                            except KeyError:
                                self.o("](" + escape_md(urlparse.urljoin(self.baseurl, a['href'])) + ")")
                            else:
                                self.o("](" + escape_md(urlparse.urljoin(self.baseurl, a['href']))
                                       + ' "' + title + '" )')
                        else:
                            i = self.previousIndex(a)
                            if i is not None:
                                a = self.a[i]
                            else:
                                self.acount += 1
                                a['count'] = self.acount
                                a['outcount'] = self.outcount
                                self.a.append(a)
                            self.o("][" + str(a['count']) + "]")

        if tag == "img" and start and not self.ignore_images:
            if 'src' in attrs:
                if not self.images_to_alt:
                    attrs['href'] = attrs['src']
                alt = attrs.get('alt') or self.default_image_alt

                # If we have images_with_size, write raw html including width,
                # height, and alt attributes
                if self.images_with_size and \
                        ("width" in attrs or "height" in attrs):
                    self.o("<img src='" + attrs["src"] + "' ")
                    if "width" in attrs:
                        self.o("width='" + attrs["width"] + "' ")
                    if "height" in attrs:
                        self.o("height='" + attrs["height"] + "' ")
                    if alt:
                        self.o("alt='" + alt + "' ")
                    self.o("/>")
                    return

                # If we have a link to create, output the start
                if not self.maybe_automatic_link is None:
                    href = self.maybe_automatic_link
                    if self.images_to_alt and escape_md(alt) == href and \
                            self.absolute_url_matcher.match(href):
                        self.o("<" + escape_md(alt) + ">")
                        self.empty_link = False
                        return
                    else:
                        self.o("[")
                        self.maybe_automatic_link = None
                        self.empty_link = False

                # If we have images_to_alt, we discard the image itself,
                # considering only the alt text.
                if self.images_to_alt:
                    self.o(escape_md(alt))
                else:
                    self.o("![" + escape_md(alt) + "]")
                    if self.inline_links:
                        href = attrs.get('href') or ''
                        self.o("(" + escape_md(urlparse.urljoin(self.baseurl, href)) + ")")
                    else:
                        i = self.previousIndex(attrs)
                        if i is not None:
                            attrs = self.a[i]
                        else:
                            self.acount += 1
                            attrs['count'] = self.acount
                            attrs['outcount'] = self.outcount
                            self.a.append(attrs)
                        self.o("[" + str(attrs['count']) + "]")

        if tag == 'dl' and start:
            self.p()
        if tag == 'dt' and not start:
            self.pbr()
        if tag == 'dd' and start:
            self.o('    ')
        if tag == 'dd' and not start:
            self.pbr()

        if tag in ["ol", "ul"]:
            # Google Docs create sub lists as top level lists
            if (not self.list) and (not self.lastWasList):
                self.p()
            if start:
                if self.google_doc:
                    list_style = google_list_style(tag_style)
                else:
                    list_style = tag
                numbering_start = list_numbering_start(attrs)
                self.list.append({
                    'name': list_style,
                    'num': numbering_start
                })
            else:
                if self.list:
                    self.list.pop()
                    if (not self.google_doc) and (not self.list):
                        self.o('\n')
            self.lastWasList = True
        else:
            self.lastWasList = False

        if tag == 'li':
            self.pbr()
            if start:
                if self.list:
                    li = self.list[-1]
                else:
                    li = {'name': 'ul', 'num': 0}
                if self.google_doc:
                    nest_count = self.google_nest_count(tag_style)
                else:
                    nest_count = len(self.list)
                # TODO: line up <ol><li>s > 9 correctly.
                self.o("  " * nest_count)
                if li['name'] == "ul":
                    self.o(self.ul_item_mark + " ")
                elif li['name'] == "ol":
                    li['num'] += 1
                    self.o(str(li['num']) + ". ")
                self.start = 1

        if tag in ["table", "tr", "td", "th"]:
            if self.ignore_tables:
                if tag == 'tr':
                    if start:
                        pass
                    else:
                        self.soft_br()
                else:
                    pass

            elif self.bypass_tables:
                if start:
                    self.soft_br()
                if tag in ["td", "th"]:
                    if start:
                        self.o('<{0}>\n\n'.format(tag))
                    else:
                        self.o('\n</{0}>'.format(tag))
                else:
                    if start:
                        self.o('<{0}>'.format(tag))
                    else:
                        self.o('</{0}>'.format(tag))

            else:
                if tag == "table":
                    if start:
                        self.table_start = True
                        if self.pad_tables:
                            self.o("<"+config.TABLE_MARKER_FOR_PAD+">")
                            self.o("  \n")
                    else:
                        if self.pad_tables:
                            self.o("</"+config.TABLE_MARKER_FOR_PAD+">")
                            self.o("  \n")
                if tag in ["td", "th"] and start:
                    if self.split_next_td:
                        self.o("| ")
                    self.split_next_td = True

                if tag == "tr" and start:
                    self.td_count = 0
                if tag == "tr" and not start:
                    self.split_next_td = False
                    self.soft_br()
                if tag == "tr" and not start and self.table_start:
                    # Underline table header
                    self.o("|".join(["---"] * self.td_count))
                    self.soft_br()
                    self.table_start = False
                if tag in ["td", "th"] and start:
                    self.td_count += 1

        if tag == "pre":
            if start:
                self.startpre = 1
                self.pre = 1
            else:
                self.pre = 0
                if self.mark_code:
                    self.out("\n[/code]")
            self.p()

    # TODO: Add docstring for these one letter functions
    def pbr(self):
        "Pretty print has a line break"
        if self.p_p == 0:
            self.p_p = 1

    def p(self):
        "Set pretty print to 1 or 2 lines"
        self.p_p = 1 if self.single_line_break else 2

    def soft_br(self):
        "Soft breaks"
        self.pbr()
        self.br_toggle = '  '

    def o(self, data, puredata=0, force=0):
        """
        Deal with indentation and whitespace
        """
        if self.abbr_data is not None:
            self.abbr_data += data

        if not self.quiet:
            if self.google_doc:
                # prevent white space immediately after 'begin emphasis'
                # marks ('**' and '_')
                lstripped_data = data.lstrip()
                if self.drop_white_space and not (self.pre or self.code):
                    data = lstripped_data
                if lstripped_data != '':
                    self.drop_white_space = 0

            if puredata and not self.pre:
                # This is a very dangerous call ... it could mess up
                # all handling of &nbsp; when not handled properly
                # (see entityref)
                data = re.sub(r'\s+', r' ', data)
                if data and data[0] == ' ':
                    self.space = 1
                    data = data[1:]
            if not data and not force:
                return

            if self.startpre:
                #self.out(" :") #TODO: not output when already one there
                if not data.startswith("\n"):  # <pre>stuff...
                    data = "\n" + data
                if self.mark_code:
                    self.out("\n[code]")
                    self.p_p = 0

            bq = (">" * self.blockquote)
            if not (force and data and data[0] == ">") and self.blockquote:
                bq += " "

            if self.pre:
                if not self.list:
                    bq += "    "
                #else: list content is already partially indented
                for i in range(len(self.list)):
                    bq += "    "
                data = data.replace("\n", "\n" + bq)

            if self.startpre:
                self.startpre = 0
                if self.list:
                    # use existing initial indentation
                    data = data.lstrip("\n")

            if self.start:
                self.space = 0
                self.p_p = 0
                self.start = 0

            if force == 'end':
                # It's the end.
                self.p_p = 0
                self.out("\n")
                self.space = 0

            if self.p_p:
                self.out((self.br_toggle + '\n' + bq) * self.p_p)
                self.space = 0
                self.br_toggle = ''

            if self.space:
                if not self.lastWasNL:
                    self.out(' ')
                self.space = 0

            if self.a and ((self.p_p == 2 and self.links_each_paragraph)
                           or force == "end"):
                if force == "end":
                    self.out("\n")

                newa = []
                for link in self.a:
                    if self.outcount > link['outcount']:
                        self.out("   [" + str(link['count']) + "]: " +
                                 urlparse.urljoin(self.baseurl, link['href']))
                        if 'title' in link:
                            self.out(" (" + link['title'] + ")")
                        self.out("\n")
                    else:
                        newa.append(link)

                # Don't need an extra line when nothing was done.
                if self.a != newa:
                    self.out("\n")

                self.a = newa

            if self.abbr_list and force == "end":
                for abbr, definition in self.abbr_list.items():
                    self.out("  *[" + abbr + "]: " + definition + "\n")

            self.p_p = 0
            self.out(data)
            self.outcount += 1

    def handle_data(self, data, entity_char=False):
        if self.style:
            self.style_def.update(dumb_css_parser(data))

        if not self.maybe_automatic_link is None:
            href = self.maybe_automatic_link
            if (href == data and self.absolute_url_matcher.match(href)
                    and self.use_automatic_links):
                self.o("<" + data + ">")
                self.empty_link = False
                return
            else:
                self.o("[")
                self.maybe_automatic_link = None
                self.empty_link = False

        if not self.code and not self.pre and not entity_char:
            data = escape_md_section(data, snob=self.escape_snob)
        self.o(data, 1)

    def unknown_decl(self, data):  # pragma: no cover
        # TODO: what is this doing here?
        pass

    def charref(self, name):
        if name[0] in ['x', 'X']:
            c = int(name[1:], 16)
        else:
            c = int(name)

        if not self.unicode_snob and c in unifiable_n.keys():
            return unifiable_n[c]
        else:
            try:
                try:
                    return unichr(c)
                except NameError:  # Python3
                    return chr(c)
            except ValueError:  # invalid unicode
                return ''

    def entityref(self, c):
        if not self.unicode_snob and c in config.UNIFIABLE.keys():
            return config.UNIFIABLE[c]
        else:
            try:
                name2cp(c)
            except KeyError:
                return "&" + c + ';'
            else:
                if c == 'nbsp':
                    return config.UNIFIABLE[c]
                else:
                    try:
                        return unichr(name2cp(c))
                    except NameError:  # Python3
                        return chr(name2cp(c))

    def replaceEntities(self, s):
        s = s.group(1)
        if s[0] == "#":
            return self.charref(s[1:])
        else:
            return self.entityref(s)

    def unescape(self, s):
        return config.RE_UNESCAPE.sub(self.replaceEntities, s)

    def google_nest_count(self, style):
        """
        Calculate the nesting count of google doc lists

        :type style: dict

        :rtype: int
        """
        nest_count = 0
        if 'margin-left' in style:
            nest_count = int(style['margin-left'][:-2]) \
                         // self.google_list_indent

        return nest_count

    def optwrap(self, text):
        """
        Wrap all paragraphs in the provided text.

        :type text: str

        :rtype: str
        """
        if not self.body_width:
            return text

        assert wrap, "Requires Python 2.3."
        result = ''
        newlines = 0
        # I cannot think of a better solution for now.
        # To avoid the non-wrap behaviour for entire paras
        # because of the presence of a link in it
        if not self.wrap_links:
            self.inline_links = False
        for para in text.split("\n"):
            if len(para) > 0:
                if not skipwrap(para, self.wrap_links):
                    result += "\n".join(
                        wrap(para, self.body_width, break_long_words=False)
                    )
                    if para.endswith('  '):
                        result += "  \n"
                        newlines = 1
                    else:
                        result += "\n\n"
                        newlines = 2
                else:
                    # Warning for the tempted!!!
                    # Be aware that obvious replacement of this with
                    # line.isspace()
                    # DOES NOT work! Explanations are welcome.
                    if not config.RE_SPACE.match(para):
                        result += para + "\n"
                        newlines = 1
            else:
                if newlines < 2:
                    result += "\n"
                    newlines += 1
        return result


def html2text(html, baseurl='', bodywidth=None):
    if bodywidth is None:
        bodywidth = config.BODY_WIDTH
    h = HTML2Text(baseurl=baseurl, bodywidth=bodywidth)

    return h.handle(html)


def unescape(s, unicode_snob=False):
    h = HTML2Text()
    h.unicode_snob = unicode_snob

    return h.unescape(s)


if __name__ == "__main__":
    from html2text.cli import main

    main()
