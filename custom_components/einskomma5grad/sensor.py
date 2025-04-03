"""Support for Einskomma5grad sensors."""
from __future__ import annotations

import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN
from .coordinator import Coordinator
from .sensor_electricity_price_netto import ElectricityPriceEuroSensor
from .sensor_electricity_price_total import ElectricityPriceTotalSensor
from .sensor_power_generic import GenericPowerSensor

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Einskomma5grad sensors from a config entry."""
    coordinator: Coordinator = hass.data[DOMAIN][config_entry.entry_id]

    # Initialize sensors list
    sensors = []

    # Add Cent price sensors
    sensors.extend([
        ElectricityPriceEuroSensor(coordinator, system.id())
        for system in coordinator.data.systems
    ])

    # Add total price sensors (including grid costs and VAT)
    sensors.extend([
        ElectricityPriceTotalSensor(system.id(), coordinator)
        for system in coordinator.data.systems
    ])

    for system in coordinator.data.systems:
        sensors.append(
            GenericPowerSensor(
                coordinator=coordinator,
                key="gridConsumption",
                icon="mdi:transmission-tower-export",
                system_id=system.id(),
                name="Grid Consumption",
            )
        )
        sensors.append(
            GenericPowerSensor(
                coordinator=coordinator,
                icon="mdi:transmission-tower",
                key="grid",
                system_id=system.id(),
                name="Grid",
            )
        )
        sensors.append(
            GenericPowerSensor(
                coordinator=coordinator,
                icon="mdi:home-lightning-bolt-outline",
                key="consumption",
                system_id=system.id(),
                name="Consumption",
            )
        )
        sensors.append(
            GenericPowerSensor(
                coordinator=coordinator,
                icon="mdi:solar-power",
                key="production",
                system_id=system.id(),
                name="Production",
            )
        )
        sensors.append(
            GenericPowerSensor(
                coordinator=coordinator,
                icon="mdi:car-electric",
                key="evChargersAggregated",
                system_id=system.id(),
                name="EV Chargers Aggregated",
            )
        )
        sensors.append(
            GenericPowerSensor(
                coordinator=coordinator,
                icon="mdi:heat-pump",
                key="heatPumpsAggregated",
                system_id=system.id(),
                name="Heat Pumps Aggregated",
            )
        )
        sensors.append(
            GenericPowerSensor(
                coordinator=coordinator,
                icon="mdi:transmission-tower-import",
                key="gridFeedIn",
                system_id=system.id(),
                name="Grid Feed In",
            )
        )

    async_add_entities(sensors)
