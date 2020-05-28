import re
import os
import sys
import concurrent.futures

# 29-30-0-3-43_8093284.jpg
# 29-83-0-1.1-171_42804506.jpg
# 29-90-0---13_26276696.jpg
filename_re = re.compile('^(\d+)-(\d+)-(\d+)-([\d\.-]+)?-(\d+)_(\d+).jpg$')

def update_tags(filename):
    match = re.match(filename_re, filename)
    groups = match.groups()
    sig = '/'.join(groups[0:5])
    image_description = f"Archiwum Narodowe w Krakowie, nazwa zespołu archiwalnego, sygn. {sig}. Oryginał dostepny w Archiwum Narodowym w Krakowie."
    return os.system(f'exiftran -i -g -p -c "{image_description}" {filename}')

if __name__ ==  "__main__":
    if len(sys.argv) < 2:
        print("usage: annotate_exif.py 31337")
        exit(1)
        
    set_id = str(int(sys.argv[1]))
    os.chdir(set_id)
    filenames = [f for f in os.listdir('.') if os.path.isfile(f) and f.endswith('.jpg')]

    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as executor:
        futures = [executor.submit(update_tags, f) for f in filenames]
        for f in concurrent.futures.as_completed(futures):
            if f.result != 0:
                print(f.result())
                exit(1)
            
