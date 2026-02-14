import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.components import number

from .sensor import axp192_ns, AXP192Component

CONF_AXP192_ID = "axp192_id"
CONF_CHARGE_CURRENT_LIMIT = "charge_current_limit"

AXP192Number = axp192_ns.class_("AXP192Number", number.Number, cg.Parented.template(AXP192Component))
AXP192NumberType = axp192_ns.enum("AXP192NumberType")

CONFIG_SCHEMA = cv.Schema({
    cv.Required(CONF_AXP192_ID): cv.use_id(AXP192Component),
    cv.Optional(CONF_CHARGE_CURRENT_LIMIT): number.number_schema(AXP192Number),
})


def to_code(config):
    parent = yield cg.get_variable(config[CONF_AXP192_ID])

    if CONF_CHARGE_CURRENT_LIMIT in config:
        conf = config[CONF_CHARGE_CURRENT_LIMIT]
        var = yield number.new_number(conf, min_value=100, max_value=700, step=10)
        cg.add(var.set_parent(parent))
        cg.add(var.set_type(AXP192NumberType.AXP192_NUMBER_CHARGE_CURRENT_LIMIT))
