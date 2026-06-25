**Allgemeiner Ablauf des Algorithmus mit jeweiligem CI-Test:**  

| Schritt | Braucht den CI-Test? | Was passiert? |
|----|----|----|
| 1\. Variablen erkennen und Typen zuordnen | indirekt ja | nötig, damit der passende CI-Test weiß, wie er Variablen behandelt |
| 2\. CI-Tests ohne Kontrollvariablen | ja | marginale Unabhängigkeiten werden getestet |
| 3\. CI-Tests mit größeren Kontrollvariablen-Sets | ja | bedingte Unabhängigkeiten werden getestet |
| 4\. Kanten entfernen oder behalten | nutzt Testergebnis | auf Basis der p-Werte/CI-Entscheidungen |
| 5\. Separating Sets speichern | nutzt Testergebnis | das (Z), das (X) und (Y) getrennt hat, wird gespeichert |
| 6\. Kantenrichtungen bestimmen | nein, nicht direkt | nutzt Skeleton + Separating Sets + Orientierungsregeln |
| 7\. Finaler Graph | nein | Ergebnis der vorherigen Schritte |

Allgemein Informationen:

Zu 4.:

-Jeder CI-Test gibt einen p-Wert zurück

-Alpha lässt sich für jeden CI-Test tunen (größeres alpha macht H0 leichter verwerfbar → mehr Abhängigkeiten und dichterer Graph)

-Beim CI-Tests ist meist H0 Unabhängigkeit → X⊥Y∣Z → X und Y sind unabhängig gegeben Z

-wenn p größer als alpha dann bleibt H0 (Kante entfernen), sonst H1

**-alpha:** maximale type 1 error rate

**-p-Wert:** wie ungewöhnlich Daten wären, wenn H0 stimmt / Wie wahrscheinlich wäre ein Ergebnis, das mindestens so stark gegen H0​ spricht wie unser beobachtetes Ergebnis, ****wenn H0​ tatsächlich stimmt****?

------------------------------------------------------------------------------------------------------------------------

------------------------------------------------------------------------------------------------------------------------

Detallierte Beschreibung der verwendeten Tests:

**Conditional Gaussian**

Basiert auf likelihood-Vergleich in mixed-model:

-Nullmodell/H0: X und Y sind unabhägig gegeben Z

-Vollmodell/H1: X und Y sind abhängig gegeben Z

Annahmen:

-kontinuierliche Variablen sind bedingt auf kategoriale Gruppen ungefähr Gaussian-verteilt

-genug Beobachtungen pro kategoriale Gruppe für Messung der Kovarianz und stabile p-Werte

-erkennt lineare Abhänge, schwächer bei stark schiefen Verteilungen oder starker Nichtlinearität

-nimmt IID an

Mögliches Preprocessing für Conditional Gaussian:

-ggf. Bodyweight, Best3SquatKg, Age zu log-Werten transformieren → kann Schiefe von Verteilungen reduzieren

-Imbalancen von kategorischen Daten bei kleinen Gruppen → eventuell größere Gruppen bilden, um für alle kategorischen Gruppen genug Samples zu haben

-Year zu Perioden (Abschnitt) umwandeln → Annäherung an Gaussian-Verteilung, Reduzierung von Ausreißern, stabilere Gruppen, Nutzung von Year als kategorische Gruppierungsvariable

**zu 2. und 3. (individuelle CI-Tests)**

**Allgemeine Erklärungen:**

-Für jeden individuellen Test wird ein p-Wert zurückgeliefert (bei kleinen/instabilen Gruppen kann der Test scheitern/unzuverlässig werden)

-Die Orientierung der Varaiblen ist in diesem Schritt noch irrelevant

-Kategoriale Variablen definieren Gruppen bzw. kategoriale Konfigurationen:

- Kontinuierliche Variablen werden innerhalb dieser je Gruppen als ungefähr univariat/multivariat Gaussian modelliert (Abhängig der Anzahl)

<!-- -->

