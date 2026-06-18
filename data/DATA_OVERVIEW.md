# OpenPowerlifting Dataset — Column Reference

**Source:** `https://openpowerlifting.gitlab.io/opl-csv/bulk-csv.html`  
**Source file:** `openpowerlifting-2026-05-16-d230fa1a.csv`  
**Rows:** 3,925,887 competition entries  
**Columns:** 42  
**Date range:** 1964-09-05 → 2026-05-10  
**Unique athletes:** ~989,691 | **Unique meets:** ~33,653

---

## Column Overview

<table>
  <thead>
    <tr><th>Group</th><th>Column</th><th>Type</th><th>Missing</th><th>Description</th></tr>
  </thead>
  <tbody>
    <!-- Athlete identity #c9e4ff -->
    <tr style="background-color:#c9e4ff"><td><strong>Athlete identity</strong></td><td>Name</td><td>string</td><td>0%</td><td>Athlete's name</td></tr>
    <tr style="background-color:#c9e4ff"><td><strong>Athlete identity</strong></td><td>Sex</td><td>categorical</td><td>0%</td><td>Biological sex</td></tr>
    <!-- Competition format #c9f5d3 -->
    <tr style="background-color:#c9f5d3"><td><strong>Competition format</strong></td><td>Event</td><td>categorical</td><td>0%</td><td>Lifts contested</td></tr>
    <tr style="background-color:#c9f5d3"><td><strong>Competition format</strong></td><td>Equipment</td><td>categorical</td><td>0%</td><td>Equipment category</td></tr>
    <!-- Age & division #fff3b0 -->
    <tr style="background-color:#fff3b0"><td><strong>Age &amp; division</strong></td><td>Age</td><td>continuous</td><td>37.0%</td><td>Age at time of meet</td></tr>
    <tr style="background-color:#fff3b0"><td><strong>Age &amp; division</strong></td><td>AgeClass</td><td>categorical</td><td>27.6%</td><td>Age bracket</td></tr>
    <tr style="background-color:#fff3b0"><td><strong>Age &amp; division</strong></td><td>BirthYearClass</td><td>categorical</td><td>34.8%</td><td>Birth-year bracket</td></tr>
    <tr style="background-color:#fff3b0"><td><strong>Age &amp; division</strong></td><td>Division</td><td>string</td><td>0.1%</td><td>Federation-specific division label</td></tr>
    <!-- Body & weight class #ffd9a0 -->
    <tr style="background-color:#ffd9a0"><td><strong>Body &amp; weight class</strong></td><td>BodyweightKg</td><td>continuous</td><td>1.1%</td><td>Lifter's bodyweight in kg</td></tr>
    <tr style="background-color:#ffd9a0"><td><strong>Body &amp; weight class</strong></td><td>WeightClassKg</td><td>string</td><td>1.5%</td><td>Official weight class</td></tr>
    <!-- Squat attempts #ffc4c4 -->
    <tr style="background-color:#ffc4c4"><td><strong>Squat attempts</strong></td><td>Squat1Kg</td><td>continuous</td><td>67.8%</td><td>First squat attempt</td></tr>
    <tr style="background-color:#ffc4c4"><td><strong>Squat attempts</strong></td><td>Squat2Kg</td><td>continuous</td><td>68.1%</td><td>Second squat attempt</td></tr>
    <tr style="background-color:#ffc4c4"><td><strong>Squat attempts</strong></td><td>Squat3Kg</td><td>continuous</td><td>68.9%</td><td>Third squat attempt</td></tr>
    <tr style="background-color:#ffc4c4"><td><strong>Squat attempts</strong></td><td>Squat4Kg</td><td>continuous</td><td>99.8%</td><td>Fourth squat attempt (rare)</td></tr>
    <tr style="background-color:#ffc4c4"><td><strong>Squat attempts</strong></td><td>Best3SquatKg</td><td>continuous</td><td>30.1%</td><td>Best of first three squat attempts</td></tr>
    <!-- Bench attempts #e8c9ff -->
    <tr style="background-color:#e8c9ff"><td><strong>Bench attempts</strong></td><td>Bench1Kg</td><td>continuous</td><td>53.3%</td><td>First bench press attempt</td></tr>
    <tr style="background-color:#e8c9ff"><td><strong>Bench attempts</strong></td><td>Bench2Kg</td><td>continuous</td><td>53.8%</td><td>Second bench press attempt</td></tr>
    <tr style="background-color:#e8c9ff"><td><strong>Bench attempts</strong></td><td>Bench3Kg</td><td>continuous</td><td>55.1%</td><td>Third bench press attempt</td></tr>
    <tr style="background-color:#e8c9ff"><td><strong>Bench attempts</strong></td><td>Bench4Kg</td><td>continuous</td><td>99.4%</td><td>Fourth bench press attempt (rare)</td></tr>
    <tr style="background-color:#e8c9ff"><td><strong>Bench attempts</strong></td><td>Best3BenchKg</td><td>continuous</td><td>11.3%</td><td>Best of first three bench attempts</td></tr>
    <!-- Deadlift attempts #b8f0e0 -->
    <tr style="background-color:#b8f0e0"><td><strong>Deadlift attempts</strong></td><td>Deadlift1Kg</td><td>continuous</td><td>64.0%</td><td>First deadlift attempt</td></tr>
    <tr style="background-color:#b8f0e0"><td><strong>Deadlift attempts</strong></td><td>Deadlift2Kg</td><td>continuous</td><td>64.6%</td><td>Second deadlift attempt</td></tr>
    <tr style="background-color:#b8f0e0"><td><strong>Deadlift attempts</strong></td><td>Deadlift3Kg</td><td>continuous</td><td>65.9%</td><td>Third deadlift attempt</td></tr>
    <tr style="background-color:#b8f0e0"><td><strong>Deadlift attempts</strong></td><td>Deadlift4Kg</td><td>continuous</td><td>99.3%</td><td>Fourth deadlift attempt (rare)</td></tr>
    <tr style="background-color:#b8f0e0"><td><strong>Deadlift attempts</strong></td><td>Best3DeadliftKg</td><td>continuous</td><td>25.0%</td><td>Best of first three deadlift attempts</td></tr>
    <!-- Result #ffe680 -->
    <tr style="background-color:#ffe680"><td><strong>Result</strong></td><td>TotalKg</td><td>continuous</td><td>6.8%</td><td>Sum of best squat + bench + deadlift</td></tr>
    <tr style="background-color:#ffe680"><td><strong>Result</strong></td><td>Place</td><td>mixed</td><td>0%</td><td>Finishing place or special result code</td></tr>
    <!-- Bodyweight-adjusted scores #b8e8ff -->
    <tr style="background-color:#b8e8ff"><td><strong>Bodyweight-adjusted scores</strong></td><td>Dots</td><td>continuous</td><td>7.4%</td><td>Dots score</td></tr>
    <tr style="background-color:#b8e8ff"><td><strong>Bodyweight-adjusted scores</strong></td><td>Wilks</td><td>continuous</td><td>7.4%</td><td>Wilks score</td></tr>
    <tr style="background-color:#b8e8ff"><td><strong>Bodyweight-adjusted scores</strong></td><td>Glossbrenner</td><td>continuous</td><td>7.4%</td><td>Glossbrenner score</td></tr>
    <tr style="background-color:#b8e8ff"><td><strong>Bodyweight-adjusted scores</strong></td><td>Goodlift</td><td>continuous</td><td>15.1%</td><td>IPF Goodlift score</td></tr>
    <!-- Drug testing #f5c9e8 -->
    <tr style="background-color:#f5c9e8"><td><strong>Drug testing</strong></td><td>Tested</td><td>categorical</td><td>23.9%</td><td>Drug-testing status (only "Yes" recorded)</td></tr>
    <!-- Lifter location #c9f5c9 -->
    <tr style="background-color:#c9f5c9"><td><strong>Lifter location</strong></td><td>Country</td><td>string</td><td>44.1%</td><td>Lifter's country of representation</td></tr>
    <tr style="background-color:#c9f5c9"><td><strong>Lifter location</strong></td><td>State</td><td>string</td><td>78.7%</td><td>Lifter's state / region</td></tr>
    <!-- Federation #ffc9a0 -->
    <tr style="background-color:#ffc9a0"><td><strong>Federation</strong></td><td>Federation</td><td>string</td><td>0%</td><td>Federation that sanctioned the meet</td></tr>
    <tr style="background-color:#ffc9a0"><td><strong>Federation</strong></td><td>ParentFederation</td><td>string</td><td>39.9%</td><td>International umbrella federation</td></tr>
    <!-- Meet details #d8d8d8 -->
    <tr style="background-color:#d8d8d8"><td><strong>Meet details</strong></td><td>Date</td><td>date</td><td>0%</td><td>Meet date (YYYY-MM-DD)</td></tr>
    <tr style="background-color:#d8d8d8"><td><strong>Meet details</strong></td><td>MeetCountry</td><td>string</td><td>0%</td><td>Country where the meet was held</td></tr>
    <tr style="background-color:#d8d8d8"><td><strong>Meet details</strong></td><td>MeetState</td><td>string</td><td>28.4%</td><td>State/region where the meet was held</td></tr>
    <tr style="background-color:#d8d8d8"><td><strong>Meet details</strong></td><td>MeetTown</td><td>string</td><td>13.9%</td><td>Town/city where the meet was held</td></tr>
    <tr style="background-color:#d8d8d8"><td><strong>Meet details</strong></td><td>MeetName</td><td>string</td><td>0%</td><td>Name of the meet</td></tr>
    <tr style="background-color:#d8d8d8"><td><strong>Meet details</strong></td><td>Sanctioned</td><td>categorical</td><td>0%</td><td>Whether the meet is officially sanctioned</td></tr>
  </tbody>
