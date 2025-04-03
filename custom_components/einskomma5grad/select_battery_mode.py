"""Battery mode select entity for 1KOMMA5GRAD integration."""
from __future__ import annotations

import logging
from typing import Any, Final

from homeassistant.components.select import SelectEntity
from homeassistant.core import callback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN
from .coordinator import Coordinator

_LOGGER = logging.getLogger(__name__)

# Define the available battery modes
BATTERY_MODES: Final = {
    "automatic": "Automatic",
    "self_consumption": "Self Consumption",
    "time_of_use": "Time of Use",
    "backup_power": "Backup Power",
}


class BatteryModeSelect(CoordinatorEntity, SelectEntity):
    """Representation of a Battery Mode Select entity."""

    def __init__(self, coordinator: Coordinator, system_id: str) -> None:
        """Initialize the battery mode select entity."""
        super().__init__(coordinator)
        self._system_id = system_id
        self._attr_options = list(BATTERY_MODES.values())
        self._attr_current_option = BATTERY_MODES["automatic"]  # Default mode

    @property
    def name(self) -> str:
        """Return the name of the entity."""
        return f"Battery Mode {self._system_id}"

    @property
    def unique_id(self) -> str:
        """Return a unique ID."""
        return f"{DOMAIN}_battery_mode_{self._system_id}"

    @property
    def icon(self) -> str:
        """Return the icon to use in the frontend."""
        return "mdi:battery-charging"

    async def async_select_option(self, option: str) -> None:
        """Change the selected option."""
        # Get the mode key from the display name
        mode_key = next(
            (key for key, value in BATTERY_MODES.items() if value == option), None
        )
        
        if mode_key is None:
            _LOGGER.error("Invalid battery mode selected: %s", option)
            return

        # Call the API to set the battery mode
        success = await self.coordinator.set_battery_mode(self._system_id, mode_key)
        
        if success:
            self._attr_current_option = option
            self.async_write_ha_state()
        else:
            _LOGGER.error("Failed to set battery mode to %s", option)

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        # Update the current mode if available from the coordinator
        battery_data = self.coordinator.get_battery_data_by_id(self._system_id)
        if battery_data and "mode" in battery_data:
            mode_key = battery_data["mode"]
            if mode_key in BATTERY_MODES:
                self._attr_current_option = BATTERY_MODES[mode_key]
        
        self.async_write_ha_state()