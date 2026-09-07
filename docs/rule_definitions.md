# Rule Definitions

## Project

A Rule-Based Diagnostic Worklist Prioritisation System for Urgent Cardiology Cases Using Multi-Vendor Diagnostic Data

## Objective

The proposed system assigns a priority score to each diagnostic referral using
explainable rule-based indicators.

The system produces three priority levels:

- Urgent
- Priority
- Routine

The rules are designed for an academic prototype and are not medically
validated clinical decision rules.

---

## Priority Scoring Rules

| Indicator | Condition | Score |
|---|---|---:|
| Urgency | High | +3 |
| Urgency | Medium | +1 |
| Symptom severity | Severe | +2 |
| Symptom severity | Moderate | +1 |
| Abnormal finding | Yes | +2 |
| Critical finding | Yes | +3 |
| Syncope | Yes | +2 |
| Chest pain | Yes | +1 |
| Shortness of breath | Yes | +1 |
| Waiting time | More than 48 hours | +2 |
| Waiting time | More than 24 hours | +1 |

---

## Priority Classification

| Total Score | System Priority |
|---:|---|
| 7 or more | Urgent |
| 4–6 | Priority |
| Below 4 | Routine |

---

## Priority Explanation

For every referral, the system records the indicators that contributed
to the priority score.

Example:

> High urgency, critical finding, chest pain → Score 7 → Urgent

This makes the prioritisation decision explainable and auditable.

---

## Baseline Method

The baseline uses a simple First-Come, First-Served (FCFS) approach.

Referrals are ordered according to their referral datetime.

The baseline also uses waiting-time thresholds for comparison:

| Waiting Time | Baseline Priority |
|---|---|
| More than 48 hours | Urgent |
| More than 24 hours | Priority |
| 24 hours or less | Routine |

---

## Important Design Principles

### 1. Explainability

Every priority assignment should have an identifiable reason.

### 2. Human Oversight

The system is intended to support clinical workflow, not replace
clinical judgement.

### 3. Safety

The prototype should be evaluated for false negatives, especially cases
that should be considered urgent but are not assigned high priority.

### 4. Fairness

Routine cases should not be permanently ignored because urgent cases
receive higher priority.

### 5. Privacy

Consent status, data sensitivity, and role visibility should control
data access and processing. They should not be treated as clinical
urgency indicators.

### 6. Synthetic Data

The dataset contains synthetic records created for academic evaluation.
It does not represent real patient records.

### 7. Reference Labels

`clinician_priority_label` represents a synthetic reference label.
It is not actual clinical ground truth from cardiologists.