</table>

---

## Categorical Columns — Discrete Values

### Sex

3 values

| Value | Meaning            |
| ----- | ------------------ |
| `F`   | Female             |
| `M`   | Male               |
| `Mx`  | Non-binary / mixed |

### Event

7 values — combinations of S (squat), B (bench), D (deadlift)

| Value | Lifts contested                     |
| ----- | ----------------------------------- |
| `SBD` | Squat, Bench, Deadlift (full power) |
| `B`   | Bench only                          |
| `D`   | Deadlift only                       |
| `BD`  | Bench + Deadlift                    |
| `S`   | Squat only                          |
| `SB`  | Squat + Bench                       |
| `SD`  | Squat + Deadlift                    |

### Equipment

6 values

| Value        | Description                                     |
| ------------ | ----------------------------------------------- |
| `Raw`        | No supportive gear (belt only permitted)        |
| `Wraps`      | Knee wraps allowed                              |
| `Single-ply` | Single-ply squat suit / bench shirt             |
| `Multi-ply`  | Multi-ply suit / bench shirt                    |
| `Unlimited`  | Any equipment                                   |
| `Straps`     | Lifting straps permitted (deadlift-only events) |

### AgeClass

18 values

`5-12`, `13-15`, `16-17`, `18-19`, `20-23`, `24-34`, `35-39`, `40-44`, `45-49`, `50-54`, `55-59`, `60-64`, `65-69`, `70-74`, `75-79`, `80-84`, `85-89`, `90-999`

