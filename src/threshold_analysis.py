import pandas as pd

input_file = "data/processed/prioritized_referrals.csv"

df = pd.read_csv(input_file)

print("=" * 60)
print("PRIORITY THRESHOLD ANALYSIS")
print("=" * 60)

reference_urgent = (
    df["clinician_priority_label"] == "Urgent"
)

for threshold in [4, 5, 6, 7]:

    system_urgent = (
        df["priority_score"] >= threshold
    )

    true_positive = (
        reference_urgent & system_urgent
    ).sum()

    false_positive = (
        (~reference_urgent) & system_urgent
    ).sum()

    false_negative = (
        reference_urgent & (~system_urgent)
    ).sum()

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

    print("\nThreshold:", threshold)
    print("-" * 40)
    print("True Positives :", true_positive)
    print("False Positives:", false_positive)
    print("False Negatives:", false_negative)
    print(f"Precision      : {precision:.3f}")
    print(f"Recall         : {recall:.3f}")

print("\n" + "=" * 60)
print("THRESHOLD ANALYSIS COMPLETED")
print("=" * 60)