# Generator Testova

## Opis

_Generator Testova_ je program za automatsko generisanje testova za teorijsku provjeru znanja. Učitava podatke iz Excel formulara (_.xlsm_ fajl) i na osnovu tih podataka kreira poseban Word dokument sa odabranim pitanjima za svaku oblast. Svi dokumenti za jednog kandidata su sačuvani u folderu sa imenom tog kandidata.

## Funkcionalnosti

- Sva podešavanja se unose u Excel formular
- Automatsko generisanje Word dokumenata sa izabranim pitanjima za svaku oblast
- Organizovanje generisanih testova u posebne foldere po kandidatu

## Zahtijevi

- Windows operativni sistem

## Korišćenje

1. Preuzmite najnoviju verziju sa [stranice sa izdanjima](https://github.com/goranstevanovic/bhansa-generator-testova/releases)
1. Raspakujte ZIP arhivu
1. Popunite folder `baza/pitanja` folderima i pitanjima za svaku oblast
1. Priložite, popunite i sačuvajte Excel formular (_.xlsm_)
1. Pokrenite `generator-testova.exe`
