import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import os

os.makedirs("outputs", exist_ok=True)

df = pd.read_csv("data/jd_with_performance.csv")

# Split into high and low performers
high_jds = df[df['quality_label'] == 'high']['job_description'].tolist()
low_jds  = df[df['quality_label'] == 'low']['job_description'].tolist()

print(f"High-performing JDs: {len(high_jds)}")
print(f"Low-performing JDs:  {len(low_jds)}")

# ── TF-IDF on high performers ──────────────────────────────────────────────────
# TF-IDF measures: how important is a word in a document, relative to all documents?
# Words with high TF-IDF scores are distinctive and important for that group.

tfidf = TfidfVectorizer(
    stop_words='english',   # remove common words like "the", "and", "is"
    ngram_range=(1, 2),     # look at single words AND two-word phrases
    max_features=50,        # keep top 50 terms
    min_df=2                # word must appear in at least 2 documents
)

# Fit on ALL JDs, then compare scores between groups
all_jds = high_jds + low_jds
labels  = ['high'] * len(high_jds) + ['low'] * len(low_jds)

tfidf_matrix = tfidf.fit_transform(all_jds)
feature_names = tfidf.get_feature_names_out()

# Average TF-IDF score for each word in each group
high_indices = [i for i, l in enumerate(labels) if l == 'high']
low_indices  = [i for i, l in enumerate(labels) if l == 'low']

high_scores = np.asarray(tfidf_matrix[high_indices].mean(axis=0)).flatten()
low_scores  = np.asarray(tfidf_matrix[low_indices].mean(axis=0)).flatten()

# Words that score higher in high-performing JDs = effective keywords
keyword_df = pd.DataFrame({
    'keyword':    feature_names,
    'high_score': high_scores,
    'low_score':  low_scores,
    'difference': high_scores - low_scores,
})

keyword_df = keyword_df.sort_values('difference', ascending=False)

print("\n=== Top 15 Keywords in High-Performing JDs ===")
print(keyword_df.head(15)[['keyword', 'high_score', 'low_score', 'difference']].to_string(index=False))

print("\n=== Top 15 Keywords in Low-Performing JDs ===")
print(keyword_df.tail(15)[['keyword', 'high_score', 'low_score', 'difference']].to_string(index=False))

# ── Visualization 1: Bar chart of top keywords ────────────────────────────────
top_effective = keyword_df.head(15)
top_harmful   = keyword_df.tail(15)

fig, axes = plt.subplots(1, 2, figsize=(14, 6))
fig.suptitle("Keyword Analysis: High vs Low Performing JDs", fontsize=14, fontweight='bold')

axes[0].barh(top_effective['keyword'], top_effective['difference'], color='#27ae60')
axes[0].set_title("Words more common in HIGH-performing JDs")
axes[0].set_xlabel("TF-IDF Score Difference")
axes[0].invert_yaxis()

axes[1].barh(top_harmful['keyword'].iloc[::-1], top_harmful['difference'].iloc[::-1], color='#e74c3c')
axes[1].set_title("Words more common in LOW-performing JDs")
axes[1].set_xlabel("TF-IDF Score Difference (negative)")
axes[1].invert_yaxis()

plt.tight_layout()
plt.savefig("outputs/keyword_analysis.png", dpi=150, bbox_inches='tight')
print("\n✅ Chart saved: outputs/keyword_analysis.png")

# ── Visualization 2: Word clouds ──────────────────────────────────────────────
# Word clouds give a visual feel for the vocabulary of each group

high_text = " ".join(high_jds)
low_text  = " ".join(low_jds)

fig2, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

wc_high = WordCloud(width=600, height=300, background_color='white',
                    colormap='Greens', stopwords=None, max_words=60)
wc_high.generate(high_text)
ax1.imshow(wc_high, interpolation='bilinear')
ax1.axis('off')
ax1.set_title("High-Performing JD Vocabulary", fontweight='bold')

wc_low = WordCloud(width=600, height=300, background_color='white',
                   colormap='Reds', stopwords=None, max_words=60)
wc_low.generate(low_text)
ax2.imshow(wc_low, interpolation='bilinear')
ax2.axis('off')
ax2.set_title("Low-Performing JD Vocabulary", fontweight='bold')

plt.tight_layout()
plt.savefig("outputs/wordclouds.png", dpi=150, bbox_inches='tight')
print("✅ Word clouds saved: outputs/wordclouds.png")

# Save keyword results
keyword_df.to_csv("data/keyword_analysis.csv", index=False)
print("✅ Keyword data saved: data/keyword_analysis.csv")