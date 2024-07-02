# Initialisation Protocol (V2)
## Main Changes
## Changes from V1
The LEDs are used to indicate the internal address of the module. Here are what the LED colours indicate before settling for the final colour:
* Blue: running the main loop.
* Blinks red: adds 1 count/ received a rising edge

The colour of the LED indicates the internal address:
* Red: internal address is 1
* Orange: internal address is 2
* Yellow: internal address is 3
* Green: internal address is 4

In terms of wiring and pin selection, only the FPC cable (communication bus) was used. No extra wires are added to the PCBs.

## Pin Selection

**IO1_out (15)**:
* Read StopState from the previous module
* Allows StopState to be propagated along the chain of modules

**IO1_in (3)**:
* Pulled LOW to stop the next module counting (i.e. send StopState to the next module)
* Allows StopState to be propagated along the chain of modules

**I2C_SCL (20)**: 
* Read CLK signal from the Teensy 4.0 controller 
* Shared between all modules
* Interrupt request (IRQ) is enabled. Each rising edge read by the pin sends a signal to the controller and the interrupt routine is carried out

![alt text](pinout2.PNG)
Fig.1 Pinout

## Method
More information can be found on [hc32l110_clvhd](https://github.com/Aightech/hc32l110_clvhd.git).
