Tests
=====

Testing is essential.

Run the tests
-------------

`PYTHONPATH=$PYTHONPATH:. coverage run --source=html2text setup.py test -v`

Coverage results can be seen with

`coverage combine`

`coverage html`

and then opening the `./htmlcov/index.html` file with your browser.

New tests
---------
New tests are always welcome see [contributing](contributing.md) for guidelines.
