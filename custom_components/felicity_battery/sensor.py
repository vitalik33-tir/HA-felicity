from __future__ import annotations
# -*- coding: utf-8 -*-

from dataclasses import dataclass
from typing import Any

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorEntityDescription,
    SensorStateClass,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import (
    CONF_HOST,
    PERCENTAGE,
    UnitOfElectricCurrent,
    UnitOfElectricPotential,
    UnitOfPower,
    UnitOfTemperature,
)
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import EntityCategory
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN, DEVICE_TYPE_BATTERY, DEVICE_TYPE_INVERTER


@dataclass
class FelicitySensorDescription(SensorEntityDescription):
    """Extended description for Felicity sensors."""


SENSOR_DESCRIPTIONS: tuple[FelicitySensorDescription, ...] = (
    # --- Основные рабочие сенсоры ---
    FelicitySensorDescription(
        key="soc",
        name="Battery SOC",
        native_unit_of_measurement=PERCENTAGE,
        device_class=SensorDeviceClass.BATTERY,
        state_class=SensorStateClass.MEASUREMENT,
        icon="mdi:battery",
        suggested_display_precision=1,
    ),
    FelicitySensorDescription(
        key="voltage",
        name="Battery Voltage",
        native_unit_of_measurement=UnitOfElectricPotential.VOLT,
        device_class=SensorDeviceClass.VOLTAGE,
        state_class=SensorStateClass.MEASUREMENT,
        icon="mdi:current-dc",
        suggested_display_precision=2,
    ),
    FelicitySensorDescription(
        key="current",
        name="Battery Current",
        native_unit_of_measurement=UnitOfElectricCurrent.AMPERE,
        device_class=SensorDeviceClass.CURRENT,
        state_class=SensorStateClass.MEASUREMENT,
        icon="mdi:current-dc",
        suggested_display_precision=1,
    ),
    FelicitySensorDescription(
        key="power",
        name="Battery Power",
        native_unit_of_measurement=UnitOfPower.WATT,
        device_class=SensorDeviceClass.POWER,
        state_class=SensorStateClass.MEASUREMENT,
        icon="mdi:flash",
    ),
    # Разделённые токи/мощности
    FelicitySensorDescription(
        key="charge_current",
        name="Battery Charge Current",
        native_unit_of_measurement=UnitOfElectricCurrent.AMPERE,
        device_class=SensorDeviceClass.CURRENT,
        state_class=SensorStateClass.MEASUREMENT,
        icon="mdi:current-dc",
        suggested_display_precision=1,
    ),
    FelicitySensorDescription(
        key="discharge_current",
        name="Battery Discharge Current",
        native_unit_of_measurement=UnitOfElectricCurrent.AMPERE,
        device_class=SensorDeviceClass.CURRENT,
        state_class=SensorStateClass.MEASUREMENT,
        icon="mdi:current-dc",
        suggested_display_precision=1,
    ),
    FelicitySensorDescription(
        key="charge_power",
        name="Battery Charge Power",
        native_unit_of_measurement=UnitOfPower.WATT,
        device_class=SensorDeviceClass.POWER,
        state_class=SensorStateClass.MEASUREMENT,
        icon="mdi:flash",
    ),
    FelicitySensorDescription(
        key="discharge_power",
        name="Battery Discharge Power",
        native_unit_of_measurement=UnitOfPower.WATT,
        device_class=SensorDeviceClass.POWER,
        state_class=SensorStateClass.MEASUREMENT,
        icon="mdi:flash-outline",
    ),

    # --- Температуры батареи ---
    FelicitySensorDescription(
        key="temp_1",
        name="Battery Temp 1",
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
        icon="mdi:thermometer",
        suggested_display_precision=1,
    ),
    FelicitySensorDescription(
        key="temp_2",
        name="Battery Temp 2",
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
        icon="mdi:thermometer",
        suggested_display_precision=1,
    ),
    FelicitySensorDescription(
        key="temp_3",
        name="Battery Temp 3",
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
        icon="mdi:thermometer",
        suggested_display_precision=1,
    ),
    FelicitySensorDescription(
        key="temp_4",
        name="Battery Temp 4",
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
        icon="mdi:thermometer",
        suggested_display_precision=1,
    ),

    # --- Клетки: макс/мин и номера ---
    FelicitySensorDescription(
        key="cell_max_voltage",
        name="Max Cell Voltage",
        native_unit_of_measurement=UnitOfElectricPotential.VOLT,
        device_class=SensorDeviceClass.VOLTAGE,
        state_class=SensorStateClass.MEASUREMENT,
        icon="mdi:battery-positive",
        suggested_display_precision=3,
        entity_category=EntityCategory.DIAGNOSTIC,
    ),
    FelicitySensorDescription(
        key="cell_min_voltage",
        name="Min Cell Voltage",
        native_unit_of_measurement=UnitOfElectricPotential.VOLT,
        device_class=SensorDeviceClass.VOLTAGE,
        state_class=SensorStateClass.MEASUREMENT,
        icon="mdi:battery-negative",
        suggested_display_precision=3,
        entity_category=EntityCategory.DIAGNOSTIC,
    ),
    FelicitySensorDescription(
        key="cell_max_index",
        name="Max Cell Index",
        icon="mdi:numeric",
        entity_category=EntityCategory.DIAGNOSTIC,
    ),
    FelicitySensorDescription(
        key="cell_min_index",
        name="Min Cell Index",
        icon="mdi:numeric",
        entity_category=EntityCategory.DIAGNOSTIC,
    ),

    # --- Напряжения по ячейкам 1-16 ---
    FelicitySensorDescription(
        key="cell_1_v",
        name="Cell 1 Voltage",
        native_unit_of_measurement=UnitOfElectricPotential.VOLT,
        device_class=SensorDeviceClass.VOLTAGE,
        state_class=SensorStateClass.MEASUREMENT,
        icon="mdi:battery",
        suggested_display_precision=3,
        entity_category=EntityCategory.DIAGNOSTIC,
    ),
    FelicitySensorDescription(
        key="cell_2_v",
        name="Cell 2 Voltage",
        native_unit_of_measurement=UnitOfElectricPotential.VOLT,
        device_class=SensorDeviceClass.VOLTAGE,
        state_class=SensorStateClass.MEASUREMENT,
        icon="mdi:battery",
        suggested_display_precision=3,
        entity_category=EntityCategory.DIAGNOSTIC,
    ),
    FelicitySensorDescription(
        key="cell_3_v",
        name="Cell 3 Voltage",
        native_unit_of_measurement=UnitOfElectricPotential.VOLT,
        device_class=SensorDeviceClass.VOLTAGE,
        state_class=SensorStateClass.MEASUREMENT,
        icon="mdi:battery",
        suggested_display_precision=3,
        entity_category=EntityCategory.DIAGNOSTIC,
    ),
    FelicitySensorDescription(
        key="cell_4_v",
        name="Cell 4 Voltage",
        native_unit_of_measurement=UnitOfElectricPotential.VOLT,
        device_class=SensorDeviceClass.VOLTAGE,
        state_class=SensorStateClass.MEASUREMENT,
        icon="mdi:battery",
        suggested_display_precision=3,
        entity_category=EntityCategory.DIAGNOSTIC,
    ),
    FelicitySensorDescription(
        key="cell_5_v",
        name="Cell 5 Voltage",
        native_unit_of_measurement=UnitOfElectricPotential.VOLT,
        device_class=SensorDeviceClass.VOLTAGE,
        state_class=SensorStateClass.MEASUREMENT,
        icon="mdi:battery",
        suggested_display_precision=3,
        entity_category=EntityCategory.DIAGNOSTIC,
    ),
    FelicitySensorDescription(
        key="cell_6_v",
        name="Cell 6 Voltage",
        native_unit_of_measurement=UnitOfElectricPotential.VOLT,
        device_class=SensorDeviceClass.VOLTAGE,
        state_class=SensorStateClass.MEASUREMENT,
        icon="mdi:battery",
        suggested_display_precision=3,
        entity_category=EntityCategory.DIAGNOSTIC,
    ),
    FelicitySensorDescription(
        key="cell_7_v",
        name="Cell 7 Voltage",
        native_unit_of_measurement=UnitOfElectricPotential.VOLT,
        device_class=SensorDeviceClass.VOLTAGE,
        state_class=SensorStateClass.MEASUREMENT,
        icon="mdi:battery",
        suggested_display_precision=3,
        entity_category=EntityCategory.DIAGNOSTIC,
    ),
    FelicitySensorDescription(
        key="cell_8_v",
        name="Cell 8 Voltage",
        native_unit_of_measurement=UnitOfElectricPotential.VOLT,
        device_class=SensorDeviceClass.VOLTAGE,
        state_class=SensorStateClass.MEASUREMENT,
        icon="mdi:battery",
        suggested_display_precision=3,
        entity_category=EntityCategory.DIAGNOSTIC,
    ),
    FelicitySensorDescription(
        key="cell_9_v",
        name="Cell 9 Voltage",
        native_unit_of_measurement=UnitOfElectricPotential.VOLT,
        device_class=SensorDeviceClass.VOLTAGE,
        state_class=SensorStateClass.MEASUREMENT,
        icon="mdi:battery",
        suggested_display_precision=3,
        entity_category=EntityCategory.DIAGNOSTIC,
    ),
    FelicitySensorDescription(
        key="cell_10_v",
        name="Cell 10 Voltage",
        native_unit_of_measurement=UnitOfElectricPotential.VOLT,
        device_class=SensorDeviceClass.VOLTAGE,
        state_class=SensorStateClass.MEASUREMENT,
        icon="mdi:battery",
        suggested_display_precision=3,
        entity_category=EntityCategory.DIAGNOSTIC,
    ),
    FelicitySensorDescription(
        key="cell_11_v",
        name="Cell 11 Voltage",
        native_unit_of_measurement=UnitOfElectricPotential.VOLT,
        device_class=SensorDeviceClass.VOLTAGE,
        state_class=SensorStateClass.MEASUREMENT,
        icon="mdi:battery",
        suggested_display_precision=3,
        entity_category=EntityCategory.DIAGNOSTIC,
    ),
    FelicitySensorDescription(
        key="cell_12_v",
        name="Cell 12 Voltage",
        native_unit_of_measurement=UnitOfElectricPotential.VOLT,
        device_class=SensorDeviceClass.VOLTAGE,
        state_class=SensorStateClass.MEASUREMENT,
        icon="mdi:battery",
        suggested_display_precision=3,
        entity_category=EntityCategory.DIAGNOSTIC,
    ),
    FelicitySensorDescription(
        key="cell_13_v",
        name="Cell 13 Voltage",
        native_unit_of_measurement=UnitOfElectricPotential.VOLT,
        device_class=SensorDeviceClass.VOLTAGE,
        state_class=SensorStateClass.MEASUREMENT,
        icon="mdi:battery",
        suggested_display_precision=3,
        entity_category=EntityCategory.DIAGNOSTIC,
    ),
    FelicitySensorDescription(
        key="cell_14_v",
        name="Cell 14 Voltage",
        native_unit_of_measurement=UnitOfElectricPotential.VOLT,
        device_class=SensorDeviceClass.VOLTAGE,
        state_class=SensorStateClass.MEASUREMENT,
        icon="mdi:battery",
        suggested_display_precision=3,
        entity_category=EntityCategory.DIAGNOSTIC,
    ),
    FelicitySensorDescription(
        key="cell_15_v",
        name="Cell 15 Voltage",
        native_unit_of_measurement=UnitOfElectricPotential.VOLT,
        device_class=SensorDeviceClass.VOLTAGE,
        state_class=SensorStateClass.MEASUREMENT,
        icon="mdi:battery",
        suggested_display_precision=3,
        entity_category=EntityCategory.DIAGNOSTIC,
    ),
    FelicitySensorDescription(
        key="cell_16_v",
        name="Cell 16 Voltage",
        native_unit_of_measurement=UnitOfElectricPotential.VOLT,
        device_class=SensorDeviceClass.VOLTAGE,
        state_class=SensorStateClass.MEASUREMENT,
        icon="mdi:battery",
        suggested_display_precision=3,
        entity_category=EntityCategory.DIAGNOSTIC,
    ),

    # --- Лимиты по фактическим данным ---
    FelicitySensorDescription(
        key="max_charge_current",
        name="Max Charge Current (runtime)",
        native_unit_of_measurement=UnitOfElectricCurrent.AMPERE,
        device_class=SensorDeviceClass.CURRENT,
        state_class=SensorStateClass.MEASUREMENT,
        icon="mdi:current-ac",
        suggested_display_precision=1,
        entity_category=EntityCategory.DIAGNOSTIC,
    ),
    FelicitySensorDescription(
        key="max_discharge_current",
        name="Max Discharge Current (runtime)",
        native_unit_of_measurement=UnitOfElectricCurrent.AMPERE,
        device_class=SensorDeviceClass.CURRENT,
        state_class=SensorStateClass.MEASUREMENT,
        icon="mdi:current-ac",
        suggested_display_precision=1,
        entity_category=EntityCategory.DIAGNOSTIC,
    ),

    # --- Состояние / коды ---
    FelicitySensorDescription(
        key="state",
        name="Battery State",
        icon="mdi:battery-heart",
    ),
    FelicitySensorDescription(
        key="fw_version",
        name="BMS Firmware Version",
        icon="mdi:chip",
        entity_category=EntityCategory.DIAGNOSTIC,
    ),
    FelicitySensorDescription(
        key="bms_m1_fw",
        name="BMS M1 FW",
        icon="mdi:chip",
        entity_category=EntityCategory.DIAGNOSTIC,
    ),
    FelicitySensorDescription(
        key="bms_m2_fw",
        name="BMS M2 FW",
        icon="mdi:chip",
        entity_category=EntityCategory.DIAGNOSTIC,
    ),
    FelicitySensorDescription(
        key="battery_type",
        name="Battery Type",
        icon="mdi:battery",
        entity_category=EntityCategory.DIAGNOSTIC,
    ),
    FelicitySensorDescription(
        key="battery_subtype",
        name="Battery Subtype",
        icon="mdi:battery",
        entity_category=EntityCategory.DIAGNOSTIC,
    ),
    FelicitySensorDescription(
        key="serial",
        name="Battery Serial",
        icon="mdi:identifier",
        entity_category=EntityCategory.DIAGNOSTIC,
    ),
    FelicitySensorDescription(
        key="wifi_serial",
        name="Wi-Fi Serial",
        icon="mdi:wifi",
        entity_category=EntityCategory.DIAGNOSTIC,
    ),

    # --- Настройки / пороги (из dev set infor) ---
    FelicitySensorDescription(
        key="ttl_pack",
        name="Battery Pack Count",
        icon="mdi:battery-multiple",
        entity_category=EntityCategory.DIAGNOSTIC,
    ),
    FelicitySensorDescription(
        key="cell_over_voltage",
        name="Cell Over Voltage",
        native_unit_of_measurement=UnitOfElectricPotential.VOLT,
        device_class=SensorDeviceClass.VOLTAGE,
        icon="mdi:arrow-up-bold",
        suggested_display_precision=3,
        entity_category=EntityCategory.DIAGNOSTIC,
    ),
    FelicitySensorDescription(
        key="cell_under_voltage",
        name="Cell Under Voltage",
        native_unit_of_measurement=UnitOfElectricPotential.VOLT,
        device_class=SensorDeviceClass.VOLTAGE,
        icon="mdi:arrow-down-bold",
        suggested_display_precision=3,
        entity_category=EntityCategory.DIAGNOSTIC,
    ),
    FelicitySensorDescription(
        key="cell_v_80",
        name="Cell Voltage @80%",
        native_unit_of_measurement=UnitOfElectricPotential.VOLT,
        device_class=SensorDeviceClass.VOLTAGE,
        icon="mdi:battery-80",
        suggested_display_precision=3,
        entity_category=EntityCategory.DIAGNOSTIC,
    ),
    FelicitySensorDescription(
        key="cell_v_20",
        name="Cell Voltage @20%",
        native_unit_of_measurement=UnitOfElectricPotential.VOLT,
        device_class=SensorDeviceClass.VOLTAGE,
        icon="mdi:battery-20",
        suggested_display_precision=3,
        entity_category=EntityCategory.DIAGNOSTIC,
    ),
    FelicitySensorDescription(
        key="charge_limit_setting",
        name="Charge Current Limit (setting)",
        native_unit_of_measurement=UnitOfElectricCurrent.AMPERE,
        device_class=SensorDeviceClass.CURRENT,
        icon="mdi:current-dc",
        suggested_display_precision=1,
        entity_category=EntityCategory.DIAGNOSTIC,
    ),
    FelicitySensorDescription(
        key="discharge_limit_setting",
        name="Discharge Current Limit (setting)",
        native_unit_of_measurement=UnitOfElectricCurrent.AMPERE,
        device_class=SensorDeviceClass.CURRENT,
        icon="mdi:current-dc",
        suggested_display_precision=1,
        entity_category=EntityCategory.DIAGNOSTIC,
    ),
)

