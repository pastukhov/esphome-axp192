import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.components import i2c, sensor, binary_sensor
from esphome.const import CONF_ID,\
    CONF_BATTERY_LEVEL, CONF_BRIGHTNESS, UNIT_PERCENT, ICON_BATTERY, CONF_MODEL, \
    UNIT_VOLT, UNIT_AMPERE, UNIT_WATT, UNIT_CELSIUS

CONF_CHARGING = "charging"
CONF_BATTERY_VOLTAGE = "battery_voltage"
CONF_BATTERY_CHARGE_CURRENT = "battery_charge_current"
CONF_BATTERY_DISCHARGE_CURRENT = "battery_discharge_current"
CONF_BATTERY_POWER = "battery_power"
CONF_VBUS_VOLTAGE = "vbus_voltage"
CONF_VBUS_CURRENT = "vbus_current"
CONF_VIN_VOLTAGE = "vin_voltage"
CONF_VIN_CURRENT = "vin_current"
CONF_APS_VOLTAGE = "aps_voltage"
CONF_PMU_TEMPERATURE = "pmu_temperature"
CONF_COULOMB_IN = "coulomb_in"
CONF_COULOMB_OUT = "coulomb_out"
CONF_COULOMB_DELTA = "coulomb_delta"
CONF_VBUS_PRESENT = "vbus_present"
CONF_BATTERY_PRESENT = "battery_present"
CONF_WARNING_LEVEL = "warning_level"

DEPENDENCIES = ['i2c']

axp192_ns = cg.esphome_ns.namespace('axp192')
AXP192Component = axp192_ns.class_('AXP192Component', cg.PollingComponent, i2c.I2CDevice)
AXP192Model = axp192_ns.enum("AXP192Model")

MODELS = {
    "M5CORE2": AXP192Model.AXP192_M5CORE2,
    "M5STICKC": AXP192Model.AXP192_M5STICKC,
    "M5TOUGH": AXP192Model.AXP192_M5TOUGH,
}

AXP192_MODEL = cv.enum(MODELS, upper=True, space="_")

CONFIG_SCHEMA = cv.Schema({
    cv.GenerateID(): cv.declare_id(AXP192Component),
    cv.Required(CONF_MODEL): AXP192_MODEL,
    cv.Optional(CONF_BATTERY_LEVEL):
        sensor.sensor_schema(
            unit_of_measurement=UNIT_PERCENT,
            accuracy_decimals=1,
            icon=ICON_BATTERY,
        ),
    cv.Optional(CONF_CHARGING): binary_sensor.binary_sensor_schema(),
    cv.Optional(CONF_BATTERY_VOLTAGE):
        sensor.sensor_schema(
            unit_of_measurement=UNIT_VOLT,
            accuracy_decimals=3,
            icon=ICON_BATTERY,
        ),
    cv.Optional(CONF_BATTERY_CHARGE_CURRENT):
        sensor.sensor_schema(
            unit_of_measurement=UNIT_AMPERE,
            accuracy_decimals=3,
            icon="mdi:current-ac",
        ),
    cv.Optional(CONF_BATTERY_DISCHARGE_CURRENT):
        sensor.sensor_schema(
            unit_of_measurement=UNIT_AMPERE,
            accuracy_decimals=3,
            icon="mdi:current-ac",
        ),
    cv.Optional(CONF_BATTERY_POWER):
        sensor.sensor_schema(
            unit_of_measurement=UNIT_WATT,
            accuracy_decimals=3,
        ),
    cv.Optional(CONF_VBUS_VOLTAGE):
        sensor.sensor_schema(
            unit_of_measurement=UNIT_VOLT,
            accuracy_decimals=3,
        ),
    cv.Optional(CONF_VBUS_CURRENT):
        sensor.sensor_schema(
            unit_of_measurement=UNIT_AMPERE,
            accuracy_decimals=3,
            icon="mdi:current-ac",
        ),
    cv.Optional(CONF_VIN_VOLTAGE):
        sensor.sensor_schema(
            unit_of_measurement=UNIT_VOLT,
            accuracy_decimals=3,
        ),
    cv.Optional(CONF_VIN_CURRENT):
        sensor.sensor_schema(
            unit_of_measurement=UNIT_AMPERE,
            accuracy_decimals=3,
            icon="mdi:current-ac",
        ),
    cv.Optional(CONF_APS_VOLTAGE):
        sensor.sensor_schema(
            unit_of_measurement=UNIT_VOLT,
            accuracy_decimals=3,
        ),
    cv.Optional(CONF_PMU_TEMPERATURE):
        sensor.sensor_schema(
            unit_of_measurement=UNIT_CELSIUS,
            accuracy_decimals=1,
        ),
    cv.Optional(CONF_COULOMB_IN):
        sensor.sensor_schema(
            unit_of_measurement="mAh",
            accuracy_decimals=3,
        ),
    cv.Optional(CONF_COULOMB_OUT):
        sensor.sensor_schema(
            unit_of_measurement="mAh",
            accuracy_decimals=3,
        ),
    cv.Optional(CONF_COULOMB_DELTA):
        sensor.sensor_schema(
            unit_of_measurement="mAh",
            accuracy_decimals=3,
        ),
    cv.Optional(CONF_VBUS_PRESENT): binary_sensor.binary_sensor_schema(),
    cv.Optional(CONF_BATTERY_PRESENT): binary_sensor.binary_sensor_schema(),
    cv.Optional(CONF_WARNING_LEVEL): binary_sensor.binary_sensor_schema(),
    cv.Optional(CONF_BRIGHTNESS, default=1.0): cv.percentage,
}).extend(cv.polling_component_schema('60s')).extend(i2c.i2c_device_schema(0x77))


