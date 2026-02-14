# TODO: AXP192 Component Improvements (M5Stack Core2)

Этот план для форка `makerwolf/esphome-axp192` с целью добавить недостающий функционал PMU для Core2.

## 1. Цель

Сделать компонент `axp192` полноценным для Core2:
- наблюдаемость (напряжения/токи/мощность/температура PMU),
- управление линиями питания и GPIO PMU (LED, vibration, speaker enable),
- безопасные дефолты и совместимость с текущими конфигами.

## 2. Недостающий функционал (приоритет P0)

Сейчас доступны только:
- `battery_level`
- `brightness`

Нужно добавить:
- `sensor`:
  - `battery_voltage`
  - `battery_charge_current`
  - `battery_discharge_current`
  - `battery_power`
  - `vbus_voltage`
  - `vbus_current`
  - `vin_voltage`
  - `vin_current`
  - `aps_voltage`
  - `pmu_temperature`
  - `coulomb_in`
  - `coulomb_out`
  - `coulomb_delta` (или `coulomb_balance`)
- `binary_sensor`:
  - `charging`
  - `vbus_present`
  - `battery_present`
  - `warning_level` (если есть явная трактовка)
- `switch`:
  - `ldo2` (LCD power)
  - `ldo3` (vibration motor rail)
  - `dcdc1`
  - `dcdc3`
  - `speaker_enable` (через PMU GPIO, для Core2)
  - `green_led` (через PMU GPIO, для Core2)
  - `adc_enable` (опционально)
- `button`:
  - `power_off`
  - `coulomb_clear`
- `number`:
  - `charge_current_limit`
  - (опционально) пороги/лимиты, если API чипа позволяет

## 3. Core2-специфичные соответствия

Зафиксировать в docs/README компонента:
- `AXP_IO1 -> Green LED`
- `AXP_LDO3 -> Vibration Motor`
- `AXP_IO2 -> NS4168 SPK_EN`
- `AXP_LDO2 -> LCD Power`
- `AXP_DC3 -> LCD Backlight` (уже используется через brightness)

Важно: сделать это именно через модель `M5CORE2`, не ломая `M5STICKC` и `M5TOUGH`.

## 4. YAML API (что должно быть в итоге)

Добавить в `sensor.py`/`switch.py`/`binary_sensor.py`/`number.py` схему уровня ESPHome:
- отдельные опциональные блоки для новых сущностей;
- `restore_mode`/безопасные дефолты для `switch`;
- валидация несовместимых опций (например, если функция недоступна у выбранной модели).

Пример ожидаемого использования:

```yaml
sensor:
  - platform: axp192
    model: M5CORE2
    id: pmu
    battery_level:
      name: Battery Level
    battery_voltage:
      name: Battery Voltage
    pmu_temperature:
      name: PMU Temperature

switch:
  - platform: axp192
    axp192_id: pmu
    speaker_enable:
      name: Speaker Enable
    green_led:
      name: Green LED
```

## 5. Реализация (технические шаги)

1. Разделить код по платформам ESPHome:
   - оставить `sensor.py` для сенсоров PMU;
   - добавить новые `switch.py`, `binary_sensor.py`, `number.py`, `button.py`.
2. В `axp192.h/cpp`:
   - публичные методы для чтения телеметрии и управления rail/GPIO;
   - аккуратная обработка ошибок I2C;
   - `dump_config()` со всеми включенными каналами.
3. Добавить модельные ограничения:
   - `if model == M5CORE2` для Core2-специфичных выходов.
4. Стабилизировать `update()`:
   - не публиковать NaN/мусор,
   - ограничить частоту чтений тяжёлых каналов при необходимости.

## 6. Тесты и валидация (P0)

- Unit tests на Python-слой (config validation):
  - корректные/некорректные YAML-конфиги,
  - проверка обязательных и несовместимых полей.
- Smoke build tests:
  - минимум `M5CORE2` + `M5STICKC` конфиги проходят `esphome config`.
- Hardware test checklist (Core2):
  - читаются новые сенсоры;
  - `green_led` включается/выключается;
  - `vibration` срабатывает через `ldo3`;
  - `speaker_enable` реально влияет на звук;
  - нет boot-loop и safe mode.

## 7. Обратная совместимость (обязательно)

- Старые конфиги с `battery_level` + `brightness` должны работать без изменений.
- Дефолтное поведение питания не должно неожиданно выключать LCD/ESP.
- Все новые фичи только опциональные.

## 8. Документация (P1)

- Обновить README компонента:
  - матрица поддерживаемых фич по моделям;
  - готовые примеры YAML для Core2;
  - known limitations.
- Добавить troubleshooting:
  - типичные проблемы I2C,
  - влияние линий питания PMU на периферию.

## 9. Критерии готовности (Definition of Done)

- Все пункты P0 реализованы.
- `esphome config` проходит на примерах для Core2.
- Аппаратная проверка Core2 пройдена по чеклисту.
- Нет регрессий в существующих примерах.
- Подготовлен PR с Conventional Commit сообщениями.

## 10. Рекомендуемый порядок задач

1. Добавить sensor-телеметрию PMU.
2. Добавить switch для rail/GPIO (LED/vibration/speaker).
3. Добавить binary_sensor статусы питания/заряда.
4. Добавить button/number сущности.
5. Закрыть тесты + docs.
