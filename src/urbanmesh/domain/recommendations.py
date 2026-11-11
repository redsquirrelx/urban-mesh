"""Suggested maintenance parts for common repair categories."""
from urbanmesh.infrastructure.gateways.analytics import AnalyticsClient

def suggested_parts(asset_type: str) -> list[str]:
    client = AnalyticsClient()
    return client.top_parts(asset_type)
