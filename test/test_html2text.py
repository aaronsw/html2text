import glob
import os
import re
import subprocess
import sys

import pytest

import html2text

skip = object()


def cleanup_eol(clean_str):
    if os.name == "nt" or sys.platform == "cygwin":
        # Fix the unwanted CR to CRCRLF replacement
        # during text pipelining on Windows/cygwin
        # on cygwin, os.name == 'posix', not nt
        clean_str = re.sub(r"\r+", "\r", clean_str)
        clean_str = clean_str.replace("\r\n", "\n")
    return clean_str


def generate_testdata():
    test_dir_name = os.path.dirname(os.path.realpath(__file__))
    for fn in glob.glob("%s/*.html" % test_dir_name):
        module_args = {}
        cmdline_args = []
        func_args = {}
        base_fn = os.path.basename(fn).lower()

        if base_fn.startswith("default_image_alt"):
            module_args["default_image_alt"] = "Image"
            cmdline_args.append("--default-image-alt=Image")
            func_args = skip

        if base_fn.startswith("google"):
            module_args["google_doc"] = True
            cmdline_args.append("--googledoc")
            func_args = skip

        if base_fn.find("unicode") >= 0:
            module_args["unicode_snob"] = True
            cmdline_args.append("--unicode-snob")
            func_args = skip

        if base_fn.find("flip_emphasis") >= 0:
            module_args["emphasis_mark"] = "*"
            module_args["strong_mark"] = "__"
            cmdline_args.append("-e")
            func_args = skip

        if base_fn.find("escape_snob") >= 0:
            module_args["escape_snob"] = True
            cmdline_args.append("--escape-all")
            func_args = skip

        if base_fn.find("table_bypass") >= 0:
            module_args["bypass_tables"] = True
            cmdline_args.append("--bypass-tables")
            func_args = skip

        if base_fn.startswith("table_ignore"):
            module_args["ignore_tables"] = True
            cmdline_args.append("--ignore-tables")
            func_args = skip

        if base_fn.startswith("bodywidth"):
            module_args["body_width"] = 0
            cmdline_args.append("--body-width=0")
            func_args["bodywidth"] = 0

        if base_fn.startswith("protect_links"):
            module_args["protect_links"] = True
            cmdline_args.append("--protect-links")
            func_args = skip

        if base_fn.startswith("images_as_html"):
            module_args["images_as_html"] = True
            cmdline_args.append("--images-as-html")
            func_args = skip

        if base_fn.startswith("images_to_alt"):
            module_args["images_to_alt"] = True
            cmdline_args.append("--images-to-alt")
            func_args = skip

        if base_fn.startswith("images_with_size"):
            module_args["images_with_size"] = True
            cmdline_args.append("--images-with-size")
            func_args = skip

        if base_fn.startswith("single_line_break"):
            module_args["body_width"] = 0
            cmdline_args.append("--body-width=0")
            module_args["single_line_break"] = True
            cmdline_args.append("--single-line-break")
            func_args = skip

        if base_fn.startswith("no_inline_links"):
            module_args["inline_links"] = False
            cmdline_args.append("--reference-links")
            func_args = skip

        if base_fn.startswith("no_mailto_links"):
            module_args["ignore_mailto_links"] = True
            cmdline_args.append("--ignore-mailto-links")
            func_args = skip

        if base_fn.startswith("no_wrap_links"):
            module_args["wrap_links"] = False
            cmdline_args.append("--no-wrap-links")
            func_args = skip

        if base_fn.startswith("mark_code"):
            module_args["mark_code"] = True
            cmdline_args.append("--mark-code")
            func_args = skip

        if base_fn.startswith("pad_table"):
            module_args["pad_tables"] = True
            cmdline_args.append("--pad-tables")
            func_args = skip

        if base_fn.startswith("wrap_list_items"):
            module_args["wrap_list_items"] = True
            cmdline_args.append("--wrap-list-items")
            func_args = skip

        if base_fn.startswith("wrap_tables"):
            module_args["wrap_tables"] = True
            cmdline_args.append("--wrap-tables")
            func_args = skip

        if base_fn == "inplace_baseurl_substitution.html":
            module_args["baseurl"] = "http://brettterpstra.com"
            module_args["body_width"] = 0
            func_args["baseurl"] = "http://brettterpstra.com"
            func_args["bodywidth"] = 0
            # CLI doesn't support baseurl.
            cmdline_args = skip

        yield fn, module_args, cmdline_args, func_args


def generate_module_testdata():
    for fn, module_args, cmdline_args, func_args in generate_testdata():
        yield fn, module_args


def generate_command_testdata():
    for fn, module_args, cmdline_args, func_args in generate_testdata():
        if cmdline_args is not skip:
            yield fn, cmdline_args


def generate_function_testdata():
    for fn, module_args, cmdline_args, func_args in generate_testdata():
        if func_args is not skip:
            yield fn, func_args


@pytest.mark.parametrize("fn,module_args", generate_module_testdata())
def test_module(fn, module_args):
    h = html2text.HTML2Text()
    h.fn = fn

    if module_args.pop("google_doc", False):
        h.google_doc = True
        h.ul_item_mark = "-"
        h.body_width = 0
        h.hide_strikethrough = True

    for k, v in module_args.items():
        setattr(h, k, v)

    result = get_baseline(fn)
    with open(fn) as inf:
        actual = cleanup_eol(inf.read())
        actual = h.handle(actual)
    assert result == actual


@pytest.mark.parametrize("fn,cmdline_args", generate_command_testdata())
def test_command(fn, cmdline_args):
    args = list(cmdline_args)
    cmd = [sys.executable, "-m", "html2text"]

    if "--googledoc" in args:
        args.remove("--googledoc")
        cmd += ["-g", "-d", "-b", "0", "-s"]

    if args:
        cmd.extend(args)

    cmd += [fn]

    result = get_baseline(fn)
    out = subprocess.check_output(cmd)

    actual = out.decode()

    actual = cleanup_eol(actual)

    assert result == actual


@pytest.mark.parametrize("fn,func_args", generate_function_testdata())
def test_function(fn, func_args):
    with open(fn) as inf:
        actual = html2text.html2text(inf.read(), **func_args)
    result = get_baseline(fn)
    assert result == actual


def get_baseline_name(fn):
    return os.path.splitext(fn)[0] + ".md"


def get_baseline(fn):
    name = get_baseline_name(fn)
    with open(name, encoding="utf-8") as f:
        out = f.read()
    return cleanup_eol(out)


def test_tag_callback():
    def _skip_certain_tags(h2t, tag, attrs, start):
        if tag == "b":
            return True

    h = html2text.HTML2Text()
    h.tag_callback = _skip_certain_tags
    ret = h.handle(
        'this is a <b>txt</b> and this is a <b class="skip">with text</b> and '
        "some <i>italics</i> too."
    )
    assert ret == ("this is a txt and this is a with text and some _italics_ too.\n\n")
