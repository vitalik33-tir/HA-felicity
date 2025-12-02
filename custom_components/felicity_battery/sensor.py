from __future__ import annotations

from homeassistant.components.sensor import SensorEntity
from homeassistant.const import UnitOfElectricPotential, UnitOfElectricCurrent
from homeassistant.helpers.entity import Entity
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.components.sensor import SensorDeviceClass

from .const import DOMAIN
from .coordinator import FelicityDataUpdateCoordinator


async def async_setup_entry(hass, entry, async_add_entities):
    coordinator: FelicityDataUpdateCoordinator = hass.data[DOMAIN][entry.entry_id]
    entities: list[Entity] = []

    def make_sensor(name, key, unit=None, device_class=None, scale=1.0, icon=None):
        entities.append(
            FelicitySensor(
                coordinator=coordinator,
                name=name,
                key=key,
                unit=unit,
                device_class=device_class,
                scale=scale,
                icon=icon,
            )
        )

    # Настройки (из _settings)
    make_sensor("Battery Pack Count", "ttl_pack", unit="шт", icon="mdi:counter")
    make_sensor("Cell Over Voltage", "cell_over_voltage", unit=UnitOfElectricPotential.VOLT, device_class=SensorDeviceClass.VOLTAGE, scale=0.001)
    make_sensor("Cell Under Voltage", "cell_under_voltage", unit=UnitOfElectricPotential.VOLT, device_class=SensorDeviceClass.VOLTAGE, scale=0.001)
    make_sensor("Cell Voltage @20%", "cell_v_20", unit=UnitOfElectricPotential.VOLT, device_class=SensorDeviceClass.VOLTAGE, scale=0.001)
    make_sensor("Cell Voltage @80%", "cell_v_80", unit=UnitOfElectricPotential.VOLT, device_class=SensorDeviceClass.VOLTAGE, scale=0.001)
    make_sensor("Charge Current Limit (setting)", "charge_limit_setting", unit=UnitOfElectricCurrent.AMPERE, device_class=SensorDeviceClass.CURRENT, scale=0.1)
    make_sensor("Discharge Current Limit (setting)", "discharge_limit_setting", unit=UnitOfElectricCurrent.AMPERE, device_class=SensorDeviceClass.CURRENT, scale=0.1)

    async_add_entities(entities)


class FelicitySensor(CoordinatorEntity, SensorEntity):
    def __init__(
        self,
        coordinator: FelicityDataUpdateCoordinator,
        name: str,
        key: str,
        unit: str | None = None,
        device_class: SensorDeviceClass | None = None,
        scale: float = 1.0,
        icon: str | None = None,
    ) -> None:
        super().__init__(coordinator)
        self._attr_name = name
        self._attr_unique_id = f"{coordinator.base_unique_id}_{key}"
        self._key = key
        self._scale = scale
        self._attr_native_unit_of_measurement = unit
        self._attr_icon = icon
        self._attr_device_class = device_class

    @property
    def native_value(self):
        value = self.coordinator.data.get("_settings", {}).get(self._key)
        if value is None:
            return None
        try:
            return round(float(value) * self._scale, 2)
        except Exception:
            return None
