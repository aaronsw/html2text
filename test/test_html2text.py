import codecs
import glob
import html2text
import os
import re
import subprocess
import sys
import unittest


def cleanup_eol(clean_str):
    if os.name == 'nt' or sys.platform == 'cygwin':
        # Fix the unwanted CR to CRCRLF replacement
        # during text pipelining on Windows/cygwin
        # on cygwin, os.name == 'posix', not nt
        clean_str = re.sub(r'\r+', '\r', clean_str)
        clean_str = clean_str.replace('\r\n', '\n')
    return clean_str


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
    with open(fn) as inf:
        actual = cleanup_eol(inf.read())
        actual = h.handle(actual)
    return result, actual


def test_command(fn, *args):
    args = list(args)
    cmd = [sys.executable, '-m', 'html2text']

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

    actual = cleanup_eol(actual)

    return result, actual


def test_function(fn, **kwargs):
    with open(fn) as inf:
        actual = html2text.html2text(inf.read(), **kwargs)
    result = get_baseline(fn)
    return result, actual


def get_baseline_name(fn):
    return os.path.splitext(fn)[0] + '.md'


def get_baseline(fn):
    name = get_baseline_name(fn)
    with codecs.open(name, mode='r', encoding='utf8') as f:
        out = f.read()
    out = cleanup_eol(out)
    return out


class TestHTML2Text(unittest.TestCase):

    def test_html_escape(self):
        self.assertEqual(
            html2text.compat.html_escape('<pre>and then<div> & other tags'),
            '&lt;pre&gt;and then&lt;div&gt; &amp; other tags'
        )

    def test_unescape(self):
        self.assertEqual(
            '<pre>and then<div> & other tags',
            html2text.unescape(
                '&lt;pre&gt;and then&lt;div&gt; &amp; other tags'
            )
        )

    def _skip_certain_tags(self, h2t, tag, attrs, start):
        if tag == 'b':
            return True

    def test_tag_callback(self):
        h = html2text.HTML2Text()
        h.tag_callback = self._skip_certain_tags
        ret = h.handle(
            'this is a <b>txt</b> and this is a'
            ' <b class="skip">with text</b> and '
            'some <i>italics</i> too.'
        )
        self.assertEqual(
            ret,
            'this is a txt and this is a'
            ' with text and '
            'some _italics_ too.\n\n'
        )


def generate_test(fn):
    def _test_mod(self):
        self.maxDiff = None
        result, actual = test_module(fn, **module_args)
        self.assertEqual(result, actual)

    def _test_cmd(self):
        # Because there is no command-line option to control unicode_snob
        if 'unicode_snob' not in module_args:
            self.maxDiff = None
            result, actual = test_command(fn, *cmdline_args)
            self.assertEqual(result, actual)

    def _test_func(self):
        result, actual = test_function(fn, **func_args)
        self.assertEqual(result, actual)

    module_args = {}
    cmdline_args = []
    func_args = {}
    skip_func = False
    base_fn = os.path.basename(fn).lower()

    if base_fn.startswith('default_image_alt'):
        module_args['default_image_alt'] = 'Image'
        cmdline_args.append('--default-image-alt=Image')
        skip_func = True

    if base_fn.startswith('google'):
        module_args['google_doc'] = True
        cmdline_args.append('--googledoc')
        skip_func = True

    if base_fn.find('unicode') >= 0:
        module_args['unicode_snob'] = True
        skip_func = True

    if base_fn.find('flip_emphasis') >= 0:
        module_args['emphasis_mark'] = '*'
        module_args['strong_mark'] = '__'
        cmdline_args.append('-e')
        skip_func = True

    if base_fn.find('escape_snob') >= 0:
        module_args['escape_snob'] = True
        cmdline_args.append('--escape-all')
        skip_func = True

    if base_fn.find('table_bypass') >= 0:
        module_args['bypass_tables'] = True
        cmdline_args.append('--bypass-tables')
        skip_func = True

    if base_fn.startswith('table_ignore'):
        module_args['ignore_tables'] = True
        cmdline_args.append('--ignore-tables')
        skip_func = True

    if base_fn.startswith('bodywidth'):
        # module_args['unicode_snob'] = True
        module_args['body_width'] = 0
        cmdline_args.append('--body-width=0')
        func_args['bodywidth'] = 0

    if base_fn.startswith('protect_links'):
        module_args['protect_links'] = True
        cmdline_args.append('--protect-links')
        skip_func = True

    if base_fn.startswith('images_as_html'):
        module_args['images_as_html'] = True
        cmdline_args.append('--images-as-html')
        skip_func = True

    if base_fn.startswith('images_to_alt'):
        module_args['images_to_alt'] = True
        cmdline_args.append('--images-to-alt')
        skip_func = True

    if base_fn.startswith('images_with_size'):
        module_args['images_with_size'] = True
        cmdline_args.append('--images-with-size')
        skip_func = True

    if base_fn.startswith('single_line_break'):
        module_args['body_width'] = 0
        cmdline_args.append('--body-width=0')
        module_args['single_line_break'] = True
        cmdline_args.append('--single-line-break')
        skip_func = True

    if base_fn.startswith('no_inline_links'):
        module_args['inline_links'] = False
        cmdline_args.append('--reference-links')
        skip_func = True

    if base_fn.startswith('no_wrap_links'):
        module_args['wrap_links'] = False
        cmdline_args.append('--no-wrap-links')
        skip_func = True

    if base_fn.startswith('mark_code'):
        module_args['mark_code'] = True
        cmdline_args.append('--mark-code')
        skip_func = True

    if base_fn.startswith('pad_table'):
        module_args['pad_tables'] = True
        cmdline_args.append('--pad-tables')
        skip_func = True

    if base_fn.startswith('wrap_list_items'):
        module_args['wrap_list_items'] = True
        cmdline_args.append('--wrap-list-items')
        skip_func = True

    if base_fn == 'inplace_baseurl_substitution.html':
        module_args['baseurl'] = 'http://brettterpstra.com'
        module_args['body_width'] = 0
        func_args['baseurl'] = 'http://brettterpstra.com'
        func_args['bodywidth'] = 0
        # there is no way to specify baseurl in cli :(
        test_cmd = None
    else:
        test_cmd = _test_cmd

    if skip_func:
        test_func = None
    else:
        test_func = _test_func

    return _test_mod, test_cmd, test_func


# Originally from https://stackoverflow.com/q/32899
#    how-to-generate-dynamic-parametrized-unit-tests-in-python
test_dir_name = os.path.dirname(os.path.realpath(__file__))
for fn in glob.glob("%s/*.html" % test_dir_name):
    test_name = 'test_%s' % os.path.splitext(os.path.basename(fn))[0].lower()
    test_m, test_c, test_func = generate_test(fn)
    setattr(TestHTML2Text, test_name + "_mod", test_m)
    if test_c:
        setattr(TestHTML2Text, test_name + "_cmd", test_c)
    if test_func:
        setattr(TestHTML2Text, test_name + "_func", test_func)
