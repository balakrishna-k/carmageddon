# Carmageddon - Vehicle Simulations on Carla

## Prerequisites
- Python 3.6
- Carla 0.9.2 and its dependencies
- PyTrees 0.8.3
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

## Instructions:
- First start the Carla Server. There are many ways to do this. If you have downloaded a pre-compiled version for Linux, then first navigate to the directory containing Carla files and run the following command on the terminal. 
```bash
./CarlaUE4.sh -windowed -ResX=800 -ResY=600 -carla-server  
```

- To Execute the tutorial, run the following command on the terminal.
```bash
./tutorial.py 
```
- To test out manual control, run the following command on the terminal.
```bash
./control.py 
```

- To test out in autopilot mode, run the following command on the terminal.
```bash
./control.py --autopilot
```

* View Outputs:
```
Look in the _out folder
```

## Important Modules [WIP]

* `scenario_management`
    * `scenario_definition`
    * `scenarios_manager`
* `environment`
    * `sensors`
    * `controllers`
    * `displays`
    * `worlds`
