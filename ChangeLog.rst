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
