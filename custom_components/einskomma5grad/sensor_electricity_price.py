from zoneinfo import ZoneInfo

from homeassistant.components.sensor import SensorEntity
from homeassistant.const import UnitOfEnergy
from homeassistant.core import callback
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.util import dt as dt_util

from .const import CURRENCY_ICON, DOMAIN, TIMEZONE
from .coordinator import Coordinator


class ElectricityPriceSensor(CoordinatorEntity, SensorEntity):
    """Base class for Electricity Price Sensors."""

    def __init__(self, coordinator: Coordinator, system_id: str) -> None:
        """Initialise sensor."""
        super().__init__(coordinator)

        self._system_id = system_id
        self._prices = {}
        self._unit = 'ct/kWh' # Default unit

    @property
    def icon(self):
        """Return the icon to use in the frontend."""
        return CURRENCY_ICON

    @property
    def unit_of_measurement(self):
        """Return the unit of measurement."""
        return self._unit

    @property
    def device_class(self):
        """Return the device class of the sensor."""
        return UnitOfEnergy.KILO_WATT_HOUR

    def _get_current_time(self) -> str:
        """Get the current time formatted for API requests."""
        tz = ZoneInfo(TIMEZONE)
        return (
            dt_util.now()
            .replace(minute=0, second=0, microsecond=0)
            .astimezone(tz)
            .strftime("%Y-%m-%dT%H:%MZ")
        ) 