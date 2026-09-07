# BUS_FPC — bus board, FPC variant

> **Status:** KiCad project created with a generated draft schematic (all parts placed with values and nets attached by labels, no wiring tidy-up, empty PCB). Generator: `scripts/boards.py`. Plots below appear after running the jobset.


Passive board that gives a master (COM module or CTRL node) access to the bus
through two 18-way 0.5 mm FPC connectors, IN and OUT, exactly as `COM_MOD` v2
did. It sits on top of the master on the 3×10 stack field.

## Mapping

| Cable pin (v2 order) | Line | Stack field pin |
| :-: | --- | :-: |
| 1 | `AUX1` | C3 (`AUX0`) |
| 2 | `3V3` | A2 |
| 3, 19, 20 | `GND` | A1, A3, B10 |
| 4 | `AUX3` | C5 (`AUX2`) |
| 5–9 | `A0…A4` | B1–B5 |
| 10 | `POCI` | A5 |
| 11 | `PICO` | A6 |
| 12 | `SCLK` | A7 |
| 13 | `STOP` (v2 `IO1`) | IN → B8 (`STOP_IN`), OUT → B9 (`STOP_OUT`) |
| 14 | `IO2` | C6 (`AUX3`) |
| 15 | `SDA` | B6 |
| 16 | `SCL` | B7 |
| 17 | `AUX2` | C4 (`AUX1`) |
| 18 | `extRef` | A9 (`AREF`) |

`STOP` is the only line that does not pass straight through: IN goes to the
master, OUT comes back from it. The OUT connector is pin-reversed so a
same-side FFC links OUT to the next node's IN. Existing v2 controller shields
and v2 `COM_MOD` nodes share this cable pinout.

## Key parts

| Function | Part | Qty |
| --- | --- | :-: |
| FPC connector 18-way 0.5 mm, bottom contact | FPC-05F-18PH20 (as `COM_MOD`) or Omron XF2J-1824-12A (as `BUS_CONN`) | 2 |
| Test pads | `VIN`, `STOP_IN`, `STOP_OUT` | 3 |

No active parts. Optional 100 nF on `3V3` at each connector.

## Electrical schematic
![BUS_FPC_sch](plots/BUS_FPC.svg)

## PCB layout
| top | bottom |
| --- | --- |
| ![BUS_FPC_pcb](plots/pcb_svg/BUS_FPC-Front.svg) | ![BUS_FPC_pcb](plots/pcb_svg/BUS_FPC-Back.svg) |
