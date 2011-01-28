import sys
from setuptools import setup, find_packages

setup(
   name = "html2text",
   version = "2.40",
   description = "Turn HTML into equivalent Markdown-structured text.",
   author = "Aaron Swartz",
   author_email = "me@aaronsw.com",
   url='http://www.aaronsw.com/2002/html2text/',
   classifiers=[
       'Development Status :: 5 - Production/Stable',
       'Intended Audience :: Developers',
       'License :: OSI Approved :: GNU General Public License (GPL)',
     ],
   license='GNU GPL 3',
   packages=find_packages(),
   py_modules=['html2text'],
   include_package_data=True,
   zip_safe=False,
)
