# ==========================================================
# VENDOR ADAPTER TEST
# ==========================================================
from adapters.philips_adapter import PhilipsAdapter
from adapters.ge_adapter import GEAdapter

# ----------------------------------------------------------
# Philips sample data
# ----------------------------------------------------------

philips_data = {
    "patient": "REF0001",
    "hr": 118,
    "ecg_status": "Abnormal",
    "spo2": 91
}


# ----------------------------------------------------------
# GE sample data
# ----------------------------------------------------------

ge_data = {
    "referral": "REF0002",
    "heart_rate": 105,
    "ecg": "Normal",
    "oxygen": 96
}


# ----------------------------------------------------------
# Convert vendor data to common format
# ----------------------------------------------------------

philips_adapter = PhilipsAdapter()
ge_adapter = GEAdapter()

philips_result = philips_adapter.adapt(philips_data)
ge_result = ge_adapter.adapt(ge_data)


# ----------------------------------------------------------
# Display results
# ----------------------------------------------------------

print("=" * 60)
print("VENDOR ADAPTER TEST")
print("=" * 60)

print("\nPhilips converted data:")
print(philips_result)

print("\nGE converted data:")
print(ge_result)

print("\n" + "=" * 60)
print("ADAPTER TEST COMPLETED")
print("=" * 60)