
# fourier-grx 

## Environment Setup

1. Install Conda environment

    Miniconda download:

    ```bash
    https://docs.anaconda.com/free/miniconda/index.html
    ```

    Miniconda install:

    ```bash
    bash ./Miniconda3-latest-Linux-x86_64.sh
    ```

2. Create Conda environment:
    > **Notice**: We should create the environment with Python 3.11 because all the libraries are compatible with this version.

    ```bash
    conda create -n grx-env python=3.11
    conda activate grx-env
    ```

3. The official `wiki-grx-deploy` Git repository can be cloned from:

    ```bash
    git clone https://gitee.com/FourierIntelligence/wiki-grx-deploy.git
    ```

4. Setting up firewall

    Enable firewall access for the server connection.

    ```bash
    sudo ufw allow 7446/udp
    ```

    The setup link for firewall for ubuntu is: *https://ubuntu.com/server/docs/firewalls*

    The correct setup of the firewall can be checked by

    ```bash
    sudo ufw status
    ```

    If all the setup is correct, you should see information like this on the terminal:

    ```txt
    To                         Action      From
    --                         ------      ----
    Anywhere                   ALLOW       224.0.0.0/24              
    7446/udp                   ALLOW       Anywhere                  
    7446/udp (v6)              ALLOW       Anywhere (v6)  
    ```

5. Installing is as easy as running the following command:

    ```bash
    python -m pip install fourier-grx
    ```

    It will intall the `fourier_grx` library along with a command line tool `grx`. You can check the installation by running the following command:

    ```bash
    grx --help
    ```


<!-- # Setting up RBDL before running the demo

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
    ``` -->


## Calibration

> [!CAUTION]
> Always make sure the `sensor_offset.json` file is filled with the correct absolute encoder values before running any code. The calibration process is crucial for the robot to work properly. Otherwise it may cause damage to the robot.
> The `grx run` command reads the `sensor_offset.json` file from the same directory where the server is started. Make sure the `sensor_offset.json` file is in the same directory as where you start the server.


The `sensor_offset.json` file contains the absolute encoder values for the robot, which is unique to each robot. Usually, the `sensor_offset.json` file should be provided with the onboard computer. If the file is not provided, the calibration process should be done manually.

Before running the calibration process, make sure the robot is in the correct position. The robot should be in the zero position, with all joints at the pin position.
After you have finished the machine's physical calibration process (moving all joints to the pin position), you can follow the following instructions to do the calibration for absolute encoder. The `grx` tool will record the absolute encoder values and store them in the `sensor_offset.json` file.

THe following instructions help you to run the server and `set_home` properly.


### Calibration for absolute encoder procedure:

First, run the `grx` server in a terminal with the sample config file. Make sure to use the correct config file for the T1 and T2 robots. We provide sample config files for the GR1T1 and GR1T2 robots. The sample code runs with *config_GR1_T1.yaml* for the GR1T1 robot.
First start a `grx` server:

```bash
grx run ./config/config_GR1_T1.yaml --urdf-path ./urdf
```

Open a second terminal, activate the environment and run:

```bash
grx calibrate
```

And it will get sensor offsets and save to `sensor_offset.json`, keep the file in the same directory you are starting the `grx` server from.

## Usage

### Running clinet(using sample config file):

irst, start a `grx` server in a terminal with sample config file (demo using T1 config file). The `grx run` command needs the path to the config file and the URDF folder. The sample code runs with *config_GR1_T1.yaml* for the GR1T1 robot and *config_GR1_T2.yaml* for the GR1T2 robot. 

```bash
grx run ./config/config_GR1_TX.yaml --urdf-path ./urdf
```

Once the server started, you can run the robot client to control the robot. A demo usage is given in the `demo_robot_client.py` script.
To run it, open a second terminal, while keeping the server running in the first terminal. In the second terminal, activate the environment and run `demo_robot_client.py`

```bash
conda activate grx-env
python demo_robot_client.py
```

When running *demo_robot_client* scripts, it will pop up a robot client panel in the command window. There are thirteen selections for the user to choose from. Type out the name and press Enter to select and use different functions:

- **Enable**: The enable function results in the motor being operable; the motor cannot move freely.

- **Disable**: The disable function results in the motor being inoperable.; the robot arm can move freely.

- **Set_Home**: This function is used during the calibration task before any work starts. It gets sensor offsets and saves them to `sensor_offset.json`. This file can be used to calibrate all the absolute encoders.

- **set_gains**: Set the PD parameters for the motors.

- **reboot**: Reboot all the motors and return them to the zero position.

- **Print_States**: Print the motor status and information.

- **Move_to_Default**: Move the joint to the default position.

- **Record**: Record the movement of the robot joint as an `.npy` file.

- **Play**: Replay the task recorded in the `record.npy` file from the "Record" function.

- **Abort**: Stop any movement that the robot is performing at the moment.

- **list_frames**: List all the links from the robot URDF.

- **get_transform**: Get the transformation matrix from one link frame to another. The options could be checked by using `List_frams` function.

- **Exit**: Exit the robot client panel.


## RL demo

> [!CAUTION] 
> When running the demo, make sure the robot is in a safe position and there is enough space around the robot. Always be ready to push the emergency stop button in case of any unexpected behavior.

We also provide a demo for the reinforcement learning waliking.

To run the demo, first start a `grx` server in a terminal with the sample config file (demo using T1 config file). The `grx run` command needs the path to the config file and the URDF folder. The sample code runs with *config_GR1_T1.yaml* for the GR1T1 robot and *config_GR1_T2.yaml* for the GR1T2 robot. 

```bash
grx run ./config/config_GR1_TX.yaml --urdf-path ./urdf
```

Wait for a few seconds for the server to start. Then open a second terminal, activate the environment and run the `demo_nohla_stand.py` script.

```bash
python demo_nohla_stand.py --act
```

After the robot is in a standing position, you can lower the robot to the ground and then run the `demo_nohla_walk.py` script to make the robot walk.

```bash
python demo_nohla_walk.py --model-dir ./data/nohla_rl_walk --act
```
