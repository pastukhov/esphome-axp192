# ESPHome AXP192 Component
ESPHome AXP192 Component

This custom component it to implement support for the AXP192 for both the M5Stick-C, and the M5Stack Core2, building on top of airy10's code. 

*Update - January 2026*

**ESP-IDF Framework Support**: @makerwolf added full compatibility with the ESP-IDF framework. The component now works with both Arduino and ESP-IDF frameworks! You can use either framework type in your ESPHome configuration.

*Update - February 2026*

**Expanded PMU API**: added extended AXP192 telemetry sensors plus dedicated `switch`, `button`, and `number` platforms for PMU rail/GPIO control and charger limit management.

*Update - September 2023*

**Charging Status Sensor**: @landonr added support for battery charging state detection via a binary sensor. The component now exposes a `charging` binary sensor that indicates whether the battery is currently being charged.

*Update - 17th April 2023*  

@paulchilton has added support for the M5Tough, which requires a different register configuration for the M5Tough ILI9342C display. Other changes include a fix to stop the log being spammed with brightness values continually, these are only logged on change. Also the M5Tough needs resetting once the axp192 registers are set for the display to properly initialise so this version sets up the axp and then resets the ESP32 automatically.

## Installation

Copy the components to a custom_components directory next to your .yaml configuration file, or include directly from this repository.

## Configuration

Sample configurations are found in the `/sample-config` folder.

This component adds a new model configuration to the AXP192 sensor which determines which registers are needed for each device. Available models are `model: M5CORE2`, `model: M5STICKC` and `model: M5TOUGH`.

### Include axp192 component

```yaml
external_components:
  - source: github://martydingo/esphome-axp192
    components: [axp192]
```

### M5Stick-C

```yaml
sensor:
  - platform: axp192
    model: M5STICKC
    address: 0x34
    i2c_id: bus_a
    update_interval: 30s
    battery_level:
      name: "M5Stick Battery Level"
      id: "m5stick_batterylevel"
    charging:
      name: "M5Stick Charging"
```

### M5Stack Core2

```yaml
sensor:
  - platform: axp192
    id: pmu
    model: M5CORE2
    address: 0x34
    i2c_id: bus_a
    update_interval: 30s
    battery_level:
      name: "${upper_devicename} Battery Level"
      id: "${devicename}_batterylevel"
    battery_voltage:
      name: "${upper_devicename} Battery Voltage"
    pmu_temperature:
      name: "${upper_devicename} PMU Temperature"

binary_sensor:
  - platform: axp192
    axp192_id: pmu
    charging:
      name: "${upper_devicename} Charging"
    vbus_present:
      name: "${upper_devicename} VBUS Present"
    battery_present:
      name: "${upper_devicename} Battery Present"

switch:
  - platform: axp192
    axp192_id: pmu
    model: M5CORE2
    speaker_enable:
      name: "${upper_devicename} Speaker Enable"
    green_led:
      name: "${upper_devicename} Green LED"

button:
  - platform: axp192
    axp192_id: pmu
    coulomb_clear:
      name: "${upper_devicename} Coulomb Clear"

number:
  - platform: axp192
    axp192_id: pmu
    charge_current_limit:
      name: "${upper_devicename} Charge Current Limit"
```

### Supported Entities

- `sensor`: `battery_level`, `battery_voltage`, `battery_charge_current`, `battery_discharge_current`, `battery_power`, `vbus_voltage`, `vbus_current`, `vin_voltage`, `vin_current`, `aps_voltage`, `pmu_temperature`, `coulomb_in`, `coulomb_out`, `coulomb_delta`
- `binary_sensor`: `charging`, `vbus_present`, `battery_present`, `warning_level` (`axp192_id` required)
- `switch`: `ldo2`, `ldo3`, `dcdc1`, `dcdc3`, `speaker_enable`, `green_led`, `adc_enable`
- `button`: `power_off`, `coulomb_clear`
- `number`: `charge_current_limit`

`speaker_enable` and `green_led` are Core2-specific mappings and are only supported on `model: M5CORE2` (set this in the `switch:` block).
For backward compatibility, `charging/vbus_present/battery_present/warning_level` are also accepted under the `sensor` platform.

### Core2 PMU Mappings

- `AXP_IO1` -> `green_led`
- `AXP_LDO3` -> vibration rail (`ldo3`)
- `AXP_IO2` -> `speaker_enable`
- `AXP_LDO2` -> LCD power (`ldo2`)
- `AXP_DC3` -> LCD backlight (`brightness`)

### M5Tough

```yaml
sensor:
  - platform: axp192
    model: M5Tough
    address: 0x34
    i2c_id: bus_a
    update_interval: 30s
    battery_level:
      name: "${upper_devicename} Battery Level"
      id: "${devicename}_batterylevel"
    charging:
      name: "${upper_devicename} Charging"
```

The display component required for the M5Tough is as follows:

```yaml
display:
  - platform: ili9341
    # 320x240
    model: M5STACK
    cs_pin: GPIO5
    dc_pin: GPIO15
    lambda: |-
      it.print(160, 0, id(title_font), id(color_white), TextAlign::TOP_CENTER, "Hello World");
```
