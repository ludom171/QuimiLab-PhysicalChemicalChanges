# Evaluation

This folder contains the supplementary materials used in the preliminary perception-based evaluation of the virtual prototype presented in the paper:

**Development and Preliminary Evaluation of a Virtual Prototype for Physical and Chemical Changes Laboratory Practice**

## Files

- `Evaluation_Instrument.pdf` — Original questionnaire administered through Microsoft Forms.
- `anonymized_responses.csv` — Anonymized participant responses used in the statistical analysis.
- `statistical_analysis.py` — Python script used to reproduce the statistical analyses and figures reported in the manuscript.
- `requirements.txt` — Python dependencies required to reproduce the analysis.
- `figure_5.pdf` — Mean perception scores by evaluation dimension.
- `figure_6.pdf` — Acceptance and Adoption Potential scores by participant profile.
- `figure_7.pdf` — Overall perception scores by previous experience with virtual simulators.

## Evaluation Instrument

The study-specific questionnaire comprised 23 Likert-type items:

- 20 common items organized into four dimensions:
  - Usability
  - Technical Quality
  - Perceived Experimental Fidelity
  - Acceptance and Adoption Potential
- 3 profile-specific items adapted to the participant role:
  - Students
  - Laboratory Staff
  - Faculty Members

Responses were recorded using a five-point Likert scale:

1. Strongly disagree
2. Disagree
3. Neither agree nor disagree
4. Agree
5. Strongly agree

The original evaluation instrument is provided in Spanish, as administered during the study.

## Statistical Analysis

The statistical analysis was performed using **Python 3.10**.

The provided script reproduces the analyses reported in the manuscript, including:

- Mean scores and sample standard deviations.
- Internal consistency using Cronbach's alpha.
- Item-level descriptive statistics.
- Exploratory comparison among participant profiles using the Kruskal--Wallis test.
- Spearman's rank correlation between previous experience with virtual simulators and overall perception.
- Generation of Figures 5, 6, and 7 in PDF format.

To reproduce the analysis:

```bash
pip install -r requirements.txt
python statistical_analysis.py
