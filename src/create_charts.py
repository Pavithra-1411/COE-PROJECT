import pandas as pd
import matplotlib.pyplot as plt
import os

# ==========================================================
# CARDIOLOGY PROJECT - REVIEW 1 CHARTS
# ==========================================================

os.makedirs("outputs/charts", exist_ok=True)

# ----------------------------------------------------------
# Load datasets
# ----------------------------------------------------------

v1 = pd.read_csv(
    "data/processed/prioritized_referrals.csv"
)

v2 = pd.read_csv(
    "data/processed/prioritized_referrals_v2.csv"
)

baseline = pd.read_csv(
    "data/processed/baseline_results.csv"
)

evaluation_v2 = pd.read_csv(
    "outputs/results/evaluation_v2_results.csv"
)

# ==========================================================
# CHART 1 - VERSION 2 PRIORITY DISTRIBUTION
# ==========================================================

priority_counts = v2[
    "system_priority_label_v2"
].value_counts()

priority_counts = priority_counts.reindex(
    ["Urgent", "Priority", "Routine"]
)

plt.figure(figsize=(8, 5))

priority_counts.plot(kind="bar")

plt.title("Version 2 Priority Distribution")
plt.xlabel("Priority Level")
plt.ylabel("Number of Referrals")

plt.xticks(rotation=0)

plt.tight_layout()

plt.savefig(
    "outputs/charts/priority_distribution_v2.png"
)

plt.close()


# ==========================================================
# CHART 2 - BASELINE VS PROPOSED URGENT CASES
# ==========================================================

baseline_urgent = (
    baseline["baseline_priority"] == "Urgent"
).sum()

v1_urgent = (
    v1["system_priority_label"] == "Urgent"
).sum()

v2_urgent = (
    v2["system_priority_label_v2"] == "Urgent"
).sum()

systems = [
    "Baseline",
    "Version 1",
    "Version 2"
]

urgent_counts = [
    baseline_urgent,
    v1_urgent,
    v2_urgent
]

plt.figure(figsize=(8, 5))

plt.bar(
    systems,
    urgent_counts
)

plt.title("Urgent Referrals: Baseline vs Proposed Systems")
plt.xlabel("System")
plt.ylabel("Number of Urgent Referrals")

plt.tight_layout()

plt.savefig(
    "outputs/charts/urgent_comparison.png"
)

plt.close()


# ==========================================================
# CHART 3 - THRESHOLD VS RECALL
# ==========================================================

thresholds = [4, 5, 6, 7]

recall_values = [
    0.900,
    0.714,
    0.467,
    0.244
]

plt.figure(figsize=(8, 5))

plt.plot(
    thresholds,
    recall_values,
    marker="o"
)

plt.title("Priority Threshold vs Recall")
plt.xlabel("Urgent Classification Threshold")
plt.ylabel("Recall")

plt.xticks(thresholds)

plt.ylim(0, 1)

plt.grid(True)

plt.tight_layout()

plt.savefig(
    "outputs/charts/threshold_vs_recall.png"
)

plt.close()


# ==========================================================
# CHART 4 - FALSE NEGATIVES BY PRIORITY SCORE
# ==========================================================

evaluation = pd.read_csv(
    "data/processed/evaluated_referrals.csv"
)

false_negatives = evaluation[
    (
        evaluation["clinician_priority_label"]
        == "Urgent"
    )
    &
    (
        evaluation["system_priority_label"]
        != "Urgent"
    )
]

fn_by_score = (
    false_negatives[
        "priority_score"
    ]
    .value_counts()
    .sort_index()
)

plt.figure(figsize=(8, 5))

fn_by_score.plot(
    kind="bar"
)

plt.title("False Negatives by Priority Score")
plt.xlabel("Version 1 Priority Score")
plt.ylabel("Number of False Negatives")

plt.xticks(rotation=0)

plt.tight_layout()

plt.savefig(
    "outputs/charts/false_negatives_by_score.png"
)

plt.close()


# ==========================================================
# COMPLETION
# ==========================================================

print("=" * 60)
print("CHART CREATION COMPLETED")
print("=" * 60)

print("\nCharts saved in:")
print("outputs/charts/")

print("\nCreated charts:")

print("1. priority_distribution_v2.png")
print("2. urgent_comparison.png")
print("3. threshold_vs_recall.png")
print("4. false_negatives_by_score.png")