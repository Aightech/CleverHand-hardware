# v3 iteration — parts to source

Manufacturer part numbers to search on LCSC / JLCPCB. Parts marked *(lib)* are
already in the project libraries (`00_lcsc`, `00_custom`) from earlier boards.
Passives (0402 100 nF / 1 µF / 10 µF, 10 kΩ, 4.7 kΩ, 200 kΩ, 5.1 kΩ) are not
listed. Quantities are per board.

## Common to every new board

| Function | Part | Package | Notes |
| --- | --- | --- | --- |
| Stack field pins | 1.27 mm pin header strips, THT, to cut single pins (e.g. PZ127V-11-40P or any 1.27 mm 1×40 THT header) | — | 12–20 pins per joint; 0.4 mm square pins |
| Status LED | WS2812C-2020-V1 *(lib)* | 2.0×2.0 | masters only |
| Button | TS-1088R-02026 *(lib)* | SMD 3.9×3.0 | masters only |

## A1 COM_MOD_PIC

| Function | Part | Package | Qty |
| --- | --- | --- | :-: |
| MCU with CLB | PIC16F13145-I/REB (20-VQFN 3×3) | VQFN-20 0.4 mm | 1 |
| I²C bus switch | PCA9306YZTR *(lib, emgvib)* — or PCA9306DCUR (VSSOP-8) if BGA assembly is a concern | DSBGA-8 / VSSOP-8 | 1 |
| Inverter (CSB → EN) | SN74LVC1G04DSFR *(lib, emgvib)* | SON-6 | 1 |
| Schottky for `DRDY#` → `AUX0` wired-OR (optional) | BAT54SWFILM *(lib)* or 1N5819-class SOD-323 | SOD-323 | 1 |
| Programming footprint | Tag-Connect TC2030-NL pads (no part) | — | — |

Dev board for the bench: Microchip **EV06M52A** (PIC16F13145 Curiosity Nano).

## A2 COM_MOD_PAK

| Function | Part | Package | Qty |
| --- | --- | --- | :-: |
| MCU | HC32L110C6UA *(lib, COM_MOD)* | QFN-20 3×3 0.4 mm | 1 |
| GreenPAK decoder | SLG46826V | STQFN-20 2×3 0.4 mm | 1 |
| I²C bus switch | PCA9306YZTR / PCA9306DCUR | — | 1 |
| Inverter | SN74LVC1G04DSFR | SON-6 | 1 |
| Schottky (optional) | BAT54SWFILM | SOD-323 | 1 |

Dev board for the bench: Renesas **SLG4DVKADV** (GreenPAK advanced development
platform) with an SLG46826 socket adapter.

## A3 BUS_FPC

| Function | Part | Qty |
| --- | --- | :-: |
| FPC 18-way 0.5 mm bottom-contact | FPC-05F-18PH20 *(lib, COM_MOD)* or Omron XF2J-1824-12A *(lib, BUS_CONN)* | 2 |
| FFC cable 18-way 0.5 mm, same-side contacts | length per node spacing (e.g. 30–50 mm) | per node |

## A4 BUS_IDC

| Function | Part | Qty |
| --- | --- | :-: |
| Board header 2×9 1.27 mm shrouded SMD | Samtec FTSH-109-01-L-DV-K, or generic "1.27 mm 2×9 SMD box header" | 1 |
| Cable IDC socket 2×9 1.27 mm | Samtec FFSD-09-D or 3M 451 series 18-pos; **verify** mid-ribbon crimping | per node |
| Ribbon cable | 18-conductor, 0.635 mm pitch, 28 AWG | — |
| STOP link connector | JST SM02B-SRSS-TB (SH 1.0 mm, 2-pin, side entry) + SHR-02V-S housings and pre-crimped wires | 1 + cable |

## A5 CTRL_NRF52840

