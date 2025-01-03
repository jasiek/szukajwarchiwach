import re
import os
import sys
import concurrent.futures
from urllib.parse import urlparse
from PIL import Image

def check(filename):
    im = Image.open(filename)
    if im.format != 'JPEG':
        print(f'{filename}: not jpeg')

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("usage: quality_control.py <set_id>")
        exit(1)

    set_id = str(int(sys.argv[1]))
    if not os.path.exists(set_id):
        print(f"directory not found: {set_id}")
        exit(1)
    if not os.path.exists(f"sets/{set_id}"):
        print(f"file list does not exist: sets/{set_id}")
        exit(1)

    urls = open(f"sets/{set_id}").readlines()
    os.chdir(set_id)

    to_fetch_ids = set([urlparse(u).path.split('/')[-1].strip() for u in urls])
    # sanity check
    for i in to_fetch_ids:
        int(i)

    fetched_filenames = [f for f in os.listdir('.') if os.path.isfile(f) and f.endswith('.jpg')]
    fetched_ids = set([f.split('_')[-1].split('.')[0] for f in fetched_filenames])
    for i in fetched_ids:
        int(i)

    missing = to_fetch_ids - fetched_ids
        
    if len(missing) > 0:
        print("missing files: ")
        for i in missing:
            print(i)
        # grep -E <output> sets/<id> > sets/1
        print('|'.join(missing))
        exit(1)

    for f in fetched_filenames:
        check(f)
    print('OK')
