# ==========================================================
# VENDOR ADAPTER DEMO
# ==========================================================

from adapters.philips_adapter import PhilipsAdapter
from adapters.ge_adapter import GEAdapter


# ----------------------------------------------------------
# Sample Philips device data
# ----------------------------------------------------------

philips_data = {
    "patient": "REF0001",
    "hr": 118,
    "ecg_status": "Abnormal",
    "spo2": 91
}


# ----------------------------------------------------------
# Sample GE device data
# ----------------------------------------------------------

ge_data = {
    "referral": "REF0002",
    "heart_rate": 105,
    "ecg": "Normal",
    "oxygen": 96
}


# ----------------------------------------------------------
# Create adapters
# ----------------------------------------------------------

philips_adapter = PhilipsAdapter()
ge_adapter = GEAdapter()


# ----------------------------------------------------------
# Convert vendor data to common format
# ----------------------------------------------------------

philips_common = philips_adapter.adapt(philips_data)
ge_common = ge_adapter.adapt(ge_data)


# ----------------------------------------------------------
# Display standardized data
# ----------------------------------------------------------

print("=" * 60)
print("MULTI-VENDOR ADAPTER DEMO")
print("=" * 60)

print("\nPhilips standardized data:")
print(philips_common)

print("\nGE standardized data:")
print(ge_common)

print("\n" + "=" * 60)
print("ALL VENDOR DATA CONVERTED TO COMMON FORMAT")
print("=" * 60)