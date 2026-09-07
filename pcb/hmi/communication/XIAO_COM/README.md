# XIAO_COM — Seeed XIAO ESP32-S3 mono controller

`XIAO_COM` is a controller board in the **node form factor**: it sits directly on
top of a CleverHand submodule stack (like `MONO_CTRL`) instead of driving a chain
through the bus. It carries a Seeed XIAO ESP32-S3 module, a 6-axis IMU, a
battery fuel gauge and a status LED. It is the ESP32-S3 candidate of the
nRF52840-versus-ESP32-S3 evaluation (autonomy, link throughput, performance).

The XIAO module itself is bought separately from Seeed Studio and soldered on
the bottom side.

## Hardware

| Component | Part | Function | Interface to the XIAO |
| --- | --- | --- | --- |
| MCU module | XIAO ESP32-S3 | Dual-core ESP32-S3, Wi-Fi + BLE, USB-C, on-module LiPo charger | — |
| IMU | ICM-42670 (LGA-14) | 3-axis accelerometer + 3-axis gyroscope | SPI shared with the stack, `CS` = GPIO5, `INT1` = GPIO6, `FSYNC` = GPIO43 |
| Fuel gauge | BQ27421-G1A (DSBGA-9) | Battery state of charge, current sense | I²C `SDA` = GPIO2, `SCL` = GPIO3 |
| Status LED | WS2812B-2020 | Single NeoPixel | Data = GPIO1 |
| Stack header `J4` | 1×10, 1.27 mm | Submodule interface (see below) | |
| Battery `J1` / `J2` | 2× 1×2, 1.27 mm | Battery in (through the gauge sense path) / battery out | |
| Jumper `JP1` | 3-pad solder jumper | Routes the battery through the fuel-gauge sense input (`SRX`, default, pads 1-2) or bypasses it (pads 2-3) | |

Board size ≈ 18 × 20 mm, 2 layers, components on both sides.

## Stack header `J4` (submodule interface)

`J4` reproduces the "bus row" of the v2 submodule stack, so the board drops onto
any `EMG_DAQ_*` / `IMU_*` submodule without a communication module.

| Pin | Signal | XIAO GPIO | Notes |
| --: | --- | --- | --- |
| 1 | `AUX1` | — | pass-through pad only |
| 2 | `3V3` | `3V3` | from the XIAO regulator |
| 3 | `GND` | `GND` | |
| 4 | `AUX3` | — | pass-through pad only |
| 5 | `POCI` | GPIO8 (MISO) | shared with the IMU `SDO` |
| 6 | `PICO` | GPIO9 (MOSI) | shared with the IMU `SDI` |
| 7 | `SCLK` | GPIO7 (SCK) | shared with the IMU `SCLK` |
| 8 | `CSB` | GPIO44 | chip-select of the submodule, active low |
| 9 | `AREF` (`extRef`) | — | pass-through pad only, no DAC on this board |
| 10 | `AUX2` | GPIO4 | spare GPIO / ADC input |

Not present on the header: the shared I²C (`SDA`/`SCL` only reach the fuel
gauge) and the ARM/SWD row. I²C-only submodules (e.g. a `DRV2625` haptic
driver) are therefore **not** reachable from this revision; the v3 stack
interface adds the local I²C segment (see [`docs/bus`](../../../../docs/bus/README.md)).

## Power

- Battery on `J1` (+, GND) is measured by the BQ27421 and delivered on `+BATT`
  (`J2`). Charging and the 3.3 V rail come from the XIAO module.
- `JP1` lets you bypass the gauge sense path for tests without the gauge.

## Bus role

Mono controller only: no bus connector, no address lines, no enumeration.
`CSB` is driven directly by GPIO44. To head a chain, use a shield
(`S_XIAO`) or the planned separable bus board.

## Electrical schematic
[XIAO_COM.pdf](plots/XIAO_COM.pdf) (schematic PDF)

## PCB layout
| top | bottom |
| --- | --- |
| ![XIAO_COM_pcb](plots/pcb_svg/XIAO_ADAPTER-Front.svg) | ![XIAO_COM_pcb](plots/pcb_svg/XIAO_ADAPTER-Back.svg) |

## 3D model
[XIAO_COM.step](plots/XIAO_COM.step) · [XIAO_COM.stl](plots/XIAO_COM.stl)

## Notes
- Plot files still carry the pre-refactor name `XIAO_ADAPTER`; regenerate with the jobset to rename them.
- The schematic title block still reads "EMG ADS1298" (copied template); update on next edit.
