import codecs
import glob
import os
import subprocess
import sys

sys.path.append('..')
import html2text


def test_module(fn, unicode_snob=False, google_doc=False):
    format = "%s (module, unicode_snob=%d, google_doc=%d): "
    sys.stdout.write(format % (fn, int(unicode_snob), int(google_doc)))

    h = html2text.HTML2Text()

    if unicode_snob:
        h.unicode_snob = True

    if google_doc:
        h.google_doc = True
        h.ul_item_mark = '-'
        h.body_width = 0
        h.hide_strikethrough = True

    result = get_baseline(fn, unicode_snob)
    actual_result = h.handle(file(fn).read())
    passed = result == actual_result

    if passed:
        print('PASS')
    else:
        print('FAIL')
        dump_name = get_dump_name(fn, 'module')
        open(dump_name, 'w').write(result)
        print("Use: diff -u %s %s" % (get_baseline_name(fn), dump_name))

    return passed


def get_dump_name(fn, suffix):
    return '%s-%s_output.md' % (os.path.splitext(fn)[0], suffix)


def get_baseline_name(fn):
    return os.path.splitext(fn)[0] + '.md'


def test_command(fn, google_doc=False):
    return True
    cmd = ['python', '../html2text.py']
    if fn.lower().startswith('google'):
        cmd += ['-g', '-d', '-b', '0', '-s']
    cmd += [fn]
    return subprocess.Popen(cmd, stdout=subprocess.PIPE).stdout.read()


def get_baseline(fn, unicode_snob=False):
    name = get_baseline_name(fn)
    if unicode_snob:
        with codecs.open(name, mode='r', encoding='utf8') as f:
            return f.read()
    else:
        return unicode(open(name).read())

# def print_result(out, baseline, fn):
#         if out == baseline:
#             print 'PASS'
#         else:
#             print 'FAIL'
#             file('output.md', 'w').write(out)
#             raise Exception("test failed: diff -u %s output.md" % fn.replace('.html', '.md'))


# def print_case(fn, mode, unicode_snob, google_doc):
#     format = "%s (%s, unicode_snob=%d, google_doc=%d): "
#     sys.stdout.write(format % (fn, mode, int(unicode_snob), int(google_doc)))


# def print_result(result, result_fn, dump_fn):
#     if result:
#         print('PASS')
#     else:
#         print('FAIL')
#         print("Use: diff -u %s %s" % (result_fn, dump_fn))


def run_all_tests():
    html_files = glob.glob("*.html")
    for fn in html_files:
        google_doc = fn.lower().startswith('google')
        unicode_snob = fn.lower().find('unicode') > 0

        test_module(fn, unicode_snob, google_doc)

        # print_case(fn, 'module', unicode_snob, google_doc)
        # print_result(test_module(fn, unicode_snob, google_doc))

        # if not unicode_snob:
        #     # (Because there is no command-line option to control unicode_snob)
            # print_case(fn, 'script', unicode_snob, google_doc)
            # print_result(test_command(fn, google_doc=False))
        # test_command(fn, google_doc=google_doc)


        # if unicode_snob:
        #     baseline = codecs.open(baseline_fn, mode='r', encoding='utf8').read()
        #     print '%s (module, unicode_snob=1):' % fn,
        #     out = test_module(fn, unicode_snob, google_doc)
        #     print_result(out, baseline, fn)

        # else:
        #     baseline = file(baseline_fn).read()

        #     print '%s (module):' % fn,
        #     out = test_module(fn, unicode_snob, google_doc)
        #     print_result(out, baseline, fn)

        #     print '%s (script):' % fn,
        #     out = test_command(fn)
        #     print_result(out, baseline, fn)

if __name__ == "__main__":
    run_all_tests()
