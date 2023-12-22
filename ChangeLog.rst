UNRELEASED
==========
----

* Fix #332: Insert at most one space for multiple emphasis
* Feature #318: Make padded tables more similar to pandoc's pipe_tables.
* Add support for Python 3.9.
* Fix extra line breaks inside html link text (between '[' and ']')
* Fix #344: indent ``<ul>`` inside ``<ol>`` three spaces instead of two to comply with CommonMark, GFM, etc.
* Fix #324: unnecessary spaces around ``<b>``, ``<em>``, and ``strike`` tags.
* Don't wrap tables by default and add a ``--wrap-tables`` config option
* Remove support for Python ≤ 3.5. Now requires Python 3.6+.
* Support for Python 3.10.
* Fix #320 padding empty tables and tables with no </tr> tags.
* Add ``ignore_mailto_links`` config option to ignore ``mailto:`` style links.



2020.1.16
=========
----

* Add type annotations.
* Add support for Python 3.8.
* Performance improvements when ``wrap_links`` is ``False`` (the default).
* Configure setuptools using setup.cfg.


2019.9.26
=========
----

* Fix long blockquotes wrapping.
* Remove the trailing whitespaces that were added after wrapping list items & blockquotes.
* Remove support for Python ≤ 3.4. Now requires Python 3.5+.
* Fix memory leak when processing a document containing a ``<abbr>`` tag.
* Fix ``AttributeError`` when reading text from stdin.
* Fix ``UnicodeEncodeError`` when writing output to stdout.


2019.8.11
=========
----

* Add support for wrapping list items.
* Fix #201: handle &lrm;/&rlm; marks mid-text within stressed tags or right after stressed tags.
* Feature #213: ``images_as_html`` config option to always generate an ``img`` html tag. preserves "height", "width" and "alt" if possible.
* Remove support for end-of-life Pythons. Now requires Python 2.7 or 3.4+.
* Remove support for retrieving HTML over the network.
* Add ``__main__.py`` module to allow running the CLI using ``python -m html2text ...``.
* Fix #238: correct spacing when a HTML entity follows a non-stressed tags which follow a stressed tag.
* Remove unused or deprecated:

  * ``html2text.compat.escape()``
  * ``html2text.config.RE_UNESCAPE``
  * ``html2text.HTML2Text.replaceEntities()``
  * ``html2text.HTML2Text.unescape()``
  * ``html2text.unescape()``

* Fix #208: handle LEFT-TO-RIGHT MARK after a stressed tag.


2018.1.9
========
----

* Fix #188: Non-ASCII in title attribute causes encode error.
* Feature #194: Add support for the <kbd> tag.
* Feature #193: Add support for the <q> tag.


2017.10.4
==========
----

* Fix #157: Fix images link with div wrap
* Fix #55: Fix error when empty title tags
* Fix #160: The html2text tests are failing on Windows and on Cygwin due to differences in eol handling between windows/*nix
* Feature #164: Housekeeping: Add flake8 to the travis build, cleanup existing flake8 violations, add py3.6 and pypy3 to the travis build
* Fix #109: Fix for unexpanded &lt; &gt; &amp;
* Fix #143: Fix line wrapping for the lines starting with bold
* Adds support for numeric bold text indication in ``font-weight``,
  as used by Google (and presumably others.)
* Fix #173 and #142: Stripping whitespace in crucial markdown and adding whitespace as necessary
* Don't drop any cell data on tables uneven row lengths (e.g. colspan in use)


2016.9.19
=========
----

* Default image alt text option created and set to a default of empty string "" to maintain backward compatibility
* Fix #136: --default-image-alt now takes a string as argument
* Fix #113: Stop changing quiet levels on \/script tags.
* Merge #126: Fix deprecation warning on py3 due to html.escape
* Fix #145: Running test suite on Travis CI for Python 2.6.


2016.5.29
=========
----

* Fix #125: --pad_tables now pads table cells to make them look nice.
* Fix #114: Break does not interrupt blockquotes
* Deprecation warnings for URL retrieval.


2016.4.2
=========
----

* Fix #106: encoding by stdin
* Fix #89: Python 3.5 support.
* Fix #113: inplace baseurl substitution for <a> and <img> tags.
* Feature #118: Update the badges to badge.kloud51.com
* Fix #119: new-line after a list is inserted


