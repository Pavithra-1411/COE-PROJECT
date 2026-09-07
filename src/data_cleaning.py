import pandas as pd

# --------------------------------------------------
# 1. LOAD RAW DATASET
# --------------------------------------------------

input_file = "data/raw/cardiology_dataset_raw.csv"
output_file = "data/processed/cleaned_referrals.csv"

df = pd.read_csv(input_file)

print("=" * 60)
print("CARDIOLOGY DATA CLEANING")
print("=" * 60)

print("\nOriginal dataset:")
print("Rows    :", df.shape[0])
print("Columns :", df.shape[1])


# --------------------------------------------------
# 2. REMOVE DUPLICATE REFERRAL IDs
# --------------------------------------------------

duplicates = df["referral_id"].duplicated().sum()

print("\nDuplicate referral IDs:", duplicates)

if duplicates > 0:
    df = df.drop_duplicates(
        subset="referral_id",
        keep="first"
    )

print("Rows after duplicate removal:", len(df))


# --------------------------------------------------
# 3. CONVERT DATE/TIME COLUMNS
# --------------------------------------------------

df["referral_datetime"] = pd.to_datetime(
    df["referral_datetime"],
    errors="coerce"
)

df["current_datetime"] = pd.to_datetime(
    df["current_datetime"],
    errors="coerce"
)

print("\nDatetime columns converted successfully.")


# --------------------------------------------------
# 4. CHECK IMPORTANT NUMERIC COLUMNS
# --------------------------------------------------

numeric_columns = [
    "patient_age",
    "heart_rate_bpm",
    "systolic_bp",
    "diastolic_bp",
    "oxygen_saturation",
    "waiting_hours",
    "priority_score",
    "baseline_rank",
    "proposed_rank"
]

for column in numeric_columns:
    df[column] = pd.to_numeric(
        df[column],
        errors="coerce"
    )

print("Numeric columns checked successfully.")


# --------------------------------------------------
# 5. CHECK MISSING VALUES
# --------------------------------------------------

print("\nMissing values after cleaning:")
missing = df.isnull().sum()

missing = missing[missing > 0]

if len(missing) == 0:
    print("No missing values found.")
else:
    print(missing)


# --------------------------------------------------
# 6. SAVE CLEANED DATASET
# --------------------------------------------------

df.to_csv(
    output_file,
    index=False
)

print("\nCleaned dataset saved to:")
print(output_file)


# --------------------------------------------------
# 7. FINAL STATUS
# --------------------------------------------------

print("\n" + "=" * 60)
print("DATA CLEANING COMPLETED")
print("=" * 60)

print("Final rows    :", df.shape[0])
print("Final columns :", df.shape[1])