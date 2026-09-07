import pandas as pd

system_file = "data/processed/prioritized_referrals_v2.csv"
reference_file = "data/processed/cleaned_referrals.csv"
output_file = "outputs/results/evaluation_v2_results.csv"

print("=" * 60)
print("CARDIOLOGY PRIORITISATION SYSTEM - VERSION 2 EVALUATION")
print("=" * 60)

# Load datasets
system_df = pd.read_csv(system_file)
reference_df = pd.read_csv(reference_file)

print("\nSystem dataset loaded.")
print("Reference dataset loaded.")

# Keep only the reference columns needed for evaluation
reference_labels = reference_df[
    [
        "referral_id",
        "clinician_priority_label"
    ]
].copy()

# Remove clinician label from system dataset if it already exists
# This prevents pandas from creating _x and _y columns.
if "clinician_priority_label" in system_df.columns:
    system_df = system_df.drop(columns=["clinician_priority_label"])

# Merge system results with reference labels
df = system_df.merge(
    reference_labels,
    on="referral_id",
    how="left"
)

# Check that the reference label exists
if "clinician_priority_label" not in df.columns:
    print("\nERROR: clinician_priority_label was not found after merging.")
    print("Available columns:")
    print(df.columns.tolist())
    raise SystemExit

# Create binary labels
df["reference_urgent"] = (
    df["clinician_priority_label"] == "Urgent"
).astype(int)

df["system_urgent_v2"] = (
    df["system_priority_label_v2"] == "Urgent"
).astype(int)

# Calculate confusion matrix values
true_positive = (
    (df["reference_urgent"] == 1) &
    (df["system_urgent_v2"] == 1)
).sum()

true_negative = (
    (df["reference_urgent"] == 0) &
    (df["system_urgent_v2"] == 0)
).sum()

false_positive = (
    (df["reference_urgent"] == 0) &
    (df["system_urgent_v2"] == 1)
).sum()

false_negative = (
    (df["reference_urgent"] == 1) &
    (df["system_urgent_v2"] == 0)
).sum()

# Calculate metrics
if true_positive + false_positive > 0:
    precision = true_positive / (true_positive + false_positive)
else:
    precision = 0

if true_positive + false_negative > 0:
    recall = true_positive / (true_positive + false_negative)
else:
    recall = 0

accuracy = (
    true_positive + true_negative
) / len(df)

# Display results
print("\nVERSION 2 REFERENCE VS SYSTEM")
print("-" * 40)
print("True Positives :", true_positive)
print("True Negatives :", true_negative)
print("False Positives:", false_positive)
print("False Negatives:", false_negative)

print("\nVERSION 2 PERFORMANCE METRICS")
print("-" * 40)
print(f"Precision : {precision:.3f}")
print(f"Recall    : {recall:.3f}")
print(f"Accuracy  : {accuracy:.3f}")

print("\nVERSION 2 PRIORITY DISTRIBUTION")
print("-" * 40)
print(df["system_priority_label_v2"].value_counts())

print("\nREFERENCE PRIORITY DISTRIBUTION")
print("-" * 40)
print(df["clinician_priority_label"].value_counts())

# Save evaluation results
results = pd.DataFrame({
    "metric": [
        "True Positives",
        "True Negatives",
        "False Positives",
        "False Negatives",
        "Precision",
        "Recall",
        "Accuracy"
    ],
    "value": [
        true_positive,
        true_negative,
        false_positive,
        false_negative,
        precision,
        recall,
        accuracy
    ]
})

results.to_csv(output_file, index=False)

print("\nEvaluation results saved to:")
print(output_file)

print("\n" + "=" * 60)
print("VERSION 2 EVALUATION COMPLETED")
print("=" * 60)