import pandas as pd

# --------------------------------------------------
# 1. LOAD EVALUATED DATA
# --------------------------------------------------

input_file = "data/processed/evaluated_referrals.csv"
output_file = "outputs/reports/false_negative_analysis.csv"

df = pd.read_csv(input_file)

print("=" * 60)
print("FALSE NEGATIVE ANALYSIS")
print("=" * 60)


# --------------------------------------------------
# 2. SELECT FALSE NEGATIVES
# --------------------------------------------------

false_negatives = df[
    df["evaluation_result"] == "False Negative"
].copy()

print("\nTotal False Negatives:", len(false_negatives))


# --------------------------------------------------
# 3. FALSE NEGATIVES BY PRIORITY SCORE
# --------------------------------------------------

print("\nFALSE NEGATIVES BY PRIORITY SCORE")
print("-" * 40)

score_distribution = (
    false_negatives["priority_score"]
    .value_counts()
    .sort_index()
)

print(score_distribution)


# --------------------------------------------------
# 4. FALSE NEGATIVES BY EDGE CASE
# --------------------------------------------------

print("\nFALSE NEGATIVES BY EDGE CASE")
print("-" * 40)

edge_cases = (
    false_negatives["edge_case_type"]
    .value_counts()
)

print(edge_cases)


# --------------------------------------------------
# 5. FALSE NEGATIVES BY PRIORITY REASON
# --------------------------------------------------

print("\nFALSE NEGATIVES BY PRIORITY REASON")
print("-" * 40)

reason_distribution = (
    false_negatives["priority_reason"]
    .value_counts()
)

print(reason_distribution)


# --------------------------------------------------
# 6. REFERENCE URGENT CASES BY SYSTEM SCORE
# --------------------------------------------------

print("\nREFERENCE URGENT CASES BY SYSTEM SCORE")
print("-" * 40)

reference_urgent = df[
    df["clinician_priority_label"] == "Urgent"
]

urgent_score_distribution = (
    reference_urgent["priority_score"]
    .value_counts()
    .sort_index()
)

print(urgent_score_distribution)


# --------------------------------------------------
# 7. FALSE NEGATIVES BY SYSTEM LABEL
# --------------------------------------------------

print("\nFALSE NEGATIVES BY SYSTEM LABEL")
print("-" * 40)

print(
    false_negatives["system_priority_label"]
    .value_counts()
)


# --------------------------------------------------
# 8. IMPORTANT INDICATORS
# --------------------------------------------------

print("\nFALSE NEGATIVES - IMPORTANT INDICATORS")
print("-" * 40)

indicators = [
    "urgency_indicator",
    "symptom_flag",
    "abnormal_finding",
    "critical_finding",
    "syncope_flag",
    "chest_pain",
    "shortness_of_breath",
    "waiting_time_category"
]

for column in indicators:

    print(f"\n{column}:")

    print(
        false_negatives[column]
        .value_counts()
    )


# --------------------------------------------------
# 9. SAVE SUMMARY
# --------------------------------------------------

summary = pd.DataFrame({
    "Analysis": [
        "Total False Negatives",
        "False Negatives with score 6",
        "False Negatives with score 5",
        "False Negatives with score 4",
        "False Negatives with score below 4"
    ],
    "Value": [
        len(false_negatives),
        (false_negatives["priority_score"] == 6).sum(),
        (false_negatives["priority_score"] == 5).sum(),
        (false_negatives["priority_score"] == 4).sum(),
        (false_negatives["priority_score"] < 4).sum()
    ]
})

summary.to_csv(
    output_file,
    index=False
)


# --------------------------------------------------
# 10. DISPLAY SAMPLE CASES
# --------------------------------------------------

print("\nSAMPLE FALSE NEGATIVE CASES")
print("-" * 40)

print(
    false_negatives[
        [
            "referral_id",
            "clinician_priority_label",
            "system_priority_label",
            "priority_score",
            "priority_reason",
            "edge_case_type"
        ]
    ].head(15).to_string(index=False)
)


# --------------------------------------------------
# 11. FINAL STATUS
# --------------------------------------------------

print("\nAnalysis saved to:")
print(output_file)

print("\n" + "=" * 60)
print("FALSE NEGATIVE ANALYSIS COMPLETED")
print("=" * 60)