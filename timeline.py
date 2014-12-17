#!/usr/bin/env python3

import os.path
from urllib.request import urlopen, urlretrieve, urlparse
import json


def gen_url(story_id):
    '''story_id is sth like user/storyname'''
    return 'http://www.dipity.com/%s/json' % story_id


def get_data(story_id):
    url = gen_url(story_id)
    return json.loads(urlopen(url).read().decode('utf-8'))


def get_events(data, res_dir='.'):
    evs = sorted(data['events'].values(),
                 key=lambda e: int(e['utc_ts']))

    def update_img(ev):
        url = ev.get('img_url', None)
        if url:
            o = urlparse(url)
            fname = os.path.join(res_dir, os.path.basename(o.path))
            if not os.path.exists(res_dir):
                os.mkdir(res_dir)
            if not os.path.exists(fname):
                urlretrieve(url, fname)
            ev['img_cache'] = fname
        return ev
    evs = list(map(update_img, evs))
    return evs


def get_parser():
    import argparse
    p = argparse.ArgumentParser(description='Fetch a dipity.com story')
    p.add_argument('story', metavar='STORY_PATH', nargs=1,
                   help='sth like user/storyname')
    p.add_argument('--base-dir', metavar='BASEDIR', default='.')
    return p


if __name__ == '__main__':
    args = get_parser().parse_args()
    data = get_data(args.story[0])
    evs = get_events(data, os.path.join(args.base_dir, 'res'))
    with open(os.path.join(args.base_dir, 'story.json'), 'w') as buf:
        json.dump(evs, buf)
