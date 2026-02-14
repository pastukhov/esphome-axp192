# ESPHome AXP192 Component

Custom ESPHome component for the AXP192 PMU used on `M5STICKC`, `M5CORE2`, and `M5TOUGH`.

It supports both Arduino and ESP-IDF based ESPHome builds.

## Installation

Use as an external component.

### From GitHub

```yaml
external_components:
  - source: github://pastukhov/esphome-axp192
    components: [axp192]
```

### From local checkout

```yaml
external_components:
  - source:
      type: local
      path: ../components
    components: [axp192]
```

## Basic Configuration

```yaml
sensor:
  - platform: axp192
    id: pmu
    model: M5CORE2
    address: 0x34
    i2c_id: bus_a
    update_interval: 30s
    battery_level:
      name: "Battery Level"
    battery_voltage:
      name: "Battery Voltage"

binary_sensor:
  - platform: axp192
    axp192_id: pmu
    charging:
      name: "Charging"
```

## Supported Entities

- `sensor`: `battery_level`, `battery_voltage`, `battery_charge_current`, `battery_discharge_current`, `battery_power`, `vbus_voltage`, `vbus_current`, `vin_voltage`, `vin_current`, `aps_voltage`, `pmu_temperature`, `coulomb_in`, `coulomb_out`, `coulomb_delta`
- `binary_sensor`: `charging`, `vbus_present`, `battery_present`, `warning_level`
- `switch`: `ldo2`, `ldo3`, `dcdc1`, `dcdc3`, `adc_enable`, `speaker_enable`, `green_led`
- `button`: `power_off`, `coulomb_clear`
- `number`: `charge_current_limit`

Notes:
- `binary_sensor`, `switch`, `button`, and `number` use `axp192_id` to reference the main `sensor` platform instance.
- `speaker_enable` and `green_led` are Core2-only mappings and require `model: M5CORE2` in the `switch` block.
- For backward compatibility, `charging/vbus_present/battery_present/warning_level` are also accepted under the `sensor` platform.

## Core2 PMU Mappings

- `AXP_IO1` -> `green_led`
- `AXP_IO2` -> `speaker_enable`
- `AXP_LDO2` -> LCD power (`ldo2`)
- `AXP_LDO3` -> vibration rail (`ldo3`)
- `AXP_DC3` -> LCD backlight (`brightness`)

## Sample Configs

See `sample-config/`:
- `sample-config/m5stickc.yaml`
- `sample-config/m5core2.yaml`
- `sample-config/m5tough.yaml`
- `sample-config/m5core2-hwtest.yaml` (hardware test profile)

## Validation Commands

Run before committing:

```bash
esphome config sample-config/m5stickc.yaml
esphome config sample-config/m5core2.yaml
esphome config sample-config/m5tough.yaml

esphome compile sample-config/m5stickc.yaml
esphome compile sample-config/m5core2.yaml
esphome compile sample-config/m5tough.yaml
```

## Security

Do not commit real Wi-Fi credentials, API keys, or OTA secrets.
