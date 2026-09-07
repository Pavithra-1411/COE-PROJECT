import pandas as pd

# --------------------------------------------------
# 1. LOAD CLEANED DATASET
# --------------------------------------------------

input_file = "data/processed/cleaned_referrals.csv"
output_file = "data/processed/baseline_results.csv"

df = pd.read_csv(input_file)

print("=" * 60)
print("BASELINE PRIORITISATION - FIRST COME FIRST SERVED")
print("=" * 60)


# --------------------------------------------------
# 2. CONVERT REFERRAL DATETIME
# --------------------------------------------------

df["referral_datetime"] = pd.to_datetime(
    df["referral_datetime"],
    errors="coerce"
)


# --------------------------------------------------
# 3. SORT BY REFERRAL TIME
# --------------------------------------------------

df = df.sort_values(
    by="referral_datetime",
    ascending=True
).reset_index(drop=True)


# --------------------------------------------------
# 4. CREATE FCFS RANK
# --------------------------------------------------

df["fcfs_rank"] = range(1, len(df) + 1)


# --------------------------------------------------
# 5. CREATE BASELINE PRIORITY
# --------------------------------------------------

def assign_baseline_priority(waiting_hours):

    if waiting_hours > 48:
        return "Urgent"

    elif waiting_hours > 24:
        return "Priority"

    else:
        return "Routine"


df["baseline_priority"] = df["waiting_hours"].apply(
    assign_baseline_priority
)


# --------------------------------------------------
# 6. DISPLAY DISTRIBUTION
# --------------------------------------------------

print("\nBASELINE PRIORITY DISTRIBUTION")
print("-" * 40)

print(
    df["baseline_priority"].value_counts()
)


# --------------------------------------------------
# 7. SAVE BASELINE RESULTS
# --------------------------------------------------

df.to_csv(
    output_file,
    index=False
)

print("\nBaseline results saved to:")
print(output_file)


# --------------------------------------------------
# 8. FINAL STATUS
# --------------------------------------------------

print("\n" + "=" * 60)
print("BASELINE CREATION COMPLETED")
print("=" * 60)

print("Total referrals:", len(df))
print("First referral :", df.iloc[0]["referral_id"])
print("Last referral  :", df.iloc[-1]["referral_id"])