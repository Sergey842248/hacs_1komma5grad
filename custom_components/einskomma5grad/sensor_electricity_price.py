from zoneinfo import ZoneInfo

from homeassistant.components.sensor import SensorEntity
from homeassistant.const import UnitOfEnergy
from homeassistant.core import callback
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.util import dt as dt_util

from .const import CURRENCY_ICON, DOMAIN, TIMEZONE
from .coordinator import Coordinator


class NetElectricityPriceSensor(CoordinatorEntity, SensorEntity):
    """Representation of a Net Electricity Price Sensor."""

    def __init__(self, coordinator: Coordinator, system_id: str) -> None:
        """Initialise sensor."""
        super().__init__(coordinator)

        self._system_id = system_id
        self._prices = {}
        self._unit = 'ct/kWh'

    @property
    def icon(self):
        """Return the icon to use in the frontend."""
        return CURRENCY_ICON

    @property
    def name(self):
        """Return the name of the sensor."""
        return f"Net Electricity Price {self._system_id}"

    @property
    def unit_of_measurement(self):
        """Return the unit of measurement."""
        return self._unit

    @property
    def unique_id(self) -> str:
        """Return unique id."""
        return f"{DOMAIN}_net_electricity_price_{self._system_id}"

    @property
    def native_value(self) -> None | float:
        """Return the state of the entity."""
        tz = ZoneInfo(TIMEZONE)
        current_time = (
            dt_util.now()
            .replace(minute=0, second=0, microsecond=0)
            .astimezone(tz)
            .strftime("%Y-%m-%dT%H:%MZ")
        )

        if current_time in self._prices:
            return float(self._prices[current_time]["price"])

        return None

    @property
    def device_class(self):
        """Return the device class of the sensor."""
        return UnitOfEnergy.KILO_WATT_HOUR

    @callback
    def _handle_coordinator_update(self) -> None:
        """Update sensor with latest data from coordinator."""
        prices = self.coordinator.get_prices_by_id(self._system_id)
        self._prices = prices["energyMarket"]["data"]
        self._unit = prices["energyMarket"]["metadata"]["units"]["price"]
        self.async_write_ha_state()


class GrossElectricityPriceSensor(CoordinatorEntity, SensorEntity):
    """Representation of a Gross Electricity Price Sensor."""

    def __init__(self, coordinator: Coordinator, system_id: str) -> None:
        """Initialise sensor."""
        super().__init__(coordinator)

        self._system_id = system_id
        self._prices = {}
        self._unit = 'ct/kWh'

    @property
    def icon(self):
        """Return the icon to use in the frontend."""
        return CURRENCY_ICON

    @property
    def name(self):
        """Return the name of the sensor."""
        return f"Gross Electricity Price {self._system_id}"

    @property
    def unit_of_measurement(self):
        """Return the unit of measurement."""
        return self._unit

    @property
    def unique_id(self) -> str:
        """Return unique id."""
        return f"{DOMAIN}_gross_electricity_price_{self._system_id}"

    @property
    def native_value(self) -> None | float:
        """Return the state of the entity."""
        tz = ZoneInfo(TIMEZONE)
        current_time = (
            dt_util.now()
            .replace(minute=0, second=0, microsecond=0)
            .astimezone(tz)
            .strftime("%Y-%m-%dT%H:%MZ")
        )

        if current_time in self._prices:
            return float(self._prices[current_time]["price"])

        return None

    @property
    def device_class(self):
        """Return the device class of the sensor."""
        return UnitOfEnergy.KILO_WATT_HOUR

    @callback
    def _handle_coordinator_update(self) -> None:
        """Update sensor with latest data from coordinator."""
        prices = self.coordinator.get_prices_by_id(self._system_id)
        self._prices = prices["energyMarketWithGridCosts"]["data"]
        self._unit = prices["energyMarketWithGridCosts"]["metadata"]["units"]["price"]
        self.async_write_ha_state()


"""Electricity price sensor for 1komma5grad integration."""
from __future__ import annotations

from datetime import datetime
import logging

from homeassistant.components.sensor import SensorEntity, SensorStateClass
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.const import (
    CURRENCY_EURO,
    UnitOfEnergy,
)

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

class ElectricityPriceSensor(SensorEntity):
    """Representation of an Electricity Price Sensor."""

    def __init__(self, hass: HomeAssistant, entry: ConfigEntry):
        """Initialize the sensor."""
        self._hass = hass
        self._entry = entry
        self._attr_name = "Electricity Price"
        self._attr_unique_id = f"{entry.entry_id}_electricity_price"
        self._attr_native_unit_of_measurement = f"{CURRENCY_EURO}/{UnitOfEnergy.KILO_WATT_HOUR}"
        self._attr_state_class = SensorStateClass.MEASUREMENT
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, entry.entry_id)},
            name="1komma5grad Energy",
            manufacturer="1komma5grad",
        )
        self._attr_native_value = None

    async def async_update(self):
        """Fetch new state data for the sensor."""
        # Implement the logic to fetch the current electricity price
        # This is a placeholder - you'll need to implement the actual API call
        # self._attr_native_value = await get_electricity_price()
        pass
