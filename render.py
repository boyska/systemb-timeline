#!/usr/bin/env python3
'''
from the json created by timeline.py, make a html ready for deck.js
'''

import jinja2
from datetime import datetime

jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader('templates'))
default_tmpl = 'slides.html'


def read_data(fname):
    import json
    return json.load(open(fname))


def datetimeformat(value, fmt='%d %b %Y'):
    date = datetime.fromtimestamp(int(value))
    native = date.replace(tzinfo=None)
    return native.strftime(fmt) 

jinja_env.filters['strftime'] = datetimeformat


def get_parser():
    import argparse
    p = argparse.ArgumentParser(description='Fetch a dipity.com story')
    p.add_argument('story', metavar='STORY_JSON', nargs=1,
                   help='the json file produced by timeline.py')
    p.add_argument('--out', metavar='HTML_OUT', default='-')
    return p


if __name__ == '__main__':
    args = get_parser().parse_args()
    d = read_data(args.story[0])
    tmpl = jinja_env.get_template(default_tmpl)
    out = tmpl.render(events=d, timeout=5000)
    if args.out == '-':
        print(out)
    else:
        with open(args.out, 'w') as buf:
            buf.write(out)
