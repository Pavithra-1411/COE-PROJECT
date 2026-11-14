
from pathlib import Path
from datetime import datetime, timezone

import pandas as pd


# ==========================================================
# CONFIGURATION
# ==========================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

RESULTS_DIR = PROJECT_ROOT / "results"

WORKFLOW_FILE = (
    RESULTS_DIR / "referral_workflow_status.csv"
)

VALID_STATUSES = [
    "New",
    "Waiting",
    "Under_Review",
    "Completed",
    "Cancelled"
]

WORKFLOW_COLUMNS = [
    "timestamp",
    "referral_id",
    "old_status",
    "new_status",
    "updated_by",
    "reason"
]


# ==========================================================
# LOAD WORKFLOW HISTORY
# ==========================================================

def load_workflow_history():

    if not WORKFLOW_FILE.exists():
        return pd.DataFrame(columns=WORKFLOW_COLUMNS)

    if WORKFLOW_FILE.stat().st_size == 0:
        return pd.DataFrame(columns=WORKFLOW_COLUMNS)

    try:
        history = pd.read_csv(
            WORKFLOW_FILE,
            dtype=str
        )

        missing = [
            col for col in WORKFLOW_COLUMNS
            if col not in history.columns
        ]

        if missing:
            raise ValueError(
                "Missing workflow columns: "
                + ", ".join(missing)
            )

        return history[WORKFLOW_COLUMNS].fillna("")

    except (
        OSError,
        pd.errors.ParserError,
        pd.errors.EmptyDataError
    ) as error:

        raise ValueError(
            f"Unable to load workflow history: {error}"
        )


# ==========================================================
# APPLY SAVED WORKFLOW STATUSES
# ==========================================================

def apply_workflow_statuses(referrals):

    referrals = referrals.copy()

    if "referral_id" not in referrals.columns:
        raise ValueError("Referral ID column is missing.")

    if "study_status" not in referrals.columns:
        raise ValueError("Study status column is missing.")

    referrals["study_status"] = (
        referrals["study_status"].fillna("New")
    )

    history = load_workflow_history()

    if history.empty:
        return referrals

    valid_history = history[
        history["new_status"].isin(VALID_STATUSES)
        & history["referral_id"].ne("")
    ].copy()

    latest = valid_history.drop_duplicates(
        subset=["referral_id"],
        keep="last"
    )

    status_lookup = dict(
        zip(
            latest["referral_id"],
            latest["new_status"]
        )
    )

    referrals["study_status"] = (
        referrals["referral_id"]
        .astype(str)
        .map(status_lookup)
        .fillna(referrals["study_status"])
    )

    return referrals


# ==========================================================
# SAVE WORKFLOW STATUS UPDATE
# ==========================================================

def update_workflow_status(
    referral_id,
    old_status,
    new_status,
    updated_by,
    reason
):

    referral_id = str(referral_id).strip()
    old_status = str(old_status).strip()
    new_status = str(new_status).strip()
    updated_by = str(updated_by).strip()
    reason = str(reason).strip()

    if not referral_id:
        raise ValueError("Referral ID is required.")

    if old_status not in VALID_STATUSES:
        raise ValueError("Invalid old status.")

    if new_status not in VALID_STATUSES:
        raise ValueError("Invalid new status.")

    if old_status == new_status:
        raise ValueError(
            "New status must be different."
        )

    if not updated_by:
        raise ValueError("User ID is required.")

    if not reason:
        raise ValueError("Update reason is required.")

    RESULTS_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    record = {
        "timestamp": datetime.now(
            timezone.utc
        ).isoformat(),
        "referral_id": referral_id,
        "old_status": old_status,
        "new_status": new_status,
        "updated_by": updated_by,
        "reason": reason
    }

    file_exists = (
        WORKFLOW_FILE.exists()
        and WORKFLOW_FILE.stat().st_size > 0
    )

    pd.DataFrame(
        [record],
        columns=WORKFLOW_COLUMNS
    ).to_csv(
        WORKFLOW_FILE,
        mode="a",
        header=not file_exists,
        index=False
    )

    return True
