# ==========================================================
# GE VENDOR ADAPTER
# ==========================================================

from adapters.base_adapter import BaseAdapter

class GEAdapter(BaseAdapter):

    def adapt(self, payload):

        common_data = {
            "referral_id": payload.get("referral"),
            "heart_rate_bpm": payload.get("heart_rate"),
            "ecg_finding": payload.get("ecg"),
            "oxygen_saturation": payload.get("oxygen"),
            "vendor": "GE"
        }

        return common_data