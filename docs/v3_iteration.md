# v3 iteration — work list

Goals of the iteration: an EMG + vibration mono node, an nRF52840 vs ESP32-S3
controller comparison, a smaller communication module with I²C bridge, and a
bus whose connector is separable from the communication logic (FPC vs IDC).
Bus-level decisions are tracked in [bus/README.md §8](bus/README.md#8-planned-changes-for-v3-decisions-and-open-points).

Every new PCB folder follows the existing layout:
`NAME.kicad_pro/.kicad_sch/.kicad_pcb`, `description.yaml`, `README.md`,
`jobs.kicad_jobset` (copy of `scripts/jobs.kicad_jobset`), `plots/` (generated),
`jlcpcb/` (production files).

## A. KiCad projects / folders to create

All new boards use the **3×10 stack field** (`docs/bus/interfaces.md`), plated
holes only, one net per position. Standard folder content: `NAME.kicad_pro/.kicad_sch/.kicad_pcb`,
`description.yaml`, `README.md`, `jobs.kicad_jobset`, `plots/`, `jlcpcb/`.

| # | Path | Kind | Contents | Blocks |
| --- | --- | --- | --- | --- |
| A0 | `pcb/config_file/templates/` + footprints in the custom library | templates & footprints | `CLVHD_STACK_3x10` (all PTH, done), `CLVHD_STACK_1x8_V2` (legacy row); template projects `HMI_15x11` and `MASTER_15x11` with outline, inserts and the field placed off-centre | everything below |
| A1 | `pcb/hmi/communication/COM_MOD_PIC` | master | PIC16F13145 (CLB 5-bit decode, `CLBSWIN` address), PCA9306 + `SN74LVC1G04`, STOP in/out, WS2812 ×1–2, ICSP pads, master field | A0 |
| A2 | `pcb/hmi/communication/COM_MOD_PAK` | master | HC32L110 + SLG46826 on a private 2-wire link, PCA9306 + inverter, STOP in/out, WS2812, SWD pads, master field | A0 |
| A3 | `pcb/hmi/communication/BUS_FPC` | bus board | two `FPC-05F-18PH20` / `XF2J-1824` (IN, OUT mirrored), **v2 cable pinout**, PTH field, `STOP_IN`/`STOP_OUT` to pins 16/18, AUX3/IO2 to test pads | A0 |
| A4 | `pcb/hmi/communication/BUS_IDC` | bus board | one 2×9 1.27 mm IDC (mid-ribbon), same conductor order, 2-pin `STOP` neighbour link header, PTH field | A0, ribbon pitch choice |
| A5 | `pcb/controller/node/CTRL_NRF52840` | master (mono + head) | MDBT50Q or Holyiot 18010, LiPo charger + BQ27421 gauge (from XIAO_COM), master field, USB-C, optional MCP4728 AREF DAC, WS2812 | A0 |
| A6 | `pcb/controller/node/CTRL_ESP32S3` | master (mono + head) | ESP32-S3FH4R2 chip-down + chip antenna (RF/power blocks from MONO_CTRL), same charger/gauge/field as A5 | A0 |
| A7 | `pcb/hmi/submodule/feedback/VIB_DRV2625` | HMI (`H-i2c`) | DRV2625 on `SDA_L`/`SCL_L`, `EN` → NRST, LRA/ERM output header, PTH field with only the pins it uses | A0 |

Status: A1–A7 folders exist with `README.md`, `description.yaml`, `jobs.kicad_jobset`,
a `.kicad_pro`, an empty `.kicad_pcb` and a **generated draft schematic** (parts, values,
nets by labels; ERC clean apart from pin-type warnings from LCSC symbols). A0 footprint
`CLVHD_STACK_3x10` (all PTH) and its symbol are in `pcb/config_file/clvhd_stack.*`
(project-local lib tables point to them). Generator: `scripts/boards.py`. Parts to source:
[`v3_parts.md`](v3_parts.md).

## B. Existing projects / files to edit

| # | Path | Change | Blocks |
| --- | --- | --- | --- |
| B1 | `pcb/hmi/submodule/sensor/EMG_DAQ_ADS1292` (in progress) | Port the `emgvib` front end (ADS1292R, RLD, TPS7A02, ESD/clamp, `electrodeFilter` sheet, pogo contacts); replace the header by the PTH field with the `H-spi` pins (row A + `DRDY#`, `START`, corners); solder jumper CS_A/CS_B; add `plots/`, `jlcpcb/`; fill `capabilities` in `description.yaml` | A0 |
| B2 | `pcb/hmi/submodule/v2/emgvib` | Move to `pcb/.archived/emgvib` once B1 and A7 exist; delete `_autosave-*` | B1, A7 |
| B3 | `pcb/hmi/communication/XIAO_COM` | Re-run jobset to rename plots from `XIAO_ADAPTER_*`; fix title block. Optional rev 1.1: replace the 1×10 header by the master field so it takes v3 HMI boards and a bus board | — |
| B4 | `pcb/hmi/communication/MONO_CTRL` | Optional rev: master field instead of single pins; otherwise README note "v2 stack only" | — |
| B5 | `pcb/hmi/communication/MONO_CTRL`, `XIAO_COM` | Optional move to `pcb/controller/node/` next to A5/A6; update `location:` and README links | — |
| B6 | `pcb/hmi/communication/COM_MOD` | README: bus v2 reference design, cable-compatible with v3 chains; no hardware change | — |
| B7 | `pcb/controller/shield/S_XIAO`, `S_PICO`, `S_TEENSY4` | README note: usable as head of a v3 chain (same cable pinout) | — |
| B8 | `pcb/tool/bridge/BUS_CONN` | Add the 2×9 IDC footprint variant next to the two FPC | A4 |
| B9 | `pcb/tool/flexBracelet` | Confirm pad set = 18-way v2 order; add the STOP break between node positions if the flex is used as the bus | — |
| B10 | v2 submodules (`EMG_DAQ_ADS1293`, `EMG_DAQ_ADS1298`, `EMG_INA331*`, `IMU_ICM2094`, `FES_AO4882`, `VIB_STSPIN240`) | **No change required** (`H-v2` profile). Optional on next spin: add row B pads for `DRDY#`/`START` | — |
| B11 | `docs/bus/README.md`, `docs/bus/interfaces.md` | Fill measured `t_sel` (§5.1); close connector choice (§8.9) after A3/A4 tests; freeze IDC ribbon pitch | A3, A4 |
| B12 | `README.md` | Catalog table: add A1, A2, A5, A6, A7, B1 | boards |
| B13 | `scripts/extractJSON.py` | Still walks `../KiCad/`; point it to `../pcb/` | — |
| B14 | `scripts/bundles.json` | Bundles: "EMG+VIB mono node" (B1 + A7 + A5 or A6), "v3 chain node" (A1 or A2 + A3 or A4 + B1) | — |
| B15 | `docs/initialisation/README.md` | Add general-call re-enumeration and `0x08 + n` client address once in firmware | C1–C3 |

## C. Outside this repository

| # | Repo | Change |
| --- | --- | --- |
| C1 | `hc32l110_clvhd` | `set_address()` writes the SLG46826 LUTs over the private link (A2); general-call re-enumeration; client address `0x08 + n`; LED chain pass-through |
| C2 | new PIC16F13145 firmware | Port of the enumeration state machine, CLB bitstream with `CLBSWIN` address, MSSP client, same register map as C1 |
| C3 | controller firmware (nRF / ESP) | Enumeration driver, select + `t_sel`, PCA9306-aware I²C access, WS2812 streaming, USB/BLE/Wi-Fi transport for the comparison |
| C4 | shared register map | One document used by C1, C2, C3 |

## Suggested order

1. **A0** footprints and templates — every board depends on the field position.
2. **B1 + A7 + A5**: the nRF EMG+VIB mono node, no bus needed.
3. **A6**: the ESP32-S3 node for the comparison.
4. **A3 + A1**: FPC bus board and COM_MOD_PIC, 3-node chain test with a v2 shield as head.
5. **A4 + A2**: IDC bus board and COM_MOD_PAK.
6. **B11–B15** documentation and catalog as boards land.
