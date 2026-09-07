# emgvib — v3 EMG + vibration node (draft)

**Status: draft, superseded as a single board.** This schematic was the first
sketch of a combined EMG + haptic node for the v3 iteration. It will not be
manufactured as one PCB. Its content is being split into a stack of separate
boards:

| Future board | Taken from this draft |
| --- | --- |
| `EMG_DAQ_ADS1292` submodule | ADS1292R front end, RLD, `TPS7A02` analog LDO, electrode ESD/clamp network, pogo contacts |
| `DRV` haptic submodule | `DRV2625` driver (I²C) and vibration output |
| new mono controller **or** new v3 communication module with an IDC bus connector | `PCA9306` I²C bridge enabled by `¬CS` (`SN74LVC1G04`), WS2812, stack field |

What stays as the reference for the v3 design:

- the **I²C bridge** scheme (`PCA9306`, `EN` driven by the inverted chip-select),
  now specified in [`docs/bus`](../../../../../docs/bus/README.md) §5.2;
- the move to a multi-row 1.27 mm **stack field** for the intra-node interface,
  now specified as the 3×10 plated field in `docs/bus/interfaces.md`. The
  header is intentionally unconnected in this draft.

The schematic is kept for reference only. No PCB layout is maintained.
