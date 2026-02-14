#ifndef __AXP192_H__
#define __AXP192_H__

#include "esphome/core/component.h"
#include "esphome/components/sensor/sensor.h"
#include "esphome/components/binary_sensor/binary_sensor.h"
#include "esphome/components/i2c/i2c.h"
#ifdef USE_SWITCH
#include "esphome/components/switch/switch.h"
#endif
#ifdef USE_BUTTON
#include "esphome/components/button/button.h"
#endif
#ifdef USE_NUMBER
#include "esphome/components/number/number.h"
#endif

namespace esphome {
namespace axp192 {

enum AXP192Model {
  AXP192_M5STICKC = 0,
  AXP192_M5CORE2,
  AXP192_M5TOUGH,
};

enum AXP192SwitchType {
  AXP192_SWITCH_LDO2 = 0,
  AXP192_SWITCH_LDO3,
  AXP192_SWITCH_DCDC1,
  AXP192_SWITCH_DCDC3,
  AXP192_SWITCH_SPEAKER_ENABLE,
  AXP192_SWITCH_GREEN_LED,
  AXP192_SWITCH_ADC_ENABLE,
};

enum AXP192ButtonType {
  AXP192_BUTTON_POWER_OFF = 0,
  AXP192_BUTTON_COULOMB_CLEAR,
};

enum AXP192NumberType {
  AXP192_NUMBER_CHARGE_CURRENT_LIMIT = 0,
};

#define SLEEP_MSEC(us) (((uint64_t)us) * 1000L)
#define SLEEP_SEC(us)  (((uint64_t)us) * 1000000L)
#define SLEEP_MIN(us)  (((uint64_t)us) * 60L * 1000000L)
#define SLEEP_HR(us)   (((uint64_t)us) * 60L * 60L * 1000000L)

#define CURRENT_100MA  (0b0000)
#define CURRENT_190MA  (0b0001)
#define CURRENT_280MA  (0b0010)
#define CURRENT_360MA  (0b0011)
#define CURRENT_450MA  (0b0100)
#define CURRENT_550MA  (0b0101)
#define CURRENT_630MA  (0b0110)
#define CURRENT_700MA  (0b0111)

class AXP192Component : public PollingComponent, public i2c::I2CDevice {
public:
  void set_batterylevel_sensor(sensor::Sensor *batterylevel_sensor) { batterylevel_sensor_ = batterylevel_sensor; }
  void set_charging_sensor(binary_sensor::BinarySensor *charging_sensor) { charging_sensor_ = charging_sensor; }
  void set_battery_voltage_sensor(sensor::Sensor *sensor) { battery_voltage_sensor_ = sensor; }
  void set_battery_charge_current_sensor(sensor::Sensor *sensor) { battery_charge_current_sensor_ = sensor; }
  void set_battery_discharge_current_sensor(sensor::Sensor *sensor) { battery_discharge_current_sensor_ = sensor; }
  void set_battery_power_sensor(sensor::Sensor *sensor) { battery_power_sensor_ = sensor; }
  void set_vbus_voltage_sensor(sensor::Sensor *sensor) { vbus_voltage_sensor_ = sensor; }
  void set_vbus_current_sensor(sensor::Sensor *sensor) { vbus_current_sensor_ = sensor; }
  void set_vin_voltage_sensor(sensor::Sensor *sensor) { vin_voltage_sensor_ = sensor; }
  void set_vin_current_sensor(sensor::Sensor *sensor) { vin_current_sensor_ = sensor; }
  void set_aps_voltage_sensor(sensor::Sensor *sensor) { aps_voltage_sensor_ = sensor; }
  void set_pmu_temperature_sensor(sensor::Sensor *sensor) { pmu_temperature_sensor_ = sensor; }
  void set_coulomb_in_sensor(sensor::Sensor *sensor) { coulomb_in_sensor_ = sensor; }
  void set_coulomb_out_sensor(sensor::Sensor *sensor) { coulomb_out_sensor_ = sensor; }
  void set_coulomb_delta_sensor(sensor::Sensor *sensor) { coulomb_delta_sensor_ = sensor; }
  void set_vbus_present_sensor(binary_sensor::BinarySensor *sensor) { vbus_present_sensor_ = sensor; }
  void set_battery_present_sensor(binary_sensor::BinarySensor *sensor) { battery_present_sensor_ = sensor; }
  void set_warning_level_sensor(binary_sensor::BinarySensor *sensor) { warning_level_sensor_ = sensor; }
  void set_brightness(float brightness) { brightness_ = brightness; }
  void set_model(AXP192Model model) { this->model_ = model; }
  AXP192Model get_model() const { return this->model_; }
  void set_switch_state(AXP192SwitchType type, bool state);
  void press_button(AXP192ButtonType type);
  void set_number_value(AXP192NumberType type, float value);

