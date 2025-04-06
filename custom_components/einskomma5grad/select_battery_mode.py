import logging

from homeassistant.components.select import SelectEntity
from homeassistant.core import callback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN
from .coordinator import Coordinator

_LOGGER = logging.getLogger(__name__)


class BatteryModeSelect(CoordinatorEntity, SelectEntity):
    """Representation of a Battery Mode Select entity."""

    def __init__(self, coordinator: Coordinator, system_id: str) -> None:
        """Initialize the select entity."""
        super().__init__(coordinator)

        self._system_id = system_id
        self._attr_options = [
            "OPTIMIZE_FEED_IN",
            "OPTIMIZE_SELF_CONSUMPTION",
            "FULL_BACKUP",
            "PREVENT_FEED_IN",
            "AUTO"
        ]
        self._attr_current_option = None

    @property
    def icon(self):
        return "mdi:battery"

    @property
    def options(self) -> list[str]:
        """Return the list of options."""
        return [
            "Optimize Feed In",
            "Optimize Self Consumption",
            "Full Backup",
            "Prevent Feed In",
            "Auto"
        ]

    @property
    def current_option(self) -> str | None:
        """Return the selected option."""
        # Map the internal mode to the display name
        mode_mapping = {
            "OPTIMIZE_FEED_IN": "Optimize Feed In",
            "OPTIMIZE_SELF_CONSUMPTION": "Optimize Self Consumption",
            "FULL_BACKUP": "Full Backup",
            "PREVENT_FEED_IN": "Prevent Feed In",
            "AUTO": "Auto"
        }
        return mode_mapping.get(self._attr_current_option, self._attr_current_option)

    @property
    def unique_id(self) -> str:
        """Return unique id."""
        return f"{DOMAIN}_battery_mode_{self._system_id}"

    @property
    def name(self) -> str:
        """Return the name of the select entity."""
        return f"Battery Mode {self._system_id}"

    async def async_select_option(self, option: str) -> None:
        """Change the selected option."""
        # Map the display name back to the internal mode
        mode_mapping = {
            "Optimize Feed In": "OPTIMIZE_FEED_IN",
            "Optimize Self Consumption": "OPTIMIZE_SELF_CONSUMPTION",
            "Full Backup": "FULL_BACKUP",
            "Prevent Feed In": "PREVENT_FEED_IN",
            "Auto": "AUTO"
        }
        
        internal_mode = mode_mapping.get(option)
        if internal_mode is None:
            _LOGGER.error("Invalid option selected: %s", option)
            return

        # Call the API to change the mode
        await self.hass.async_add_executor_job(
            self.coordinator.set_battery_mode,
            self._system_id,
            internal_mode,
        )

        # Update the current option
        self._attr_current_option = internal_mode
        self.async_write_ha_state()

    @callback
    def _handle_coordinator_update(self) -> None:
        """Update sensor with latest data from coordinator."""
        live_overview = self.coordinator.get_live_data_by_id(self._system_id)
        
        # Get battery mode from live overview
        if "battery" in live_overview["summaryCards"]:
            battery_data = live_overview["summaryCards"]["battery"]
            if "mode" in battery_data:
                self._attr_current_option = battery_data["mode"]

        self.async_write_ha_state()