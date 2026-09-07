# System Workflow

## 1. Overview

The proposed system follows a sequence of data validation, cleaning,
prioritisation, ranking, and evaluation steps.

The workflow is designed to transform raw multi-vendor diagnostic
referral data into an explainable prioritised worklist.

---

## 2. Overall Workflow

```text
Raw Diagnostic Referral Data
            |
            v
      Data Validation
            |
            v
       Data Cleaning
            |
            v
   Standardised Referral Data
            |
            v
    Priority Rule Engine
            |
            v
     Priority Score
            |
            v
   Priority Classification
            |
     +------+------+
     |             |
     v             v
 Proposed       Baseline
  System        FCFS Method
     |             |
     +------+------+
            |
            v
       Comparison
            |
            v
       Evaluation
            |
            v
   Error & Edge Case Analysis