import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.components import button

from .sensor import axp192_ns, AXP192Component

CONF_AXP192_ID = "axp192_id"
CONF_POWER_OFF = "power_off"
CONF_COULOMB_CLEAR = "coulomb_clear"

AXP192Button = axp192_ns.class_("AXP192Button", button.Button, cg.Parented.template(AXP192Component))
AXP192ButtonType = axp192_ns.enum("AXP192ButtonType")

BUTTON_TYPES = {
    CONF_POWER_OFF: AXP192ButtonType.AXP192_BUTTON_POWER_OFF,
    CONF_COULOMB_CLEAR: AXP192ButtonType.AXP192_BUTTON_COULOMB_CLEAR,
}

CONFIG_SCHEMA = cv.Schema({
    cv.Required(CONF_AXP192_ID): cv.use_id(AXP192Component),
    cv.Optional(CONF_POWER_OFF): button.button_schema(AXP192Button),
    cv.Optional(CONF_COULOMB_CLEAR): button.button_schema(AXP192Button),
})


def to_code(config):
    parent = yield cg.get_variable(config[CONF_AXP192_ID])

    for key, button_type in BUTTON_TYPES.items():
        if key not in config:
            continue
        conf = config[key]
        var = yield button.new_button(conf)
        cg.add(var.set_parent(parent))
        cg.add(var.set_type(button_type))
