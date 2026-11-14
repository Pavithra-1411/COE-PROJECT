
from pathlib import Path
from datetime import datetime, timezone

import pandas as pd


# ==========================================================
# CONFIGURATION
# ==========================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

RESULTS_DIR = PROJECT_ROOT / "results"

AUDIT_FILE = RESULTS_DIR / "clinician_override_audit.csv"

PRIORITIES = ["Urgent", "Priority", "Routine"]

REQUIRED_COLUMNS = [
    "timestamp",
    "referral_id",
    "clinician_id",
    "old_priority",
    "new_priority",
    "reason"
]


# ==========================================================
# LOAD AUDIT HISTORY
# ==========================================================

def load_audit_history():

    if not AUDIT_FILE.exists():
        return pd.DataFrame(columns=REQUIRED_COLUMNS)

    if AUDIT_FILE.stat().st_size == 0:
        return pd.DataFrame(columns=REQUIRED_COLUMNS)

    try:
        history = pd.read_csv(AUDIT_FILE, dtype=str)

        missing = [
            column for column in REQUIRED_COLUMNS
            if column not in history.columns
        ]

        if missing:
            raise ValueError(
                "Audit file is missing columns: "
                + ", ".join(missing)
            )

        return history[REQUIRED_COLUMNS].fillna("")

    except (OSError, pd.errors.ParserError,
            pd.errors.EmptyDataError) as error:

        raise ValueError(
            f"Unable to read audit history: {error}"
        )


# ==========================================================
# APPLY SAVED CLINICIAN OVERRIDES
# ==========================================================

def apply_overrides(referrals):

    referrals = referrals.copy()

    if "system_priority_label_v2" not in referrals.columns:
        raise ValueError(
            "Dataset must contain system_priority_label_v2."
        )

    referrals["effective_priority"] = (
        referrals["system_priority_label_v2"]
    )

    history = load_audit_history()

    if history.empty:
        return referrals

    valid_history = history[
        history["new_priority"].isin(PRIORITIES)
        & history["referral_id"].ne("")
    ].copy()

    # Use the latest saved override for each referral.
    latest_overrides = valid_history.drop_duplicates(
        subset=["referral_id"],
        keep="last"
    )

    override_lookup = dict(
        zip(
            latest_overrides["referral_id"],
            latest_overrides["new_priority"]
        )
    )

    referrals["effective_priority"] = (
        referrals["referral_id"]
        .astype(str)
        .map(override_lookup)
        .fillna(referrals["effective_priority"])
    )

    return referrals


# ==========================================================
# SAVE CLINICIAN OVERRIDE
# ==========================================================

def save_override(
    referral_id,
    clinician_id,
    old_priority,
    new_priority,
    reason
):

    referral_id = str(referral_id).strip()
    clinician_id = str(clinician_id).strip()
    old_priority = str(old_priority).strip()
    new_priority = str(new_priority).strip()
    reason = str(reason).strip()

    # Validate required fields.
    if not referral_id:
        raise ValueError("Referral ID is required.")

    if not clinician_id:
        raise ValueError("Clinician ID is required.")

    if not reason:
        raise ValueError("Override reason is required.")

    # Validate priority values.
    if old_priority not in PRIORITIES:
        raise ValueError("Invalid old priority.")

    if new_priority not in PRIORITIES:
        raise ValueError("Invalid new priority.")

    if old_priority == new_priority:
        raise ValueError(
            "New priority must be different from old priority."
        )

    # Create audit directory if necessary.
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)

    # Prepare audit record.
    record = {
        "timestamp": datetime.now(
            timezone.utc
        ).isoformat(),
        "referral_id": referral_id,
        "clinician_id": clinician_id,
        "old_priority": old_priority,
        "new_priority": new_priority,
        "reason": reason
    }

    # Append record without deleting previous history.
    audit_record = pd.DataFrame(
        [record],
        columns=REQUIRED_COLUMNS
    )

    file_exists = (
        AUDIT_FILE.exists()
        and AUDIT_FILE.stat().st_size > 0
    )

    audit_record.to_csv(
        AUDIT_FILE,
        mode="a",
        header=not file_exists,
        index=False
    )

    return True