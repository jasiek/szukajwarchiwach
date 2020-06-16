import os
import sys
import concurrent.futures
import requests

def fetch(i, url):
    try:
        response = requests.get(url.strip())
        # attachment; filename="29/338/0/1/1_7549212.jpg"
        _, filename = response.headers['content-disposition'].split("filename=")
        filename = filename.replace('"', '')
        filename = filename.replace('/', '-')
        filename = "%05d-" % i + filename
        with open(filename, "wb") as f:
            f.write(response.content)
            print(f"downloaded {filename}")
    except Exception:
        print(f'error on {filename}')
    
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("usage: downloader.py 31337")
        exit(1)
        
    set_id = str(int(sys.argv[1]))
    if not os.path.exists(set_id):
        os.mkdir(set_id)

    urls = open(f"sets/{set_id}").readlines()
    os.chdir(set_id)
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as executor:
        futures = [executor.submit(fetch, i, u) for (i, u) in enumerate(urls)]
        concurrent.futures.wait(futures)
            
