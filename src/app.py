import streamlit as st
import pandas as pd


# ==========================================================
# PAGE CONFIGURATION
# ==========================================================

st.set_page_config(
    page_title="CardioGuard",
    page_icon="❤️",
    layout="wide"
)


# ==========================================================
# CUSTOM CSS
# ==========================================================

st.markdown("""
<style>

.main {
    padding-top: 1rem;
}

.block-container {
    padding-top: 1.5rem;
    padding-bottom: 2rem;
}

.hero {
    padding: 25px;
    border-radius: 18px;
    background: linear-gradient(
        135deg,
        #151922,
        #242936
    );
    border: 1px solid #3b4252;
    margin-bottom: 25px;
}

.hero-title {
    font-size: 38px;
    font-weight: 800;
    margin-bottom: 5px;
}

.hero-subtitle {
    font-size: 17px;
    color: #b9c0cc;
}

.status {
    display: inline-block;
    padding: 7px 14px;
    border-radius: 20px;
    background: #173d2c;
    color: #6ee7a0;
    font-weight: 700;
    font-size: 13px;
}

.priority-card {
    padding: 18px;
    border-radius: 15px;
    background: #1b1f28;
    border: 1px solid #343a46;
    min-height: 125px;
}

.priority-title {
    font-size: 15px;
    color: #aeb5c2;
}

.priority-number {
    font-size: 32px;
    font-weight: 800;
    margin-top: 8px;
}

.priority-description {
    font-size: 13px;
    color: #8f97a6;
}

.section-title {
    font-size: 25px;
    font-weight: 750;
    margin-top: 20px;
    margin-bottom: 12px;
}

.case-card {
    padding: 18px;
    border-radius: 14px;
    background: #1b1f28;
    border: 1px solid #343a46;
    margin-bottom: 10px;
}

.case-id {
    font-size: 20px;
    font-weight: 750;
}

.case-info {
    color: #aeb5c2;
    font-size: 14px;
}

.explanation {
    padding: 18px;
    border-radius: 15px;
    background: #191e27;
    border: 1px solid #394150;
}

.explanation-title {
    font-size: 20px;
    font-weight: 750;
    margin-bottom: 12px;
}

.score-box {
    padding: 15px;
    border-radius: 12px;
    background: #222733;
    text-align: center;
}

.score-number {
    font-size: 30px;
    font-weight: 800;
}

.small-label {
    color: #9da5b3;
    font-size: 13px;
}

div[data-testid="stMetric"] {
    background-color: #1b1f28;
    border: 1px solid #343a46;
    padding: 15px;
    border-radius: 14px;
}

</style>
""", unsafe_allow_html=True)


# ==========================================================
# LOAD DATA
# ==========================================================

DATA_FILE = "data/processed/prioritized_referrals_v2.csv"

df = pd.read_csv(DATA_FILE)


# ==========================================================
# HELPER FUNCTIONS
# ==========================================================

def get_value(row, column, default="Not available"):
    if column in row.index:
        value = row[column]

        if pd.isna(value):
            return default

        return value

    return default


def priority_icon(priority):
    if priority == "Urgent":
        return "🔴"

    if priority == "Priority":
        return "🟠"

    return "🟢"


# ==========================================================
# HEADER
# ==========================================================

st.markdown("""
<div class="hero">

<div style="display:flex; justify-content:space-between;
align-items:center;">

<div>

<div class="hero-title">
❤️ CardioGuard
</div>

<div class="hero-subtitle">
Explainable Cardiology Diagnostic Worklist
</div>

</div>

<div class="status">
● SYSTEM ONLINE
</div>

</div>

</div>
""", unsafe_allow_html=True)


# ==========================================================
# SIDEBAR
# ==========================================================

st.sidebar.title("⚙ Worklist Controls")

st.sidebar.subheader("User Role")

role = st.sidebar.selectbox(
    "Select role",
    [
        "Technician",
        "Cardiologist"
    ]
)


st.sidebar.subheader("Priority Filter")

priority_filter = st.sidebar.selectbox(
    "Show priority",
    [
        "All",
        "Urgent",
        "Priority",
        "Routine"
    ]
)


# ==========================================================
# FILTER DATA
# ==========================================================

if priority_filter == "All":

    display_df = df.copy()

else:

    display_df = df[
        df["system_priority_label_v2"] == priority_filter
    ].copy()


# ==========================================================
# TOP SUMMARY
# ==========================================================

