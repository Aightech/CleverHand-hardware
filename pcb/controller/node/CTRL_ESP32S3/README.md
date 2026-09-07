# CTRL_ESP32S3 — ESP32-S3 controller node

> **Status:** KiCad project created with a generated draft schematic (all parts placed with values and nets attached by labels, no wiring tidy-up, empty PCB). Generator: `scripts/boards.py`. Plots below appear after running the jobset.


Same role and stack field as `CTRL_NRF52840`, with a chip-down ESP32-S3 for the
Wi-Fi / BLE / USB comparison. RF, antenna and power blocks follow `MONO_CTRL`
(ESP32-C3 chip-down), charger and gauge follow `XIAO_COM`. See
[`docs/bus/interfaces.md`](../../../../docs/bus/interfaces.md).

## Function

Identical block diagram to `CTRL_NRF52840` with the ESP32-S3FH4R2 in place of
the nRF module; the S3 GPIO matrix routes SPI, I²C and the `SCL`-as-clock
enumeration trick to any pin.

- **Radio**: Wi-Fi (TCP streaming of a full chain) and BLE 5; USB OTG FS.
- **Power**: Wi-Fi bursts reach 300 mA, so the LDO is a 600 mA class part and
  the battery path is sized accordingly.

## Key parts

| Function | Part | Notes |
| --- | --- | --- |
| SoC | ESP32-S3FH4R2 (4 MB flash + 2 MB PSRAM in package) | QFN-56 7×7; no external flash needed |
| Crystal | 40 MHz, 3225, ±10 ppm, 10 pF (e.g. ECS-400-10-33-CKM or X322540MSB4SI) | |
| Antenna | TDK ANT016008LCS2442MA1 chip antenna (the Johanson part of `MONO_CTRL` is out of stock) + π-match (0402 L/C, values at tuning) | keep-out per datasheet |
| LiPo charger | MCP73831T-2ACI/OT | 500 mA |
| Fuel gauge | BQ27421YZFR-G1A + 10 mΩ sense | |
| 3V3 LDO | AP2112K-3.3TRG1 (600 mA, in the library) or TLV75533PDBVR | MIC5504 is too small here |
| USB-C receptacle + ESD | 16-pin USB-C, USBLC6-2SC6 | native USB on GPIO19/20 |
| AREF DAC | MCP4728A0T-E/UN | optional |
| LED, buttons, battery connector | WS2812C-2020-V1, TS-1088R-02026 ×2 (boot, reset), JST SH 2-pin | |
| Programming | USB (native), plus TX/RX/EN/IO0 pads | |

## Electrical schematic
![CTRL_ESP32S3_sch](plots/CTRL_ESP32S3.svg)

## PCB layout
| top | bottom |
| --- | --- |
| ![CTRL_ESP32S3_pcb](plots/pcb_svg/CTRL_ESP32S3-Front.svg) | ![CTRL_ESP32S3_pcb](plots/pcb_svg/CTRL_ESP32S3-Back.svg) |

## 3D model
[CTRL_ESP32S3_3D](plots/CTRL_ESP32S3_pcb.stl)
