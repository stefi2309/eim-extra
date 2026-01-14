# eim-extra
Simulator avahi mDNS/DNS-SD CLI folosind libraria zeroconf

## Functionalitati:
- sa descopere toate tipurile de servicii anuntate in retea
- sa descopere instantele unui tip specific de serviciu
- sa rezolve serviciile descoperite (IP / port / TXT)
- sa urmareasca toate tipurile de servicii descoperite si instantele acestora
- sa ruleze continuu sau pentru un timp limitat

## Pentru utilizare:
- instalat zeroconf(comanda: pip install zeroconf)
- testat pe python 3.11 (cel mai sigur)

Pentru optiunile de comenzi, rulati: 
`python mdns_cli.py --help`

## Comenzi disponibile: 
1. Descoperirea tuturor tipurilor de servicii(echivalent avahi-browse -a):
   `python mdns_cli.py --all-types`
2. Descoperirea instantelor unui tip de serviciu(echivalent avahi-browse -k _chatservice._tcp):
   `python mdns_cli.py --type _chatservice._tcp`
3. Descoperire + rezolvare completa (IP, port, TXT) (echivalent avahi-browse -rk _chatservice._tcp):
   `python mdns_cli.py --type _chatservice._tcp --resolve`
4. Descoperirea tuturor tipurilor + instantele lor:
   `python mdns_cli.py --all-types --follow-types`
5. Descoperire completa pentru toate serviciile (tipuri + instante + rezolvare):
   `python mdns_cli.py --all-types --follow-types --resolve`
6. Afisare detaliata a evenimentelor (mod verbose). Afiseaza si evenimentele de tip update:
   `python mdns_cli.py --type _chatservice._tcp --resolve --verbose`
7. Rulare pentru o durata limitata:
   `python mdns_cli.py --type _chatservice._tcp --resolve --seconds 5`

Note importante:
- Scriptul foloseste UDP port 5353 (mDNS)
- Pe Windows trebuie permisa comunicarea Python in firewall
- Apasa Enter pentru oprire manuala sau foloseste --seconds pentru oprire automata

## In plus:
  Pentru a testa in afara wifi-ului de la facultate, ar fi indicat sa se foloseasca intr-un terminal separat scriptul de publisher care anunta explicit serviciul chatservice in retea.
  
  In plus, script-ul browse_chatservice realizeaza doar descoperirea serviciilor de tip _chatservice._tcp anuntate in reteaua locala, afisand evenimentele de aparitie, modificare si disparitie ale acestora. Este practic o varianta simpla si rapida pentru testare.