st.markdown(
    '<div class="section-title">📊 Worklist Overview</div>',
    unsafe_allow_html=True
)

col1, col2, col3, col4 = st.columns(4)


with col1:

    st.metric(
        "Total Referrals",
        len(display_df)
    )


with col2:

    urgent_count = len(
        display_df[
            display_df["system_priority_label_v2"] == "Urgent"
        ]
    )

    st.metric(
        "🔴 Urgent",
        urgent_count
    )


with col3:

    priority_count = len(
        display_df[
            display_df["system_priority_label_v2"] == "Priority"
        ]
    )

    st.metric(
        "🟠 Priority",
        priority_count
    )


with col4:

    routine_count = len(
        display_df[
            display_df["system_priority_label_v2"] == "Routine"
        ]
    )

    st.metric(
        "🟢 Routine",
        routine_count
    )


# ==========================================================
# STARVATION PROTECTION
# ==========================================================

aging_count = 0

if "waiting_age_bonus" in display_df.columns:

    aging_count = len(
        display_df[
            display_df["waiting_age_bonus"] > 0
        ]
    )


st.markdown(
    '<div class="section-title">⏱ Starvation Protection</div>',
    unsafe_allow_html=True
)

aging_col1, aging_col2, aging_col3 = st.columns(3)


with aging_col1:

    st.metric(
        "Cases Receiving Aging",
        aging_count
    )


with aging_col2:

    if "waiting_age_bonus" in display_df.columns:

        plus_one = len(
            display_df[
                display_df["waiting_age_bonus"] == 1
            ]
        )

    else:

        plus_one = 0

    st.metric(
        "+1 Aging Bonus",
        plus_one
    )


with aging_col3:

    if "waiting_age_bonus" in display_df.columns:

        plus_two = len(
            display_df[
                display_df["waiting_age_bonus"] == 2
            ]
        )

    else:

        plus_two = 0

    st.metric(
        "+2 Aging Bonus",
        plus_two
    )


# ==========================================================
# ROLE INDICATOR
# ==========================================================

st.markdown("---")

if role == "Technician":

    st.info(
        "🔧 Technician View: Operational information is displayed."
    )

else:

    st.info(
        "🩺 Cardiologist View: Clinical evidence and "
        "prioritization information are displayed."
    )


# ==========================================================
# WORKLIST
# ==========================================================

st.markdown(
    '<div class="section-title">📋 Diagnostic Worklist</div>',
    unsafe_allow_html=True
)


# Sort urgent cases first

priority_order = {
    "Urgent": 0,
    "Priority": 1,
    "Routine": 2
}

display_df["priority_order"] = display_df[
    "system_priority_label_v2"
].map(priority_order)

display_df = display_df.sort_values(
    by=["priority_order", "waiting_hours"],
    ascending=[True, False]
)


# Show maximum 20 cases

worklist_df = display_df.head(20)


# ==========================================================
# WORKLIST DISPLAY
# ==========================================================

for index, row in worklist_df.iterrows():

    referral_id = get_value(
        row,
        "referral_id"
    )

    priority = get_value(
        row,
        "system_priority_label_v2"
    )

    vendor = get_value(
        row,
        "vendor"
    )

    device = get_value(
        row,
        "device_id"
    )

    modality = get_value(
        row,
        "modality"
    )

    waiting = get_value(
        row,
        "waiting_hours"
    )

    score = get_value(
        row,
        "priority_score_v2"
    )

    icon = priority_icon(priority)


    col1, col2, col3 = st.columns(
        [4, 2, 2]
    )


    with col1:

        st.markdown(
            f"""
            <div class="case-card">

            <div class="case-id">
            {icon} {referral_id}
            </div>

            <div class="case-info">
            {modality} &nbsp;•&nbsp;
            {vendor} &nbsp;•&nbsp;
            {device}
            </div>

            </div>
            """,
            unsafe_allow_html=True
        )


    with col2:

        st.metric(
            "Priority",
            priority
        )


    with col3:

        st.metric(
            "Waiting",
            f"{waiting} h"
        )


# ==========================================================
# SELECT REFERRAL
# ==========================================================

st.markdown(
    '<div class="section-title">🔎 Review Referral</div>',
    unsafe_allow_html=True
)


