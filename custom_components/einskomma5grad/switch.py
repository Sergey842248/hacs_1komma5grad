import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN
from .coordinator import Coordinator
from .switch_ems import EmsSwitch

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
):
    """Set up the switch entities."""
    coordinator: Coordinator = hass.data[DOMAIN][config_entry.entry_id].coordinator

    entities = []

    for system in coordinator.data.systems:
        entities.append(EmsSwitch(coordinator, system.id()))

    async_add_entities(entities)
