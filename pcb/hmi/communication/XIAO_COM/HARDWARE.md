# XIAO_COM

## Overview
Mono controller in CleverHand node form factor: Seeed XIAO ESP32-S3 + ICM-42670 IMU + BQ27421 fuel gauge + WS2812 status LED, mounted directly on a submodule stack. ESP32-S3 candidate for the nRF52840 vs ESP32-S3 evaluation.

## Basic information

| Field | Value |
|-------|-------|
| **Board name** | XIAO_COM (plots still named XIAO_ADAPTER) |
| **Version** | 1.0 |
| **Status** | Prototype |
| **Created** | August 2025 |
| **Last modified** | January 2026 |
| **Designer** | adev |

## Purpose

- Run a single CleverHand node standalone (no communication module, no bus), streaming over Wi-Fi / BLE / USB.
- Compare ESP32-S3 against the nRF52840 mono controller on autonomy, link throughput and SPI performance.
- Provide an IMU and battery gauge on the controller itself.

## Interfaces

| Interface | Details |
|-----------|---------|
| Stack header J4 | 1×10 1.27 mm: AUX1, 3V3, GND, AUX3, POCI, PICO, SCLK, CSB, AREF, AUX2 |
| SPI | GPIO7 SCK / GPIO8 MISO / GPIO9 MOSI, shared by the submodule (CSB = GPIO44) and the IMU (CS = GPIO5) |
| I²C | GPIO2 SDA / GPIO3 SCL, fuel gauge only |
| LED | GPIO1 → WS2812B-2020 |
| Battery | J1 in (via gauge sense), J2 out, JP1 sense bypass |

## Compatibility

| Component | Compatible |
|-----------|------------|
| Submodules | any v2 `EMG_DAQ_*` / `IMU_*` (SPI + CSB); I²C submodules not reachable |
| Bus | none (mono only) |

## Manufacturing

- **Fabrication / assembly:** JLCPCB (`jlcpcb/`), XIAO module hand-soldered.

## Changelog

### v1.0 (August 2025)
- Initial design.
