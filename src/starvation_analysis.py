import pandas as pd
import os

# ==========================================================
# STARVATION ANALYSIS
# ==========================================================
# Measures whether routine cases are waiting too long
# and whether waiting-time aging reduces starvation.
# ==========================================================

# File paths
input_file = "data/processed/prioritized_referrals_v2.csv"
output_dir = "results"
output_file = os.path.join(output_dir, "starvation_results.csv")

# Create results folder if it does not exist
os.makedirs(output_dir, exist_ok=True)

# Load dataset
df = pd.read_csv(input_file)

print("=" * 60)
print("STARVATION PREVENTION ANALYSIS")
print("=" * 60)

# ----------------------------------------------------------
# Find the priority label column
# ----------------------------------------------------------

priority_column = "system_priority_label_v2"

# ----------------------------------------------------------
# Identify routine cases
# ----------------------------------------------------------

routine_df = df[
    df[priority_column].astype(str).str.lower() == "routine"
].copy()

# If the dataset uses another label, check the available labels
if len(routine_df) == 0:
    print("\nAvailable priority labels:")
    print(df[priority_column].value_counts())
    print("\nNo records were found with the label 'Routine'.")
    exit()

# ----------------------------------------------------------
# Calculate starvation indicators
# ----------------------------------------------------------

total_routine = len(routine_df)

routine_over_24 = len(
    routine_df[routine_df["waiting_hours"] > 24]
)

routine_over_48 = len(
    routine_df[routine_df["waiting_hours"] > 48]
)

routine_over_72 = len(
    routine_df[routine_df["waiting_hours"] > 72]
)

maximum_wait = routine_df["waiting_hours"].max()

average_wait = routine_df["waiting_hours"].mean()

# ----------------------------------------------------------
# Calculate aging bonus information
# ----------------------------------------------------------

total_with_aging = len(
    df[df["waiting_age_bonus"] > 0]
)

aging_bonus_1 = len(
    df[df["waiting_age_bonus"] == 1]
)

aging_bonus_2 = len(
    df[df["waiting_age_bonus"] == 2]
)

# ----------------------------------------------------------
# Create results table
# ----------------------------------------------------------

results = pd.DataFrame({
    "metric": [
        "Total routine cases",
        "Routine cases waiting > 24 hours",
        "Routine cases waiting > 48 hours",
        "Routine cases waiting > 72 hours",
        "Average routine waiting time (hours)",
        "Maximum routine waiting time (hours)",
        "Cases receiving waiting-time aging",
        "Cases receiving +1 aging bonus",
        "Cases receiving +2 aging bonus"
    ],
    "value": [
        total_routine,
        routine_over_24,
        routine_over_48,
        routine_over_72,
        round(average_wait, 2),
        round(maximum_wait, 2),
        total_with_aging,
        aging_bonus_1,
        aging_bonus_2
    ]
})

# Save results
results.to_csv(output_file, index=False)

# ----------------------------------------------------------
# Display results
# ----------------------------------------------------------

print("\nSTARVATION INDICATORS")
print("-" * 60)

for _, row in results.iterrows():
    print(f"{row['metric']}: {row['value']}")

print("\n" + "=" * 60)
print("STARVATION ANALYSIS COMPLETED")
print("=" * 60)

print(f"\nResults saved to:")
print(output_file)