if len(worklist_df) > 0:

    selected_referral = st.selectbox(
        "Select a referral for details",
        worklist_df["referral_id"].tolist()
    )


    selected_row = worklist_df[
        worklist_df["referral_id"] == selected_referral
    ].iloc[0]


    # ======================================================
    # REFERRAL HEADER
    # ======================================================

    selected_priority = get_value(
        selected_row,
        "system_priority_label_v2"
    )

    selected_score = get_value(
        selected_row,
        "priority_score_v2"
    )

    selected_waiting = get_value(
        selected_row,
        "waiting_hours"
    )

    selected_bonus = get_value(
        selected_row,
        "waiting_age_bonus",
        0
    )


    st.markdown(
        f"""
        <div class="explanation">

        <div class="explanation-title">
        {priority_icon(selected_priority)}
        {selected_referral}
        — {selected_priority}
        </div>

        <div class="case-info">
        Selected referral for detailed review
        </div>

        </div>
        """,
        unsafe_allow_html=True
    )


    # ======================================================
    # TWO COLUMN DETAILS
    # ======================================================

    left_col, right_col = st.columns(2)


    # ======================================================
    # EVIDENCE
    # ======================================================

    with left_col:

        st.subheader("🧠 Decision Evidence")

        reason = get_value(
            selected_row,
            "priority_reason",
            "No explanation available"
        )

        st.markdown(
            f"""
            <div class="explanation">

            <div class="explanation-title">
            Why was this case prioritized?
            </div>

            <p>✓ {reason}</p>

            <p>
            ✓ Waiting time: {selected_waiting} hours
            </p>

            <p>
            ✓ Priority score: {selected_score}
            </p>

            </div>
            """,
            unsafe_allow_html=True
        )


    # ======================================================
    # SCORE BREAKDOWN
    # ======================================================

    with right_col:

        st.subheader("📈 Priority Breakdown")

        score_col1, score_col2, score_col3 = st.columns(3)


        with score_col1:

            st.markdown(
                f"""
                <div class="score-box">

                <div class="small-label">
                Clinical Score
                </div>

                <div class="score-number">
                {float(selected_score) - float(selected_bonus):.0f}
                </div>

                </div>
                """,
                unsafe_allow_html=True
            )


        with score_col2:

            st.markdown(
                f"""
                <div class="score-box">

                <div class="small-label">
                Aging Bonus
                </div>

                <div class="score-number">
                +{selected_bonus}
                </div>

                </div>
                """,
                unsafe_allow_html=True
            )


        with score_col3:

            st.markdown(
                f"""
                <div class="score-box">

                <div class="small-label">
                Final Score
                </div>

                <div class="score-number">
                {selected_score}
                </div>

                </div>
                """,
                unsafe_allow_html=True
            )


# ==========================================================
# CARDIOLOGIST DETAILS
# ==========================================================

if role == "Cardiologist":

    st.markdown("---")

    st.markdown(
        '<div class="section-title">🩺 Clinical Review</div>',
        unsafe_allow_html=True
    )


    clinical_col1, clinical_col2 = st.columns(2)


    with clinical_col1:

        st.subheader("Clinical Indicators")

        clinical_fields = [
            ("Heart Rate", "heart_rate_bpm", "bpm"),
            ("Systolic BP", "systolic_bp", "mmHg"),
            ("Oxygen Saturation", "oxygen_saturation", "%"),
            ("Chest Pain", "chest_pain", ""),
            ("Shortness of Breath", "shortness_of_breath", ""),
            ("Syncope", "syncope_flag", ""),
            ("Abnormal Finding", "abnormal_finding", ""),
            ("Critical Finding", "critical_finding", "")
        ]

        for label, column, unit in clinical_fields:

            if column in selected_row.index:

                value = get_value(
                    selected_row,
                    column
                )

                st.write(
                    f"**{label}:** {value} {unit}"
                )


    with clinical_col2:

        st.subheader("Privacy & Clinician Control")

        consent = get_value(
            selected_row,
            "consent_status"
        )

        sensitivity = get_value(
            selected_row,
            "data_sensitivity"
        )

        visibility = get_value(
            selected_row,
            "role_visibility"
        )

        override = get_value(
            selected_row,
            "clinician_override"
        )


        st.write(
            f"**Consent Status:** {consent}"
        )

        st.write(
            f"**Data Sensitivity:** {sensitivity}"
        )

        st.write(
            f"**Role Visibility:** {visibility}"
        )

        st.write(
            f"**Clinician Override:** {override}"
        )


# ==========================================================
# FOOTER
# ==========================================================

st.markdown("---")

st.caption(
    "CardioGuard | Explainable diagnostic-worklist prototype | "
    "Synthetic data only | Clinician remains responsible for final decisions"
)