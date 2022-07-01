# CleverHand

## EMG Electrodes

Robotics prosthesis are highly sophisticated devices, which imply very expensive components to provide acceptable performances. Consequently, it is almost impossible to find effective hand prosthesis for less than tens of thousands euros. To tackle this issue, we are designing the "Clever Hand", a low-cost alternative for electromyography (EMG).

Top layer            |  Bottom layer
:-------------------------:|:-------------------------:
![Top layer](docs/clvHdTop.png) |  ![Bop layer](docs/clvHdBot.png)

![3D](docs/clvHd3D.PNG)
![Animation](docs/animation.gif)
![Schematics](docs/schematic.png)

# BOM
![placement](docs/placement.png)
Part|Value|Device|Package|Description|
:---:|:---:|:---:|:---:|:---:
1||X05C2018TZ||18p FPC connector|
2||X05C2018TZ||18p FPC connector|
ADC||ADS1293CISQ|RSG28_3P6X3P6_TEX||
C1|22pF|Capacitor|C0402||
C2|22pF|Capacitor|C0402||
C3|1nF|Capacitor|C0402||
C4|100nF|Capacitor|C0402||
C5|100nF|Capacitor|C0402||
C6|1uF|Capacitor|C0402||
L1|Green|LED0603|0603|LED|
L2|Red|LED0603|0603|LED|
L3|White|LED0603|0603|LED|
L_AND|SN74ALVC08|SN74ALVC08RGY|VQFN-14|4xAND gate|
L_NAND|SN74AUP2G00|SN74AUP2G00DCU|VSSOP|2xNAND GATE|
L_XOR|SN74LVC86|SN74LVC86ARGY|VQFN-14|4xXOR gate|
R1|51|Resistor|R0402||
R2|51|Resistor|R0402||
R3|51|Resistor|R0402||
R4|51|Resistor|R0402||
R5|10k|Resistor|R0402||
R6|1M|Resistor|R0402||
R7|10M|Resistor|R0402||
TAL|4.096MHZ|C387328|SMD-3225_4P|3.3V CMOS Crystal|
