"""Spare-parts recommendation adapter."""
class AnalyticsClient:
    def top_parts(self, asset_type: str) -> list[str]:
        return ["CHAIN-01", "BRAKE-02"] if asset_type == "bicycle" else ["FILTER-01"]