- Wenn nur kontinuierliche Variablen vorkommen, werden diese gemeinsam als ungefähr multivariat Gaussian modelliert.

<!-- -->

- Wenn kontinuierliche Kontrollvariablen in (Z) enthalten sind, werden sie aus kontinuierlichen Variablen herausgerechnet oder innerhalb der kategorischen Variablen, ihrer kategorischen Gruppen, als gaussian modelliert

<!-- -->

- Wenn kategoriale Kontrollvariablen in (Z) enthalten sind, wird die Unabhängigkeit innerhalb bzw. bedingt auf diese kategorialen Gruppen geprüft.

Detallierte Erklärungen zu Vorkommnissen mit Beispielen:

Ohne Kontrollvariablen:

→ wenn zwei kategorische Variablen geprüft werden: Sex⊥Equipment

- Unabhängig, wenn folgendes zutrifft: P(Sex,Equipment)=P(Sex)P(Equipment)
- Es wird geprüft, ob die gemeinsame Verteilung der Kategorien durch die Einzelverteilungen erklärt werden kann.

→ wenn eine kategorische und eine kontinuierliche Variable geprüft werden: Bodyweight⊥Sex

- Unabhängig, wenn: P(BodyweightKg∣Sex)=P(BodyweightKg)
- Es wird geprüft, ob sich die Verteilung von *BodyweightKg* zwischen den *Sex*-Gruppen unterscheidet. Die kontinuierliche Variable wird innerhalb der Gruppen ungefähr Gaussian modelliert.

→ wenn zwei kontinuierliche Variablen geprüft werden: Bodyweight⊥Best3SquatKg

- Unabhängig wenn Kovarianz = 0: Cov(BodyweightKg,Best3SquatKg)=0
- Die beiden Variablen werden gemeinsam als ungefähr multivariat Gaussian modelliert.

Mit Kontrollvariablen:

→ Wenn zwei kategorische Variablen geprüft werden und für eine kontinuierliche kontrolliert wird:

Sex⊥Equipment \| Bodyweight

- Hier wird geprüft, ob *Sex* und *Equipment* noch abhängig sind, wenn *BodyweightKg* berücksichtigt wird
- Die kontinuierliche Kontrollvariable wird in den möglichen kategorischen Gruppen der geprüften kategorischen Variablen jeweils als ungefähr gaussian modelliert

→ Wenn zwei kategorische Variablen geprüft werden und für eine kategorische kontrolliert wird:

Sex⊥Equipment \| ParentFederation

- Unabhängig wenn: P(Sex,Equipment∣ParentFederation)=P(Sex∣ParentFederation)P(Equipment∣ParentFederation)
- Hängen Sex und Equipment in der jeweiligen Parent Federation zusammen?

→ Wenn zwei kategorische Variablen geprüft werden und für kategorische sowie kontinuierliche kontrolliert wird: Sex⊥Equipment∣ParentFederation, BodyweightKg

- Unabhängig wenn: P(Sex,Equipment∣ParentFederation,BodyweightKg)=P(Sex∣ParentFederation,BodyweightKg)P(Equipment∣ParentFederation,BodyweightKg)
- Es wird im Hinblick auf die die kategorischen Gruppen der kategorsichen Kontrollvariable ParentFederation geprüft
- Die kontinuierlichen Variablen werden gaussian in den kategorischen Gruppen ausgehend von den kategorischen Kontrollvariablen modelliert

→ Wenn zwei kontinuierliche Variablen geprüft werden und für eine kontinuierliche kontrolliert wird: Bodyweight⊥BestSquat3Kg \| Age

- Es wird geprüft, ob *BodyweightKg* und *Best3SquatKg* noch zusammenhängen, nachdem *Age* berücksichtigt wurde. Alle kontinuierlichen Variablen werden dabei gemeinsam als ungefähr multivariat Gaussian modelliert.
- partielle Korrelation → entfernt Einflüsse von Kontrollvariable Age aus Bodyweight und BestSquat3Kg
- Bodyweight und BestSquat3Kg werden gemeinsam/multivariat als ungefähr gaussian modelliert

