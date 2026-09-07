import pandas as pd

# --------------------------------------------------
# 1. LOAD EVALUATED DATA
# --------------------------------------------------

input_file = "data/processed/evaluated_referrals.csv"

df = pd.read_csv(input_file)

print("=" * 60)
print("URGENT CASES WITH LOW PRIORITY SCORES")
print("=" * 60)


# --------------------------------------------------
# 2. SELECT REFERENCE URGENT CASES
#    WITH SCORE BELOW 4
# --------------------------------------------------

low_score_urgent = df[
    (df["clinician_priority_label"] == "Urgent") &
    (df["priority_score"] < 4)
].copy()

print("\nTotal urgent cases with score below 4:")
print(len(low_score_urgent))


# --------------------------------------------------
# 3. DISPLAY CASES
# --------------------------------------------------

print("\nURGENT LOW-SCORE CASES")
print("-" * 60)

columns = [
    "referral_id",
    "urgency_indicator",
    "symptom_flag",
    "chest_pain",
    "shortness_of_breath",
    "syncope_flag",
    "abnormal_finding",
    "critical_finding",
    "priority_score",
    "system_priority_label",
    "priority_reason",
    "edge_case_type"
]

print(
    low_score_urgent[columns]
    .to_string(index=False)
)


# --------------------------------------------------
# 4. INDICATOR DISTRIBUTION
# --------------------------------------------------

print("\nURGENCY INDICATOR")
print("-" * 40)
print(
    low_score_urgent["urgency_indicator"]
    .value_counts()
)


print("\nSYMPTOM FLAG")
print("-" * 40)
print(
    low_score_urgent["symptom_flag"]
    .value_counts()
)


print("\nABNORMAL FINDING")
print("-" * 40)
print(
    low_score_urgent["abnormal_finding"]
    .value_counts()
)


print("\nCRITICAL FINDING")
print("-" * 40)
print(
    low_score_urgent["critical_finding"]
    .value_counts()
)


print("\nSYNCOPE")
print("-" * 40)
print(
    low_score_urgent["syncope_flag"]
    .value_counts()
)


print("\nCHEST PAIN")
print("-" * 40)
print(
    low_score_urgent["chest_pain"]
    .value_counts()
)


print("\nSHORTNESS OF BREATH")
print("-" * 40)
print(
    low_score_urgent["shortness_of_breath"]
    .value_counts()
)


# --------------------------------------------------
# 5. EDGE CASES
# --------------------------------------------------

print("\nEDGE CASE DISTRIBUTION")
print("-" * 40)

print(
    low_score_urgent["edge_case_type"]
    .value_counts()
)


# --------------------------------------------------
# 6. PRIORITY REASONS
# --------------------------------------------------

print("\nPRIORITY REASONS")
print("-" * 40)

print(
    low_score_urgent["priority_reason"]
    .value_counts()
)


# --------------------------------------------------
# 7. FINAL STATUS
# --------------------------------------------------

print("\n" + "=" * 60)
print("LOW-SCORE URGENT ANALYSIS COMPLETED")
print("=" * 60)