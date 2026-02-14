import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.components import binary_sensor

from .sensor import axp192_ns, AXP192Component

CONF_AXP192_ID = "axp192_id"
CONF_CHARGING = "charging"
CONF_VBUS_PRESENT = "vbus_present"
CONF_BATTERY_PRESENT = "battery_present"
CONF_WARNING_LEVEL = "warning_level"

CONFIG_SCHEMA = cv.Schema({
    cv.Required(CONF_AXP192_ID): cv.use_id(AXP192Component),
    cv.Optional(CONF_CHARGING): binary_sensor.binary_sensor_schema(),
    cv.Optional(CONF_VBUS_PRESENT): binary_sensor.binary_sensor_schema(),
    cv.Optional(CONF_BATTERY_PRESENT): binary_sensor.binary_sensor_schema(),
    cv.Optional(CONF_WARNING_LEVEL): binary_sensor.binary_sensor_schema(),
})


def to_code(config):
    parent = yield cg.get_variable(config[CONF_AXP192_ID])

    if CONF_CHARGING in config:
        conf = config[CONF_CHARGING]
        sens = yield binary_sensor.new_binary_sensor(conf)
        cg.add(parent.set_charging_sensor(sens))

    if CONF_VBUS_PRESENT in config:
        conf = config[CONF_VBUS_PRESENT]
        sens = yield binary_sensor.new_binary_sensor(conf)
        cg.add(parent.set_vbus_present_sensor(sens))

    if CONF_BATTERY_PRESENT in config:
        conf = config[CONF_BATTERY_PRESENT]
        sens = yield binary_sensor.new_binary_sensor(conf)
        cg.add(parent.set_battery_present_sensor(sens))

    if CONF_WARNING_LEVEL in config:
        conf = config[CONF_WARNING_LEVEL]
        sens = yield binary_sensor.new_binary_sensor(conf)
        cg.add(parent.set_warning_level_sensor(sens))
