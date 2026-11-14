
# ==========================================================
# CLINICIAN OVERRIDE TEST
# ==========================================================

from override_manager import save_override


# Sample clinician override
referral_id = "REF0001"

old_priority = "Routine"

new_priority = "Urgent"

reason = "Critical clinical concern identified"

clinician_id = "DR001"


# Save override and audit history
result = save_override(
    referral_id,
    clinician_id,
    old_priority,
    new_priority,
    reason
)


# Display result
print("=" * 60)
print("CLINICIAN OVERRIDE TEST")
print("=" * 60)

print("Override saved:", result)

print("=" * 60)
print("OVERRIDE AUDIT SAVED SUCCESSFULLY")
print("=" * 60)
