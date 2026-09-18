# Data dictionary

## Primary analysis file

**File:** `survey_42.csv`  
**Description:** Export of the anonymous expert questionnaire used in the manuscript.  
**Sample size:** 42 respondents retained for analysis (test / incomplete pilot rows removed upstream).  
**Collection period:** January–September 2024.

### Notes on structure

- The first rows of the Google Forms export may contain form metadata / scale labels; analysis scripts skip header/meta rows as in the manuscript pipeline (`iloc[2:]` where applicable).
- Column 1 (index 1): self-reported expertise level  
  (`No expertise`, `Beginner Level`, `Intermediate Level`, `Advanced Level`, `Expert Level`).
- Column 2 (index 2): questionnaire **branch** self-selection  
  (`Intersection`, `Type of user`, `Exit`, `Specific Lane`, `Driver's Vision`, `Sunny`, `Curved road`).
- Subsequent columns: Likert-style confidence ratings and pairwise comparisons within the selected branch (French/English wording as in the original form).

### Branch-level sample sizes (*n* = 42)

| Branch | *n* |
|--------|-----|
| Intersection | 11 |
| Type of user | 9 |
| Exit | 7 |
| Specific Lane | 6 |
| Driver's Vision | 4 |
| Sunny | 3 |
| Curved road | 2 |

## Other CSV files

| File | Role |
|------|------|
| `survey.csv`, `survey_2.csv`, …, `survey_5.csv` | Intermediate exports retained for traceability; **not** the manuscript analysis set. |

## Privacy

No personally identifiable information is included. Do not attempt to re-identify respondents.
