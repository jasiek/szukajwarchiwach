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

## Gotchas

* Wygląda na to, że cały serwis jest stateful, tj polega na danych zapisanych w sesji, więc URL-e muszą być crawlowane
  w określonym porządku.
* PR-e mile widziane.
* Ktoś powinien z tego zrobić torrenty, bo czemu nie?


## Zespoły scrawlowane:

* [Urząd Zdrowia w Krakowie](sets/30904) - 40GB
* [Spis ludności miasta Krakowa z r. 1870](sets/30906) - 15GB
* [Spis ludności miasta Krakowa z r. 1880](sets/30907) - 36G
* [Spis ludności miasta Krakowa z r. 1890](sets/30908) ([szczegóły](sets/30908.md)) - 38GB
* [Spis ludności miasta Krakowa z r. 1900](sets/30909) - 15GB
* [Spis ludności miasta Krakowa z r. 1910](sets/30910) - 22GB
* [Akta stanu cywilnego Parafii Rzymskokatolickiej w Białym Kościele](sets/31534) - 832MB
* [Akta stanu cywilnego Parafii Rzymskokatolickiej w Giebułtowie](sets/34816) - 2.7GB
* [Akta stanu cywilnego Parafii Rzymskokatolickiej w Modlnicy Wielkiej](sets/31540) - 6.1GB
* [Akta Komisji Porządkowej Cywilno-Wojskowej Województwa Krakowskiego](sets/30674) - 15GB
* [Księgi Ziemskie Krakowskie](sets/30638) - 300GB (!)
* [Archiwum Miasta Kleparza](sets/30843) - 42GB
* [Akta stanu cywilnego Parafii Rzymskokatolickiej w Bolechowicach](sets/31533) - 6.8GB

