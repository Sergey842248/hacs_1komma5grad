from zoneinfo import ZoneInfo

from homeassistant.components.sensor import SensorEntity
from homeassistant.const import UnitOfEnergy
from homeassistant.core import callback
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.util import dt as dt_util

from .const import CURRENCY_ICON, DOMAIN, TIMEZONE
from .coordinator import Coordinator


class ElectricityPriceSensor(CoordinatorEntity, SensorEntity):
    """Representation of an Energy Price Sensor."""

    def __init__(self, coordinator: Coordinator, system_id: str, price_type: str = None) -> None:
        """Initialise sensor."""
        super().__init__(coordinator)

        self._system_id = system_id
        self._prices_net = {}
        self._prices_gross = {}
        self._vat = 0
        self._unit = 'ct/kWh' # Default unit
        self._price_type = price_type

    @property
    def icon(self):
        """Return the icon to use in the frontend."""
        return CURRENCY_ICON

    @property
    def name(self):
        """Return the name of the sensor."""
        if self._price_type == "net":
            return f"Electricity Price Net {self._system_id}"
        elif self._price_type == "gross":
            return f"Electricity Price Gross {self._system_id}"
        else:
            return f"Electricity Price {self._system_id}"

    @property
    def unit_of_measurement(self):
        """Return the unit of measurement."""
        return self._unit

    @property
    def unique_id(self) -> str:
        """Return unique id."""
        # All entities must have a unique id.  Think carefully what you want this to be as
        # changing it later will cause HA to create new entities.
        if self._price_type == "net":
            return f"{DOMAIN}_electricity_price_net_{self._system_id}"
        elif self._price_type == "gross":
            return f"{DOMAIN}_electricity_price_gross_{self._system_id}"
        else:
            return f"{DOMAIN}_electricity_price_{self._system_id}"

    @property
    def native_value(self) -> None | float:
        """Return the state of the entity."""
        # Using native value and native unit of measurement, allows you to change units
        # in Lovelace and HA will automatically calculate the correct value.

        tz = ZoneInfo(TIMEZONE)
        current_time = (
            dt_util.now()
            .replace(minute=0, second=0, microsecond=0)
            .astimezone(tz)
            .strftime("%Y-%m-%dT%H:%MZ")
        )

        if self._price_type == "net" and current_time in self._prices_net:
            # Return net price (ohne MwSt. und ohne Netzentgelte)
            current_price = float(self._prices_net[current_time]["price"])
            return round(current_price / 100.0, 4)
        elif self._price_type == "gross" and current_time in self._prices_gross:
            # Return gross price (mit MwSt. und mit Netzentgelten)
            current_price = float(self._prices_gross[current_time]["price"])
            return round(current_price / 100.0, 4) * self._vat
        elif current_time in self._prices_gross:
            # Legacy behavior - return gross price
            current_price = float(self._prices_gross[current_time]["price"])
            return round(current_price / 100.0, 4) * self._vat

        return None

    @property
    def device_class(self):
        """Return the device class of the sensor."""
        return UnitOfEnergy.KILO_WATT_HOUR

    @callback
    def _handle_coordinator_update(self) -> None:
        """Update sensor with latest data from coordinator."""
        prices = self.coordinator.get_prices_by_id(self._system_id)

        self._vat = float(prices["vat"] + 1)
        # Für den Nettopreis verwenden wir energyMarket (ohne Netzentgelte)
        self._prices_net = prices["energyMarket"]["data"]
        # Für den Bruttopreis verwenden wir energyMarketWithGridCosts (mit Netzentgelten)
        self._prices_gross = prices["energyMarketWithGridCosts"]["data"]
        # Wir verwenden die Einheit aus der Quelle mit Netzentgelten
        self._unit = prices["energyMarketWithGridCosts"]["metadata"]["units"]["price"]

        self.async_write_ha_state()
