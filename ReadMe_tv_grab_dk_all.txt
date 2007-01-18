Hvordan man nemt henter data fra seks-syv forskellige kilder i xmltv.

1) Hav python og perl installeret.

2) Installer tv2grabberen f.eks. fra XMLTV-modules.zip. Se hvordan det g�res p� windows i "README.w32.txt". P� fedora kan det g�res med "yum install xmltv" fra atrpms.

3) Download filegrabber.py fra gruppens filer

4) K�r "python filegrabber.py" *

5) Hvis du ikke k�rer *nix system eller ikke har tv2 grabberen liggende i
/usr/bin/tv_grab_dk skal du rette tv_grab_dk_all.py med den rigtige placering.
(Omkring linje 20)

6) K�r "python xmltv/tv_grab_dk_all.py --configure" **

7) K�r "python xmltv/tv_grab_dk_tdc.py" for at konfigurere tdc grabberen. Dens konfigurationsfil har et format 
som g�r at tv_grab_dk_all ikke kan konfigurere den direkte.

8) K�r "python xmltv/tv_grab_dk_all.py --out ud.xml" ***

Nu burde ud.xml v�re en fuld merged, timefixet etc. xmltvfil lige til at
fodre sine programmer med. N�r man senere k�rer grabberen igen, s�rger
den automatisk for at hente nyeste grabber/parser/util-filer fra
gruppen, s� alt er up to date****.

Grabberen er fuld stabil for mig, men sig endelig til, hvis den f.eks.
fejler p� et windowssystem.
Outputtet er ogs� meget rodet. Det burde dog ikke v�re vanskeligt at
rette i en senere version.

Det er muligt at sl� grabbere fra, s�tte flere grabbere til eller �ndre merge-r�kkef�lgen via linie 7 i 
tv_grab_dk_all.py:

   mergeorder = ("jubii","tv2","tdc","ahot","tvguiden","ontv")

Fjern de grabbere, som du ikke vil have startet eller skift r�kkef�lgen. F.eks har "tdc" mange titler p� originalsprog,
men hvis "tdc" ikke er den f�rste i merge r�kkef�lgen, s� bliver originalsprogstitlerne oftest skjult af den danske titel.
"tvguiden" har meget gode og lange beskrivelse til programmerne, men bytter ofte rundt i hvilke programmer der 
sendes hvorn�r. S� den er ofte �rsag til at programmer har forkert beskrivelse. Hvis dette er et problem for
dig, s� kan du sl� "tvguiden" fra.

Du kan ogs� tilf�je den svenske grabber tv_grab_se_swedb, da den har de fleste programmer som sendes via det 
svenske DVB-T net. Jeg mener at den grabberen f�lger med xmltv pakken, s� den burde ligge samme sted som tv2 
grabberen (tv_grab_dk). tv_grab_dk_all.py er forberedt til den svenske grabber, s� du skal bare tilf�je "swedb" 
i mergeorder tabellen.

--

Noter:

* Denne komando vil lave en mappe kaldet "xmltv" med alle n�dvendige
filer. Hvis du hellere vil have mappen et andet sted, eller med et andet
navn, s� ret det i sidste linje i filegrabber.py.
Du vil ogs� bliver spurgt om dit yahoo brugernavn og password, der
bruges til at hente filerne.

** Hvis man i starten har brug for at kalde tv_grab_dk_all.py ofte, kan
man med fordel bruge "--noupdate" kommandoen, s� tingene k�rer lidt
hurtigere.

*** Hvis tv_grab_dk_all.py kaldes uden et "--out" argument, bliver filen
gemt i samme mappe som tv_grab_dk_all.py (her xmltv) ved et navn ala
jubiitv2tdcahottvguidenontv_time.

**** Bem�rk at tv_grab_dk_all.py ikke automatisk opdaterer sig selv og
filegrabber.py. Skal disse filer opdateres, m� du enten selv k�re
filegrabber.py eller hente filerne i gruppen.
