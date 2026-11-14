
from pathlib import Path
import os
import pandas as pd
import streamlit as st

# Import existing override functions
from override_manager import apply_overrides, save_override

# Import workflow functions
from workflow_manager import (
    apply_workflow_statuses,
    update_workflow_status,
    load_workflow_history
)

st.set_page_config(
    page_title="CardioGuard",
    page_icon="❤️",
    layout="wide"
)

ROOT = Path(__file__).resolve().parent.parent

DATA_FILE = ROOT / "data" / "processed" / "prioritized_referrals_v2.csv"
AUDIT_FILE = ROOT / "results" / "clinician_override_audit.csv"

PRIORITIES = ["Urgent", "Priority", "Routine"]
PRIORITY_ORDER = {
    name: i for i, name in enumerate(PRIORITIES)
}

WORKFLOW_STATUSES = [
    "New",
    "Waiting",
    "Under_Review",
    "Completed",
    "Cancelled"
]

# Ensure project-relative paths work
os.chdir(ROOT)


# ==========================================================
# HELPER FUNCTIONS
# ==========================================================

def safe_value(row, name, default="Not available"):
    if name not in row.index:
        return default

    value = row[name]

    return default if pd.isna(value) else value


def read_history(referral_id):

    if not AUDIT_FILE.is_file() or AUDIT_FILE.stat().st_size == 0:
        return pd.DataFrame()

    try:
        history = pd.read_csv(AUDIT_FILE, dtype=str)

    except (OSError, pd.errors.EmptyDataError, pd.errors.ParserError):
        return pd.DataFrame()

    if "referral_id" not in history.columns:
        return pd.DataFrame()

    return history.loc[
        history["referral_id"] == str(referral_id)
    ].iloc[::-1].reset_index(drop=True)


# ==========================================================
# LOAD DATASET
# ==========================================================

if not DATA_FILE.is_file():
    st.error(f"Dataset not found: {DATA_FILE}")
    st.stop()

try:

    referrals = pd.read_csv(DATA_FILE)

    required = [
        "referral_id",
        "system_priority_label_v2",
        "waiting_hours",
        "study_status"
    ]

    missing = [
        name for name in required
        if name not in referrals.columns
    ]

    if missing:
        st.error(
            "Missing required dataset columns: "
            + ", ".join(missing)
        )
        st.stop()

    referrals["referral_id"] = (
        referrals["referral_id"].astype(str)
    )

    # Apply saved clinician priority overrides
    referrals = apply_overrides(referrals)

    # Apply saved workflow status updates
    referrals = apply_workflow_statuses(referrals)

except (OSError, ValueError, KeyError) as error:

    st.error(f"Unable to load referrals: {error}")
    st.stop()


# ==========================================================
# DASHBOARD HEADER
# ==========================================================

st.title("❤️ CardioGuard")

st.write(
    "Explainable Cardiology Diagnostic Worklist"
)

st.success("● PROTOTYPE ONLINE")


# ==========================================================
# SIDEBAR CONTROLS
# ==========================================================

with st.sidebar:

    st.header("⚙️ Worklist Controls")

    role = st.selectbox(
        "Select role",
        ["Technician", "Cardiologist"]
    )

    priority_filter = st.selectbox(
        "Show priority",
        ["All"] + PRIORITIES
    )

    st.caption(
        "Role selection is for demonstration only; "
        "it is not authentication."
    )


# ==========================================================
# FILTER REFERRALS
# ==========================================================

if priority_filter == "All":

    display_df = referrals.copy()

else:

    display_df = referrals.loc[
        referrals["effective_priority"] == priority_filter
    ].copy()


# ==========================================================
# WORKLIST OVERVIEW
# ==========================================================

st.header("📊 Worklist Overview")

metrics = st.columns(4)

metrics[0].metric(
    "Total Referrals",
    len(display_df)
)

for column, priority, icon in zip(
    metrics[1:],
    PRIORITIES,
    ["🔴", "🟠", "🟢"]
):

    column.metric(
        f"{icon} {priority}",
        int(
            (
                display_df["effective_priority"] == priority
            ).sum()
        )
    )


# ==========================================================
# WORKFLOW STATUS OVERVIEW
# ==========================================================

st.header("🔄 Referral Workflow Overview")

status_columns = st.columns(5)

