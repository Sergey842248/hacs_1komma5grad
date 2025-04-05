"""Battery API client for 1komma5grad."""
from enum import Enum

class BatteryMode(Enum):
    """Battery mode enum."""
    OPTIMIZE_FEED_IN = "optimize_feed_in"
    FULL_BACKUP = "full_backup"
    OPTIMIZE_SELF_CONSUMPTION = "optimize_self_consumption"
    MANUAL = "manual"

class BatteryClient:
    """Battery API client."""

    def __init__(self, api_client):
        """Initialize the battery client."""
        self._api_client = api_client

    def set_battery_mode(self, mode: str) -> None:
        """Set the battery mode."""
        # TODO: Implement the actual API call here
        # This is a placeholder for the actual API implementation
        pass

    def get_battery_mode(self) -> str:
        """Get the current battery mode."""
        # TODO: Implement the actual API call here
        # This is a placeholder for the actual API implementation
        return BatteryMode.OPTIMIZE_SELF_CONSUMPTION.value 