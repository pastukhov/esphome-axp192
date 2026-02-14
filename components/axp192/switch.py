import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.components import switch

from .sensor import axp192_ns, AXP192Component, CONF_MODEL, AXP192_MODEL

CONF_AXP192_ID = "axp192_id"
CONF_LDO2 = "ldo2"
CONF_LDO3 = "ldo3"
CONF_DCDC1 = "dcdc1"
CONF_DCDC3 = "dcdc3"
CONF_SPEAKER_ENABLE = "speaker_enable"
CONF_GREEN_LED = "green_led"
CONF_ADC_ENABLE = "adc_enable"

AXP192Switch = axp192_ns.class_("AXP192Switch", switch.Switch, cg.Parented.template(AXP192Component))
AXP192SwitchType = axp192_ns.enum("AXP192SwitchType")

SWITCH_TYPES = {
    CONF_LDO2: AXP192SwitchType.AXP192_SWITCH_LDO2,
    CONF_LDO3: AXP192SwitchType.AXP192_SWITCH_LDO3,
    CONF_DCDC1: AXP192SwitchType.AXP192_SWITCH_DCDC1,
    CONF_DCDC3: AXP192SwitchType.AXP192_SWITCH_DCDC3,
    CONF_SPEAKER_ENABLE: AXP192SwitchType.AXP192_SWITCH_SPEAKER_ENABLE,
    CONF_GREEN_LED: AXP192SwitchType.AXP192_SWITCH_GREEN_LED,
    CONF_ADC_ENABLE: AXP192SwitchType.AXP192_SWITCH_ADC_ENABLE,
}

CONFIG_SCHEMA = cv.Schema({
    cv.Required(CONF_AXP192_ID): cv.use_id(AXP192Component),
    cv.Optional(CONF_MODEL): AXP192_MODEL,
    cv.Optional(CONF_LDO2): switch.switch_schema(AXP192Switch),
    cv.Optional(CONF_LDO3): switch.switch_schema(AXP192Switch),
    cv.Optional(CONF_DCDC1): switch.switch_schema(AXP192Switch),
    cv.Optional(CONF_DCDC3): switch.switch_schema(AXP192Switch),
    cv.Optional(CONF_SPEAKER_ENABLE): switch.switch_schema(AXP192Switch),
    cv.Optional(CONF_GREEN_LED): switch.switch_schema(AXP192Switch),
    cv.Optional(CONF_ADC_ENABLE): switch.switch_schema(AXP192Switch),
})


def _validate_model(config):
    if CONF_SPEAKER_ENABLE not in config and CONF_GREEN_LED not in config:
        return config

    if config.get(CONF_MODEL) != "M5CORE2":
        raise cv.Invalid(
            "speaker_enable/green_led require model: M5CORE2 in this switch block"
        )
    return config


CONFIG_SCHEMA = cv.All(CONFIG_SCHEMA, _validate_model)


def to_code(config):
    parent = yield cg.get_variable(config[CONF_AXP192_ID])

    for key, switch_type in SWITCH_TYPES.items():
        if key not in config:
            continue
        conf = config[key]
        var = yield switch.new_switch(conf)
        cg.add(var.set_parent(parent))
        cg.add(var.set_type(switch_type))
