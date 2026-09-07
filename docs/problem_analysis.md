# Problem Analysis

## Project Title

A Rule-Based Diagnostic Worklist Prioritisation System for Urgent Cardiology Cases Using Multi-Vendor Diagnostic Data

---

## 1. Problem Statement

Cardiology clinics may receive diagnostic referrals from multiple devices,
vendors, modalities, and referral sources.

When many referrals are waiting at the same time, urgent cases may not
always be prioritised consistently. A simple first-come-first-served
approach mainly considers when a referral was received and may not
adequately consider urgency-related indicators.

This project proposes an explainable rule-based prioritisation system
that helps organise diagnostic referrals according to urgency-related
indicators and waiting time.

The system is designed as an academic prototype and is not a medically
validated clinical decision-making system.

---

## 2. Existing Problem

The current workflow may face the following challenges:

- Large number of diagnostic referrals
- Data received from multiple device vendors
- Different diagnostic modalities
- Urgent referrals mixed with routine referrals
- Difficulty identifying urgent cases quickly
- First-come-first-served ordering may delay attention to urgent cases
- Lack of an explicit explanation for why a referral is prioritised
- Potential inconsistency in manual prioritisation

---

## 3. Proposed Solution

The proposed solution is a rule-based diagnostic worklist
prioritisation system.

The system:

1. Accepts diagnostic referral information.
2. Standardises relevant referral data.
3. Checks important urgency-related indicators.
4. Calculates an explainable priority score.
5. Assigns one of three priority levels:
   - Urgent
   - Priority
   - Routine
6. Generates a reason for the assigned priority.
7. Ranks referrals in a proposed worklist.
8. Compares the proposed approach with a baseline approach.
9. Evaluates false positives and false negatives.

---

## 4. Why a Rule-Based Approach?

A rule-based approach was selected because the project requires:

- Explainability
- Transparency
- Easy auditing
- Simple implementation
- Clear reasoning for each priority assignment
- Human oversight

Each priority score can be traced back to specific indicators.

For example:

High urgency + Critical finding + Chest pain

can produce a higher priority score than a referral with only a
long waiting time.

---

## 5. Dataset

A synthetic dataset containing 1,000 diagnostic referral records was
created for the project.

The dataset contains information related to:

- Diagnostic vendor
- Device
- Modality
- Referral source
- Demographic information
- Urgency indicators
- Symptoms
- Diagnostic findings
- Vital signs
- Referral time
- Waiting time
- Consent and privacy information
- Clinician override information
- System priority
- Baseline priority
- Evaluation results
- Edge cases

The dataset contains synthetic records only and does not contain
real patient information.

---

## 6. Main Users

The intended users of the proposed system are:

### Clinical Staff

Can view prioritised referrals and understand the reasons for
priority assignment.

### Diagnostic Staff

Can use the worklist to organise pending diagnostic referrals.

### Supervisors

Can monitor workload, priority distribution, and system performance.

---

## 7. Key Requirements

### Functional Requirements

The system should:

- Load diagnostic referral data.
- Validate the dataset.
- Clean invalid or inconsistent data.
- Calculate priority scores.
- Assign priority levels.
- Provide explanations for priority assignments.
- Rank referrals.
- Compare the proposed approach with a baseline.
- Calculate evaluation metrics.
- Identify false negative cases.
- Analyse edge cases.

### Non-Functional Requirements

The system should be:

- Explainable
- Transparent
- Easy to understand
- Auditable
- Maintainable
- Privacy-aware
- Accessible
- Human-controlled

---

## 8. Safety and Ethical Considerations

The system is an academic prototype and should not replace
clinical judgement.

Important considerations include:

- False negatives must be analysed carefully.
- Clinicians should be able to review or override system results.
- Patient privacy must be protected.
- Consent and access permissions should be respected.
- The system should not use sensitive information as a reason
  for clinical prioritisation.
- Routine cases should not be permanently ignored.
- Synthetic data should be clearly distinguished from real patient data.

---

## 9. Project Objective

The main objective is to develop and evaluate an explainable
rule-based prioritisation method that can help organise cardiology
diagnostic referrals and identify potentially urgent cases more
systematically than a simple baseline approach.

---

## 10. Expected Outcome

The expected outcome is a prototype prioritisation system that:

- Produces an ordered diagnostic worklist.
- Identifies urgent referrals.
- Provides reasons for priority assignments.
- Allows comparison with a baseline approach.
- Measures precision, recall, accuracy, false positives,
  and false negatives.
- Demonstrates behaviour on synthetic edge cases.