# ==========================================================
# BASE VENDOR ADAPTER
# ==========================================================

class BaseAdapter:

    def adapt(self, payload):
        """
        Convert vendor-specific device data
        into the common internal format.
        """
        raise NotImplementedError(
            "Each vendor adapter must implement adapt()"
        )