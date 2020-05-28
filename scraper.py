import re
import logging
from bs4 import BeautifulSoup

jednostka_re = re.compile(
    "^https://www.szukajwarchiwach.gov.pl/jednostka/-/jednostka/\d+"
)
site_re = re.compile("^https://www.szukajwarchiwach.gov.pl/")

class Depaginator:
    def __init__(self, session):
        self.s = session

    def _next_page_url(self, url):
        page = self.s.get(url)
        soup = BeautifulSoup(page.content, "html.parser")
        widget = soup.select("ul.pagination li a span.icon-caret-right")
        if widget == []:
            logging.error(f"url: {url} didn't have a pagination widget")
            return None
        a = widget[0].parent
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
    soup = BeautifulSoup(page.content, "html.parser")
    elements = soup.select("td.col-md-5 a")
    if elements == []:
        logging.error(f"{url} - brak jednostek")
        return
    for a in elements:
        href = a.get("href")
        if href and jednostka_re.match(href):
            logging.info(href)
            yield href

def serie_url_extractor(url, session):
    page = session.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    elements = soup.select(".odsylacze a.btn[href]")
    if elements == []:
        logging.error(f"{url} - brak linka do serii")
        return
    for a in elements:
        if a.text.strip().startswith("Serie"):
            page = session.get(a.get("href"))
            soup = BeautifulSoup(page.content, "html.parser")
            for e in soup.select(".jednostkaObiekty.row td.col-md-5 a"):
                yield e.get("href")
            

# Wyciąga identyfikator zdjęcia, które można pociągnąć przez "API"
def picture_id_extractor(url, session):
    page = session.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    elements = soup.select("div.jednostka-skan a.load-photo-slider")
    for e in elements:
        id = e.get("data-plikid")
        yield id

def picture_url_extractor(url, session):
    page = session.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    elements = soup.select("div.jednostka-skan a.load-photo-slider img")
    for e in elements:
        yield e.get("src").replace("_mid", "_max")
        


# Wyciąga link ze strony zespołu danych.
def jednostki_url_extractor(url, session):
    page = session.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    element = soup.select("a#przejdzDoJednostek")[0]
    return element.get("href")
