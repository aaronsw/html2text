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

* Fix #38: Anchor tags with empty text or with `<img>` tags inside are no longer stripped.


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

* Feature #49: Added a images_to_alt option to discard images and keep only their alt.
* Feature #50: Protect links, surrounding them with angle brackets to avoid breaking...
* Feature: Add ``setup.cfg`` file.


2014.12.5
=========
----

* Feature: Update `README.md` with usage examples.
* Fix #35: Remove `py_modules` from `setup.py`.
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
* Fix #20: Replace project website with: http://alir3z4.github.io/html2text/ .


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
