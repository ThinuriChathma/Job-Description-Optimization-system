print("=" * 60)
print("JD OPTIMIZATION SYSTEM — RUNNING FULL PIPELINE")
print("=" * 60)

import subprocess, sys

steps = [
    ("Generating synthetic dataset",       "src/generate_dataset.py"),
    ("Analyzing performance",              "src/analyze_performance.py"),
    ("Running keyword analysis",           "src/keyword_analysis.py"),
    ("Running NLP scoring",                "src/nlp_scoring.py"),
    ("Generating effectiveness report",    "src/generate_report.py"),
    ("Generating templates library",       "src/generate_templates.py"),
    ("Generating writing guidelines",      "src/generate_guidelines.py"),
]

for description, script in steps:
    print(f"\n→ {description}...")
    result = subprocess.run([sys.executable, script], capture_output=False)
    if result.returncode != 0:
        print(f"  ❌ ERROR in {script}")
        break

print("\n" + "=" * 60)
print("✅ PIPELINE COMPLETE")
print("  Outputs: outputs/  (charts)")
print("  Reports: reports/  (Word documents)")
print("  Data:    data/      (CSV files)")
print("=" * 60)