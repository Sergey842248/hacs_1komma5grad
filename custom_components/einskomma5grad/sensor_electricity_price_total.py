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
        self._grid_fee = 15.2  # Grid fee in ct/kWh
        self._vat_rate = 0.19  # 19% VAT

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

        # Get net price from the coordinator
        prices_netto = self.coordinator.get_prices_by_id(self._system_id)
        if current_time in prices_netto["energyMarket"]["data"]:
            # Get net price
            net_price = float(prices_netto["energyMarket"]["data"][current_time]["price"])
            
            # Calculate total price: net price + VAT + grid fee
            vat_amount = net_price * self._vat_rate
            total_price = net_price + vat_amount + self._grid_fee
            
            return round(total_price, 2)

        return None

    @property
    def device_class(self):
        """Return the device class of the sensor."""
        return UnitOfEnergy.KILO_WATT_HOUR

    @callback
    def _handle_coordinator_update(self) -> None:
        """Update sensor with latest data from coordinator."""
        prices = self.coordinator.get_prices_by_id(self._system_id)

        # Store both price types for calculation
        self._prices = prices
        
        self.async_write_ha_state()