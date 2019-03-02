# coding: utf-8
from setuptools import setup


def readall(f):
    with open(f) as fp:
        return fp.read()


setup(
    name="html2text",
    version=".".join(map(str, __import__("html2text").__version__)),
    description="Turn HTML into equivalent Markdown-structured text.",
    long_description=readall("README.md"),
    long_description_content_type="text/markdown",
    author="Aaron Swartz",
    author_email="me@aaronsw.com",
    maintainer="Alireza Savand",
    maintainer_email="alireza.savand@gmail.com",
    url="https://github.com/Alir3z4/html2text/",
    platforms="OS Independent",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU General Public License (GPL)",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
    ],
    python_requires=">=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*",
    entry_points={"console_scripts": ["html2text = html2text.cli:main"]},
    license="GNU GPL 3",
    packages=["html2text"],
)
