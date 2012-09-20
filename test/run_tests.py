import codecs
import glob
import os
import re
import subprocess
import sys

sys.path.insert(0, '..')
import html2text


def test_module(fn, google_doc=False, **kwargs):
    print_conditions('module', google_doc=google_doc, **kwargs)

    h = html2text.HTML2Text()

    if google_doc:
        h.google_doc = True
        h.ul_item_mark = '-'
        h.body_width = 0
        h.hide_strikethrough = True

    for k, v in kwargs.iteritems():
        setattr(h, k, v)

    result = get_baseline(fn)
    actual = h.handle(file(fn).read())
    return print_result(fn, 'module', result, actual)

def test_command(fn, *args):
    print_conditions('command', *args)
    args = list(args)

    cmd = [sys.executable or 'python', '../html2text.py']

    if '--googledoc' in args:
        args.remove('--googledoc')
        cmd += ['-g', '-d', '-b', '0', '-s']

    if args:
        cmd.extend(args)

    cmd += [fn]

    result = get_baseline(fn)
    actual = subprocess.Popen(cmd, stdout=subprocess.PIPE).stdout.read()

    if os.name == 'nt':
        # Fix the unwanted CR to CRCRLF replacement
        # during text pipelining on Windows/cygwin
        actual = re.sub(r'\r+', '\r', actual)
        actual = actual.replace('\r\n', '\n')

    return print_result(fn, 'command', result, actual)

def print_conditions(mode, *args, **kwargs):
    format = " * %s %s, %s: "
    sys.stdout.write(format % (mode, args, kwargs))

def print_result(fn, mode, result, actual):
    if result == actual:
        print('PASS')
        return True
    else:
        print('FAIL')

        if mode == 'command':
            print(len(result), len(actual))

        dump_name = get_dump_name(fn, mode)

        f = codecs.open(dump_name, encoding='utf-8', mode='w+')
        f.write(actual)

        print("  Use: diff -u %s %s" % (get_baseline_name(fn), dump_name))
        return False

def get_dump_name(fn, suffix):
    return '%s-%s_output.md' % (os.path.splitext(fn)[0], suffix)

def get_baseline_name(fn):
    return os.path.splitext(fn)[0] + '.md'

def get_baseline(fn):
    name = get_baseline_name(fn)
    f = codecs.open(name, mode='r', encoding='utf8')
    return f.read()

def run_all_tests():
    html_files = glob.glob("*.html")
    passing = True
    for fn in html_files:
        module_args = {}
        cmdline_args = []

        if fn.lower().startswith('google'):
            module_args['google_doc'] = True
            cmdline_args.append('--googledoc')

        if fn.lower().find('unicode') >= 0:
            module_args['unicode_snob'] = True

        if fn.lower().find('flip_emphasis') >= 0:
            module_args['emphasis_mark'] = '*'
            module_args['strong_mark'] = '__'
            cmdline_args.append('-e')

        if fn.lower().find('escape_snob') >= 0:
            module_args['escape_snob'] = True
            cmdline_args.append('--escape-all')

        print('\n' + fn + ':')
        passing = passing and test_module(fn, **module_args)

        if not 'unicode_snob' in module_args: # Because there is no command-line option to control unicode_snob
            passing = passing and test_command(fn, *cmdline_args)
    if passing:
        print("ALL TESTS PASSED")
    else:
        print("Fail.")
        sys.exit(1)

if __name__ == "__main__":
    run_all_tests()