| Function | Part | Package | Qty |
| --- | --- | --- | :-: |
| BLE module | Raytac MDBT50Q-1MV2 (nRF52840, 1 MB, chip antenna) — alt. Holyiot 18010 | 10.5 × 15.5 mm | 1 |
| LiPo charger | MCP73831T-2ACI/OT *(lib, MONO_CTRL)* | SOT-23-5 | 1 |
| Fuel gauge | BQ27421YZFR-G1A *(lib, XIAO_COM)* | DSBGA-9 | 1 |
| Sense resistor | 10 mΩ 1 % 0805 | 0805 | 1 |
| 3V3 LDO | MIC5504-3.3YM5 *(lib, MONO_CTRL)* | SOT-23-5 | 1 |
| USB-C receptacle | HRO TYPE-C-31-M-12 (16-pin, USB 2.0) or equivalent | SMD + THT posts | 1 |
| USB ESD | USBLC6-2SC6 | SOT-23-6 | 1 |
| AREF DAC (optional) | MCP4728A0T-E/UN *(lib, shields)* | MSOP-10 | 1 |
| Battery connector | JST SM02B-SRSS-TB (SH) or S2B-PH-SM4-TB (PH) | — | 1 |
| Power switch (optional) | slide switch as `MONO_CTRL` *(lib, 00_custom:switch)* | — | 1 |

## A6 CTRL_ESP32S3

| Function | Part | Package | Qty |
| --- | --- | --- | :-: |
| SoC | ESP32-S3FH4R2 | QFN-56 7×7 | 1 |
| Crystal 40 MHz | 3225, ±10 ppm, CL 10 pF (e.g. ECS-400-10-33-CKM, or LCSC "X322540MSB4SI") | 3225 | 1 |
| Chip antenna | Johanson 2450AT18B100 *(lib, MONO_CTRL Antenna_Chip)* | 3.2×1.6 | 1 |
| π-match | 0402 inductor + 2 capacitors per Espressif reference | 0402 | 3 |
| LiPo charger | MCP73831T-2ACI/OT | SOT-23-5 | 1 |
| Fuel gauge + sense | BQ27421YZFR-G1A + 10 mΩ 0805 | — | 1 |
| 3V3 LDO ≥ 600 mA | AP2112K-3.3TRG1 *(lib, EMG_DAQ_ADS1293)* or TLV75533PDBVR | SOT-23-5 | 1 |
| USB-C receptacle + ESD | HRO TYPE-C-31-M-12 + USBLC6-2SC6 | — | 1 + 1 |
| AREF DAC (optional) | MCP4728A0T-E/UN | MSOP-10 | 1 |
| Battery connector | JST SH / PH 2-pin | — | 1 |

## A7 VIB_DRV2625

| Function | Part | Package | Qty |
| --- | --- | --- | :-: |
| Haptic driver | DRV2625YFFR *(lib, emgvib)* — alt. DRV2605LYZFR | DSBGA-9 | 1 |
| Motor connector | JST SM02B-SRSS-TB or solder pads | — | 1 |
| Motor for tests | LRA (e.g. Jinlong G0825001 / Vybronics VG0825001D) or 8 mm coin ERM | — | 1 |

## B1 EMG_DAQ_ADS1292 (already in the emgvib draft)

ADS1292RIRSMR, TPS7A0230PDQNR, BAT54SWFILM ×4, PGB1010402KR ×4, pogo contacts
YZP0120-16020-01 / YZP0664-20036-01, 1.27 mm field pins.

## Bench / development boards

| Board | For |
| --- | --- |
| Microchip EV06M52A (PIC16F13145 Curiosity Nano) | A1 decode timing, firmware port |
| Renesas GreenPAK dev kit + SLG46826 adapter | A2 LUT config, decode timing |
| Raytac MDBT50Q-DB-40 or nRF52840-DK | A5 firmware before the board exists |
| ESP32-S3-DevKitC-1 | A6 firmware |

---

## LCSC codes, stock and price

Queried through the JLCPCB parts catalog on 2026-09-05. Stock = JLCPCB SMT
warehouse (LCSC retail stock can be higher); price = USD per unit at 10 pcs.
"Assembly" = fine for JLC SMT; all are "extended" parts.

### MCUs, logic, radio

