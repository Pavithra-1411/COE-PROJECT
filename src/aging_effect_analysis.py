import pandas as pd
import os

# ==========================================================
# WAITING-TIME AGING EFFECT ANALYSIS
# ==========================================================

input_file = "data/processed/prioritized_referrals_v2.csv"

output_dir = "results"
output_file = os.path.join(
    output_dir,
    "aging_effect_analysis.csv"
)

os.makedirs(output_dir, exist_ok=True)

# Load dataset
df = pd.read_csv(input_file)

print("=" * 60)
print("WAITING-TIME AGING EFFECT ANALYSIS")
print("=" * 60)

# ----------------------------------------------------------
# Calculate score before waiting-time aging
# ----------------------------------------------------------

df["clinical_score_before_aging"] = (
    df["priority_score_v2"] - df["waiting_age_bonus"]
)

# ----------------------------------------------------------
# Calculate score after waiting-time aging
# ----------------------------------------------------------

df["final_score_after_aging"] = df["priority_score_v2"]

# ----------------------------------------------------------
# Find cases whose score increased because of aging
# ----------------------------------------------------------

changed_cases = df[
    df["waiting_age_bonus"] > 0
].copy()

# ----------------------------------------------------------
# Find cases receiving the maximum aging bonus
# ----------------------------------------------------------

max_aging_cases = df[
    df["waiting_age_bonus"] == 2
].copy()

# ----------------------------------------------------------
# Count cases whose score changed
# ----------------------------------------------------------

total_cases = len(df)

cases_with_aging = len(changed_cases)

# ----------------------------------------------------------
# Calculate average score increase
# ----------------------------------------------------------

if cases_with_aging > 0:
    average_increase = changed_cases["waiting_age_bonus"].mean()
else:
    average_increase = 0

# ----------------------------------------------------------
# Maximum score increase
# ----------------------------------------------------------

maximum_increase = df["waiting_age_bonus"].max()

# ----------------------------------------------------------
# Create summary
# ----------------------------------------------------------

results = pd.DataFrame({
    "metric": [
        "Total referrals",
        "Cases receiving waiting-time aging",
        "Cases receiving maximum aging bonus",
        "Average score increase from aging",
        "Maximum score increase"
    ],
    "value": [
        total_cases,
        cases_with_aging,
        len(max_aging_cases),
        round(average_increase, 2),
        maximum_increase
    ]
})

# Save
results.to_csv(output_file, index=False)

# ----------------------------------------------------------
# Display
# ----------------------------------------------------------

print("\nAGING EFFECT")
print("-" * 60)

for _, row in results.iterrows():
    print(f"{row['metric']}: {row['value']}")

print("\nExamples of cases receiving aging:")

columns_to_show = [
    "referral_id",
    "waiting_hours",
    "clinical_score_before_aging",
    "waiting_age_bonus",
    "final_score_after_aging",
    "system_priority_label_v2"
]

available_columns = [
    col for col in columns_to_show
    if col in df.columns
]

print(
    df[
        df["waiting_age_bonus"] > 0
    ][available_columns].head(10).to_string(index=False)
)

print("\n" + "=" * 60)
print("AGING EFFECT ANALYSIS COMPLETED")
print("=" * 60)

print("\nResults saved to:")
print(output_file)