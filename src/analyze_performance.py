import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

os.makedirs("outputs", exist_ok=True)

# ── Load data ──────────────────────────────────────────────────────────────────
df = pd.read_csv("data/job_descriptions.csv")
print(f"Loaded {len(df)} job descriptions\n")

# ── 1. Overall application stats ──────────────────────────────────────────────
print("=== Application Count Statistics ===")
print(df['applications'].describe().round(1))

# Classify JDs into performance tiers
df['performance_tier'] = pd.cut(
    df['applications'],
    bins=[0, 50, 90, 999],
    labels=['Low (0–50)', 'Medium (51–90)', 'High (91+)']
)

print("\nPerformance tier distribution:")
print(df['performance_tier'].value_counts())

# ── 2. Applications by job title ───────────────────────────────────────────────
avg_by_role = df.groupby('job_title')['applications'].mean().sort_values(ascending=False)
print("\n=== Average Applications by Role ===")
print(avg_by_role.round(1))

fig, axes = plt.subplots(1, 2, figsize=(14, 5))
fig.suptitle("Job Description Performance Analysis", fontsize=14, fontweight='bold')

# Chart 1: Average applications by role
avg_by_role.plot(kind='barh', ax=axes[0], color='steelblue')
axes[0].set_title("Average Applications by Job Title")
axes[0].set_xlabel("Average Applications")
axes[0].axvline(df['applications'].mean(), color='red', linestyle='--', label='Overall avg')
axes[0].legend()

# Chart 2: Applications by quality tier (validation check)
quality_order = ['high', 'medium', 'low']
qual_avg = df.groupby('quality_label')['applications'].mean().reindex(quality_order)
colors = ['#2ecc71', '#f39c12', '#e74c3c']
qual_avg.plot(kind='bar', ax=axes[1], color=colors, edgecolor='white')
axes[1].set_title("Average Applications by JD Quality")
axes[1].set_xlabel("Quality Level")
axes[1].set_ylabel("Average Applications")
axes[1].tick_params(axis='x', rotation=0)

plt.tight_layout()
plt.savefig("outputs/performance_analysis.png", dpi=150, bbox_inches='tight')
print("\n✅ Chart saved: outputs/performance_analysis.png")

# ── 3. Word count vs applications ─────────────────────────────────────────────
fig2, ax = plt.subplots(figsize=(8, 5))
scatter = ax.scatter(
    df['word_count'], df['applications'],
    c=df['quality_label'].map({'high': '#2ecc71', 'medium': '#f39c12', 'low': '#e74c3c'}),
    alpha=0.6, edgecolors='white', linewidth=0.5, s=60
)
ax.set_title("Word Count vs Applications Received")
ax.set_xlabel("Word Count of Job Description")
ax.set_ylabel("Number of Applications")

from matplotlib.patches import Patch
legend_elements = [
    Patch(facecolor='#2ecc71', label='High quality'),
    Patch(facecolor='#f39c12', label='Medium quality'),
    Patch(facecolor='#e74c3c', label='Low quality'),
]
ax.legend(handles=legend_elements)
plt.tight_layout()
plt.savefig("outputs/wordcount_vs_applications.png", dpi=150, bbox_inches='tight')
print("✅ Chart saved: outputs/wordcount_vs_applications.png")

# ── 4. Top 10 and Bottom 10 JDs ───────────────────────────────────────────────
top10    = df.nlargest(10,  'applications')[['jd_id', 'job_title', 'applications', 'quality_label', 'word_count']]
bottom10 = df.nsmallest(10, 'applications')[['jd_id', 'job_title', 'applications', 'quality_label', 'word_count']]

print("\n=== Top 10 Best-Performing JDs ===")
print(top10.to_string(index=False))
print("\n=== Bottom 10 Worst-Performing JDs ===")
print(bottom10.to_string(index=False))

# Save enriched dataset
df.to_csv("data/jd_with_performance.csv", index=False)
print("\n✅ Enriched dataset saved: data/jd_with_performance.csv")