# Device Vendor Adapter Specification

## 1. Purpose

The vendor adapter layer converts device-specific diagnostic data into a common internal format used by the cardiology diagnostic-worklist prioritizer.

Different medical-device vendors may use different field names and payload structures. The adapter layer prevents these differences from affecting the main prioritization system.

---

## 2. Adapter Flow

```text
Vendor Device
     |
     v
Vendor-Specific Payload
     |
     v
Vendor Adapter
     |
     v
Common Internal Schema
     |
     v
Prioritization Engine
     |
     v
Diagnostic Worklist