  // ========== INTERNAL METHODS ==========
  // (In most use cases you won't need these)
  void setup() override;
  void dump_config() override;
  float get_setup_priority() const override;
  void update() override;

private:
    static std::string GetStartupReason();

protected:
    sensor::Sensor *batterylevel_sensor_{nullptr};
    binary_sensor::BinarySensor *charging_sensor_{nullptr};
    sensor::Sensor *battery_voltage_sensor_{nullptr};
    sensor::Sensor *battery_charge_current_sensor_{nullptr};
    sensor::Sensor *battery_discharge_current_sensor_{nullptr};
    sensor::Sensor *battery_power_sensor_{nullptr};
    sensor::Sensor *vbus_voltage_sensor_{nullptr};
    sensor::Sensor *vbus_current_sensor_{nullptr};
    sensor::Sensor *vin_voltage_sensor_{nullptr};
    sensor::Sensor *vin_current_sensor_{nullptr};
    sensor::Sensor *aps_voltage_sensor_{nullptr};
    sensor::Sensor *pmu_temperature_sensor_{nullptr};
    sensor::Sensor *coulomb_in_sensor_{nullptr};
    sensor::Sensor *coulomb_out_sensor_{nullptr};
    sensor::Sensor *coulomb_delta_sensor_{nullptr};
    binary_sensor::BinarySensor *vbus_present_sensor_{nullptr};
    binary_sensor::BinarySensor *battery_present_sensor_{nullptr};
    binary_sensor::BinarySensor *warning_level_sensor_{nullptr};
    float brightness_{1.0f};
    float curr_brightness_{-1.0f};
    AXP192Model model_;

    /** M5 Stick Values
     * LDO2: Display backlight
     * LDO3: Display Control
     * RTC: Don't set GPIO1 as LDO
     * DCDC1: Main rail. When not set the controller shuts down.
     * DCDC3: Use unknown
     ***********************
     * M5Stack Core2 Values
     * LDO2: ILI9342C PWR (Display)
     * LD03: Vibration Motor
     */

    void  begin(bool disableLDO2 = false, bool disableLDO3 = false, bool disableRTC = false, bool disableDCDC1 = false, bool disableDCDC3 = false);
    void  UpdateBrightness();
    bool  GetBatState();
    bool  GetChargingState();
    bool  GetVBusPresent();
    uint8_t  GetBatData();

    void  EnableCoulombcounter(void);
    void  DisableCoulombcounter(void);
    void  StopCoulombcounter(void);
    void  ClearCoulombcounter(void);
    uint32_t GetCoulombchargeData(void);
    uint32_t GetCoulombdischargeData(void);
    float GetCoulombData(void);

    uint16_t GetVbatData(void) __attribute__((deprecated));
    uint16_t GetIchargeData(void) __attribute__((deprecated));
    uint16_t GetIdischargeData(void) __attribute__((deprecated));
    uint16_t GetTempData(void) __attribute__((deprecated));
    uint32_t GetPowerbatData(void) __attribute__((deprecated));
    uint16_t GetVinData(void) __attribute__((deprecated));
    uint16_t GetIinData(void) __attribute__((deprecated));
    uint16_t GetVusbinData(void) __attribute__((deprecated));
    uint16_t GetIusbinData(void) __attribute__((deprecated));
    uint16_t GetVapsData(void) __attribute__((deprecated));
    uint8_t GetBtnPress(void);

      // -- sleep
    void SetSleep(void);
    void DeepSleep(uint64_t time_in_us = 0);
    void LightSleep(uint64_t time_in_us = 0);

    // void SetChargeVoltage( uint8_t );
    void  SetChargeCurrent( uint8_t );
    float GetBatVoltage();
    float GetBatCurrent();
    float GetVinVoltage();
    float GetVinCurrent();
    float GetVBusVoltage();
    float GetVBusCurrent();
    float GetTempInAXP192();
    float GetBatPower();
    float GetBatChargeCurrent();
    float GetAPSVoltage();
    float GetBatCoulombInput();
    float GetBatCoulombOut();
    uint8_t GetWarningLevel(void);
    void SetCoulombClear();
    void SetLDO2( bool State );
    void SetLDO3( bool State );
    void SetDCDC1(bool State);
    void SetDCDC3(bool State);
    void SetGPIO1(bool State);
    void SetGPIO2(bool State);
    void SetAdcState(bool State);

    void PowerOff();


    void Write1Byte( uint8_t Addr ,  uint8_t Data );
    uint8_t Read8bit( uint8_t Addr );
    uint16_t Read12Bit( uint8_t Addr);
    uint16_t Read13Bit( uint8_t Addr);
    uint16_t Read16bit( uint8_t Addr );
    uint32_t Read24bit( uint8_t Addr );
    uint32_t Read32bit( uint8_t Addr );
    void ReadBuff( uint8_t Addr , uint8_t Size , uint8_t *Buff );
};

#ifdef USE_SWITCH
class AXP192Switch : public switch_::Switch, public Parented<AXP192Component> {
 public:
  void set_type(AXP192SwitchType type) { this->type_ = type; }

 protected:
  void write_state(bool state) override;

  AXP192SwitchType type_;
};
#endif

#ifdef USE_BUTTON
class AXP192Button : public button::Button, public Parented<AXP192Component> {
 public:
  void set_type(AXP192ButtonType type) { this->type_ = type; }

 protected:
  void press_action() override;

  AXP192ButtonType type_;
};
#endif

#ifdef USE_NUMBER
class AXP192Number : public number::Number, public Parented<AXP192Component> {
 public:
  void set_type(AXP192NumberType type) { this->type_ = type; }

 protected:
  void control(float value) override;

  AXP192NumberType type_;
};
#endif

}
}

#endif