| Part | LCSC | Stock | $ @10 | Note |
| --- | --- | --: | --: | --- |
| PIC16F13145T-I/REB (VQFN-20 3×3) | **C26081950** | 12 | 2.09 | low stock: pre-order or buy from LCSC retail |
| PIC16F13145-I/SS (SSOP-20) | C23848320 | 211 | 1.64 | same silicon, bigger package; fallback for a first prototype |
| SLG46826V (STQFN-20 2×3) | **C5334557** | 59 | 2.15 | enough for a prototype run |
| SLG46826G (TSSOP-20) | C3281959 | 85 | 2.65 | larger fallback |
| HC32L110C6UA-SFN20TR (QFN-20 3×3) | **C493490** | 2905 | 0.59 | as `COM_MOD`, used on COM_MOD_PAK |
| HC32L110B6YA-CSP16TR (CSP-16, 0.35 mm pitch) | C840729 | 4718 | 0.60 | rejected: inner balls not routable within JLC trace/via rules |
| PCA9306DQER (X2SON-8, 1.4 × 0.8 mm) | **C440032** | 21682 | 0.52 | smallest package, used on the COM modules |
| PCA9306DCUR (VSSOP-8) | C33196 | 4047 | 0.55 | easier to hand-solder |
| PCA9306DCTR (VSSOP-8) | C123752 | 11660 | 0.42 | same die, cheaper |
| PCA9306YZTR (DSBGA-8) | C414602 | 244 | 0.48 | as `emgvib` |
| SN74LVC1G04DPWR (X2SON-4, 0.8 × 0.8 mm) | **C2872975** | 193 | 0.29 | smallest package, used on the COM modules |
| SN74LVC1G04DSFR (SON-6 1×1) | C2872331 | 293 | 0.11 | TI |
| SN74LVC1G04DSFR (UMW clone) | C42165060 | 7504 | 0.06 | |
| nRF52840 module: Ebyte E73-2G4M08S1C (18×13 mm, PCB antenna) | **C356849** | 2051 | 7.29 | the only nRF52840 module in stock; 18 mm long → node grows to ~18 × 13 |
| Raytac MDBT50Q-1MV2 | C5118826 | 0 | 18.44 | out of stock at JLC; check LCSC retail / Raytac |
| nRF52840-QIAA-R (bare, aQFN-73) | C190794 | 51278 | 5.19 | chip-down: needs RF layout + certification |
| ESP32-S3FH4R2 (QFN-56, 4 MB flash + 2 MB PSRAM) | **C3013940** | 2867 | 3.03 | |
| ESP32-S3FN8 (8 MB flash, no PSRAM) | C2913196 | 3127 | 2.98 | alternative |

### Power, USB, gauge

| Part | LCSC | Stock | $ @10 | Note |
| --- | --- | --: | --: | --- |
| MCP73831T-2ACI/OT | **C424093** | 7292 | 0.66 | |
| BQ27421YZFR-G1A | **C139621** | 884 | 1.79 | |
| 10 mΩ 1 % 0805 (Milliohm HoJLR0805-1/2W) | **C41427589** | 6082 | 0.04 | gauge sense |
| MIC5504-3.3YM5-TR (300 mA) | **C88419** | 45328 | 0.25 | nRF board |
| AP2112K-3.3TRG1 (600 mA) | **C51118** | 63214 | 0.17 | ESP32-S3 board (in library) |
| TLV75533PDBVR (500 mA) | C404027 | 61610 | 0.16 | alternative |
| TYPE-C-31-M-12 (HRO, 16-pin) | **C165948** | 296798 | 0.19 | |
| USBLC6-2SC6 (ST) | **C7519** | 48462 | 0.18 | UMW clone C2687116 at 0.05 |
| MCP4728A0T-E/UN | C627341 | 88 | 2.36 | optional AREF DAC |
| JST SM02B-SRSS-TB(LF)(SN) | **C160402** | 82612 | 0.13 | battery / STOP link / motor |
| JST S2B-PH-SM4-TB(LF)(SN) | C295747 | 28961 | 0.24 | PH 2.0 mm battery alternative |

### RF passives (ESP32-S3 board)

