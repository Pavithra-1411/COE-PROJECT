# ==========================================================
# PHILIPS VENDOR ADAPTER
# ==========================================================

from adapters.base_adapter import BaseAdapter


class PhilipsAdapter(BaseAdapter):

    def adapt(self, payload):

        common_data = {
            "referral_id": payload.get("patient"),
            "heart_rate_bpm": payload.get("hr"),
            "ecg_finding": payload.get("ecg_status"),
            "oxygen_saturation": payload.get("spo2"),
            "vendor": "Philips"
        }

        return common_data