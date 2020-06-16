import json
import sys
import requests
from scraper import *

class BaseExtractor:
    def __init__(self, session):
        self.s = session

    def blend(self, url):
        page = self.s.get(url)
        return BeautifulSoup(page.content, "html.parser")
    
    def from_metadata_header(self, soup, label):
        elements = soup.select('div.metadaneJednostki.row div.border-left')
        for e in elements:
            if e.select("div.title")[0].text.strip() == label:
                return e.select("div.value")[0].text.strip()

    def text_of_css(self, soup, selector):
        element = soup.select(selector)[0]
        return element.text.strip()

    def extract_signature(self, soup):
        return self.from_metadata_header(soup, "Sygnatura")

    def extract_dates(self, soup):
        return self.from_metadata_header(soup, "Daty skrajne") or self.from_metadata_header(soup, "Daty")
    

class ZespolExtractor(BaseExtractor):
    def to_dict(self, url):
        soup = self.blend(url)
        return {
            "url": url,
            "sygnatura": self.extract_signature(soup),
            "archiwum": self.extract_archive(soup),
            "zawartosc": self.extract_contents(soup),
            "daty": self.extract_dates(soup),
            "dodatkowe_informacje": self.extract_extra_info(soup)
        }

    def extract_archive(self, soup):
        return self.from_metadata_header(soup, "Archiwum")

    def extract_contents(self, soup):
        return self.text_of_css(soup, "#opis_zespolu > div:nth-child(1) > div.col-md-9 > p > span")

    def extract_extra_info(self, soup):
        return self.text_of_css(soup, "#opis_zespolu > div:nth-child(14) > div > p > span")

class SeriaExtractor(BaseExtractor):
    def to_dict(self, url):
        soup = self.blend(url)
        return {
            "url": url,
            "sygnatura": self.extract_signature(soup),
            "daty": self.extract_dates(soup),
            "nazwa": self.extract_name(soup)
        }

    def extract_name(self, soup):
        return self.text_of_css(soup, "p.hide-long-tekst.hide-long.h2")

class JednostkaExtractor(BaseExtractor):
    def to_dict(self, url):
        soup = self.blend(url)
        return {
            "url": url,
            "sygnatura": self.extract_signature(soup),
            "nazwa": self.extract_name(soup),
            "daty": self.extract_dates(soup),
            "wielkosc": self.extract_size(soup)
        }

    def extract_name(self, soup):
        return self.text_of_css(soup, "div.tytulJednostki.col-md-10.hide-long-div > h2")

    def extract_size(self, soup):
        text = self.text_of_css(soup, "#_Jednostka_fm > div:nth-child(2) > div > h3")
        m = re.match('Skany \((\d+)\)', text)
        return int(m[1])

    
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(f"usage: {sys.argv[0]} <id>")
        exit(1)

    def crawl_jednostka(url, session):
        jednostki = []
        jednostka_extractor = JednostkaExtractor(session)
        jednostka = jednostka_extractor.to_dict(ju)
        jednostki.append(jednostka)
        jednostka["skany"] = []
        picture_ids = Depaginator(session).crawl(ju, picture_id_extractor)
        picture_urls = Depaginator(session).crawl(ju, picture_url_extractor)
        for id, url in zip(picture_ids, picture_urls):
            jednostka["skany"].append({"id": id, "url": url})
        return jednostki

    zespol_id = int(sys.argv[1])
    session = requests.Session()
    zespol_extractor = ZespolExtractor(session)
    zespol_dict = zespol_extractor.to_dict(f"https://www.szukajwarchiwach.gov.pl/zespol/-/zespol/{zespol_id}")
    zespol_dict["serie"] = []
    serie_urls = Depaginator(session).crawl(f"https://www.szukajwarchiwach.gov.pl/zespol/-/zespol/{zespol_id}", serie_url_extractor)
    if serie_urls:
        for su in serie_urls:
            seria_extractor = SeriaExtractor(session)
            seria = seria_extractor.to_dict(su)
            zespol_dict["serie"].append(seria)
            seria["jednostki"] = []
            jednostki_urls = Depaginator(session).crawl(seria["url"], jednostka_url_extractor)
            for ju in jednostki_urls:
                seria["jednostki"].append(crawl_jednostka(ju, session))
        else:
            zespol_dict["jednostki"] = []
            url = f"https://www.szukajwarchiwach.gov.pl/zespol?p_p_id=Zespol&p_p_lifecycle=1&p_p_state=normal&p_p_mode=view&_Zespol_javax.portlet.action=zmienWidok&_Zespol_nameofjsp=jednostki&_Zespol_id_zespolu={zespol_id}"
            jednostki_urls = Depaginator(session).crawl(url, jednostka_url_extractor)
            for ju in jednostki_urls:
                zespol_dict["jednostki"].append(crawl_jednostka(ju, session))
            
    print(json.dumps(zespol_dict))