| Part | LCSC | Stock | $ @10 | Note |
| --- | --- | --: | --: | --- |
| 40 MHz 3225 12 pF ±10 ppm (Changjing) | **C47089401** | 1123 | 0.11 | |
| 40 MHz 3225 (HELE X3S040000FA1H) | C254336 | 2602 | 0.15 | check CL vs Espressif reference (10 pF) |
| TDK ANT016008LCS2442MA1 (1.6×0.8 chip antenna) | **C76585** | 2655 | 0.25 | Johanson 2450AT18B100E (C2917717) is out of stock; TDK needs its own matching/keep-out |

### Haptics, ADC

| Part | LCSC | Stock | $ @10 | Note |
| --- | --- | --: | --: | --- |
| DRV2625YFFR (DSBGA-9) | **C553134** | 158 | 0.93 | |
| DRV2605LYZFR (DSBGA-9) | C2869341 | 86 | 1.28 | |
| DRV2605LDGSR (VSSOP-10) | C527464 | 1935 | 1.14 | easiest package if BGA is a concern |
| ADS1292RIRSMR | **C456281** | 91 | 9.04 | order early, low stock |
| TPS7A0230PDQNR | **C2867950** | 439 | 0.65 | |

### Connectors, headers, indicators

| Part | LCSC | Stock | $ @10 | Note |
| --- | --- | --: | --: | --- |
| FPC-05F-18PH20 (XUNPU, 18-way 0.5 mm) | **C2856802** | 13838 | 0.12 | BUS_FPC ×2 |
| Omron XF2J-1824-12A | C3169378 | 0 | 3.81 | out of stock |
| PZ127V-12-20-H25 (2×10 1.27 mm THT header) | **C51889474** | 490 | 0.10 | rows A+B of the 3×10 field; add a 1×10 strip for row C, or cut single pins |
| PZ127V-11-0x-H25 (1×4/5/6 1.27 mm THT strips) | C962328 / C962329 / C2832273 | 4237 / 2310 / 8957 | 0.04 | loose pins |
| BXCONN A127US-WS18P (2×9 1.27 mm shrouded, SMD) | **C41366809** | 27 | 0.25 | BUS_IDC board header |
| BXCONN A127UP-ZD18P (2×9 1.27 mm shrouded, THT) | C41366773 | 65 | 0.10 | |
| XUNPU PH1.27-01-18PZD (2×9 1.27 mm shrouded, THT) | C41360853 | 335 | 0.18 | |
| Yxcon IDC3-xx232 (1.27 mm IDC ribbon sockets) | C49073964 (10P) … C49232616 (24P) | 100–800 | 0.35–0.48 | 18/20-position variant to look up on LCSC (`IDC3-18232` / `IDC3-20232`); verify mid-ribbon crimping |
| Samtec FTSH-109 / FFSD-09 | C5707818 / C18161750 | 0 | 6–13 | out of stock and expensive: skip |
| WS2812C-2020-V1 | **C2976072** | 54427 | 0.10 | |
| TS-1088R-02026 | **C455280** | 190808 | 0.06 | |
| BAT54SWT1G (onsemi) | **C78260** | 39598 | 0.03 | wired-OR diode |

### Sourcing notes

- **nRF52840 board**: the Raytac module is unavailable at JLC. The Ebyte
  E73-2G4M08S1C is in stock and cheap but 18 × 13 mm, so CTRL_NRF52840 becomes
  an 18 × 13 mm board (still fine on a bracelet). If the 15 × 11 outline
  matters more, buy MDBT50Q-1MV2 from LCSC retail or Raytac directly.
- **PIC16F13145 VQFN** has 12 pieces at JLC: order them now, or use the
  SSOP-20 for the first COM_MOD_PIC spin.
- **Chip antenna**: the Johanson part used on MONO_CTRL is out of stock; the
  TDK ANT016008 needs a different footprint and matching.
- **IDC ribbon sockets** are the one item to confirm before committing to
  BUS_IDC: look for 18- or 20-position Yxcon IDC3 sockets on LCSC and check
  the datasheet allows the cable to pass through (mid-ribbon), not only end
  termination.
