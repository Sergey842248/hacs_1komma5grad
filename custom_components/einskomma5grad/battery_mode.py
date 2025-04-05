"""Battery Mode Entity for 1komma5grad."""
from __future__ import annotations

from homeassistant.components.select import SelectEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.entity import EntityCategory

from .const import DOMAIN
from .coordinator import Einskomma5gradDataUpdateCoordinator
from .entity import Einskomma5gradEntity

BATTERY_MODES = {
    "optimize_feed_in": "Optimize Feed In",
    "full_backup": "Full Backup",
    "optimize_self_consumption": "Optimize Self Consumption",
    "manual": "Manuell"
}

async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the battery mode select entity."""
    coordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_entities([Einskomma5gradBatteryMode(coordinator)])

class Einskomma5gradBatteryMode(Einskomma5gradEntity, SelectEntity):
    """Representation of a Battery Mode Select entity."""

    _attr_entity_category = EntityCategory.CONFIG
    _attr_name = "Batteriemodus"
    _attr_options = list(BATTERY_MODES.keys())
    _attr_translation_key = "battery_mode"

    @property
    def current_option(self) -> str:
        """Return the current selected option."""
        return self.coordinator.data.get("battery_mode", "optimize_self_consumption")

    async def async_select_option(self, option: str) -> None:
        """Change the selected option."""
        await self.coordinator.api.set_battery_mode(option)
        await self.coordinator.async_request_refresh() 