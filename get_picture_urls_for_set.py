import sys
import pdb
import requests
from scraper import *

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("usage: get_picture_urls_for_set.py <id>")
        exit(1)

    zespol_id = int(sys.argv[1])
    session = requests.Session()
    zbiory_crawler = Depaginator(session)
    for u in zbiory_crawler.crawl(
        jednostki_url_extractor(
            f"https://www.szukajwarchiwach.gov.pl/zespol/-/zespol/{zespol_id}", session
        ),
        jednostka_url_extractor,
    ):
        jednostki_crawler = Depaginator(session)
        for z in jednostki_crawler.crawl(u, picture_id_extractor):
            print(
                f"https://www.szukajwarchiwach.gov.pl/o/pliki-api/pliki/pobierzplikjpeg/{z}"
            )