### BirthYearClass

7 values

`14-18`, `19-23`, `24-39`, `40-49`, `50-59`, `60-69`, `70-999`

### Place

Numeric ranks `1`–`195` plus 4 special codes:

| Value     | Meaning                        |
| --------- | ------------------------------ |
| `1`–`195` | Finishing rank                 |
| `DQ`      | Disqualified                   |
| `DD`      | Doping disqualification        |
| `NS`      | No-show                        |
| `G`       | Guest lifter (non-competitive) |

### Tested

Only one non-null value observed: `Yes` (meet was drug-tested). `NaN` means the field was not recorded — it does not necessarily imply untested.

### Sanctioned

2 values

| Value | Count     |
| ----- | --------- |
| `Yes` | 3,915,418 |
| `No`  | 10,469    |

### ParentFederation

26 values

`GPA`, `GPC`, `IBSA`, `IDFPA`, `INTDFPA`, `IPA`, `IPF`, `IPL`, `IRP`, `MM`, `RAW`, `SPF`, `UPC`, `WABDL`, `WDFPF`, `WP`, `WPA`, `WPC`, `WPF`, `WPO`, `WPPL`, `WPSF`, `WPU`, `WRPF`, `WUAP`, `XPC`

---

## Continuous Columns — Summary Statistics

