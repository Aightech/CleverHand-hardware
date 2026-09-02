# XIAO_ADAPTER - Seeed XIAO Adapter Board

Adapter board for using Seeed XIAO ESP32-S3 modules with AxonCtrl ADC modules. Provides a low-cost MCU option for development and testing.

## Hardware

| Component | Type | Comment |
|-----------|------|---------|
| XIAO ESP32-S3 | Module | Seeed Studio module (not included) |
| 2x13 connector | Pin header | Interface to ADC modules |

## Critical Components BOM

| Component | Part Number | Function | Datasheet |
|-----------|-------------|----------|-----------|
| MCU Module | XIAO ESP32-S3 | WiFi/BLE microcontroller module | Missing (Seeed product) |
| ADC Connector | ZX-PZ1.0-2-13PWZ | 2x13 pin header to ADC board | - |

**Note:** The XIAO ESP32-S3 module is purchased separately from Seeed Studio.

## Pin Mapping

The XIAO module pins are mapped to the 2x13 ADC connector. See the schematic for detailed routing.

## Compatibility

| ADC Module | Compatible |
|------------|------------|
| EMG8_ADS1299 | Yes |
| EMG32_RHD2132 | Yes |
| EMG64_RHD2164 | Yes |

## Electrical Schematic
![XIAO_ADAPTER_sch](plots/XIAO_ADAPTER_sch.svg)

## PCB Layout
![XIAO_ADAPTER_pcb](plots/XIAO_ADAPTER_pcb.svg)

## 3D Model

| Format | Location |
|--------|----------|
| STEP | [XIAO_ADAPTER.step](plots/XIAO_ADAPTER.step) |
| STL | [XIAO_ADAPTER.stl](plots/XIAO_ADAPTER.stl) |

## Firmware

```bash
source ~/esp/esp-idf/export.sh
cd firmware/esp-idf/axonctrl
idf.py menuconfig  # Select XIAO_ESP32S3 board + ADC module
idf.py -p /dev/ttyACM0 flash monitor
```
