import pandas as pd

# --------------------------------------------------
# 1. LOAD CLEANED DATASET
# --------------------------------------------------

input_file = "data/processed/cleaned_referrals.csv"
output_file = "data/processed/prioritized_referrals.csv"

df = pd.read_csv(input_file)

print("=" * 60)
print("RULE-BASED CARDIOLOGY PRIORITISATION")
print("=" * 60)


# --------------------------------------------------
# 2. PRIORITY SCORE FUNCTION
# --------------------------------------------------

def calculate_priority(row):

    score = 0
    reasons = []

    # Urgency indicator
    if row["urgency_indicator"] == "High":
        score += 3
        reasons.append("High urgency")

    elif row["urgency_indicator"] == "Medium":
        score += 1
        reasons.append("Medium urgency")

    # Symptom severity
    if row["symptom_flag"] == "Severe":
        score += 2
        reasons.append("Severe symptoms")

    elif row["symptom_flag"] == "Moderate":
        score += 1
        reasons.append("Moderate symptoms")

    # Abnormal finding
    if row["abnormal_finding"] == "Yes":
        score += 2
        reasons.append("Abnormal finding")

    # Critical finding
    if row["critical_finding"] == "Yes":
        score += 3
        reasons.append("Critical finding")

    # Syncope
    if row["syncope_flag"] == "Yes":
        score += 2
        reasons.append("Syncope")

    # Chest pain
    if row["chest_pain"] == "Yes":
        score += 1
        reasons.append("Chest pain")

    # Shortness of breath
    if row["shortness_of_breath"] == "Yes":
        score += 1
        reasons.append("Shortness of breath")

    # Waiting time
    if row["waiting_hours"] > 48:
        score += 2
        reasons.append("Waiting more than 48 hours")

    elif row["waiting_hours"] > 24:
        score += 1
        reasons.append("Waiting more than 24 hours")

    return score, ", ".join(reasons)


# --------------------------------------------------
# 3. CALCULATE SCORES
# --------------------------------------------------

results = df.apply(
    calculate_priority,
    axis=1
)

df["priority_score"] = results.apply(lambda x: x[0])
df["priority_reason"] = results.apply(lambda x: x[1])


# --------------------------------------------------
# 4. ASSIGN SYSTEM PRIORITY
# --------------------------------------------------

def assign_priority(score):

    if score >= 7:
        return "Urgent"

    elif score >= 4:
        return "Priority"

    else:
        return "Routine"


df["system_priority_label"] = df["priority_score"].apply(
    assign_priority
)


# --------------------------------------------------
# 5. CREATE PROPOSED RANK
# --------------------------------------------------

priority_order = {
    "Urgent": 1,
    "Priority": 2,
    "Routine": 3
}

df["priority_order"] = df["system_priority_label"].map(
    priority_order
)

df = df.sort_values(
    by=[
        "priority_order",
        "priority_score",
        "waiting_hours"
    ],
    ascending=[
        True,
        False,
        False
    ]
).reset_index(drop=True)

df["proposed_rank"] = range(1, len(df) + 1)


# --------------------------------------------------
# 6. DISPLAY PRIORITY DISTRIBUTION
# --------------------------------------------------

print("\nSYSTEM PRIORITY DISTRIBUTION")
print("-" * 40)

print(
    df["system_priority_label"].value_counts()
)


# --------------------------------------------------
# 7. DISPLAY SAMPLE RESULTS
# --------------------------------------------------

print("\nTOP 10 PRIORITIZED REFERRALS")
print("-" * 40)

print(
    df[
        [
            "referral_id",
            "priority_score",
            "system_priority_label",
            "priority_reason",
            "proposed_rank"
        ]
    ].head(10).to_string(index=False)
)


# --------------------------------------------------
# 8. REMOVE HELPER COLUMN
# --------------------------------------------------

df = df.drop(
    columns=["priority_order"]
)


# --------------------------------------------------
# 9. SAVE RESULTS
# --------------------------------------------------

df.to_csv(
    output_file,
    index=False
)

print("\nPrioritized dataset saved to:")
print(output_file)


# --------------------------------------------------
# 10. FINAL STATUS
# --------------------------------------------------

print("\n" + "=" * 60)
print("PRIORITISATION COMPLETED")
print("=" * 60)

print("Total referrals:", len(df))