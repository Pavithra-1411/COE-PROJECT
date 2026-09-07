# A Rule-Based Diagnostic Worklist Prioritisation System for Urgent Cardiology Cases Using Multi-Vendor Diagnostic Data

## 1. Project Overview

This project proposes a rule-based diagnostic worklist prioritisation system for a cardiology clinic where diagnostic referrals are received from multiple vendors and devices.

The main problem is that urgent cardiology cases may not always be prioritised consistently when referrals arrive from different diagnostic devices and vendors.

The proposed system analyses referral information, urgency indicators, symptoms, diagnostic findings, and waiting time to assign a priority level to each referral.

The system produces three priority levels:

- Urgent
- Priority
- Routine

The system also provides a reason for each priority decision to improve transparency and explainability.

This project uses synthetic data for academic and prototype purposes.

---

## 2. Problem Statement

Solving urgent cases is not always prioritised consistently in a cardiology clinic when diagnostic data is received from multiple devices and vendors.

Different diagnostic devices may produce data in different formats, making it difficult to create a consistent worklist.

A transparent prioritisation mechanism is therefore required to help organise referrals based on predefined rules and available indicators.

---

## 3. Project Objective

The main objectives of this project are:

1. Generate a structured synthetic dataset representing cardiology referrals.
2. Represent diagnostic data from multiple vendors and modalities.
3. Validate and clean the referral data.
4. Establish a First Come First Served baseline.
5. Develop an explainable rule-based prioritisation system.
6. Assign referrals into Urgent, Priority, and Routine categories.
7. Provide a reason for each system priority decision.
8. Compare the proposed system with a synthetic reference label.
9. Analyse false positives and false negatives.
10. Evaluate different priority thresholds.
11. Identify limitations and edge cases in the prioritisation process.

---

## 4. Scope of Review 1

The first review focuses on the foundation of the proposed system.

The following components have been completed:

- Problem analysis
- Synthetic dataset generation
- Data validation
- Data dictionary
- Data cleaning
- First Come First Served baseline
- Rule-based prioritisation
- Initial evaluation
- False-negative analysis
- Threshold analysis
- Edge-case analysis

The full user interface and application are planned for later stages of the project.

---

## 5. Dataset

The project uses a synthetic dataset containing:

- 1,000 referral records
- 39 attributes
- Multiple diagnostic vendors
- Multiple diagnostic modalities
- Synthetic patient and referral information

The dataset does not contain real patient information.

### Main Data Categories

The dataset contains information related to:

- Referral details
- Vendor and device information
- Diagnostic modality
- Patient demographics
- Urgency indicators
- Symptoms
- Diagnostic findings
- Vital signs
- Referral and waiting times
- Consent and privacy
- Clinician oversight
- System priority
- Baseline priority
- Evaluation results
- Edge cases

The raw dataset is stored at:

`data/raw/cardiology_dataset_raw.csv`

---

## 6. Multi-Vendor Diagnostic Data

The synthetic dataset represents diagnostic referrals from multiple vendors.

The vendor information is included to simulate a real-world environment where a clinic may receive diagnostic information from different device manufacturers.

The project currently includes multiple diagnostic modalities such as:

- ECG
- Echocardiogram

The vendor and device information can later be used to demonstrate data standardisation across different diagnostic sources.

---

## 7. Data Validation

A data validation process was implemented to check the quality and structure of the dataset.

The validation process checks:

- Dataset dimensions
- Column names
- Data types
- Missing values
- Duplicate referral IDs
- Priority distributions
- Edge cases
- Date and time fields
- Waiting-time values
- Sample records

The validation script is located at:

`src/data_validation.py`

---

## 8. Data Cleaning

A data cleaning script was developed to prepare the dataset for further analysis.

The cleaning process includes:

- Checking duplicate referral IDs
- Removing duplicate referrals if present
- Converting date and time fields
- Converting numerical fields into numeric data types
- Checking missing values
- Saving the cleaned dataset

The cleaned dataset is stored at:

`data/processed/cleaned_referrals.csv`

The cleaning script is located at:

`src/data_cleaning.py`

---

## 9. Baseline Approach

A First Come First Served (FCFS) approach was implemented as the baseline.

In this approach, referrals are ordered according to their referral date and time.

The earliest referral is assigned the highest position in the queue.

A baseline priority category is also assigned using waiting time:

- More than 48 hours → Urgent
- More than 24 hours → Priority
- 24 hours or less → Routine

The baseline script is:

`src/baseline.py`

The baseline output is:

`data/processed/baseline_results.csv`

### Baseline Result

The 1,000 referrals were classified as:

- Routine: 708
- Priority: 205
- Urgent: 87

This baseline provides a simple reference for comparing the proposed prioritisation approach.

---

## 10. Proposed Rule-Based Prioritisation

The proposed system uses a weighted rule-based scoring approach.

Each referral receives a priority score based on available indicators.

