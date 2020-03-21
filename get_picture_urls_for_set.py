import sys
import pdb
import re
import requests
from bs4 import BeautifulSoup

jednostka_re = re.compile("^https://www.szukajwarchiwach.gov.pl/jednostka/-/jednostka/\d+")
site_re = re.compile("^https://www.szukajwarchiwach.gov.pl/")

class Depaginator:
    def __init__(self, session):
        self.s = session

    def _next_page_url(self, url):
        page = self.s.get(url)
        with open("url", "w") as f:
            f.write(page.text)
        soup = BeautifulSoup(page.content, 'html.parser')
        widget = soup.select("ul.pagination li a span.icon-caret-right")
        if widget != []:
            a = widget.parent
            href = a.get("href")
            if site_re.match(href):
                return href
        
    def paginate(self, url):
        yield url
        while True:
            url = self._next_page_url(url)
            if url:
                yield url
            else:
                break
        
    def crawl(self, url, extractor):
        for u in self.paginate(url):
            for x in extractor(u, self.s):
                yield x

def jednostka_url_extractor(url, session):
    page = session.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    elements = soup.select('td.col-md-5 a')
    for a in elements:
        href = a.get("href")
        if href and jednostka_re.match(href):
            yield href

def picture_id_extractor(url, session):
    page = session.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    elements = soup.select('div.jednostka-skan a.load-photo-slider')
    for e in elements:
        id = e.get("data-plikid")
        yield id

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("usage: get_picture_urls_for_set.py <id>")
        exit(1)

    zespol_id = int(sys.argv[1])
    session = requests.Session()
    zbiory_crawler = Depaginator(session)
    for u in zbiory_crawler.crawl("https://www.szukajwarchiwach.gov.pl/zespol?p_p_id=Zespol&p_p_lifecycle=1&p_p_state=normal&p_p_mode=view&_Zespol_javax.portlet.action=zmienWidok&_Zespol_nameofjsp=jednostki&_Zespol_id_zespolu={zespol_id}", jednostka_url_extractor):
        jednostki_crawler = Depaginator(session)
        for z in jednostki_crawler.crawl(u, picture_id_extractor):
            print("https://www.szukajwarchiwach.gov.pl/o/pliki-api/pliki/pobierzplikjpeg/{z}")

    
    