> **Note on lift attempt columns:** negative values indicate a failed attempt (convention in powerlifting data entry). 4th attempts (Squat4Kg, Bench4Kg, Deadlift4Kg) are extremely rare special-circumstance attempts and are missing for >99% of entries.

| Column          | Mean   | SD     | Min    | Max     |
| --------------- | ------ | ------ | ------ | ------- |
| Age             | 30.64  | 13.31  | 0.0    | 105.5   |
| BodyweightKg    | 83.75  | 22.71  | 15.0   | 300.0   |
| Squat1Kg        | 117.75 | 132.53 | −555.0 | 560.0   |
| Squat2Kg        | 103.51 | 156.17 | −600.0 | 577.5   |
| Squat3Kg        | 45.07  | 188.11 | −600.5 | 595.0   |
| Squat4Kg        | 74.89  | 178.77 | −550.0 | 592.4   |
| Best3SquatKg    | 170.91 | 67.12  | −508.0 | 595.0   |
| Bench1Kg        | 83.97  | 93.71  | −635.5 | 659.0   |
| Bench2Kg        | 59.58  | 118.40 | −635.5 | 521.6   |
| Bench3Kg        | −11.90 | 135.80 | −590.0 | 635.5   |
| Bench4Kg        | 23.78  | 158.54 | −590.0 | 567.4   |
| Best3BenchKg    | 114.55 | 52.60  | −522.5 | 659.0   |
| Deadlift1Kg     | 160.39 | 105.81 | −500.0 | 458.0   |
| Deadlift2Kg     | 136.75 | 152.15 | −502.5 | 470.0   |
| Deadlift3Kg     | 26.22  | 210.48 | −587.5 | 487.5   |
| Deadlift4Kg     | 76.98  | 186.80 | −500.0 | 520.0   |
| Best3DeadliftKg | 186.40 | 62.21  | −410.0 | 487.5   |
| TotalKg         | 380.45 | 200.60 | 1.0    | 1,407.5 |
| Dots            | 280.35 | 125.48 | 0.68   | 818.06  |
| Wilks           | 279.20 | 124.95 | 0.67   | 813.18  |
| Glossbrenner    | 262.34 | 118.73 | 0.64   | 756.90  |
| Goodlift        | 64.34  | 16.43  | 0.50   | 182.71  |

---

## High-Cardinality String Columns

These columns have too many distinct values to enumerate but are useful as identifiers or filters.

| Column        | Unique values | Notes                                                                                                            |
| ------------- | ------------- | ---------------------------------------------------------------------------------------------------------------- |
| Name          | ~989,691      | One row per competition entry; athletes appear multiple times (unique values, no two athletes sharing same name) |
| Division      | 5,707         | Free-text field set by each federation; highly inconsistent                                                      |
| WeightClassKg | 403           | Numeric kg value; `+` suffix = open/superheavy class                                                             |
| Country       | ~182          | Lifter's country; top: USA (1.05M), Russia (280k), Canada (89k)                                                  |
| State         | 162           | Lifter's state or region                                                                                         |
| Federation    | ~500+         | Meet federation; top: THSPA (536k), USAPL (360k), THSWPA (325k)                                                  |
| MeetCountry   | 131           | Country where meet was held                                                                                      |
| MeetState     | 249           | State/region where meet was held                                                                                 |
| MeetTown      | 8,676         | City/town where meet was held                                                                                    |
| MeetName      | 33,653        | Official meet name                                                                                               |
| Date          | —             | Format: `YYYY-MM-DD`; range 1964-09-05 to 2026-05-10                                                             |
