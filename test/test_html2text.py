import codecs
import glob
import os
import re
import subprocess
import sys

if sys.version_info[:2] < (2, 7):
    import unittest2 as unittest
else:
    import unittest
import logging

logging.basicConfig(format='%(levelname)s:%(funcName)s:%(message)s',
                    level=logging.DEBUG)

import html2text


def test_module(fn, google_doc=False, **kwargs):
    h = html2text.HTML2Text()
    h.fn = fn

    if google_doc:
        h.google_doc = True
        h.ul_item_mark = '-'
        h.body_width = 0
        h.hide_strikethrough = True

    for k, v in kwargs.items():
        setattr(h, k, v)

    result = get_baseline(fn)
    inf = open(fn)
    actual = h.handle(inf.read())
    inf.close()
    return result, actual


def test_command(fn, *args):
    args = list(args)
    cmd_name = os.path.join(os.path.dirname(fn), '..', 'html2text/__init__.py')
    cmd = [sys.executable, cmd_name]

    if '--googledoc' in args:
        args.remove('--googledoc')
        cmd += ['-g', '-d', '-b', '0', '-s']

    if args:
        cmd.extend(args)

    cmd += [fn]

    result = get_baseline(fn)
    pid = subprocess.Popen(cmd, stdout=subprocess.PIPE)
    out, _ = pid.communicate()

    actual = out.decode('utf8')

    if os.name == 'nt':
        # Fix the unwanted CR to CRCRLF replacement
        # during text pipelining on Windows/cygwin
        actual = re.sub(r'\r+', '\r', actual)
        actual = actual.replace('\r\n', '\n')

    return result, actual


def get_dump_name(fn, suffix):
    return '%s-%s_output.md' % (os.path.splitext(fn)[0], suffix)


def get_baseline_name(fn):
    return os.path.splitext(fn)[0] + '.md'


def get_baseline(fn):
    name = get_baseline_name(fn)
    f = codecs.open(name, mode='r', encoding='utf8')
    out = f.read()
    f.close()
    return out


class TestHTML2Text(unittest.TestCase):
    pass


def generate_test(fn):
    def test_mod(self):
        self.maxDiff = None
        result, actual = test_module(fn, **module_args)
        self.assertEqual(result, actual)

    def test_cmd(self):
        # Because there is no command-line option to control unicode_snob
        if not 'unicode_snob' in module_args:
            self.maxDiff = None
            result, actual = test_command(fn, *cmdline_args)
            self.assertEqual(result, actual)

    module_args = {}
    cmdline_args = []
    base_fn = os.path.basename(fn).lower()

    if base_fn.startswith('google'):
        module_args['google_doc'] = True
        cmdline_args.append('--googledoc')

    if base_fn.find('unicode') >= 0:
        module_args['unicode_snob'] = True

    if base_fn.find('flip_emphasis') >= 0:
        module_args['emphasis_mark'] = '*'
        module_args['strong_mark'] = '__'
        cmdline_args.append('-e')

    if base_fn.find('escape_snob') >= 0:
        module_args['escape_snob'] = True
        cmdline_args.append('--escape-all')

    if base_fn.find('table_bypass') >= 0:
        module_args['bypass_tables'] = True
        cmdline_args.append('--bypass-tables')

    if base_fn.startswith('bodywidth'):
        #module_args['unicode_snob'] = True
        module_args['body_width'] = 0
        cmdline_args.append('--body-width=0')

    return test_mod, test_cmd

# Originally from http://stackoverflow.com/questions/32899/\
#    how-to-generate-dynamic-parametrized-unit-tests-in-python
test_dir_name = os.path.dirname(os.path.realpath(__file__))
for fn in glob.glob("%s/*.html" % test_dir_name):
    test_name = 'test_%s' % os.path.splitext(os.path.basename(fn))[0].lower()
    test_m, test_c = generate_test(fn)
    setattr(TestHTML2Text, test_name + "_mod", test_m)
    if test_c:
        setattr(TestHTML2Text, test_name + "_cmd", test_c)

if __name__ == "__main__":
    unittest.main()
