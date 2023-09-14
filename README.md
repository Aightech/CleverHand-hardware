# CleverHand

![anim](docs/anim.gif)
![chain](docs/bracelet_one.png)


## EMG Electrodes

Robotics prosthesis are highly sophisticated devices, which imply very expensive components to provide acceptable performances. Consequently, it is almost impossible to find effective hand prosthesis for less than tens of thousands euros. To tackle this issue, we are designing the "Clever Hand", a low-cost modular alternative for electromyography (EMG).


## Requirememts
| **Constraint** |Status|Comment|
:---:|:---:|:---:|
|Wearable | :hammer:| Wifi feature in progress|
|>16 channels | :heavy_check_mark:| Up to 80 channels (16x5) |
|>2kHz bandwidth|:heavy_check_mark:| Up to 2.5kHz|
|>=16 bits resolution|:heavy_check_mark:| Up to 24bits|
|Bipolar/Monopolar |:heavy_check_mark:||
|Modular | :heavy_check_mark:| 1 to 16 modules by bus|
|Affordable | :heavy_check_mark:| <15€ per modules|
|Opensource |:heavy_check_mark:||

### Other features
5 on-board electrodes
Flexible ADC-elecrodes rooting
1 shared ext. electrode
1 power LED
1 alert LED
1 interface LED

## Solution

### Structure
![framework](docs/framework_con.png)

### Connection
![chain](docs/chainning.jpg)
### Structure
![mesh](docs/meshing.jpg)

### Schmatics
![Schematics](docs/schematic.png)

## Visualisation
Top layer            |  Bottom layer
:-------------------------:|:-------------------------:
![Top layer](docs/clvHdTop.png) |  ![Bop layer](docs/clvHdBot.png)

### Rendering
![3D](docs/clvHd3D.png)

### Animation
![Animation](docs/animation.gif)

## Chip select feature
![framework](docs/chipSelect.PNG)