for column, status in zip(
    status_columns,
    WORKFLOW_STATUSES
):

    count = int(
        (display_df["study_status"] == status).sum()
    )

    column.metric(
        status.replace("_", " "),
        count
    )


# ==========================================================
# STARVATION PROTECTION
# ==========================================================

st.header("⏱️ Starvation Protection")

if "waiting_age_bonus" in display_df.columns:

    aging = pd.to_numeric(
        display_df["waiting_age_bonus"],
        errors="coerce"
    ).fillna(0)

else:

    aging = pd.Series(
        0,
        index=display_df.index
    )

aging_cols = st.columns(3)

aging_cols[0].metric(
    "Cases Receiving Aging",
    int((aging > 0).sum())
)

aging_cols[1].metric(
    "+1 Aging Bonus",
    int((aging == 1).sum())
)

aging_cols[2].metric(
    "+2 Aging Bonus",
    int((aging == 2).sum())
)

st.caption(
    "Waiting-time bonuses are capped to preserve clinical urgency."
)


# ==========================================================
# ROLE INFORMATION
# ==========================================================

if role == "Technician":

    st.info(
        "🔧 Technician view: operational referral information."
    )

else:

    st.info(
        "🩺 Cardiologist view: clinical evidence, "
        "priority overrides, and audit history."
    )


# ==========================================================
# REFERRAL STATUS MANAGEMENT
# ==========================================================

st.header("🔄 Referral Status Management")

if display_df.empty:

    st.warning(
        "No referrals are available for the selected priority."
    )

else:

    referral_ids = display_df[
        "referral_id"
    ].astype(str).tolist()

    with st.form("workflow_update_form"):

        selected_referral = st.selectbox(
            "Select Referral ID",
            referral_ids
        )

        selected_row = display_df.loc[
            display_df["referral_id"] == selected_referral
        ].iloc[0]

        current_status = str(
            selected_row["study_status"]
        )

        st.write(
            f"**Current Status:** {current_status.replace('_', ' ')}"
        )

        new_status = st.selectbox(
            "Update Status",
            WORKFLOW_STATUSES
        )

        updated_by = st.text_input(
            "User ID",
            placeholder="Enter your user ID"
        )

        reason = st.text_area(
            "Reason for Status Update",
            placeholder="Enter the reason for this update"
        )

        submit_status = st.form_submit_button(
            "Save Status Update"
        )

    if submit_status:

        try:

            update_workflow_status(
                referral_id=selected_referral,
                old_status=current_status,
                new_status=new_status,
                updated_by=updated_by,
                reason=reason
            )

            st.success(
                f"Status updated successfully for {selected_referral}."
            )

            st.rerun()

        except ValueError as error:

            st.error(str(error))

        except OSError as error:

            st.error(
                f"Unable to save status update: {error}"
            )


# ==========================================================
# WORKFLOW HISTORY
# ==========================================================

st.subheader("📜 Referral Workflow History")

try:

    workflow_history = load_workflow_history()

    if not workflow_history.empty:

        if not display_df.empty:

            history_referral = st.selectbox(
                "Choose Referral to View History",
                display_df["referral_id"].astype(str).tolist(),
                key="workflow_history_referral"
            )

            referral_history = workflow_history.loc[
                workflow_history["referral_id"] == history_referral
            ].iloc[::-1].reset_index(drop=True)

            if referral_history.empty:

                st.info(
                    "No workflow history found for this referral."
                )

            else:

                st.dataframe(
                    referral_history,
                    use_container_width=True,
                    hide_index=True
                )

    else:

        st.info(
            "No workflow status updates have been recorded yet."
        )

except (OSError, ValueError, KeyError) as error:

    st.error(
        f"Unable to display workflow history: {error}"
    )


# ==========================================================
# DIAGNOSTIC WORKLIST
# ==========================================================

st.header("📋 Diagnostic Worklist")

display_df["_priority_order"] = (
    display_df["effective_priority"]
    .map(PRIORITY_ORDER)
    .fillna(3)
)

display_df = display_df.sort_values(
    by=["_priority_order", "waiting_hours"],
    ascending=[True, False]
)

display_df = display_df.drop(
    columns=["_priority_order"]
)

st.dataframe(
    display_df,
    use_container_width=True,
    hide_index=True
)
