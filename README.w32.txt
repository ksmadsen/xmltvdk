Efterf�lgende vejledning er delt op i 7 dele. Ikke alle dele er n�dvendige for at f� et XMLTV baseret system 
op at st�:

Punkt 1 er n�dvendig hvis du vil k�re med grabberne som er beskrevet under punkt 2 eller 3. 

Punkt 2 er n�dvendig hvis du vil k�re med grabberen som henter fra tv2.dk. Den grabber henter afsnitsnumre til 
relativt mange udsendelser, men mangler sluttidspunkt for sidste udsendelse hver dag og har ikke afsnitsnavne 
for s�rlig mange udsendelser. 

Punkt 3 er n�dvendig hvis du vil k�re med grabberen som henter fra tdckabeltv.dk. Den grabber er god til at hente 
kategorier, afsnitsnavne og titler p� originalsprog, men mangler afsnitsnumre. 

Punkt 4 er n�dvendig hvis du vil k�re med grabberne som henter fra tv-guiden.dk, ahot.dk, jubii.dk eller ontv.dk 
eller hvis du vil kombinere flere grabbere (se punkt 6).

Punkt 5 kan bruges hvis du vil k�re med grabberne som henter fra tv-guiden.dk, ahot.dk, jubii.dk eller ontv.dk. 
Hvad de enkelte grabbere er specielt gode eller d�rlige til kan du se i filen grabbersammenligning.pdf, hvor 
grabberne er k�rt som test og skemaet viser hvor mange procent af udsendelserne, som havde de angivne 
informationer (tags). Det er lidt indforst�et: F.eks betyder tagget "sub-titleda" dansksproget afsnitsnavn. 

Punkt 6 kan bruges hvis du vil kombinere flere grabbere. 
Alternativt til punkt 6 kan man l�se i ReadMe_tv_grab_dk_all.txt om hvordan man bruger filegrabber.py til 
automatisk at downloade grabberne som er n�vnt under punkt 5 og k�re dem alle sammen med tdc og tv2 grabberne 
og kombinere outputtet.

Punkt 7 siger stort set bare at du skal kigge i dokumentationen til dit mediasoftware for at finde ud af 
hvordan du f�r den resulterende XMLTV fil ind og dette er selvf�lgelig n�dvendigt.

S� forskellige fremgangsm�der kunne v�re: 

Punkt 1+2+7 s� k�rer du p� tv2.dk 
Punkt 1+3+7 s� k�rer du p� tdckabeltv.dk 
Punkt 4+5+7 s� k�rer du f.eks p� ontv.dk 
Punkt 1+2+3+4+ReadMe_tv_grab_dk_all.txt+7, s� k�rer du p� en kombination af tdckabeltv.dk, tv2.dk, jubii.dk, 
ahot.dk, ontv.dk og tv-guiden.dk. Det giver f.eks de l�ngste beskrivelser til hvert program, b�de afsnitsnumre 
og afsnitsnavne etc. 

Kig i grabbersammenligning.pdf og find ud af hvilken grabber du helst vil starte med. Ontv.dk kan v�re et godt valg. 
Tdckabeltv.dk er bedre hvis du hellere vil have originaltitler end danske titler p� film. Start s� med en simpel 
l�sning (1+3+7 eller 4+5+7) til det valg. N�r du har f�et det op at st� og gerne vil have bedre/mere information i 
din EPG, s� pr�v den store l�sning (1+2+3+4+ReadMe_tv_grab_dk_all.txt+7).


1	ActivePerl til Windows
------------------------------

Grabberne til tv2.dk og tdckabeltv.dk er skrevet i Perl. S� for disse skal du have Perl installeret p� dit system.
Jeg foresl�r den gratis udgave af ActivePerl:
http://www.activestate.com/Products/Download/Download.plex?id=ActivePerl
N�r ActivePerl er installeret, skal der installeres nogle ekstra moduler.
Download XMLTV-modules.zip fra http://uk.groups.yahoo.com/group/xmltvdk/files/ og kopier indholdet af zip-filen ind i 
Perl mappen. F.eks. C:\Perl\
Endelig skal filen Manip.pm under C:\Perl\site\lib\Date\ redigeres som f�lgende:

# Local timezone
$Cnf{"TZ"}="";

skal �ndres til:

# Local timezone
$Cnf{"TZ"}="CET";


2	tv_grab_dk
------------------

tv_grab_dk henter dataene fra tv2's internetside.
For at bruge den skal den f�rst konfigureres:

C:\Perl\site\lib\xmltv\dk>Perl tv_grab_dk --configure

(Bem�rk at C:\Perl\bin skal registreres under Windows PATH variabel. Perl-installationen s�rger automatisk for dette.)
F�lg anvisningerne. Programmet vil sp�rge efter dit tv2-login og password. Det er ikke n�dvendigt og kr�ver flere moduler 
end dem fra XMLTV-modules.zip
Nu er du klar til at hente dataene:

C:\Perl\site\lib\xmltv\dk>Perl tv_grab_dk --output tv2.xml --days 7


3	tv_grab_dk_tdckabeltv
-----------------------------

Denne variant henter data fra tdckabeltv's internetside. Den fungerer p� samme m�de som tv_grab_dk.
Hent grabberen fra filsektionen: http://uk.groups.yahoo.com/group/xmltvdk/files/
og gem den under C:\Perl\site\lib\xmltv\dk\
konfigurer og hent data:

C:\Perl\site\lib\xmltv\dk>Perl tv_grab_dk_tdckabeltv --configure

C:\Perl\site\lib\xmltv\dk>Perl tv_grab_dk_tdckabeltv --output tdc.xml --days 7


4	Python
--------------
Endelig er der en del grabbere, der er skrevet i Python. Hent den her: 
http://www.python.org/ftp/python/2.4.2/python-2.4.2.msi
og installer den. Her skal du selv definere installationsmappen (som regel C:\Python24) som en PATH for Windows XP.
For at g�re dette skal du h�jreklikke p� Denne Computer og v�lge Egenskaber. V�lg fanen Advanceret og tryk p� 
Milj�variabler.
Marker variabel Path og tryk Rediger. Her tilf�jer du (uden at slette noget!): C:\Python24 og trykker Ok til det hele.


5	tv_grab_dk_tvguiden.py, tv_grab_dk_ahot.py, tv_grab_dk_jubii.py
-----------------------------------------------------------------------
Download de grabbere du vil bruge fra filsektionen og konfigurer/k�r dem som f�lgende:

C:\Perl\site\lib\xmltv\dk>Python tv_grab_dk_tvguiden.py --configure

C:\Perl\site\lib\xmltv\dk>Python tv_grab_dk_tvguiden.py > tvguiden.xml

...


6	Merge data
------------------
Med alle disse forskellige grabbere at v�lge imellem, kan det v�re sv�rt at beslutte hvilken en man skal bruge.
Som hj�lp kan du bruge oversigten grabbere.pdf fra filsektionen.
Men en anden mulighed er at bruge alle grabberne, for derefter at merge alle dataene sammen.
For at g�re dette skal man f�rst s�rge for at alle kanal-id'erne i xml-filerne er ens. Heldigvis er der ogs� et 
script til dette.
Download channelid.py og channelidparsefiler.zip fra filsektionen og gem dem samme sted som dine xml-filer (udpak 
filerne fra zip-filen).
K�r nu channelid-scriptet p� alle xml-filerne:

C:\Perl\site\lib\xmltv\dk>Python channelid.py --iso tv2parsefile tv2.xml tv2_id.xml

...

Nu kan dataene merges med scriptet xmltvmerger.py (fra filsektionen):

C:\Perl\site\lib\xmltv\dk>Python xmltvmerger.py jubii_id.xml ahot_id.xml epg_merge1.xml

C:\Perl\site\lib\xmltv\dk>Python xmltvmerger.py epg_merge1.xml tv2_id.xml epg_merge2.xml

C:\Perl\site\lib\xmltv\dk>Python xmltvmerger.py epg_merge2.xml tvguiden_id.xml epg_merge3.xml

C:\Perl\site\lib\xmltv\dk>Python xmltvmerger.py epg_merge3.xml tdc_id.xml epg_merged.xml

Alternativt kig i ReadMe_tv_grab_dk_all.txt som fort�ller hvordan man g�r alt dette automatisk ved hj�lp af
scriptet filegrabber.py


7	Importer dataene ind i EPG'en (EPG=Electronic Program Guide)
--------------------------------------------------------------------
N�r du har v�ret igennem det hele, s� skulle du gerne ende med det bedste fra alle grabberne i epg_merged.xml
Nu mangles der bare at importere det ind i din tv-software.
Hvordan dette g�res varieres fra program til program, s� det m� du selv finde ud af.
Bem�rk! Det er muligt at tv-softwaren kr�ver en xmltv.dtd fil. Denne kan skaffes fra den komplette xmltv-version:
http://sourceforge.net/project/showfiles.php?group_id=39046 - nyeste version til W32 i �jeblikket findes under 
xmltv-0.5.42a-win32.zip

Endelig kan du lave en batch-fil med alle kommandoerne og f� den til at opdatere din EPG hver dag ved hj�lp af 
Windows XP's Scheduler.
Husk: Du beh�ver kun at konfigurere grabberne een gang - medmindre du vil �ndre kanalerne.
Perl-grabberne gemmer en konfigurationsfil under .\.xmltv - gerne C:\Perl\site\lib\xmltv\dk\.xmltv
mens Python-grabberne gemmer dem under ~\.xmltv - gerne: C:\Documents and Settings\"Dit brugernavn"\.xmltv

Filen bladerunnerpro.rar i gruppens filsektion indeholder filer og vejledning (se readme.txt i arkivet).
Hvis du har problemer med at pakke filarkivet ud, s� brug evt http://7-zip.org.

# $Id$
