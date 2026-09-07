# BUS_IDC — bus board, IDC ribbon variant

> **Status:** KiCad project created with a generated draft schematic (all parts placed with values and nets attached by labels, no wiring tidy-up, empty PCB). Generator: `scripts/boards.py`. Plots below appear after running the jobset.


Passive board that taps a **single continuous 18-conductor ribbon** with one
2×9 1.27 mm IDC connector per node, instead of an FPC pair. Same conductor
order as the FPC cable (v2 pinout). Sits on top of the master on the 3×10
stack field (rows A and B plus `AUX0`…`AUX3`).

## The STOP problem and its link

A continuous ribbon cannot break a line between nodes, so the chained `STOP`
signal cannot travel on it. This board therefore has a **2-pin neighbour
link**: `STOP_OUT` of node *n* goes by a short 2-wire cable to `STOP_IN` of
node *n+1* (bus README §8.10). The ribbon conductor at the `STOP` position is
left unconnected on the board (or used as an extra `GND`).

## Mapping

Identical to `BUS_FPC` for every shared line. `STOP_IN` (field pin 16) and
`STOP_OUT` (field pin 18) go to the link connector instead of the ribbon.

## Key parts

| Function | Part | Qty |
| --- | --- | :-: |
| Board header 2×9, 1.27 mm, shrouded, SMD | Samtec FTSH-109-01-L-DV-K or generic "1.27 mm 2×9 box header SMD" | 1 |
| Cable IDC socket 2×9, 1.27 mm, for 0.635 mm ribbon | Samtec FFSD-09-D or 3M 451 series (18 pos); confirm the socket can be crimped mid-ribbon | per node |
| Ribbon | 18-conductor 0.635 mm pitch (28 AWG) | — |
| STOP link | JST SH 1.0 mm 2-pin, SM02B-SRSS-TB (board) + 2-wire jumper; or a 1.27 mm 1×2 pin pair | 1 |
| Test pads | `VIN` | 1 |

Ribbon pitch (1.27 mm connector / 0.635 mm ribbon) is the choice to confirm
before ordering; a 2.54 mm variant is far larger.

## Electrical schematic
![BUS_IDC_sch](plots/BUS_IDC.svg)

## PCB layout
| top | bottom |
| --- | --- |
| ![BUS_IDC_pcb](plots/pcb_svg/BUS_IDC-Front.svg) | ![BUS_IDC_pcb](plots/pcb_svg/BUS_IDC-Back.svg) |
