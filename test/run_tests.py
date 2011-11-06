import glob
import subprocess
import sys; sys.path.append('..')
import html2text

def test_module(fn):
    h = html2text.HTML2Text()
    if fn.lower().startswith('google'):
        h.google_doc = True
        h.ul_item_mark = '-'
        h.body_width = 0
        h.hide_strikethrough = True
    
    return h.handle(file(fn).read())

def test_command(fn):
    cmd = ['python', '../html2text.py']
    if fn.lower().startswith('google'):
        cmd += ['-g', '-d', '-b', '0', '-s']
    cmd += [fn]
    return subprocess.Popen(cmd, stdout=subprocess.PIPE).stdout.read()

def print_result(out, baseline, fn):
        if out == baseline:
            print 'PASS'
        else:
            print 'FAIL'
            file('output.md', 'w').write(out)
            raise Exception("test failed: diff -u %s output.md" % fn.replace('.html', '.md'))

def run_all_tests():
    html_files = glob.glob("*.html")
    for fn in html_files:
        
        baseline = file(fn.replace('.html', '.md')).read()

        print '%s (module):' % fn,
        out = test_module(fn)
        print_result(out, baseline, fn)
        
        print '%s (script):' % fn,
        out = test_command(fn)
        print_result(out, baseline, fn)
        

if __name__ == "__main__":
    run_all_tests()
