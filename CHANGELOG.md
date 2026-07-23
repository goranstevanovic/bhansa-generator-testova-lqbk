# Istorija izmijena

## [1.7.0] - 2026-07-23

### Izmjenjeno

- Promjenjena struktura fajlova i foldera neophodnih za rad programa
- Program sadrži dodatne foldere `lib`, `licenses` i `share`
- Program sadrži dodatni fajl `python314.dll`

## [1.6.4] - 2026-07-22

### Ispravljeno

- Umjesto samo jednog fajla (`generator-testova.exe`), program sadrži i folder sa ostalim potrebnim fajlovima (`_internal`)
- Koristeći samo jedan fajl, bez pratećeg foldera, može uzrokovati da neki anti-virus programi prepoznaju ovaj program kao virus

## [1.6.3.] - 2026-07-16

### Ispravljeno

- Arhiva programa za distribuciju sadrži korisničko uputstvo

## [1.6.2] - 2026-07-16

### Ispravljeno

- Sve stranice osim prve (naslovne) su numerisane

## [1.6.1] - 2026-07-14

### Ispravljeno

- Čuvanje izgleda pitanja i odgovora u generisanim dokumentima (izgled slova, tačkice i brojevi u listama...)

## [1.6.0] - 2026-07-13

### Izmjenjeno

- Redni broj pitanja u generisanim dokumenetima je redni broj iz baze, a ne redni broj u tom dokumentu
- Umjesto da pitanja budu numerisana 1, 2, 3..., numerisana su npr. 2, 3, 5

## [1.5.0] - 2026-07-12

### Izmjenjeno

- Generisanje jednog dokumenta sa odabranim pitanjima, umjesto posebnog dokumenta za svaku oblast
- Generisanje jednog dokumenta sa odgovorima na odabrana pitanja, umjesto posebnog dokumenta za svaku oblast

## [1.4.1] - 2026-07-10

### Ispravljeno

- Program prepoznaje i generiše testove za oblasti sa dvoslovnom skraćenicom

## [1.4.0] - 2026-07-09

### Izmjenjeno

- Tekst korisničkog interfejsa programa, poruke u programu i korisničko uputstvo promijenjeni u ćirilicu

## [1.3.0] - 2026-07-08

### Izmjenjeno

- Program prilagođen tabelarnom stilu pitanja i odgovora, koji se koristi u JPAKL Banja Luka

## [1.2.0] - 2026-04-24

### Dodato

- Automatsko generisanje Word dokumenata sa odgovorima na pitanja, ukoliko su u bazi dostupni odgovori
- Ukoliko nisu dostupni odgovori na sva potrebna pitanja, dokument sa odgovorima za tu oblast se ne generiše
- Prikazivanje oblasti za koje nisu dostupni odgovori na sva pitanja, kao i lista pitanja za koja nedostaju odgovori

## [1.1.0] - 2026-04-17

### Dodato

- Provjeravanje da li su dostupna sva potrebna pitanja za generisanje testa za svaku oblast
- Kreiranje testova samo za oblasti za koje su dostupna sva potrebna pitanja
- Prikazivanje oblasti za koje nisu dostupna sva pitanja, kao i lista nedostupnih pitanja

## [1.0.1] - 2026-04-07

### Ispravljeno

- Kreiranje Windows verzije programa

## [1.0.0] - 2026-04-07

### Dodato

- Prvo izdanje
- Sva podešavanja u Excel formularu
- Automatsko generisanje Word dokumenata sa pitanjima
- Organizovanje generisanih testova u posebne foldere po kandidatu
- Uputstvo za upotrebu