### Priority Rules

High urgency:

`+3`

Medium urgency:

`+1`

Severe symptoms:

`+2`

Moderate symptoms:

`+1`

Abnormal finding:

`+2`

Critical finding:

`+3`

Syncope:

`+2`

Chest pain:

`+1`

Shortness of breath:

`+1`

Waiting more than 48 hours:

`+2`

Waiting more than 24 hours:

`+1`

### Priority Classification

A score of 7 or above is classified as:

**Urgent**

A score from 4 to 6 is classified as:

**Priority**

A score below 4 is classified as:

**Routine**

The prioritisation rules are documented in:

`docs/rule_definitions.md`

The prioritisation script is:

`src/prioritizer.py`

The generated prioritised dataset is:

`data/processed/prioritized_referrals.csv`

---

## 11. Explainability

The system does not only assign a priority level.

It also generates a priority reason based on the rules that contributed to the score.

For example, a referral may receive a reason such as:

- High urgency
- High urgency + Critical finding
- High urgency + Chest pain
- Abnormal finding + Syncope

This makes the prioritisation decision more transparent and easier to review.

The system is designed so that a user can understand why a referral received a particular priority.

---

## 12. Initial System Results

The proposed rule-based system produced the following priority distribution for the 1,000 synthetic referrals:

- Routine: 509
- Priority: 402
- Urgent: 89

Compared with the baseline:

- Baseline urgent cases: 87
- Proposed urgent cases: 89

The proposed system therefore identifies a slightly different set of urgent referrals than the simple waiting-time-based baseline.

---

## 13. Evaluation

The proposed system was compared with a synthetic reference priority label.

The evaluation produced:

- True Positives: 88
- True Negatives: 639
- False Positives: 1
- False Negatives: 272

Initial metrics:

- Precision: 0.989
- Recall: 0.244
- Accuracy: 0.727

The high precision indicates that most referrals classified as urgent by the system were also classified as urgent by the synthetic reference.

However, the low recall indicates that many synthetic reference-urgent cases were not classified as urgent by the current rule set.

This shows that the current rules require further improvement.

---

## 14. False-Negative Analysis

False-negative analysis was performed to understand why some synthetic reference-urgent cases were missed.

A total of:

**272 false negatives**

were identified.

Most false negatives were classified by the system as Priority rather than Routine.

The analysis showed that many reference-urgent cases had relatively low system scores.

This indicates that simply increasing or decreasing the final threshold may not be sufficient.

The analysis also identified cases involving:

- Conflicting indicators
- Missing findings
- Missing urgency information
- Excessive waiting time
- Abnormal values
- Invalid or unusual values
- Missing consent

The false-negative analysis is stored in:

`outputs/reports/false_negative_analysis.csv`

---

## 15. Threshold Analysis

Different priority thresholds were tested to understand the effect of changing the Urgent classification threshold.

The results showed a trade-off between precision and recall.

A lower threshold increases recall but also produces more false positives.

A higher threshold improves precision but may miss more urgent cases.

This experiment demonstrates that threshold selection is an important part of the prioritisation system.

The threshold should therefore not be selected only to maximise one metric.

---

## 16. Edge Cases

Synthetic edge cases were intentionally included in the dataset to test the robustness of the system.

The project includes examples such as:

- Missing urgency information
- Missing diagnostic findings
- Conflicting indicators
- Excessive waiting time
- Missing consent
- Abnormally high heart rate
- Invalid or unusual blood pressure values

These cases help identify situations where a simple rule-based system may produce unexpected results.

---

## 17. Privacy and Safety Considerations

This project uses synthetic data and does not use real patient information.

The dataset includes fields related to:

- Consent status
- Data sensitivity
- Role visibility

These fields are included to demonstrate that privacy and access control should be considered in the design.

Consent and privacy information are not used as clinical urgency factors.

The project is an academic prototype and is not a medically validated clinical decision-making system.

Any future real-world implementation would require appropriate clinical validation, governance, security, privacy controls, and professional oversight.

---

## 18. Project Structure

```text
CAT2/
│
├── README.md
│
├── data/
│   ├── raw/
│   │   └── cardiology_dataset_raw.csv
│   │
│   └── processed/
│       ├── baseline_results.csv
│       ├── cleaned_referrals.csv
│       ├── evaluated_referrals.csv
│       └── prioritized_referrals.csv
│
├── docs/
│   ├── data_dictionary.md
│   └── rule_definitions.md
│
├── outputs/
│   ├── charts/
│   ├── reports/
│   │   └── false_negative_analysis.csv
│   └── results/
│       └── evaluation_results.csv
│
├── src/
│   ├── baseline.py
│   ├── data_cleaning.py
│   ├── data_validation.py
│   ├── evaluation.py
│   ├── false_negative_analysis.py
│   ├── prioritizer.py
│   └── threshold_analysis.py
│
└── tests/