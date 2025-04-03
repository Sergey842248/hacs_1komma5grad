from homeassistant.core import callback

from .sensor_electricity_price import ElectricityPriceSensor
from .coordinator import Coordinator


class ElectricityPriceTotalSensor(ElectricityPriceSensor):
    """Representation of an Energy Price Sensor in Cent including grid costs and VAT."""

    def __init__(self, system_id: str, coordinator: Coordinator) -> None:
        """Initialize the sensor."""
        super().__init__(system_id, coordinator)
        self._grid_costs = 0
        self._vat = 0

    @property
    def name(self):
        """Return the name of the sensor."""
        return f"Electricity Price Total {self._system_id}"

    @property
    def unique_id(self) -> str:
        """Return unique id."""
        return f"{self.DOMAIN}_electricity_price_total_{self._system_id}"

    @property
    def native_value(self) -> None | float:
        """Return the state of the entity."""
        current_time = self._get_current_time()

        if current_time in self._prices:
            # Get the net price from energyMarket
            net_price = float(self._prices[current_time]["price"])

            # Calculate total price with grid costs and VAT
            # Total Price = (Netto-Preis + Netzentgelte) * (1 + MwSt.-Satz)
            total_price = (net_price + self._grid_costs) * (1 + self._vat)
            return round(total_price, 2)

        return None

    @callback
    def _handle_coordinator_update(self) -> None:
        """Update sensor with latest data from coordinator."""
        prices = self.coordinator.get_prices_by_id(self._system_id)

        # Use energyMarket prices which are the current market prices
        self._prices = prices["energyMarket"]["data"]

        # Get grid costs and VAT from the API
        self._grid_costs = prices["gridCostsTotal"]["data"]["value"]
        self._vat = prices["vat"]["data"]["value"]

        self.async_write_ha_state()