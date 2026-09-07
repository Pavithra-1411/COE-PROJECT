import pandas as pd

# --------------------------------------------------
# 1. LOAD RAW DATASET
# --------------------------------------------------

file_path = "data/raw/cardiology_dataset_raw.csv"

df = pd.read_csv(file_path)

print("=" * 60)
print("CARDIOLOGY DATASET VALIDATION")
print("=" * 60)


# --------------------------------------------------
# 2. DATASET SIZE
# --------------------------------------------------

print("\n1. DATASET SIZE")
print("-" * 40)

print("Rows    :", df.shape[0])
print("Columns :", df.shape[1])


# --------------------------------------------------
# 3. COLUMN NAMES
# --------------------------------------------------

print("\n2. COLUMN NAMES")
print("-" * 40)

for i, column in enumerate(df.columns, start=1):
    print(f"{i}. {column}")


# --------------------------------------------------
# 4. DATA TYPES
# --------------------------------------------------

print("\n3. DATA TYPES")
print("-" * 40)

print(df.dtypes)


# --------------------------------------------------
# 5. MISSING VALUES
# --------------------------------------------------

print("\n4. MISSING VALUES")
print("-" * 40)

missing_values = df.isnull().sum()

print(
    missing_values[
        missing_values > 0
    ]
)


# --------------------------------------------------
# 6. DUPLICATE REFERRAL IDs
# --------------------------------------------------

print("\n5. DUPLICATE REFERRAL IDs")
print("-" * 40)

duplicates = df["referral_id"].duplicated().sum()

print("Duplicate IDs:", duplicates)


# --------------------------------------------------
# 7. PRIORITY DISTRIBUTION
# --------------------------------------------------

print("\n6. SYSTEM PRIORITY DISTRIBUTION")
print("-" * 40)

print(
    df["system_priority_label"]
    .value_counts()
)


# --------------------------------------------------
# 8. CLINICIAN REFERENCE DISTRIBUTION
# --------------------------------------------------

print("\n7. CLINICIAN REFERENCE DISTRIBUTION")
print("-" * 40)

print(
    df["clinician_priority_label"]
    .value_counts()
)


# --------------------------------------------------
# 9. EDGE CASE DISTRIBUTION
# --------------------------------------------------

print("\n8. EDGE CASE DISTRIBUTION")
print("-" * 40)

print(
    df["edge_case_type"]
    .value_counts()
)


# --------------------------------------------------
# 10. DATE COLUMNS
# --------------------------------------------------

print("\n9. DATE COLUMN CHECK")
print("-" * 40)

print("Referral datetime sample:")

print(
    df["referral_datetime"].head()
)

print("\nCurrent datetime sample:")

print(
    df["current_datetime"].head()
)


# --------------------------------------------------
# 11. WAITING TIME
# --------------------------------------------------

print("\n10. WAITING TIME CHECK")
print("-" * 40)

print(
    df["waiting_hours"].describe()
)


# --------------------------------------------------
# 12. FIRST FIVE RECORDS
# --------------------------------------------------

print("\n11. FIRST FIVE RECORDS")
print("-" * 40)

print(
    df.head()
)


# --------------------------------------------------
# 13. FINAL STATUS
# --------------------------------------------------

print("\n" + "=" * 60)
print("DATASET VALIDATION COMPLETED")
print("=" * 60)