## RAG Qualitätssicherung

### 1) Bewertungskriterien
- Relevanz und Recall der abgerufenen Textausschnitte (erscheinen die richtigen Dokumente und Passagen?).
- Spezifität und Vollständigkeit (numerische Attribute, Produktcodes, IDs korrekt erfasst; Mehrfachfilter korrekt eingehalten).
- Robustheit gegenüber mehrsprachiger und domänenspezifischer Terminologie (deutsche Produktanfragen, Codes, SKUs).
- Latenz

### 2) Fragen zur Qualitätsbewertung
1. "Was ist die Farbtemperatur von SIRIUS HRI 330W 2/CS 1/SKU?"
2.  "Welche Leuchten sind gut für die Ausstattung im Operationssaal geeignet?"
3.  "Gebe mir alle Leuchtmittel mit mindestens 1000 Watt und Lebensdauer von mehr als 400 Stunden."
4. "Welche Leuchte hat die primäre Erzeugnisnummer 4062172212311?"

Zusätzlich dazu:
5. "Wie lautet die Familienmarke des Produkts mit dem Produktcode 54250?"
6. "Wie lautet die STK‑Nummer des Produkts mit dem Produktcode 4050300006741?"

### 3) Qualitätsicherung
Qualitätsicherung besteht aus 2 Teilen:
- Retrieval aus Dokumenten die per command line direkt hochgeladen werden
- Retrieval aus Dokumenten die von dem Ordner "data" hochgeladen wird

### 4) Ergebnisse

**Was ist die Farbtemperatur von SIRIUS HRI 330W 2/CS 1/SKU?**

Die Farbtemperatur des Produkts SIRIUS HRI 330W 2/CS 1/SKU (Family brand: SIRIUS HRI) beträgt 7400 K.

PASS

**Welche Leuchten sind gut für die Ausstattung im Operationssaal geeignet?**

Für Operationssäle werden in der Regel Hochleistungs‑Halogenlampen mit hoher Lichtleistung, stabiler Farbwiedergabe und engem Abstrahlverhalten eingesetzt. Aus den vorliegenden OSRAM‑Datenblättern sind insbesondere die OSRAM‑HLX‑ und HRI‑Familien zu nennen.

Empfohlene OSRAM‑Produkte (Beispiele aus den Datenblättern):
- OSRAM HRI‑Serie (z. B. HRI 371 W S+): hohe Intensität, geeignet für Anwendungen mit sehr hellem, punktförmigem Licht.  
- OSRAM HLX‑Hochleistungslampen: z. B. 64756 (1200 W, 230 V), 64721 / 64686 (650 W, 230/240 V), 64674 / 64672 (500 W, 230/240 V), 64673 / 64515 / 64516 (300 W, 230/240 V).  
- Kleinere Lampen für Kopf‑/Prüfleuchten oder Mikrochirurgie: z. B. 64222 (10 W, 6 V), 64647 (120 W, 24 V).

Wichtige Hinweise:
- Prüfen Sie vor Auswahl die relevanten Datenblätter (Lichtstrom, Farbtemperatur, Farbwiedergabe/CRI, Lebensdauer, elektrische Daten und Abstrahlcharakteristik).  
- Abstimmung mit dem Leuchtenhersteller ist erforderlich (mechanische/E‑Anforderungen, Kühlung, sterile Einsatzbedingungen).  
- Beachten Sie Wärmeabstrahlung und thermische Belastung im OP; moderne LED‑OP‑Leuchten können Vorteile (geringere Wärme, längere Lebensdauer, bessere Energieeffizienz) bieten und sollten bei Neuausstattung ebenfalls berücksichtigt werden.

Herstellerhinweis: Die genannten Lampen stammen aus dem OSRAM‑Programm (OSRAM HLX / OSRAM HRI). Für die endgültige Auswahl die jeweiligen OSRAM‑Produktdatenblätter und die Spezifikation des OP‑Leuchtenherstellers heranziehen.

PASS

**Gebe mir alle Leuchtmittel mit mindestens 1000 Watt und Lebensdauer von mehr als 400 Stunden.**

Aus dem bereitgestellten Kontext (OSRAM-Dokumente) sind folgende Leuchtmittel mit mindestens 1000 W ersichtlich:

- OSRAM 64744 — 1000 W, 240 V  
- OSRAM 64747 — 1000 W, 230 V  
- OSRAM 64748XS — 1000 W, 240 V  
- OSRAM 64752 — 1200 W, 230 V und 1200 W, 240 V (beide Varianten aufgeführt)  
- OSRAM 64754 — 1200 W, 230 V  
- OSRAM 64756 — 1200 W, 230 V

Die Dokumente gehören zur OSRAM-Familie (u. a. SIRIUS HRI / SIRIUS HRI XL / HLX werden im Kontext erwähnt).

Hinweis: Im bereitgestellten Ausschnitt sind keine Angaben zur Lebensdauer (Betriebsstunden) enthalten. Daher kann ich nicht sicher sagen, welche dieser Leuchtmittel eine Lebensdauer von mehr als 400 Stunden haben. Wenn Sie möchten, können Sie mir die vollständigen Produktdatenblätter hochladen oder ich kann gezielt nach den Lebensdauer-Angaben für die genannten OSRAM-Artikel suchen.

PASS

**Welche Leuchte hat die primäre Erzeugnisnummer 4062172212311?**

Die Primärartikelnummer 4062172212311 ist in den bereitgestellten technischen Daten nicht enthalten. Deshalb kann ich das zugehörige Leuchtmittel / die zugehörige Lampe aus diesen Unterlagen nicht identifizieren.

In den vorliegenden Daten sind unter anderem Produkte aus den Serien SIRIUS HRI (z. B. SIRIUS HRI 440 W, SIRIUS HRI 462 W) und verschiedene CP‑Lampentypen (z. B. CP/89, CP/91, CP/92 usw.) aufgeführt. Wenn Sie mir die vollständige Produktbeschreibung, die Global Order Reference (z. B. 64717, 64777 usw.) oder eine andere Artikelnummer geben, suche ich gern gezielt nach der Primärartikelnummer 4062172212311. Alternativ kann ich versuchen, in einer Produktdatenbank nachzuschauen, wenn Sie das wünschen.

Verification not possible

**Whats the family brand of the product with product code 54250?**

Produktnummer 54250 (BRJ/EVB 64633 HLX 150W 15V) gehört zur Family Brand XENOPHOT (HLX).

PASS

### 5) Schnelle Analyse

Hier sind meine Einschätzungen zum System und zu spezifischen Aspekten wie der Modellauswahl.

- Mehrsprachigkeit ist wichtig für sprach- und dokumentübergreifende Anwendungsfälle. Daher muss das Einbettungsmodell bei mehrsprachigen/metrikbezogenen Aufgaben sehr gut performen.
- Latenz ist ein zentrales Qualitätskriterium und in der aktuellen Architektur (LLM‑Kommunikation über API‑Aufrufe) unproblematisch. Alle getesteten Aufrufe dauerten weniger als 30 Sekunden. Das Retrieval ist ebenfalls sehr schnell; bei sehr vielen Dokumenten (10.000+) wird sich die Zeit jedoch leicht erhöhen.
- Antworten müssen definierten Richtlinien entsprechen; diese können dem Modell ausdrücklich als Anweisungen mitgegeben werden.