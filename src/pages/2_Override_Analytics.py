
from pathlib import Path

import pandas as pd
import streamlit as st


# ==========================================================
# OVERRIDE ANALYTICS DASHBOARD
# ==========================================================

st.set_page_config(
    page_title="Override Analytics",
    page_icon="📊",
    layout="wide"
)

BASE_DIR = Path(__file__).resolve().parents[2]

AUDIT_FILE = (
    BASE_DIR /
    "results" /
    "clinician_override_audit.csv"
)


# ==========================================================
# HEADER
# ==========================================================

st.title("📊 Clinician Override Analytics")

st.caption(
    "Monitor clinician priority changes and review "
    "override audit history."
)


# ==========================================================
# LOAD AUDIT DATA
# ==========================================================

if not AUDIT_FILE.exists():
    st.warning(
        "No override audit file found. "
        "Save a clinician override first."
    )
    st.stop()

if AUDIT_FILE.stat().st_size == 0:
    st.info("The audit history is currently empty.")
    st.stop()

try:
    df = pd.read_csv(AUDIT_FILE)

except (
    OSError,
    pd.errors.ParserError,
    pd.errors.EmptyDataError
):
    st.error("Unable to read the audit history file.")
    st.stop()


# ==========================================================
# VALIDATE DATA
# ==========================================================

required_columns = [
    "timestamp",
    "referral_id",
    "clinician_id",
    "old_priority",
    "new_priority",
    "reason"
]

missing_columns = [
    column for column in required_columns
    if column not in df.columns
]

if missing_columns:
    st.error(f"Missing columns: {missing_columns}")
    st.stop()

if df.empty:
    st.info("No clinician overrides have been recorded.")
    st.stop()


# ==========================================================
# DATA PREPARATION
# ==========================================================

df["timestamp"] = pd.to_datetime(
    df["timestamp"],
    errors="coerce",
    utc=True
)

df["priority_change"] = (
    df["old_priority"].astype(str)
    + " → "
    + df["new_priority"].astype(str)
)


# ==========================================================
# SUMMARY METRICS
# ==========================================================

st.subheader("Override Summary")

col1, col2, col3 = st.columns(3)

col1.metric(
    "Total Overrides",
    len(df)
)

col2.metric(
    "Active Clinicians",
    df["clinician_id"].nunique()
)

col3.metric(
    "Affected Referrals",
    df["referral_id"].nunique()
)


# ==========================================================
# PRIORITY CHANGE ANALYSIS
# ==========================================================

st.divider()

st.subheader("Priority Change Analysis")

change_counts = df["priority_change"].value_counts()

st.bar_chart(change_counts)


# ==========================================================
# CLINICIAN ACTIVITY
# ==========================================================

st.divider()

st.subheader("Clinician Activity")

clinician_counts = df["clinician_id"].value_counts()

st.bar_chart(clinician_counts)


# ==========================================================
# AUDIT HISTORY
# ==========================================================

st.divider()

st.subheader("Complete Override History")

display_df = df.sort_values(
    "timestamp",
    ascending=False
)

st.dataframe(
    display_df,
    use_container_width=True,
    hide_index=True
)


# ==========================================================
# DOWNLOAD AUDIT REPORT
# ==========================================================

st.divider()

st.subheader("Download Report")

csv_data = display_df.to_csv(
    index=False
).encode("utf-8")

st.download_button(
    label="⬇ Download Override Audit CSV",
    data=csv_data,
    file_name="clinician_override_report.csv",
    mime="text/csv"
)


# ==========================================================
# FOOTER
# ==========================================================

st.caption(
    "CardioGuard | Clinician Override Analytics | "
    "Audit data from the project CSV file"
)
