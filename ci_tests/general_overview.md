# Allgemeine Übersicht

Wir entscheiden uns, wenige Tests zu wählen, mit denen wir uns kritisch auseinandersetzen, statt viele verschiedene auszuprobieren. Alle gewählten Tests eignen sich für die Arbeit mit PC und FCI.

**Testwahl**

- Haupttest: Conditional Gaussian
    - Weil: geeignet für mixed-data → kann kontinuierliche und kategorische Variablen gemeinsam modellieren, ohne Diskretisierung oder numerische Kodierung
        - Dadurch geht keine Information durch Binning/Encoding verloren
- Sensitivitätsanalyse: G² → prüfen, ob Kanten im Graph ohne Gaussian-Annahme stabil
    - Weil: behandelt nach Binning alle Variablen rein kategorial und macht damit keine Gaussian-/Linearitätsannahme
        - ist Robustheitscheck: bleiben Kanten im Graph unter beiden Tests bestehen, steigt das Vertrauen in sie
- optionale Sensitivitätsanalyse: RCIT → prüfen, ob nichtlineare Abhängigkeiten den Graph verändern
    - Weil: adressiert die Schwäche, die Conditional Gaussian (rein linear) und G² (nur durch grobes Binning) gemeinsam haben; nichtlineare Abhängigkeiten

**Strukturierung und Begründung**

- Nach Datenexploration und Correlation Clouds gegen Fisher-Z entschieden, weil:
    1.  Fisher-Z für kontinuierliche, multivariat normalverteilte Variablen gedacht ist
    2.  Numerische Kodierung nominaler Variablen würde künstliche Ordnung/Abstände erzeugen
    3.  Datenset beinhaltet mixed-data (kontinuierlich und kategorisch)

- Als Haupttest Conditional Gaussian, weil:
    1.  Geeignet für mixed-data → kann kontinuierliche und kategorische Daten gemeinsam modellieren
    2.  Kein Informationsverlust, denn keine Diskretisierung oder Encoding

- Als Sensitivitätsanalyse G², weil:
    1.  Prüft, ob die Kanten im Graph bestehen bleiben/robust bleiben ohne die Gaussian-Annahme
    2.  Teilweiser Informationsverlust durch Diskretisierung/Binning, aber ausreichend für vorgesehenen Test (Im Ursprungsdatenset exisiteren bereits einige natürliche Bins, die ggf. verwendet werden können)

- Wenn noch Zeit/optional: RCIT
    1.  Mittelweg zwischen sehr rechenintensivem KCI und approximativerem RCoT
    2.  Adressiert andere Schwäche von Conditional Gaussian, nämlich Nichtlinearität
    3.  Aufgrund des Projektumfangs entscheiden wir uns für G² und machen RCIT nur, wenn es die Zeit zulässt → kann schnell sehr komplex werden (Variablenencoding, Kernel-Approximationen, Rechenaufwand, schwer interpretierbare Abweichungen)

**Vergleich zwischen Tests und Graphen**

- Tests sind parallele Robustheitschecks, keine lineare Pipeline
- verschiedene Tests können verschiedenen Preprocessing erfordern
- Hauptvergleich zuerst innerhalb des gleichen Algorithmus (PC/FCI). Danach Cross-Algorithmus-Vergleich von gleichen CI-Tests

**Vergleichsebenen der Graphen**

1.  Skeleton vergleichen
2.  stabile Kanten im Graph über Tests und Alpha-Tuning
3.  Orientierungen der Edges vergleichen → vorsichtige Interpretation
4.  Separating Sets vergleichen (durch welche Kontrollmenge wurde die Kante entfernt?)
5.  zentrale Zielkanten zu BestSquat3KG vergleichen
