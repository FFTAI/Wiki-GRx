
# Setting up the environment

1. Install Conda environment

    Miniconda download:
    ```
    https://docs.anaconda.com/free/miniconda/index.html
    ```

    Miniconda install:
    ```
    bash ./Miniconda3-latest-Linux-x86_64.sh
    ```

2. Create Conda environment:
    > **Notice**: We should create the environment with Python 3.11 because all the libraries are compatible with this version.
    ```
    conda create -n wiki-grx-deploy python=3.11
    conda activate wiki-grx-deploy
    ```

3. The official `wiki-grx-deploy` Git repository can be cloned from:
    ```
    git clone https://gitee.com/FourierIntelligence/wiki-grx-deploy.git
    ```

4. Install neccessary environment:
    > **Notice**: We should download the .whl file before installing it. The .whl files must be installed sequentially.
    ```
    python -m pip install robot_rcs-0.4.0.9-cp311-cp311-manylinux_2_30_x86_64.whl
    python -m pip install robot_rcs_gr-1.9.1.7-cp311-cp311-manylinux_2_30_x86_64.whl
    ```


# Setting up RBDL before running the demo

1. The official RBDL building and installation instructions can be found at:
    > **Notice**: Clone RBDL repository is optional
    ```
    https://github.com/rbdl/rbdl
    ```

2. The RBDL repository can be cloned from:
    ```
    git clone https://github.com/rbdl/rbdl.git
    ```

3. Install CMake:
    ```
    sudo apt install cmake
    ```

4. Install RBDL with CMake:
    ```
    mkdir rbdl && cd rbdl
    mkdir build && cd build
    cmake -D CMAKE_BUILD_TYPE=Release ..
    make
    sudo make install
    echo "export LD_LIBRARY_PATH=/usr/local/lib:$LD_LIBRARY_PATH" >> ~/.bashrc
    source ~/.bashrc
    ```


# Demo
## Calibration
The first step to run the demo code, is to make sure the sensor_offset.json is filled with your machine absolute encoder value, instead of the value in this repository (may be different from your machine).

Every machine has its own home position encoder value, which should be set with the machine power on and the joint fixed at the pin position.

After you have finished the machine's physical calibration process (moving all joints to the pin position), you can run the client code and call the **set_home** function in this repository. The **set_home** function will record the absolute encoder values and store them in the `sensor_offset.json` file.

THe following instructions help you to run the client properly.


### Running clinet(using sample config file):
First, run *run_server.py* in a terminal with sample config file
```
python run_server.py ./config/config_GR1_T1.yaml
```
Open second terminal, activate the environment and run robot_client
```
python demo_robot_client.py
```   

After client has been poped out, type **set_home** to use set_home function, and it will get sensor offsets and save to `sensor_offset.json`, the file could be used to calibrating the robot. 

## Robot Client
### Running clinet(using sample config file):
First, run *run_server.py* in a terminal with sample config file
```
python run_server.py ./config/config_GR1_T1.yaml
```
Open second terminal, activate the environment and run robot_client
```
python demo_robot_client.py
``` 

### Function Explanation(robot server)
When running the `run_server` script, you can modify and use several options. These options can be specified using the following parameters:

- **config**: Path to the config file.
- **freq**: Main loop frequency in Hz, defualt=500.
- **debug_interval**: Debug loop print interval, default=0.
- **verbose**: Flag to print internal debug info, default=True.
- **visualize**: Flag to visualize the robot in RViz, default=True.

**Sample usage**

```
python run_server.py path/to/config/file --freq 500 --debug_interval 0 --verbose True --visualize True
```
    
### Function Explanation(robot_Clinet)
When running *demo_robot_client* scripts, it will pop up a robot client panel in the command window. There are thirteen selections for the user to choose from. Type out the name and press Enter to select and use different functions:

- **Enable**: Enable the force applied to the motor; the motor cannot move freely.

- **Disable**: Disable the force applied to the motor; the robot arm can move freely.

- **Set_Home**: This function is used during the calibration task before any work starts. It gets sensor offsets and saves them to `sensor_offset.json`. This file can be used to calibrate all the absolute encoders.

- **set_gains**: Set the PD parameters for the motors.

- **reboot**: Reboot all the motors and return them to the zero position.

- **Print_States**: Print the motor status and information.

- **Move_to_Default**: Move the joint to the default position.

- **Record**: Record the movement of the robot joint as an `.npy` file.

- **Play**: Replay the task recorded in the `record.npy` file from the "Record" function.

- **Abort**: Stop any movement that the robot is performing at the moment.

- **list_frames**: List all the links and joints from the robot URDF.

- **get_transform**: Get the transformation from one link to another.

- **Exit**: Exit the robot client panel.


### Detailed explanation
1. Import and setup:
    - The script begins by importing necessary modules: Threading, msgpack_numpy, zenoh, numpy, time, rich, typer, and specific versions of robot_rcs and robot_rcs_gr.
2. Control System Initialization:
    - The RobotClient system is imported and initialized, serving as the main client panel for controlling the robot.
    - The control system has been initialized with a frequency of 150Hz..
3. Main control loop:
    - In the main control loop, the robot client panel will prompt the user to type out the function name they want to use. For example, when the client asks: "What do you want the robot to do?", simply type "set_home" to use the set_home function. This is also mentioned in the calibration task, and the goal of each function in the robot client has been listed in the client function explanation part.
    - In the main control loop, the client will keep asking for input until the user exits the client.



