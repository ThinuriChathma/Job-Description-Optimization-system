import pandas as pd
import numpy as np
import textstat
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from textblob import TextBlob
import matplotlib.pyplot as plt
import seaborn as sns
import os

os.makedirs("outputs", exist_ok=True)

df = pd.read_csv("data/jd_with_performance.csv")
analyzer = SentimentIntensityAnalyzer()

print("Running NLP scoring on all JDs...")

results = []
for _, row in df.iterrows():
    text = row['job_description']

    # ── Readability metrics ────────────────────────────────────────────────────
    # Flesch Reading Ease: 0–100, higher = easier. Target: 60–70 for JDs
    flesch_ease = textstat.flesch_reading_ease(text)

    # Flesch-Kincaid Grade: school grade level. Target: 10–12 for JDs
    fk_grade = textstat.flesch_kincaid_grade(text)

    # Gunning Fog: another grade-level measure
    gunning_fog = textstat.gunning_fog(text)

    # Average sentence length (shorter = clearer)
    avg_sentence_len = textstat.avg_sentence_length(text)

    # Interpret readability
    if fk_grade <= 10:
        readability_rating = "Easy"
    elif fk_grade <= 13:
        readability_rating = "Moderate"
    else:
        readability_rating = "Difficult"

    # ── Sentiment analysis ────────────────────────────────────────────────────
    # VADER gives: pos (positive %), neg (negative %), neu (neutral %), compound (-1 to +1)
    vader_scores = analyzer.polarity_scores(text)
    
    # TextBlob gives: polarity (-1 to +1), subjectivity (0 to 1)
    blob = TextBlob(text)

    # Tone classification
    compound = vader_scores['compound']
    if compound >= 0.3:
        tone = "Positive / Welcoming"
    elif compound >= 0:
        tone = "Neutral"
    elif compound >= -0.3:
        tone = "Slightly Negative"
    else:
        tone = "Negative / Demanding"

    # Inclusive language check
    inclusive_words = ['inclusive', 'diverse', 'collaborative', 'support', 
                       'flexible', 'grow', 'opportunity', 'passionate', 'team']
    exclusive_words = ['rockstar', 'ninja', 'mandatory', 'must', 'required',
                       'exceptional', '24/7', 'aggressive', 'demanding']
    
    inc_count = sum(1 for w in inclusive_words if w in text.lower())
    exc_count = sum(1 for w in exclusive_words if w in text.lower())

    results.append({
        'jd_id':                row['jd_id'],
        'job_title':            row['job_title'],
        'department':           row['department'],
        'applications':         row['applications'],
        'quality_label':        row['quality_label'],
        'word_count':           row['word_count'],

        # Readability
        'flesch_ease':          round(flesch_ease, 1),
        'fk_grade':             round(fk_grade, 1),
        'gunning_fog':          round(gunning_fog, 1),
        'avg_sentence_len':     round(avg_sentence_len, 1),
        'readability_rating':   readability_rating,

        # Sentiment
        'vader_positive':       round(vader_scores['pos'], 3),
        'vader_negative':       round(vader_scores['neg'], 3),
        'vader_neutral':        round(vader_scores['neu'], 3),
        'vader_compound':       round(compound, 3),
        'textblob_polarity':    round(blob.sentiment.polarity, 3),
        'textblob_subjectivity':round(blob.sentiment.subjectivity, 3),
        'tone':                 tone,

        # Inclusive language
        'inclusive_word_count': inc_count,
        'exclusive_word_count': exc_count,
        'inclusive_score':      inc_count - exc_count,
    })

scored_df = pd.DataFrame(results)
scored_df.to_csv("data/jd_scored.csv", index=False)
print(f"✅ Scoring complete. Saved to data/jd_scored.csv\n")

# ── Summary stats ──────────────────────────────────────────────────────────────
print("=== Readability by Quality ===")
print(scored_df.groupby('quality_label')[['fk_grade', 'flesch_ease', 'avg_sentence_len']].mean().round(2))

print("\n=== Sentiment by Quality ===")
print(scored_df.groupby('quality_label')[['vader_compound', 'inclusive_score']].mean().round(3))

print("\n=== Tone Distribution ===")
print(scored_df['tone'].value_counts())

# ── Visualizations ─────────────────────────────────────────────────────────────
fig, axes = plt.subplots(2, 2, figsize=(14, 10))
fig.suptitle("NLP Scoring Results — Readability & Sentiment", fontsize=14, fontweight='bold')

# Chart 1: FK Grade Level by quality
quality_order = ['high', 'medium', 'low']
colors = ['#27ae60', '#f39c12', '#e74c3c']
scored_df.boxplot(column='fk_grade', by='quality_label', ax=axes[0,0],
                  positions=[0,1,2])
axes[0,0].set_title("Readability Grade Level by Quality")
axes[0,0].set_xlabel("Quality")
axes[0,0].set_ylabel("Flesch-Kincaid Grade")
axes[0,0].axhline(12, color='red', linestyle='--', alpha=0.5, label='Grade 12 threshold')
axes[0,0].legend()
plt.sca(axes[0,0]); plt.title("Readability Grade Level by Quality")

# Chart 2: VADER compound score by quality
scored_df.boxplot(column='vader_compound', by='quality_label', ax=axes[0,1])
axes[0,1].set_title("Sentiment Score by Quality")
axes[0,1].set_xlabel("Quality")
axes[0,1].set_ylabel("VADER Compound Score (-1 to +1)")
axes[0,1].axhline(0, color='gray', linestyle='--', alpha=0.5)
plt.sca(axes[0,1]); plt.title("Sentiment Score by Quality")

# Chart 3: Inclusive vs exclusive language
inc_by_q = scored_df.groupby('quality_label')[['inclusive_word_count','exclusive_word_count']].mean().reindex(quality_order)
inc_by_q.plot(kind='bar', ax=axes[1,0], color=['#27ae60', '#e74c3c'], edgecolor='white')
axes[1,0].set_title("Inclusive vs Exclusive Language by Quality")
axes[1,0].set_xlabel("Quality")
axes[1,0].set_ylabel("Average Word Count")
axes[1,0].tick_params(axis='x', rotation=0)
axes[1,0].legend(['Inclusive words', 'Exclusive/demanding words'])

# Chart 4: Readability vs Applications scatter
scatter_colors = scored_df['quality_label'].map({'high':'#27ae60','medium':'#f39c12','low':'#e74c3c'})
axes[1,1].scatter(scored_df['fk_grade'], scored_df['applications'],
                  c=scatter_colors, alpha=0.6, s=50, edgecolors='white')
axes[1,1].set_title("Readability Grade vs Applications")
axes[1,1].set_xlabel("Flesch-Kincaid Grade Level")
axes[1,1].set_ylabel("Applications")

from matplotlib.patches import Patch
axes[1,1].legend(handles=[
    Patch(facecolor='#27ae60', label='High'),
    Patch(facecolor='#f39c12', label='Medium'),
    Patch(facecolor='#e74c3c', label='Low'),
])

plt.tight_layout()
plt.savefig("outputs/nlp_scoring.png", dpi=150, bbox_inches='tight')
print("✅ NLP charts saved: outputs/nlp_scoring.png")