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

## Gotchas

* Wygląda na to, że cały serwis jest stateful, tj polega na danych zapisanych w sesji, więc URL-e muszą być crawlowane
  w określonym porządku.
* PR-e mile widziane.


## Zespoły scrawlowane:

* [Spis ludności miasta Krakowa z r. 1870](sets/30906)
* [Spis ludności miasta Krakowa z r. 1880](sets/30907)
* [Spis ludności miasta Krakowa z r. 1890](sets/30908)
* [Spis ludności miasta Krakowa z r. 1900](sets/30909)
* [Spis ludności miasta Krakowa z r. 1910](sets/30910)
* [Urząd Zdrowia w Krakowie](sets/30904)

