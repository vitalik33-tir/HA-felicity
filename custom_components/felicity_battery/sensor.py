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

from .const import DOMAIN


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
        icon="mdi:flash",
    ),
    FelicitySensorDescription(
        key="direction",
        name="Battery Direction",
        icon="mdi:swap-vertical",
    ),
    FelicitySensorDescription(
        key="temp1",
        name="Battery Temp 1",
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
        icon="mdi:thermometer",
        suggested_display_precision=1,
    ),
    FelicitySensorDescription(
        key="temp2",
        name="Battery Temp 2",
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
        icon="mdi:thermometer",
        suggested_display_precision=1,
    ),

    # --- Диагностика по ячейкам ---
    FelicitySensorDescription(
        key="max_cell_v",
        name="Max Cell Voltage",
        native_unit_of_measurement=UnitOfElectricPotential.VOLT,
        device_class=SensorDeviceClass.VOLTAGE,
        state_class=SensorStateClass.MEASUREMENT,
        icon="mdi:battery-high",
        suggested_display_precision=3,
        entity_category=EntityCategory.DIAGNOSTIC,
    ),
    FelicitySensorDescription(
        key="min_cell_v",
        name="Min Cell Voltage",
        native_unit_of_measurement=UnitOfElectricPotential.VOLT,
        device_class=SensorDeviceClass.VOLTAGE,
        state_class=SensorStateClass.MEASUREMENT,
        icon="mdi:battery-low",
        suggested_display_precision=3,
        entity_category=EntityCategory.DIAGNOSTIC,
    ),
    FelicitySensorDescription(
        key="cell_drift",
        name="Cell Voltage Drift",
        native_unit_of_measurement=UnitOfElectricPotential.VOLT,
        device_class=SensorDeviceClass.VOLTAGE,
        state_class=SensorStateClass.MEASUREMENT,
        icon="mdi:chart-bell-curve",
        suggested_display_precision=3,
        entity_category=EntityCategory.DIAGNOSTIC,
    ),

    # --- Напряжения ячеек 1–16 (диагностика) ---
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
        key="fault",
        name="Battery Fault Code",
        icon="mdi:alert",
        entity_category=EntityCategory.DIAGNOSTIC,
    ),
    FelicitySensorDescription(
        key="warning",
        name="Battery Warning Code",
        icon="mdi:alert-circle",
        entity_category=EntityCategory.DIAGNOSTIC,
    ),

    # --- Инфо / прошивки / тип / серийники ---
    FelicitySensorDescription(
        key="fw_version",
        name="Battery FW Version",
        icon="mdi:chip",
        entity_category=EntityCategory.DIAGNOSTIC,
    ),
    FelicitySensorDescription(
        key="bms_m1_fw",
        name="Battery BMS M1 FW",
        icon="mdi:chip",
        entity_category=EntityCategory.DIAGNOSTIC,
    ),
    FelicitySensorDescription(
        key="bms_m2_fw",
        name="Battery BMS M2 FW",
        icon="mdi:chip",
        entity_category=EntityCategory.DIAGNOSTIC,
    ),
    FelicitySensorDescription(
        key="battery_type",
        name="Battery Type",
        icon="mdi:identifier",
        entity_category=EntityCategory.DIAGNOSTIC,
    ),
    FelicitySensorDescription(
        key="battery_subtype",
        name="Battery SubType",
        icon="mdi:identifier",
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
        name="WiFi Module Serial",
        icon="mdi:wifi",
        entity_category=EntityCategory.DIAGNOSTIC,
    ),

    # --- Настройки / пороги (dev set infor) ---
    FelicitySensorDescription(
        key="ttl_pack",
        name="Battery Pack Count",
        icon="mdi:battery-variant",
        entity_category=EntityCategory.DIAGNOSTIC,
    ),
    FelicitySensorDescription(
        key="cell_v_80",
        name="Cell Voltage @80%",
        native_unit_of_measurement=UnitOfElectricPotential.VOLT,
        device_class=SensorDeviceClass.VOLTAGE,
        state_class=SensorStateClass.MEASUREMENT,
        icon="mdi:battery-80",
        suggested_display_precision=3,
        entity_category=EntityCategory.DIAGNOSTIC,
    ),
    FelicitySensorDescription(
        key="cell_v_20",
        name="Cell Voltage @20%",
        native_unit_of_measurement=UnitOfElectricPotential.VOLT,
        device_class=SensorDeviceClass.VOLTAGE,
        state_class=SensorStateClass.MEASUREMENT,
        icon="mdi:battery-20",
        suggested_display_precision=3,
        entity_category=EntityCategory.DIAGNOSTIC,
    ),
    FelicitySensorDescription(
        key="cell_over_voltage",
        name="Cell Over Voltage",
        native_unit_of_measurement=UnitOfElectricPotential.VOLT,
        device_class=SensorDeviceClass.VOLTAGE,
        state_class=SensorStateClass.MEASUREMENT,
        icon="mdi:flash-alert",
        suggested_display_precision=3,
        entity_category=EntityCategory.DIAGNOSTIC,
    ),
    FelicitySensorDescription(
        key="cell_under_voltage",
        name="Cell Under Voltage",
        native_unit_of_measurement=UnitOfElectricPotential.VOLT,
        device_class=SensorDeviceClass.VOLTAGE,
        state_class=SensorStateClass.MEASUREMENT,
        icon="mdi:flash-alert-outline",
        suggested_display_precision=3,
        entity_category=EntityCategory.DIAGNOSTIC,
    ),
    FelicitySensorDescription(
        key="charge_limit_setting",
        name="Charge Current Limit (setting)",
        native_unit_of_measurement=UnitOfElectricCurrent.AMPERE,
        device_class=SensorDeviceClass.CURRENT,
        state_class=SensorStateClass.MEASUREMENT,
        icon="mdi:current-ac",
        suggested_display_precision=1,
        entity_category=EntityCategory.DIAGNOSTIC,
    ),
    FelicitySensorDescription(
        key="discharge_limit_setting",
        name="Discharge Current Limit (setting)",
        native_unit_of_measurement=UnitOfElectricCurrent.AMPERE,
        device_class=SensorDeviceClass.CURRENT,
        state_class=SensorStateClass.MEASUREMENT,
        icon="mdi:current-ac",
        suggested_display_precision=1,
        entity_category=EntityCategory.DIAGNOSTIC,
    ),

    # --- Доп. диагностические сенсоры (Templist / BattList / BtemList / EMS/BMS / BLVolCu / LVolCur row0) ---
    # Templist[0][0..1] / 10
    FelicitySensorDescription(
        key="templist_1",
        name="Temp List 1",
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
        icon="mdi:thermometer",
        suggested_display_precision=1,
        entity_category=EntityCategory.DIAGNOSTIC,
    ),
    FelicitySensorDescription(
        key="templist_2",
        name="Temp List 2",
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
        icon="mdi:thermometer",
        suggested_display_precision=1,
        entity_category=EntityCategory.DIAGNOSTIC,
    ),

    # BattList / BatsocList
    FelicitySensorDescription(
        key="battlist_voltage",
        name="Pack List Voltage",
        native_unit_of_measurement=UnitOfElectricPotential.VOLT,
        device_class=SensorDeviceClass.VOLTAGE,
        state_class=SensorStateClass.MEASUREMENT,
        icon="mdi:current-dc",
        suggested_display_precision=2,
        entity_category=EntityCategory.DIAGNOSTIC,
    ),
    FelicitySensorDescription(
        key="battlist_current",
        name="Pack List Current",
        native_unit_of_measurement=UnitOfElectricCurrent.AMPERE,
        device_class=SensorDeviceClass.CURRENT,
        state_class=SensorStateClass.MEASUREMENT,
        icon="mdi:current-dc",
        suggested_display_precision=1,
        entity_category=EntityCategory.DIAGNOSTIC,
    ),
    FelicitySensorDescription(
        key="battlist_soc",
        name="Pack List SOC",
        native_unit_of_measurement=PERCENTAGE,
        device_class=SensorDeviceClass.BATTERY,
        state_class=SensorStateClass.MEASUREMENT,
        icon="mdi:battery",
        suggested_display_precision=1,
        entity_category=EntityCategory.DIAGNOSTIC,
    ),

    # EMSpara / BMSpara
    FelicitySensorDescription(
        key="ems_para",
        name="EMS Parameter Word",
        icon="mdi:database",
        entity_category=EntityCategory.DIAGNOSTIC,
    ),
    FelicitySensorDescription(
        key="bms_para",
        name="BMS Parameter Word",
        icon="mdi:database",
        entity_category=EntityCategory.DIAGNOSTIC,
    ),

    # BLVolCu[0][0..1] / 10
    FelicitySensorDescription(
        key="blvolcu_max",
        name="BLVolCu Max Current",
        native_unit_of_measurement=UnitOfElectricCurrent.AMPERE,
        device_class=SensorDeviceClass.CURRENT,
        state_class=SensorStateClass.MEASUREMENT,
        icon="mdi:current-ac",
        suggested_display_precision=1,
        entity_category=EntityCategory.DIAGNOSTIC,
    ),
    FelicitySensorDescription(
        key="blvolcu_min",
        name="BLVolCu Min Current",
        native_unit_of_measurement=UnitOfElectricCurrent.AMPERE,
        device_class=SensorDeviceClass.CURRENT,
        state_class=SensorStateClass.MEASUREMENT,
        icon="mdi:current-ac",
        suggested_display_precision=1,
        entity_category=EntityCategory.DIAGNOSTIC,
    ),

    # LVolCur[0][0..1] / 10 (в JS это LVolCurMax / LVolCurMin, отдельные от наших runtime-ограничений)
    FelicitySensorDescription(
        key="lvolcur_max",
        name="LVolCur Max (row0)",
        native_unit_of_measurement=UnitOfElectricCurrent.AMPERE,
        device_class=SensorDeviceClass.CURRENT,
        state_class=SensorStateClass.MEASUREMENT,
        icon="mdi:current-ac",
        suggested_display_precision=1,
        entity_category=EntityCategory.DIAGNOSTIC,
    ),
    FelicitySensorDescription(
        key="lvolcur_min",
        name="LVolCur Min (row0)",
        native_unit_of_measurement=UnitOfElectricCurrent.AMPERE,
        device_class=SensorDeviceClass.CURRENT,
        state_class=SensorStateClass.MEASUREMENT,
        icon="mdi:current-ac",
        suggested_display_precision=1,
        entity_category=EntityCategory.DIAGNOSTIC,
    ),

    # BtemList[0][0..3] / 10
    FelicitySensorDescription(
        key="bms_temp_1",
        name="BMS Temp 1",
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
        icon="mdi:thermometer",
        suggested_display_precision=1,
        entity_category=EntityCategory.DIAGNOSTIC,
    ),
    FelicitySensorDescription(
        key="bms_temp_2",
        name="BMS Temp 2",
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MЕASUREMENT,
        icon="mdi:thermometer",
        suggested_display_precision=1,
        entity_category=EntityCategory.DIAGNOSTIC,
    ),
    FelicitySensorDescription(
        key="bms_temp_3",
        name="BMS Temp 3",
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MЕASUREMENT,
        icon="mdi:thermometer",
        suggested_display_precision=1,
        entity_category=EntityCategory.DИAGNOSTIC,
    ),
    FelicitySensorDescription(
        key="bms_temp_4",
        name="BMS Temp 4",
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        device_class=SensorDeviceClass.TЕМPERATURE,
        state_class=SensorStateClass.МЕASUREMENT,
        icon="mdi:thermometer",
        suggested_display_precision=1,
        entity_category=EntityCategory.DИAGNOSTIC,
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

    entities: list[FelicitySensor] = [
        FelicitySensor(coordinator, entry, desc) for desc in SENSOR_DESCRIPTIONS
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

        return {
            "identifiers": {(DOMAIN, serial)},
            "name": self._entry.data.get("name", "Felicity Battery"),
            "manufacturer": "Felicity",
            "model": "FLA48200",
            "sw_version": sw_version,
            "serial_number": serial,
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

        # --- Runtime telemetry ---
        if key == "soc":
            raw = get_nested(("Batsoc", 0, 0))
            return round(raw / 100, 1) if raw is not None else None

        if key == "voltage":
            raw = get_nested(("Batt", 0, 0))
            return round(raw / 1000, 2) if raw is not None else None

        if key == "current":
            raw = get_nested(("Batt", 1, 0))
            return round(raw / 10, 1) if raw is not None else None

        if key == "power":
            v_raw = get_nested(("Batt", 0, 0))
            i_raw = get_nested(("Batt", 1, 0))
            if v_raw is None or i_raw is None:
                return None
            v = v_raw / 1000
            i = i_raw / 10
            return round(v * i)

        if key == "charge_current":
            i_raw = get_nested(("Batt", 1, 0))
            if i_raw is None:
                return None
            current = i_raw / 10.0
            return round(current, 1) if current > 0 else 0.0

        if key == "discharge_current":
            i_raw = get_nested(("Batt", 1, 0))
            if i_raw is None:
                return None
            current = i_raw / 10.0
            return round(-current, 1) if current < 0 else 0.0

        if key == "charge_power":
            v_raw = get_nested(("Batt", 0, 0))
            i_raw = get_nested(("Batt", 1, 0))
            if v_raw is None or i_raw is None:
                return None
            v = v_raw / 1000.0
            i = i_raw / 10.0
            p = v * i
            return round(p) if p > 0 else 0

        if key == "discharge_power":
            v_raw = get_nested(("Batt", 0, 0))
            i_raw = get_nested(("Batt", 1, 0))
            if v_raw is None or i_raw is None:
                return None
            v = v_raw / 1000.0
            i = i_raw / 10.0
            p = v * i
            return round(-p) if p < 0 else 0

        if key == "direction":
            i_raw = get_nested(("Batt", 1, 0))
            if i_raw is not None:
                current = i_raw / 10.0
                if current > 0.05:
                    return "charging"
                if current < -0.05:
                    return "discharging"
            code = data.get("Estate")
            if code == 9152:
                return "charging"
            if code == 5056:
                return "discharging"
            if code in (960, 320):
                return "idle"
            return "idle"

        if key == "temp1":
            raw = get_nested(("BTemp", 0, 0))
            return round(raw / 10, 1) if raw is not None else None

        if key == "temp2":
            raw = get_nested(("BTemp", 0, 1))
            return round(raw / 10, 1) if raw is not None else None

        if key == "max_cell_v":
            raw = get_nested(("BMaxMin", 0, 0))
            return round(raw / 1000, 3) if raw is not None else None

        if key == "min_cell_v":
            raw = get_nested(("BMaxMin", 0, 1))
            return round(raw / 1000, 3) if raw is not None else None

        if key == "cell_drift":
            max_raw = get_nested(("BMaxMin", 0, 0))
            min_raw = get_nested(("BMaxMin", 0, 1))
            if max_raw is None or min_raw is None:
                return None
            return round((max_raw - min_raw) / 1000, 3)

        # --- Cell voltages 1–16 ---
        if key.startswith("cell_") and key.endswith("_v"):
            try:
                idx = int(key.split("_")[1]) - 1  # 0..15
            except (ValueError, IndexError):
                return None
            raw = get_nested(("BatcelList", 0, idx))
            if raw is None or raw == 65535:
                return None
            # мВ -> В, три знака
            return round(raw / 1000.0, 3)

        # --- Limits from runtime data ---
        if key == "max_charge_current":
            raw = get_nested(("LVolCur", 1, 0))
            return round(raw / 10, 1) if raw is not None else None

        if key == "max_discharge_current":
            raw = get_nested(("LVolCur", 1, 1))
            return round(raw / 10, 1) if raw is not None else None

        if key == "state":
            code = data.get("Estate")
            if code is None:
                return None
            if code == 320:
                return "full"
            if code == 960:
                return "standby"
            if code == 9152:
                return "charging"
            if code == 5056:
                return "discharging"
            return f"unknown({code})"

        if key == "fault":
            v = data.get("Bfault")
            if v is None:
                return None
            return int(v)

        if key == "warning":
            v = data.get("Bwarn")
            if v is None:
                return None
            return int(v)

        # --- Basic info / firmware / type ---
        basic = data.get("_basic") or {}
        settings = data.get("_settings") or {}

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
            raw = settings.get("cVolHi")
            return round(raw / 1000, 3) if isinstance(raw, (int, float)) else None

        if key == "cell_under_voltage":
            raw = settings.get("cVolLo")
            return round(raw / 1000, 3) if isinstance(raw, (int, float)) else None

        if key == "charge_limit_setting":
            raw = settings.get("bCCHi2")
            return round(raw / 10, 1) if isinstance(raw, (int, float)) else None

        if key == "discharge_limit_setting":
            raw = settings.get("bDCHi2")
            return round(raw / 10, 1) if isinstance(raw, (int, float)) else None

        # --- Доп. диагностические сенсоры на основе "dev real infor" ---

        # Templist[0][0..1] / 10
        if key == "templist_1":
            raw = get_nested(("Templist", 0, 0))
            return round(raw / 10.0, 1) if raw is not None else None

        if key == "templist_2":
            raw = get_nested(("Templist", 0, 1))
            return round(raw / 10.0, 1) if raw is not None else None

        # BattList / BatsocList
        if key == "battlist_voltage":
            raw = get_nested(("BattList", 0, 0))
            return round(raw / 1000.0, 2) if raw is not None else None

        if key == "battlist_current":
            raw = get_nested(("BattList", 1, 0))
            return round(raw / 10.0, 1) if raw is not None else None

        if key == "battlist_soc":
            raw = get_nested(("BatsocList", 0, 0))
            return round(raw / 100.0, 1) if raw is not None else None

        # EMSpara / BMSpara
        if key == "ems_para":
            raw = get_nested(("EMSpara", 0, 0))
            if isinstance(raw, (int, float)):
                return int(raw)
            return raw

        if key == "bms_para":
            raw = get_nested(("BMSpara", 0, 0))
            if isinstance(raw, (int, float)):
                return int(raw)
            return raw

        # BLVolCu[0][0..1] / 10
        if key == "blvolcu_max":
            raw = get_nested(("BLVolCu", 0, 0))
            return round(raw / 10.0, 1) if raw is not None else None

        if key == "blvolcu_min":
            raw = get_nested(("BLVolCu", 0, 1))
            return round(raw / 10.0, 1) if raw is not None else None

        # LVolCur[0][0..1] / 10 (JS: LVolCurMax / LVolCurMin)
        if key == "lvolcur_max":
            raw = get_nested(("LVolCur", 0, 0))
            return round(raw / 10.0, 1) if raw is not None else None

        if key == "lvolcur_min":
            raw = get_nested(("LVolCur", 0, 1))
            return round(raw / 10.0, 1) if raw is not None else None

        # BtemList[0][0..3] / 10
        if key == "bms_temp_1":
            raw = get_nested(("BtemList", 0, 0))
            return round(raw / 10.0, 1) if raw is not None else None

        if key == "bms_temp_2":
            raw = get_nested(("BtemList", 0, 1))
            return round(raw / 10.0, 1) if raw is not None else None

        if key == "bms_temp_3":
            raw = get_nested(("BtemList", 0, 2))
            return round(raw / 10.0, 1) if raw is not None else None

        if key == "bms_temp_4":
            raw = get_nested(("BtemList", 0, 3))
            return round(raw / 10.0, 1) if raw is not None else None

        return None

    @property
    def extra_state_attributes(self) -> dict[str, Any] | None:
        """Return extra attributes for some sensors."""
        data: dict = self.coordinator.data or {}
        key = self.entity_description.key

        # Агрегация по ячейкам для сенсора cell_drift
        if key == "cell_drift":
            attrs: dict[str, Any] = {}
            cells_list = data.get("BatcelList")
            if (
                isinstance(cells_list, list)
                and cells_list
                and isinstance(cells_list[0], list)
            ):
                raw_cells = cells_list[0]
                cells_v: list[float] = []
                for c in raw_cells:
                    if isinstance(c, int) and c != 65535:
                        cells_v.append(round(c / 1000.0, 3))
                if cells_v:
                    attrs["cells"] = cells_v
                    max_v = max(cells_v)
                    min_v = min(cells_v)
                    attrs["max_cell_voltage"] = max_v
                    attrs["min_cell_voltage"] = min_v
                    attrs["max_cell_index"] = cells_v.index(max_v) + 1
                    attrs["min_cell_index"] = cells_v.index(min_v) + 1
            return attrs or None

        if key in {
            "fw_version",
            "bms_m1_fw",
            "bms_m2_fw",
            "battery_type",
            "battery_subtype",
            "serial",
            "wifi_serial",
        }:
            basic = data.get("_basic")
            if isinstance(basic, dict):
                return basic
            return None

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

        # Сырые массивы для новых диагностических сенсоров

        # Для templist_1 / templist_2 отдадим весь Templist
        if key in {"templist_1", "templist_2"}:
            templist = data.get("Templist")
            if isinstance(templist, list):
                return {"Templist": templist}
            return None

        # Для battlist_* отдадим BattList и BatsocList
        if key in {"battlist_voltage", "battlist_current", "battlist_soc"}:
            attrs: dict[str, Any] = {}
            batt_list = data.get("BattList")
            if batt_list is not None:
                attrs["BattList"] = batt_list
            batsoc_list = data.get("BatsocList")
            if batsoc_list is not None:
                attrs["BatsocList"] = batsoc_list
            return attrs or None

        # Для bms_temp_* отдаём BtemList (все датчики BMS)
        if key in {"bms_temp_1", "bms_temp_2", "bms_temp_3", "bms_temp_4"}:
            btem = data.get("BtemList")
            if isinstance(btem, list):
                return {"BtemList": btem}
            return None

        # Для ems_para / bms_para отдадим оба массива EMSpara/BMSpara
        if key in {"ems_para", "bms_para"}:
            attrs: dict[str, Any] = {}
            ems = data.get("EMSpara")
            if ems is not None:
                attrs["EMSpara"] = ems
            bms = data.get("BMSpara")
            if bms is not None:
                attrs["BMSpara"] = bms
            return attrs or None

        # Для blvolcu_* отдадим весь BLVolCu
        if key in {"blvolcu_max", "blvolcu_min"}:
            bl = data.get("BLVolCu")
            if isinstance(bl, list):
                return {"BLVolCu": bl}
            return None

        # Для lvolcur_* отдадим весь LVolCur
        if key in {"lvolcur_max", "lvolcur_min"}:
            lc = data.get("LVolCur")
            if isinstance(lc, list):
                return {"LVolCur": lc}
            return None

        return None
