# Job Description Optimization System

A data-driven system for analyzing job descriptions (JDs), identifying what makes them effective, and generating optimized templates and writing guidelines to improve job posting performance.

## Overview

This project addresses Task — **Job Description Optimization** — with the goal of improving job posting effectiveness through NLP-based analysis. Since no company dataset was provided, the project includes a synthetic dataset generator that produces 200 realistic job descriptions with simulated application data for analysis.

## Features

- **Synthetic dataset generation** — creates realistic job descriptions across 10 roles and departments, with simulated application counts based on writing quality
- **Performance analysis** — identifies which job descriptions generate the most applications and why
- **Keyword extraction** — uses TF-IDF to find effective and ineffective keywords/phrases
- **Readability scoring** — Flesch-Kincaid Grade Level, Flesch Reading Ease, and Gunning Fog scores via `textstat`
- **Sentiment & tone analysis** — VADER and TextBlob sentiment scoring, plus inclusive language detection
- **Automated report generation** — produces three Word document deliverables

## Project structure

```
JD_Optimization/
├── main.py                          # runs the full pipeline
├── src/
│   ├── generate_dataset.py          # creates synthetic JD dataset
│   ├── analyze_performance.py       # performance analysis & charts
│   ├── keyword_analysis.py          # TF-IDF keyword extraction
│   ├── nlp_scoring.py               # readability & sentiment scoring
│   ├── generate_report.py           # builds effectiveness report
│   ├── generate_templates.py        # builds templates library
│   └── generate_guidelines.py       # builds writing guidelines
├── data/                             # generated CSV datasets
├── outputs/                          # generated charts (PNG)
└── reports/                          # generated Word documents
```

## Deliverables

| File | Description |
|------|-------------|
| `reports/JD_Effectiveness_Report.docx` | Analysis of what drives job description performance |
| `reports/JD_Templates_Library.docx` | Optimized JD templates for technical, managerial, entry-level, and sales roles |
| `reports/JD_Writing_Guidelines.docx` | Best-practice writing guidelines and a pre-posting checklist |

## Setup

### 1. Create a conda environment

```bash
conda create -n jd_optimizer python=3.11 -y
conda activate jd_optimizer
```

### 2. Install dependencies

```bash
pip install pandas numpy scikit-learn nltk spacy textblob vaderSentiment textstat matplotlib seaborn wordcloud openpyxl python-docx faker tqdm
python -m spacy download en_core_web_sm
```

## Usage

Run the full pipeline from the project root:

```bash
python main.py
```

This will sequentially:
1. Generate the synthetic dataset (`data/job_descriptions.csv`)
2. Analyze performance by role and quality tier
3. Extract effective and ineffective keywords
4. Score readability and sentiment for every job description
5. Generate all three Word document deliverables

## Methodology

### Dataset

The synthetic dataset simulates 200 job descriptions across 10 roles (Software Engineer, Data Analyst, Marketing Manager, etc.), each labeled as high, medium, or low quality based on writing style. Application counts are simulated using a base value adjusted for:

- Presence of a benefits section (+15)
- Inclusive language (e.g. "collaborative", "flexible", "grow") (+10)
- Demanding/exclusive language (e.g. "rockstar", "mandatory", "24/7") (-15)
- Random noise (±20)

### NLP techniques

- **TF-IDF** (`scikit-learn`) — compares term importance between high- and low-performing JD groups to surface effective vocabulary
- **Readability** (`textstat`) — Flesch Reading Ease, Flesch-Kincaid Grade Level, Gunning Fog Index, average sentence length
- **Sentiment** (`vaderSentiment`, `TextBlob`) — compound sentiment score, polarity, subjectivity, and a custom inclusive/exclusive word count

### Key findings (from synthetic data)

- High-performing JDs average significantly more applications than low-performing ones
- A Flesch-Kincaid Grade Level of 10–12 correlates with higher application rates
- Inclusive, welcoming language correlates positively with applications
- JDs with a clear "What We Offer" / benefits section receive more applications

## Limitations

This analysis is based on a **synthetically generated dataset** designed to model realistic patterns, since no real company data was available. The relationships modeled (readability, tone, benefits language → applications) are based on established HR research, but findings should be validated against real application data when available.

## License

Internal project — for organizational use.