→ Wenn zwei kontinuierliche Variablen geprüft werden und für eine kategorische kontrolliert wird:

Bodyweight⊥BestSquat3Kg \| Sex

- Es wird geprüft, ob der Zusammenhang zwischen *BodyweightKg* und *Best3SquatKg* innerhalb der *Sex*-Gruppen bestehen bleibt.
- Die kontinuierlichen Variablen Bodyweight und BestSquat3Kg werden innerhalb der Sex-Gruppen multivariat gaussian modelliert

→ Wenn zwei kontinuierliche Variablen geprüft werden und für kategorische sowie kontinuierliche kontrolliert wird: Bodyweight⊥BestSquat3Kg \| Sex, Equipment, Age

- *Sex* und *Equipment* definieren kategoriale Gruppen. Innerhalb dieser Gruppen werden die geprüften kontinuierlichen Variablen: Bodyweight und BestSquat3Kg, als ungefähr Gaussian modelliert.
- Die Effekt der kontinuierlichen Kontrollvariable Age auf die geprüften Variablen Bodyweight und BestSquat3Kg wird herausgerechnet
- Kategorische Variablen bilden kategorische Gruppen in welchen die numerische Variablen ungefähr gaussian sind
- Der Effekt von kontinuerlichen Kontrollvariablen auf die geprüften kontinuierlichen Variablen wird herausgerechnet

------------------------------------------------------------------------------------------------------------------------

Detallierte Beschreibung der verwendeten Tests:

**G²**

Basiert auf likelihood-ratio-test für diskrete Variablen:

-Nullmodell/H0: X und Y sind unabhägig gegeben Z

-Vollmodell/H1: X und Y sind abhängig gegeben Z

→ Prüft, ob beobachtete Häufigkeiten stark von den Häufigkeiten abweichen, die man unter Unabhängigkeit erwarten würde

Annahmen:

-nur diskrete/kategorische Variablen (kontinuierliche werden vorher diskretisiert/gebinnt)

-kein gaussian-Annahme

-nimmt IID an

Risiken/Schwächen

-Keine zu kleinen Bins, sonst Gefahr mangelnder Samples pro kategorische Gruppe

-Informationsverlust durch Kodierung

-keine Ordnung: kontinuierliche Werte werden zu Klassen

-Bei großer Stichprobe können kleinere Effekte signifikant werden

Mögliches Preprocessing für G²:

-Sinnige Bins (Teilweise in ursprünglichem Datensatz vorhanden)

-Imbalancen von kategorischen Daten bei kleinen Gruppen → eventuell größere Gruppen bilden, um für alle kategorischen Gruppen genug Samples zu haben und zu vermeiden, dass sehr kleine Effekte signifikant werden

Detallierte Erklärungen zu Vorkommnissen mit Beispielen:

Ohne Kontrollvariablen:

Test berechnet:

<img src="Pictures/1000000000000239000000F07A8BE349.png" style="width:15.055cm;height:6.35cm" />

→ Beispiel: Sex⊥Equipment

1.  Man schaut in alle kategorischen Gruppen die sich durch Kombination von Sex und Equipment bilden lassen und gewinnt aus jeder Gruppe ihre beobachtete Häufigkeit
2.  Anschließend vergleicht man die beobachteten Häufigkeit mit den erwarteten Häufigkeiten von Sex und Equipment (Erwartet Häufigkeiten = Häufigkeitsverteilungen von Sex alleine, Häufigkeitsverteilungen von Equipment alleine)

Mit Kontrollvariablen:

→ Beispiel: Sex⊥Equipment∣ParentFederation

- Unabhängig wenn: P(Sex,Equipment∣ParentFederation)=P(Sex∣ParentFederation)P(Equipment∣ParentFederation)
- Hängen Sex und Equipment innerhalb derselben ParenFederation noch zusammen?
- Unabhängigkeit wird innerhalb der Gruppen von ParentFederation geprüft