2016.1.8
=========
----

* Feature #99: Removed duplicated initialisation.
* Fix #100: Get element style key error.
* Fix #101: Fix error end tag pop exception
* <s>, <strike>, <del> now rendered as ~~text~~.


2015.11.4
=========
----

* Fix #38: Long links wrapping controlled by ``--no-wrap-links``.
* Note: ``--no-wrap-links`` implies ``--reference-links``
* Feature #83: Add callback-on-tag.
* Fix #87: Decode errors can be handled via command line.
* Feature #95: Docs, decode errors spelling mistake.
* Fix #84: Make bodywidth kwarg overridable using config.


2015.6.21
=========
----

* Fix #31: HTML entities stay inside link.
* Fix #71: Coverage detects command line tests.
* Fix #39: Documentation update.
* Fix #61: Functionality added for optional use of automatic links.
* Feature #80: ``title`` attribute is preserved in both inline and reference links.
* Feature #82: More command line options. See docs.


2015.6.12
=========
----

* Feature #76: Making ``pre`` blocks clearer for further automatic formatting.
* Fix #71: Coverage detects tests carried out in ``subprocesses``


2015.6.6
========
----

* Fix #24: ``3.200.3`` vs ``2014.7.3`` output quirks.
* Fix #61. Malformed links in markdown output.
* Feature #62: Automatic version number.
* Fix #63: Nested code, anchor bug.
* Fix #64: Proper handling of anchors with content that starts with tags.
* Feature #67: Documentation all over the module.
* Feature #70: Adding tests for the module.
* Fix #73: Typo in config documentation.


2015.4.14
=========
----


* Feature #59: Write image tags with height and width attrs as raw html to retain dimensions


2015.4.13
=========
----


* Feature #56: Treat '-' file parameter as stdin.
* Feature #57: Retain escaping of html except within code or pre tags.


2015.2.18
=========
----

* Fix #38: Anchor tags with empty text or with ``<img>`` tags inside are no longer stripped.


2014.12.29
==========
----

* Feature #51: Add single line break option.
    This feature is useful for ensuring that lots of extra line breaks do not
    end up in the resulting Markdown file in situations like Evernote .enex
    exports. Note that this only works properly if ``body-width`` is set
    to ``0``.


2014.12.24
==========
----

* Feature #49: Added an images_to_alt option to discard images and keep only their alt.
* Feature #50: Protect links, surrounding them with angle brackets to avoid breaking...
* Feature: Add ``setup.cfg`` file.


2014.12.5
=========
----

* Feature: Update ``README.md`` with usage examples.
* Fix #35: Remove ``py_modules`` from ``setup.py``.
* Fix #36: Excludes tests from being installed as a separate module.
* Fix #37: Don't hardcode the path to the installed binary.
* Fix: Readme typo in running cli.
* Feature #40: Extract cli part to ``cli`` module.
* Feature #42: Bring python version compatibility to ``compat.py`` module.
* Feature #41: Extract utility/helper methods to ``utils`` module.
* Fix #45: Does not accept standard input when running under Python 3.
* Feature: Clean up ``ChangeLog.rst`` for version and date numbers.


2014.9.25
=========
----

* Feature #29, #27: Add simple table support with bypass option.
* Fix #20: Replace project website with: https://alir3z4.github.io/html2text/ .


2014.9.8
========
----

* Fix #28: missing ``html2text`` package in installation.


2014.9.7
========
----

* Fix ``unicode``/``type`` error in memory leak unit-test.
* Feature #16: Remove ``install_deps.py``.
* Feature #17: Add status badges via pypin.
* Feature #18: Add ``Python`` ``3.4`` to travis config file.
* Feature #19: Bring ``html2text`` to a separate module and take out the ``conf``/``constant`` variables.
* Feature #21: Remove meta vars from ``html2text.py`` file header.
* Fix: Fix TypeError when parsing tags like <img src='foo' alt>. Fixed in #25.


2014.7.3
========
----

* Fix #8: Remove ``How to do a release`` section from README.md.
* Fix #11: Include test directory markdown, html files.
* Fix #13:  memory leak in using ``handle`` while keeping the old instance of ``html2text``.


2014.4.5
========
----

* Fix #1: Add ``ChangeLog.rst`` file.
* Fix #2: Add ``AUTHORS.rst`` file.
