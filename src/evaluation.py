import pandas as pd

# --------------------------------------------------
# 1. LOAD PROPOSED SYSTEM RESULTS
# --------------------------------------------------

proposed_file = "data/processed/prioritized_referrals.csv"
baseline_file = "data/processed/baseline_results.csv"

output_file = "outputs/results/evaluation_results.csv"

df = pd.read_csv(proposed_file)
baseline = pd.read_csv(baseline_file)

print("=" * 60)
print("PRIORITISATION SYSTEM EVALUATION")
print("=" * 60)


# --------------------------------------------------
# 2. ADD BASELINE RESULTS
# --------------------------------------------------

baseline_columns = [
    "referral_id",
    "baseline_priority",
    "fcfs_rank"
]

baseline = baseline[baseline_columns]

df = df.merge(
    baseline,
    on="referral_id",
    how="left"
)

print("\nBaseline results merged successfully.")


# --------------------------------------------------
# 3. COMPARE SYSTEM WITH SYNTHETIC REFERENCE
# --------------------------------------------------

reference_urgent = (
    df["clinician_priority_label"] == "Urgent"
)

system_urgent = (
    df["system_priority_label"] == "Urgent"
)


# True Positive
true_positive = (
    reference_urgent & system_urgent
).sum()

# True Negative
true_negative = (
    (~reference_urgent) & (~system_urgent)
).sum()

# False Positive
false_positive = (
    (~reference_urgent) & system_urgent
).sum()

# False Negative
false_negative = (
    reference_urgent & (~system_urgent)
).sum()


# --------------------------------------------------
# 4. CALCULATE METRICS
# --------------------------------------------------

precision = (
    true_positive / (true_positive + false_positive)
    if (true_positive + false_positive) > 0
    else 0
)

recall = (
    true_positive / (true_positive + false_negative)
    if (true_positive + false_negative) > 0
    else 0
)

accuracy = (
    (true_positive + true_negative) / len(df)
)


# --------------------------------------------------
# 5. DISPLAY REFERENCE VS SYSTEM
# --------------------------------------------------

print("\nREFERENCE VS SYSTEM")
print("-" * 40)

print("True Positives :", true_positive)
print("True Negatives :", true_negative)
print("False Positives:", false_positive)
print("False Negatives:", false_negative)


# --------------------------------------------------
# 6. DISPLAY PERFORMANCE METRICS
# --------------------------------------------------

print("\nPERFORMANCE METRICS")
print("-" * 40)

print(f"Precision : {precision:.3f}")
print(f"Recall    : {recall:.3f}")
print(f"Accuracy  : {accuracy:.3f}")


# --------------------------------------------------
# 7. BASELINE VS PROPOSED
# --------------------------------------------------

print("\nBASELINE VS PROPOSED SYSTEM")
print("-" * 40)

baseline_urgent = (
    df["baseline_priority"] == "Urgent"
).sum()

proposed_urgent = (
    df["system_priority_label"] == "Urgent"
).sum()

print("Baseline urgent cases :", baseline_urgent)
print("Proposed urgent cases :", proposed_urgent)


# --------------------------------------------------
# 8. CREATE EVALUATION RESULT
# --------------------------------------------------

df["evaluation_result"] = "True Negative"

df.loc[
    reference_urgent & system_urgent,
    "evaluation_result"
] = "True Positive"

df.loc[
    (~reference_urgent) & system_urgent,
    "evaluation_result"
] = "False Positive"

df.loc[
    reference_urgent & (~system_urgent),
    "evaluation_result"
] = "False Negative"


# --------------------------------------------------
# 9. DISPLAY EVALUATION DISTRIBUTION
# --------------------------------------------------

print("\nEVALUATION DISTRIBUTION")
print("-" * 40)

print(
    df["evaluation_result"].value_counts()
)


# --------------------------------------------------
# 10. DISPLAY FALSE NEGATIVES
# --------------------------------------------------

print("\nFALSE NEGATIVE CASES")
print("-" * 40)

false_negative_cases = df[
    df["evaluation_result"] == "False Negative"
]

if len(false_negative_cases) == 0:

    print("No false negative cases found.")

else:

    print(
        false_negative_cases[
            [
                "referral_id",
                "clinician_priority_label",
                "system_priority_label",
                "priority_score",
                "priority_reason",
                "edge_case_type"
            ]
        ].head(10).to_string(index=False)
    )


# --------------------------------------------------
# 11. CREATE EVALUATION SUMMARY
# --------------------------------------------------

evaluation_summary = pd.DataFrame({

    "Metric": [
        "Total Referrals",
        "True Positives",
        "True Negatives",
        "False Positives",
        "False Negatives",
        "Precision",
        "Recall",
        "Accuracy",
        "Baseline Urgent Cases",
        "Proposed Urgent Cases"
    ],

    "Value": [
        len(df),
        true_positive,
        true_negative,
        false_positive,
        false_negative,
        precision,
        recall,
        accuracy,
        baseline_urgent,
        proposed_urgent
    ]
})


# --------------------------------------------------
# 12. SAVE EVALUATION SUMMARY
# --------------------------------------------------

evaluation_summary.to_csv(
    output_file,
    index=False
)


# --------------------------------------------------
# 13. SAVE DETAILED RESULTS
# --------------------------------------------------

df.to_csv(
    "data/processed/evaluated_referrals.csv",
    index=False
)


# --------------------------------------------------
# 14. FINAL STATUS
# --------------------------------------------------

print("\nEvaluation summary saved to:")
print(output_file)

print("\nDetailed evaluation saved to:")
print("data/processed/evaluated_referrals.csv")

print("\n" + "=" * 60)
print("EVALUATION COMPLETED")
print("=" * 60)

print("Total referrals:", len(df))