import pandas as pd

# ==========================================================
# CARDIOLOGY DIAGNOSTIC WORKLIST
# PRIORITISATION SYSTEM - VERSION 2
# ==========================================================

input_file = "data/processed/cleaned_referrals.csv"
output_file = "data/processed/prioritized_referrals_v2.csv"

df = pd.read_csv(input_file)

print("=" * 60)
print("CARDIOLOGY PRIORITISATION SYSTEM - VERSION 2")
print("=" * 60)

print("\nDataset:")
print("Rows    :", df.shape[0])
print("Columns :", df.shape[1])


# ==========================================================
# PRIORITY SCORE
# ==========================================================

df["priority_score_v2"] = 0

df["priority_reason_v2"] = ""


# ==========================================================
# RULE 1 - URGENCY INDICATOR
# ==========================================================

df.loc[
    df["urgency_indicator"] == "High",
    "priority_score_v2"
] += 3

df.loc[
    df["urgency_indicator"] == "Medium",
    "priority_score_v2"
] += 1


# ==========================================================
# RULE 2 - SYMPTOM SEVERITY
# ==========================================================

df.loc[
    df["symptom_flag"] == "Severe",
    "priority_score_v2"
] += 2

df.loc[
    df["symptom_flag"] == "Moderate",
    "priority_score_v2"
] += 1


# ==========================================================
# RULE 3 - DIAGNOSTIC FINDINGS
# ==========================================================

df.loc[
    df["abnormal_finding"] == "Yes",
    "priority_score_v2"
] += 2

df.loc[
    df["critical_finding"] == "Yes",
    "priority_score_v2"
] += 3


# ==========================================================
# RULE 4 - SPECIFIC SYMPTOMS
# ==========================================================

df.loc[
    df["syncope_flag"] == "Yes",
    "priority_score_v2"
] += 2

df.loc[
    df["chest_pain"] == "Yes",
    "priority_score_v2"
] += 1

df.loc[
    df["shortness_of_breath"] == "Yes",
    "priority_score_v2"
] += 1


# ==========================================================
# RULE 5 - WAITING TIME
# ==========================================================

df.loc[
    df["waiting_hours"] > 48,
    "priority_score_v2"
] += 2

df.loc[
    (df["waiting_hours"] > 24) &
    (df["waiting_hours"] <= 48),
    "priority_score_v2"
] += 1


# ==========================================================
# VERSION 2 SAFETY OVERRIDE RULES
# ==========================================================
# These rules address important cases that Version 1
# could miss because their total score was too low.
#
# IMPORTANT:
# These are prototype rules for academic evaluation,
# not medically validated clinical rules.
# ==========================================================

# High urgency should not remain Routine
high_urgency = (
    df["urgency_indicator"] == "High"
)

df.loc[
    high_urgency &
    (df["priority_score_v2"] < 7),
    "priority_score_v2"
] = 7


# Critical finding should not remain Routine
critical_finding = (
    df["critical_finding"] == "Yes"
)

df.loc[
    critical_finding &
    (df["priority_score_v2"] < 7),
    "priority_score_v2"
] = 7


# High urgency + syncope gets additional importance
high_urgency_syncope = (
    (df["urgency_indicator"] == "High") &
    (df["syncope_flag"] == "Yes")
)

df.loc[
    high_urgency_syncope,
    "priority_score_v2"
] += 1


# High urgency + severe symptoms
high_urgency_severe = (
    (df["urgency_indicator"] == "High") &
    (df["symptom_flag"] == "Severe")
)

df.loc[
    high_urgency_severe,
    "priority_score_v2"
] += 1


# ==========================================================
# PRIORITY CLASSIFICATION
# ==========================================================

def assign_priority(score):

    if score >= 7:
        return "Urgent"

    elif score >= 4:
        return "Priority"

    else:
        return "Routine"


df["system_priority_label_v2"] = (
    df["priority_score_v2"].apply(assign_priority)
)


# ==========================================================
# EXPLAINABLE PRIORITY REASON
# ==========================================================

def generate_reason(row):

    reasons = []

    if row["urgency_indicator"] == "High":
        reasons.append("High urgency")

    elif row["urgency_indicator"] == "Medium":
        reasons.append("Medium urgency")

    if row["symptom_flag"] == "Severe":
        reasons.append("Severe symptoms")

    elif row["symptom_flag"] == "Moderate":
        reasons.append("Moderate symptoms")

    if row["abnormal_finding"] == "Yes":
        reasons.append("Abnormal finding")

    if row["critical_finding"] == "Yes":
        reasons.append("Critical finding")

    if row["syncope_flag"] == "Yes":
        reasons.append("Syncope")

    if row["chest_pain"] == "Yes":
        reasons.append("Chest pain")

    if row["shortness_of_breath"] == "Yes":
        reasons.append("Shortness of breath")

    if row["waiting_hours"] > 48:
        reasons.append("Waiting more than 48 hours")

    elif row["waiting_hours"] > 24:
        reasons.append("Waiting more than 24 hours")

    # Version 2 override explanation
    if (
        row["urgency_indicator"] == "High"
        and row["priority_score_v2"] >= 7
    ):
        if "High urgency" not in reasons:
            reasons.append("Urgency override")

    if (
        row["critical_finding"] == "Yes"
        and row["priority_score_v2"] >= 7
    ):
        if "Critical finding" not in reasons:
            reasons.append("Critical finding override")

    if len(reasons) == 0:
        return "No high-priority indicators"

    return ", ".join(reasons)


df["priority_reason_v2"] = df.apply(
    generate_reason,
    axis=1
)


# ==========================================================
# WORKLIST SORTING
# ==========================================================

priority_order = {
    "Urgent": 1,
    "Priority": 2,
    "Routine": 3
}

df["priority_order_v2"] = (
    df["system_priority_label_v2"]
    .map(priority_order)
)

df = df.sort_values(
    by=[
        "priority_order_v2",
        "priority_score_v2",
        "waiting_hours"
    ],
    ascending=[
        True,
        False,
        False
    ]
).reset_index(drop=True)


# ==========================================================
# PROPOSED RANK
# ==========================================================

df["proposed_rank_v2"] = range(
    1,
    len(df) + 1
)


# ==========================================================
# REMOVE HELPER COLUMN
# ==========================================================

df = df.drop(
    columns=["priority_order_v2"]
)


# ==========================================================
# DISPLAY RESULTS
# ==========================================================

print("\nVERSION 2 PRIORITY DISTRIBUTION")
print("-" * 40)

print(
    df["system_priority_label_v2"]
    .value_counts()
)


print("\nTOP 10 PRIORITISED REFERRALS")
print("-" * 40)

print(
    df[
        [
            "referral_id",
            "priority_score_v2",
            "system_priority_label_v2",
            "priority_reason_v2"
        ]
    ].head(10)
)


# ==========================================================
# SAVE RESULTS
# ==========================================================

df.to_csv(
    output_file,
    index=False
)


print("\nVersion 2 results saved to:")
print(output_file)

print("\n" + "=" * 60)
print("VERSION 2 PRIORITISATION COMPLETED")
print("=" * 60)

print("Total referrals:", len(df))