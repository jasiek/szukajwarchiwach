# szukajwarchiwach

Skrypty do scape-owania serwisu www.szukajwarchiwach.gov.pl

## Motywacja

Serwis www.szukajwarchiwach.gov.pl jest kiepski. Nie da się w sensowny sposób wyszukiwać danych (wyszukiwarka tekstowa
prawie nie działa), interfejs użytkownika nie jest zaprojektowany pod kątem użytkownika. Postanowiłem, że łatwiej jest
mi ściągnąć wszystkie dane które mnie interesują a następnie ręcznie przejrzeć podzbiór który mnie interesuje lokalnie.

## Użytkowanie

```
python get_picture_urls_for_set.py 31337 > sets/31337
```

Crawluje zespół danych nr 31337 a następnie w pliku `sets/31337` zapisuje URL-e wszystkich skanów, w formacie który
potem pozwala na ściągnięcie za pośrednictwem wget.


```
python downloader.py 31337
```

Tworzy nowy katalog `31337`, o ile nie został stworzony, następnie za pomocą 8 wątków ściąga dane - zapisując je w
pliku z użyteczną nazwą. Brak obsługi błędów, wyjątki rzucone w wątkach są ignorowane.


Aby sprawdzić czy wszystkie pliki się ściągnęły, oraz czy nie są uszkodzone (są poprawnymi plikami JPEG), należy uruchomić:


```
python quality_control.py 31337
```


## Gotchas

* Wygląda na to, że cały serwis jest stateful, tj polega na danych zapisanych w sesji, więc URL-e muszą być crawlowane
  w określonym porządku.
* PR-e mile widziane.
* Ktoś powinien z tego zrobić torrenty, bo czemu nie?


## Zespoły scrawlowane:

* [Urząd Zdrowia w Krakowie](https://www.szukajwarchiwach.gov.pl/en/zespol/-/zespol/30904) - 40GB [lista plików](sets/30904)
* [Spis ludności miasta Krakowa z r. 1870](https://www.szukajwarchiwach.gov.pl/en/zespol/-/zespol/30906) - 15GB [lista plików](sets/30906)
* [Spis ludności miasta Krakowa z r. 1880](https://www.szukajwarchiwach.gov.pl/en/zespol/-/zespol/30907) - 36G [lista plików](sets/30907)
* [Spis ludności miasta Krakowa z r. 1890](https://www.szukajwarchiwach.gov.pl/en/zespol/-/zespol/30908) ([szczegóły](sets/30908.md)) - 38GB [lista plików](sets/30908)
* [Spis ludności miasta Krakowa z r. 1900](https://www.szukajwarchiwach.gov.pl/en/zespol/-/zespol/30909) - 15GB [lista plików](sets/30909)
* [Spis ludności miasta Krakowa z r. 1910](https://www.szukajwarchiwach.gov.pl/en/zespol/-/zespol/30910) - 22GB [lista plików](sets/30910)
* [Akta stanu cywilnego Parafii Rzymskokatolickiej w Białym Kościele](https://www.szukajwarchiwach.gov.pl/en/zespol/-/zespol/31534) - 832MB [lista plików](sets/31534)
* [Akta stanu cywilnego Parafii Rzymskokatolickiej w Giebułtowie](https://www.szukajwarchiwach.gov.pl/en/zespol/-/zespol/34816) - 2.7GB [lista plików](sets/34816)
* [Akta stanu cywilnego Parafii Rzymskokatolickiej w Modlnicy Wielkiej](https://www.szukajwarchiwach.gov.pl/en/zespol/-/zespol/31540) - 6.1GB [lista plików](sets/31540)
* [Akta Komisji Porządkowej Cywilno-Wojskowej Województwa Krakowskiego](https://www.szukajwarchiwach.gov.pl/en/zespol/-/zespol/30674) - 15GB [lista plików](sets/30674)
* [Księgi Ziemskie Krakowskie](https://www.szukajwarchiwach.gov.pl/en/zespol/-/zespol/30638) - 300GB (!) [lista plików](sets/30638)
* [Archiwum Miasta Kleparza](https://www.szukajwarchiwach.gov.pl/en/zespol/-/zespol/30843) - 42GB [lista plików](sets/30843)
* [Akta stanu cywilnego Parafii Rzymskokatolickiej w Bolechowicach](https://www.szukajwarchiwach.gov.pl/en/zespol/-/zespol/31533) - 6.8GB [lista plików](31533)

