# Repository Guidelines

## Project Structure & Module Organization
- `components/axp192/` contains the custom ESPHome component:
  - `sensor.py` defines YAML schema/codegen bindings.
  - `axp192.h` and `axp192.cpp` implement PMU behavior and I2C access.
  - `__init__.py` marks the component package.
- `sample-config/` contains reference YAMLs for supported targets (`m5stickc.yaml`, `m5core2.yaml`, `m5tough.yaml`).
- `README.md` is the primary user-facing setup/configuration doc.
- `TODO.md` tracks planned feature work.

## Build, Test, and Development Commands
- `esphome config sample-config/m5core2.yaml` checks YAML/schema validity.
- `esphome compile sample-config/m5core2.yaml` builds firmware for a target config.
- Repeat validation/compile for each model before opening a PR:
  - `sample-config/m5stickc.yaml`
  - `sample-config/m5core2.yaml`
  - `sample-config/m5tough.yaml`

## Coding Style & Naming Conventions
- Python: 4-space indentation, snake_case identifiers, ESPHome constants in `UPPER_CASE` (for example `CONF_CHARGING`).
- C++: keep existing brace/spacing style in `axp192.cpp` and use clear model-specific `switch` branches.
- Preserve ESPHome naming patterns (`set_*`, `Get*`, `AXP192_*`) and keep new config keys descriptive/lowercase.
- Prefer small, focused changes; update `README.md` when YAML options or behavior change.

## Testing Guidelines
- No dedicated unit-test suite is currently committed.
- Required contribution baseline is smoke testing via `esphome config` and `esphome compile` on all sample configs.
- If adding model-specific behavior, include at least one config example that exercises it.

## Commit & Pull Request Guidelines
- Follow existing history style: concise, imperative commit subjects (for example `Add charging status sensor`, `fix comment`).
- Keep subject lines short; put details in the commit body when needed.
- PRs should include:
  - what changed and why,
  - affected model(s) (`M5STICKC`, `M5CORE2`, `M5TOUGH`),
  - local validation commands run,
  - updated docs/sample config when behavior changes.

## Security & Configuration Tips
- Do not commit Wi-Fi credentials, API keys, or OTA secrets.
- Prefer external component usage (`github://...`) or a local `custom_components` layout as described in `README.md`.

## Sub-Agent Workflow
- Use this chain for large feature work from `TODO.md`: `A0-Scout -> A1-CoreCPP -> (A2-SensorPlatform + A3-EntityPlatforms) -> A4-DocsSamples -> A5-Validator -> A6-Integrator`.
- `A0-Scout` (analysis only): map `feature -> YAML key -> C++ method -> model gate`, list blockers, and produce file-level implementation plan.
- `A1-CoreCPP` ownership: `components/axp192/axp192.h`, `components/axp192/axp192.cpp`.
- `A2-SensorPlatform` ownership: `components/axp192/sensor.py`.
- `A3-EntityPlatforms` ownership: `components/axp192/binary_sensor.py`, `components/axp192/switch.py`, `components/axp192/button.py`, `components/axp192/number.py`, optional `components/axp192/__init__.py`.
- `A4-DocsSamples` ownership: `README.md`, `sample-config/m5stickc.yaml`, `sample-config/m5core2.yaml`, `sample-config/m5tough.yaml`.
- `A5-Validator` runs smoke checks:
  - `esphome config sample-config/m5stickc.yaml`
  - `esphome config sample-config/m5core2.yaml`
  - `esphome config sample-config/m5tough.yaml`
  - `esphome compile sample-config/m5stickc.yaml`
  - `esphome compile sample-config/m5core2.yaml`
  - `esphome compile sample-config/m5tough.yaml`
- `A6-Integrator` resolves conflicts, validates backward compatibility, and prepares final PR summary.
