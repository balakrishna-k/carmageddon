# Carmageddon - Vehicle Simulations on Carla

## Prerequisites
- Python 2.7
- Carla 0.9.1 and its dependencies
- Unreal Engine 4.19 or above 
- Ubuntu/Linux

## Installation
* First download Carla 0.9.1:
``` 
https://github.com/carla-simulator/carla/releases
```

* Clone the repo:
``` 
git clone https://github.com/balakrishna-k/carmageddon.git
```

* Instructions:
```bash
./CarlaUE4.sh -windowed -ResX=800 -ResY=600 -carla-server 
```

```bash
./tutorial.py 
```

```bash
./manual_control.py 
```

* View Outputs:
```
Look in the _out folder
```

## Project Modules
* `tutorial.py`: This is the main python script that combines our separate modules to peform High Dynamic Ranging. This python file also performs the tone mapping using rienhard tone map.
* `manual_control.py`: Obtain the gamma value to raise the brightness to the power of gamma
  