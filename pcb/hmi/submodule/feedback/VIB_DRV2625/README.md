# VIB_DRV2625 — haptic feedback submodule

> **Status:** KiCad project created with a generated draft schematic (all parts placed with values and nets attached by labels, no wiring tidy-up, empty PCB). Generator: `scripts/boards.py`. Plots below appear after running the jobset.


HMI submodule driving one LRA or ERM vibration motor with a DRV2625 (I²C,
built-in waveform library, closed-loop LRA auto-resonance). Taken from the
`emgvib` draft. `H-i2c` profile on the 3×10 stack field (all through-holes,
only the used pins populated). See
[`docs/bus/interfaces.md`](../../../../docs/bus/interfaces.md).

## Stack field positions used

| Position | Line | Use |
| :-: | --- | --- |
| A1, A3 | `GND` | ground / mechanical |
| A2, A10 | `3V3`, `VIN` | logic supply; `VIN` reserved for a higher-power variant |
| C1, C2 | `SDA_L`, `SCL_L` | node-local I²C, fixed address 0x5A |
| C7 | `AUX6` | → `NRST` (enable convention) |
| C8 | `AUX7` | → `TRIG/INTZ` (interrupt convention) |

The motor draws from `3V3` here; `VIN` (A10) is available for a variant that
needs more current. Keep the motor current path short and decoupled
(10 µF) so it does not couple into the ADC of the same node; 

## Key parts

| Function | Part | Package |
| --- | --- | --- |
| Haptic driver | DRV2625YFFR (as `emgvib`) — alternative DRV2605LYZFR (same footprint family, fixed library) | DSBGA-9 |
| Motor output | 2-pin 1.0 mm JST SH or solder pads | |
| Decoupling | 1 µF + 10 µF 0603 on VDD, 1 µF on REG | |
| Optional | TRIG/INTZ to `INT` (pin 6) for waveform trigger / interrupt | |

## Electrical schematic
![VIB_DRV2625_sch](plots/VIB_DRV2625.svg)

## PCB layout
| top | bottom |
| --- | --- |
| ![VIB_DRV2625_pcb](plots/pcb_svg/VIB_DRV2625-Front.svg) | ![VIB_DRV2625_pcb](plots/pcb_svg/VIB_DRV2625-Back.svg) |

## 3D model
[VIB_DRV2625_3D](plots/VIB_DRV2625_pcb.stl)