def to_code(config):
    var = cg.new_Pvariable(config[CONF_ID])
    yield cg.register_component(var, config)
    yield i2c.register_i2c_device(var, config)

    cg.add(var.set_model(config[CONF_MODEL]))
    if CONF_BATTERY_LEVEL in config:
        conf = config[CONF_BATTERY_LEVEL]
        sens = yield sensor.new_sensor(conf)
        cg.add(var.set_batterylevel_sensor(sens))

    if CONF_CHARGING in config:
        conf = config[CONF_CHARGING]
        sens = yield binary_sensor.new_binary_sensor(conf)
        cg.add(var.set_charging_sensor(sens))

    if CONF_BATTERY_VOLTAGE in config:
        conf = config[CONF_BATTERY_VOLTAGE]
        sens = yield sensor.new_sensor(conf)
        cg.add(var.set_battery_voltage_sensor(sens))

    if CONF_BATTERY_CHARGE_CURRENT in config:
        conf = config[CONF_BATTERY_CHARGE_CURRENT]
        sens = yield sensor.new_sensor(conf)
        cg.add(var.set_battery_charge_current_sensor(sens))

    if CONF_BATTERY_DISCHARGE_CURRENT in config:
        conf = config[CONF_BATTERY_DISCHARGE_CURRENT]
        sens = yield sensor.new_sensor(conf)
        cg.add(var.set_battery_discharge_current_sensor(sens))

    if CONF_BATTERY_POWER in config:
        conf = config[CONF_BATTERY_POWER]
        sens = yield sensor.new_sensor(conf)
        cg.add(var.set_battery_power_sensor(sens))

    if CONF_VBUS_VOLTAGE in config:
        conf = config[CONF_VBUS_VOLTAGE]
        sens = yield sensor.new_sensor(conf)
        cg.add(var.set_vbus_voltage_sensor(sens))

    if CONF_VBUS_CURRENT in config:
        conf = config[CONF_VBUS_CURRENT]
        sens = yield sensor.new_sensor(conf)
        cg.add(var.set_vbus_current_sensor(sens))

    if CONF_VIN_VOLTAGE in config:
        conf = config[CONF_VIN_VOLTAGE]
        sens = yield sensor.new_sensor(conf)
        cg.add(var.set_vin_voltage_sensor(sens))

    if CONF_VIN_CURRENT in config:
        conf = config[CONF_VIN_CURRENT]
        sens = yield sensor.new_sensor(conf)
        cg.add(var.set_vin_current_sensor(sens))

    if CONF_APS_VOLTAGE in config:
        conf = config[CONF_APS_VOLTAGE]
        sens = yield sensor.new_sensor(conf)
        cg.add(var.set_aps_voltage_sensor(sens))

    if CONF_PMU_TEMPERATURE in config:
        conf = config[CONF_PMU_TEMPERATURE]
        sens = yield sensor.new_sensor(conf)
        cg.add(var.set_pmu_temperature_sensor(sens))

    if CONF_COULOMB_IN in config:
        conf = config[CONF_COULOMB_IN]
        sens = yield sensor.new_sensor(conf)
        cg.add(var.set_coulomb_in_sensor(sens))

    if CONF_COULOMB_OUT in config:
        conf = config[CONF_COULOMB_OUT]
        sens = yield sensor.new_sensor(conf)
        cg.add(var.set_coulomb_out_sensor(sens))

    if CONF_COULOMB_DELTA in config:
        conf = config[CONF_COULOMB_DELTA]
        sens = yield sensor.new_sensor(conf)
        cg.add(var.set_coulomb_delta_sensor(sens))

    if CONF_VBUS_PRESENT in config:
        conf = config[CONF_VBUS_PRESENT]
        sens = yield binary_sensor.new_binary_sensor(conf)
        cg.add(var.set_vbus_present_sensor(sens))

    if CONF_BATTERY_PRESENT in config:
        conf = config[CONF_BATTERY_PRESENT]
        sens = yield binary_sensor.new_binary_sensor(conf)
        cg.add(var.set_battery_present_sensor(sens))

    if CONF_WARNING_LEVEL in config:
        conf = config[CONF_WARNING_LEVEL]
        sens = yield binary_sensor.new_binary_sensor(conf)
        cg.add(var.set_warning_level_sensor(sens))

    if CONF_BRIGHTNESS in config:
        conf = config[CONF_BRIGHTNESS]
        cg.add(var.set_brightness(conf))
