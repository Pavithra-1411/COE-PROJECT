# Data Dictionary

## Project Title

A Rule-Based Diagnostic Worklist Prioritisation System for Urgent Cardiology Cases Using Multi-Vendor Diagnostic Data

## Dataset Overview

The dataset contains 1,000 synthetic diagnostic referral records.

The data represents referrals received by a cardiology clinic from
multiple diagnostic device vendors and modalities.

The dataset is created only for academic development, testing, and
evaluation. It does not contain real patient records or real patient
identifying information.

---

## 1. Referral Information

### referral_id

A unique identifier assigned to each diagnostic referral.

Example:

REF0001

### vendor

Represents the diagnostic device vendor associated with the referral.

Possible values include different synthetic vendors such as Vendor_A,
Vendor_B, Vendor_C, and Vendor_D.

### device_id

Identifies the diagnostic device that generated or processed the
referral.

### modality

Represents the type of diagnostic examination.

Examples include:

- ECG
- Echocardiogram

### referral_source

Represents the source from which the diagnostic referral was received.

Examples may include:

- Emergency Department
- Outpatient Clinic
- Cardiology Department
- Primary Care

---

## 2. Patient Information

### patient_age

Represents the synthetic age of the patient associated with the
referral.

This value is generated for academic purposes.

### sex

Represents the synthetic sex value associated with the referral.

No real patient demographic information is used.

---

## 3. Urgency and Symptom Information

### urgency_indicator

Represents the initial urgency level associated with the referral.

Possible values include:

- High
- Medium
- Low

This field is one of the indicators considered by the
prioritisation rules.

### symptom_flag

Represents the overall severity of symptoms associated with the
referral.

Possible values include:

- Severe
- Moderate
- Mild

### chest_pain

Indicates whether chest pain is associated with the referral.

Possible values:

- Yes
- No

### shortness_of_breath

Indicates whether shortness of breath is associated with the referral.

Possible values:

- Yes
- No

### syncope_flag

Indicates whether syncope is associated with the referral.

Possible values:

- Yes
- No

---

## 4. Diagnostic Finding Information

### abnormal_finding

Indicates whether an abnormal diagnostic finding is present.

Possible values:

- Yes
- No

### critical_finding

Indicates whether a potentially critical diagnostic finding is present.

Possible values:

- Yes
- No

### ecg_finding

Represents the synthetic ECG finding category associated with the
referral.

### echo_finding

Represents the synthetic echocardiogram finding category associated
with the referral.

---

## 5. Vital Measurements

### heart_rate_bpm

Represents heart rate measured in beats per minute.

### systolic_bp

Represents systolic blood pressure.

### diastolic_bp

Represents diastolic blood pressure.

### oxygen_saturation

Represents oxygen saturation as a percentage.

These values are included in the dataset for analysis and future
development of more detailed prioritisation rules.

---

## 6. Time and Waiting Information

### referral_datetime

Represents the date and time when the diagnostic referral was received.

### current_datetime

Represents the reference date and time used when generating the
synthetic dataset.

### waiting_hours

Represents the number of hours that the referral has been waiting.

### waiting_time_category

Groups referrals according to their waiting duration.

The categories used in the dataset include:

- Less_than_6h
- 6_to_24h
- 24_to_48h
- More_than_48h

Waiting time is considered by both the baseline method and the
proposed prioritisation system.

---

## 7. Privacy and Access Information

### consent_status

Indicates whether the required consent is available.

Possible values include:

- Yes
- No

Consent is treated as a privacy and access-control consideration.
It is not used as a clinical urgency score.

### data_sensitivity

Represents the sensitivity level associated with the referral data.

### role_visibility

Represents the type of authorised role that should be permitted to
view the referral information.

These fields are included to demonstrate privacy-aware system design.

---

## 8. Study and Clinical Oversight Information

### study_status

Represents the current status of the diagnostic study.

### clinician_override

Indicates whether a clinician has manually changed the priority
assigned by the system.

Possible values:

- Yes
- No

### override_reason

Contains the reason provided for a clinician priority override.

This supports human oversight and auditability.

---

## 9. Reference and Prioritisation Information

### clinician_priority_label

Represents the synthetic reference priority assigned to the referral.

The possible priority levels are:

- Urgent
- Priority
- Routine

This field is used for evaluation.

Important:

This is a synthetic reference label and does not represent actual
clinical ground truth from cardiologists.

### priority_score

Represents the total score calculated by the proposed rule-based
prioritisation system.

The score is calculated using urgency indicators, symptoms,
diagnostic findings, and waiting time.

### system_priority_label

Represents the priority level assigned by the proposed system.

Possible values:

- Urgent
- Priority
- Routine

### priority_reason

Contains a human-readable explanation of the indicators that
contributed to the priority score.

Example:

High urgency, Critical finding, Chest pain

This makes the system output explainable.

---

## 10. Baseline Information

### baseline_priority_label

Represents the priority assigned using the baseline waiting-time
approach.

The baseline uses waiting time as its main prioritisation factor.

### baseline_rank

Represents the referral's position when referrals are ordered using
First-Come, First-Served ordering.

The earliest referral receives the highest position.

---

## 11. Proposed Worklist Information

### proposed_rank

Represents the position of a referral in the worklist generated by
the proposed prioritisation system.

Higher-priority referrals are placed before lower-priority referrals.

The proposed ranking considers:

- Priority level
- Priority score
- Waiting time

---

## 12. Evaluation Information

### evaluation_category

Represents the evaluation result for a referral when comparing the
system's urgent classification with the synthetic reference label.

Possible categories include:

- True Positive
- True Negative
- False Positive
- False Negative

These categories are used to evaluate the performance of the
prioritisation system.

### edge_case_type

Identifies deliberately created synthetic edge or failure cases
used to test system behaviour.

Examples include:

- Normal
- Missing_Urgency
- Missing_Finding
- Conflicting_Indicators
- Excessive_Waiting_Time
- Missing_Consent
- Abnormal_Value
- Invalid_or_Unusual_Value

---

## 13. Data Types

The dataset contains several types of data:

### Categorical Data

Examples:

- vendor
- modality
- urgency_indicator
- symptom_flag
- consent_status
- system_priority_label

### Numerical Data

Examples:

- patient_age
- heart_rate_bpm
- systolic_bp
- diastolic_bp
- oxygen_saturation
- waiting_hours
- priority_score

### Date and Time Data

Examples:

- referral_datetime
- current_datetime

### Text Data

Examples:

- referral_id
- device_id
- priority_reason
- override_reason

---

## 14. Data Usage in the Project

The dataset is used for:

- Data validation
- Data cleaning
- Baseline development
- Rule-based prioritisation
- Worklist generation
- Performance evaluation
- False-negative analysis
- Threshold analysis
- Edge-case testing

---

## 15. Data Privacy and Safety

The dataset contains synthetic records created specifically for this
academic project.

No real patient information is used.

The prioritisation system is an academic prototype and is not a
medically validated clinical decision-making system.

The system is intended to support worklist organisation and
demonstrate explainable prioritisation. It should not replace
professional clinical judgement.