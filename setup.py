# coding: utf-8
import sys
from setuptools import setup, Command, find_packages

requires_list = []
try:
    import unittest2 as unittest
except ImportError:
    import unittest
else:
    if sys.version_info <= (2, 6):
        requires_list.append("unittest2")


class RunTests(Command):
    """New setup.py command to run all tests for the package.
    """
    description = "run all tests for the package"

    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        tests = unittest.TestLoader().discover('.')
        runner = unittest.TextTestRunner()
        results = runner.run(tests)
        sys.exit(not results.wasSuccessful())


setup(
    name="html2text",
    version="2015.2.18",
    description="Turn HTML into equivalent Markdown-structured text.",
    author="Aaron Swartz",
    author_email="me@aaronsw.com",
    maintainer='Alireza Savand',
    maintainer_email='alireza.savand@gmail.com',
    url='https://github.com/Alir3z4/html2text/',
    cmdclass={'test': RunTests},
    platforms='OS Independent',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.4',
        'Programming Language :: Python :: 2.5',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.0',
        'Programming Language :: Python :: 3.1',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3'
    ],
    entry_points="""
        [console_scripts]
        html2text=html2text.cli:main
    """,
    license='GNU GPL 3',
    requires=requires_list,
    packages=find_packages(exclude=['test']),
    include_package_data=True,
    zip_safe=False,
)
