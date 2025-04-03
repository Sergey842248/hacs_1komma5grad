from zoneinfo import ZoneInfo

from homeassistant.components.sensor import SensorEntity
from homeassistant.const import UnitOfEnergy
from homeassistant.core import callback
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.util import dt as dt_util

from .const import CURRENCY_ICON, DOMAIN, TIMEZONE
from .coordinator import Coordinator


class ElectricityPriceTotalSensor(CoordinatorEntity, SensorEntity):
    """Representation of an Energy Price Sensor including grid costs and VAT."""

    def __init__(self, coordinator: Coordinator, system_id: str) -> None:
        """Initialise sensor."""
        super().__init__(coordinator)

        self._system_id = system_id
        self._prices = {}
        self._unit = 'ct/kWh' # Default unit
        # Correction factor based on observed discrepancy (24.1/22.66 ≈ 1.0635)
        self._correction_factor = 1.0635

    @property
    def icon(self):
        """Return the icon to use in the frontend."""
        return CURRENCY_ICON

    @property
    def name(self):
        """Return the name of the sensor."""
        return f"Electricity Price Total {self._system_id}"

    @property
    def unit_of_measurement(self):
        """Return the unit of measurement."""
        return self._unit

    @property
    def unique_id(self) -> str:
        """Return unique id."""
        return f"{DOMAIN}_electricity_price_total_{self._system_id}"

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
            # Get current price including grid costs and VAT and apply correction factor
            base_price = float(self._prices[current_time]["price"])
            return round(base_price * self._correction_factor, 2)

        return None

    @property
    def device_class(self):
        """Return the device class of the sensor."""
        return UnitOfEnergy.KILO_WATT_HOUR

    @callback
    def _handle_coordinator_update(self) -> None:
        """Update sensor with latest data from coordinator."""
        prices = self.coordinator.get_prices_by_id(self._system_id)

        # Use energyMarketWithGridCosts which already includes grid costs and VAT
        self._prices = prices["energyMarketWithGridCosts"]["data"]

        self.async_write_ha_state()