INVERTER_SENSOR_DESCRIPTIONS: tuple[FelicitySensorDescription, ...] = (
    # --- Inverter runtime / status sensors ---
    FelicitySensorDescription(
        key="inverter_work_mode",
        name="Inverter Work Mode",
        icon="mdi:state-machine",
    ),
    FelicitySensorDescription(
        key="inverter_fault_code",
        name="Inverter Fault Code",
        icon="mdi:alert-circle",
        entity_category=EntityCategory.DIAGNOSTIC,
    ),
    FelicitySensorDescription(
        key="inverter_warning_code",
        name="Inverter Warning Code",
        icon="mdi:alert-outline",
        entity_category=EntityCategory.DIAGNOSTIC,
    ),
    FelicitySensorDescription(
        key="inverter_load_percent",
        name="Inverter Load",
        native_unit_of_measurement=PERCENTAGE,
        state_class=SensorStateClass.MEASUREMENT,
        icon="mdi:gauge",
    ),
    FelicitySensorDescription(
        key="inverter_bus_voltage",
        name="DC Bus Voltage",
        native_unit_of_measurement=UnitOfElectricPotential.VOLT,
        device_class=SensorDeviceClass.VOLTAGE,
        state_class=SensorStateClass.MEASUREMENT,
        icon="mdi:current-dc",
    ),
    FelicitySensorDescription(
        key="inverter_batt_voltage",
        name="Inverter Battery Voltage",
        native_unit_of_measurement=UnitOfElectricPotential.VOLT,
        device_class=SensorDeviceClass.VOLTAGE,
        state_class=SensorStateClass.MEASUREMENT,
        icon="mdi:battery",
    ),
    FelicitySensorDescription(
        key="inverter_batt_current",
        name="Inverter Battery Current",
        native_unit_of_measurement=UnitOfElectricCurrent.AMPERE,
        device_class=SensorDeviceClass.CURRENT,
        state_class=SensorStateClass.MEASUREMENT,
        icon="mdi:current-dc",
    ),
    FelicitySensorDescription(
        key="inverter_batt_soc",
        name="Inverter Battery SOC",
        native_unit_of_measurement=PERCENTAGE,
        device_class=SensorDeviceClass.BATTERY,
        state_class=SensorStateClass.MEASUREMENT,
        icon="mdi:battery",
    ),
)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Felicity sensors based on a config entry."""
    data = hass.data[DOMAIN][entry.entry_id]
    coordinator = data["coordinator"]
    device_type: str = data.get("device_type", DEVICE_TYPE_BATTERY)

    if device_type == DEVICE_TYPE_INVERTER:
        descriptions = INVERTER_SENSOR_DESCRIPTIONS
    else:
        descriptions = SENSOR_DESCRIPTIONS

    entities: list[FelicitySensor] = [
        FelicitySensor(coordinator, entry, desc) for desc in descriptions
    ]
    async_add_entities(entities)


class FelicitySensor(CoordinatorEntity, SensorEntity):
    """Representation of a Felicity sensor."""

    _attr_has_entity_name = True

    def __init__(
        self,
        coordinator,
        entry: ConfigEntry,
        description: FelicitySensorDescription,
    ) -> None:
        super().__init__(coordinator)
        self.entity_description = description
        self._entry = entry
        self._attr_unique_id = f"{entry.entry_id}_{description.key}"

    @property
    def device_info(self) -> dict[str, Any]:
        """Return device info to group entities into one device."""
        data = self.coordinator.data or {}
        serial = data.get("DevSN") or data.get("wifiSN") or self._entry.entry_id
        basic = data.get("_basic") or {}
        sw_version = basic.get("version")
        host = self._entry.data.get(CONF_HOST)
        serial_display = f"{serial} (IP {host})" if host else serial

        return {
            "identifiers": {(DOMAIN, serial)},
            "name": self._entry.data.get("name", "Felicity Battery"),
            "manufacturer": "Felicity",
            "model": "FLA48200",
            "sw_version": sw_version,
            "serial_number": serial_display,
        }

    @property
    def native_value(self) -> Any:
        """Return the native value of the entity."""
        data: dict = self.coordinator.data or {}
        key = self.entity_description.key

        def get_nested(path: tuple[Any, ...]):
            cur: Any = data
            try:
                for p in path:
                    cur = cur[p]
                return cur
            except (KeyError, IndexError, TypeError):
                return None

        # --- Inverter-specific telemetry ---
        if key == "inverter_work_mode":
            # Raw inverter work mode code from payload (Type-specific decoding can be added later)
            return data.get("workM")

        if key == "inverter_fault_code":
            # Raw inverter fault code bitmask/value
            return data.get("fault")

        if key == "inverter_warning_code":
            # Raw inverter warning code bitmask/value
            return data.get("warn")

        if key == "inverter_load_percent":
            raw = data.get("lPerc")
            return raw if isinstance(raw, (int, float)) else None

        if key == "inverter_bus_voltage":
            raw = data.get("busVp")
            if not isinstance(raw, (int, float)):
                return None
            # Typically reported in 0.1 V units, e.g. 3944 -> 394.4 V
            return round(raw / 10.0, 1)

        if key == "inverter_batt_voltage":
            raw = get_nested(("Batt", 0, 0))
            return round(raw / 1000.0, 2) if isinstance(raw, (int, float)) else None

        if key == "inverter_batt_current":
            raw = get_nested(("Batt", 1, 0))
            return round(raw / 10.0, 1) if isinstance(raw, (int, float)) else None

        if key == "inverter_batt_soc":
            raw = get_nested(("Batsoc", 0, 0))
            return round(raw / 100.0, 1) if isinstance(raw, (int, float)) else None

        # --- Runtime telemetry ---
        if key == "soc":
            raw = get_nested(("Batsoc", 0, 0))
            return round(raw / 100, 1) if isinstance(raw, (int, float)) else None

        if key == "voltage":
            raw = get_nested(("Batt", 0, 0))
            return round(raw / 1000, 2) if isinstance(raw, (int, float)) else None

        if key == "current":
            raw = get_nested(("Batt", 1, 0))
            return round(raw / 10, 1) if isinstance(raw, (int, float)) else None

        if key == "power":
            raw = get_nested(("BatInOut", 0))
            return raw if isinstance(raw, (int, float)) else None

        if key == "charge_current":
            raw = get_nested(("Batt", 1, 0))
            if not isinstance(raw, (int, float)):
                return None
            amp = round(raw / 10, 1)
            return amp if amp > 0 else 0.0

        if key == "discharge_current":
            raw = get_nested(("Batt", 1, 0))
            if not isinstance(raw, (int, float)):
                return None
            amp = round(raw / 10, 1)
            return abs(amp) if amp < 0 else 0.0

        if key == "charge_power":
            raw = get_nested(("Batt", 2, 0))
            return raw if isinstance(raw, (int, float)) else None

        if key == "discharge_power":
            raw = get_nested(("Batt", 2, 1))
            return raw if isinstance(raw, (int, float)) else None

        # Temps: BTemp [[t1,t2,t3,t4,...]] in 0.1 °C
        if key.startswith("temp_"):
            try:
                idx = int(key.split("_", 1)[1]) - 1
            except Exception:
                return None
            temps = get_nested(("BTemp", 0))
            if isinstance(temps, list) and 0 <= idx < len(temps):
                raw = temps[idx]
                return round(raw / 10, 1) if isinstance(raw, (int, float)) else None
            return None

        # Max/min voltage and indices
        if key == "cell_max_voltage":
            raw = get_nested(("BMaxMin", 0, 0))
            return round(raw / 1000, 3) if isinstance(raw, (int, float)) else None

        if key == "cell_min_voltage":
            raw = get_nested(("BMaxMin", 0, 1))
            return round(raw / 1000, 3) if isinstance(raw, (int, float)) else None

        if key == "cell_max_index":
            return get_nested(("BMaxMin", 1, 0))

        if key == "cell_min_index":
            return get_nested(("BMaxMin", 1, 1))

        # Cell voltages from BatcelList [[c1,c2,...]]
        if key.startswith("cell_") and key.endswith("_v"):
            try:
                idx = int(key.split("_", 1)[1].split("_")[0]) - 1
            except Exception:
                return None
            cells = get_nested(("BatcelList", 0))
            if isinstance(cells, list) and 0 <= idx < len(cells):
                raw = cells[idx]
                return round(raw / 1000, 3) if isinstance(raw, (int, float)) else None
            return None

        # Limits from runtime (LVolCur)
        if key == "max_charge_current":
            raw = get_nested(("LVolCur", 1, 0))
            return round(raw / 10, 1) if isinstance(raw, (int, float)) else None

        if key == "max_discharge_current":
            raw = get_nested(("LVolCur", 1, 1))
            return round(raw / 10, 1) if isinstance(raw, (int, float)) else None

        # State / FW / types from _basic
        basic = data.get("_basic") or {}
        settings = data.get("_settings") or {}

        if key == "state":
            return data.get("Estate")

        if key == "fw_version":
            return basic.get("version")

        if key == "bms_m1_fw":
            return basic.get("M1SwVer")

        if key == "bms_m2_fw":
            return basic.get("M2SwVer")

        if key == "battery_type":
            return basic.get("Type")

        if key == "battery_subtype":
            return basic.get("SubType")

        if key == "serial":
            return data.get("DevSN") or data.get("wifiSN")

        if key == "wifi_serial":
            return data.get("wifiSN")

        # --- Settings / thresholds ---
        if key == "ttl_pack":
            return settings.get("ttlPack")

        if key == "cell_v_80":
            raw = settings.get("wCVP80")
            return round(raw / 1000, 3) if isinstance(raw, (int, float)) else None

        if key == "cell_v_20":
            raw = settings.get("wCVP20")
            return round(raw / 1000, 3) if isinstance(raw, (int, float)) else None

        if key == "cell_over_voltage":
            raw = settings.get("FGOV")
            return round(raw / 1000, 3) if isinstance(raw, (int, float)) else None

        if key == "cell_under_voltage":
            raw = settings.get("FGUV")
            return round(raw / 1000, 3) if isinstance(raw, (int, float)) else None

        if key == "charge_limit_setting":
            raw = settings.get("BMChC")
            return round(raw / 10, 1) if isinstance(raw, (int, float)) else None

        if key == "discharge_limit_setting":
            raw = settings.get("BMDCu")
            return round(raw / 10, 1) if isinstance(raw, (int, float)) else None

        return None

    @property
    def extra_state_attributes(self) -> dict[str, Any] | None:
        """Return extra attributes for some sensors."""
        data = self.coordinator.data or {}
        key = self.entity_description.key

        if key in {
            "ttl_pack",
            "cell_v_80",
            "cell_v_20",
            "cell_over_voltage",
            "cell_under_voltage",
            "charge_limit_setting",
            "discharge_limit_setting",
        }:
            settings = data.get("_settings")
            if isinstance(settings, dict):
                return settings
            return None

        return None
