![Fourier Logo](pictures/Fourier/FOURIER%20LOGO-Standard%20Colour_EN.jpg)

# Fourier-GRX

Welcome to the Fourier-GRX SDK, your gateway to controlling [Fourier](https://fourierintelligence.com/)'s humanoid robots! This guide will help you set up your environment, calibrate your humanoid robot, and run exciting demos. Let’s dive into the
future of robotics! 🤖🚀

## 💻 System Requirement

    • Operating System: Ubuntu 20.04 and up
    • Python Version: Python 3.11

**If you are first time using the robot, please set up the permission for IMU(HIPNUC IMU) and joysticks with [permission_description](permissions.md)**

### System CPU Setup

In order to have good performance of the Neural Network inference speed, it is recommended to disable the effeciency cores of the CPU.
The following steps are for Intel CPUs:

1. Enter the BIOS setup by pressing the F2 key during boot.
2. Navigate to the Advanced tab.
3. Select Processor Configuration.
4. Disable the efficiency cores by setting the number of active cores to 0.
5. Press F10 to save and exit.
6. Reboot the system.

## 🚀 Environment Setup

### Step 1: Install Conda

1. **Download and install Miniconda:**
   Follow the instructions on the [Miniconda installation guide](https://docs.conda.io/en/latest/miniconda.html).

### Step 2: Create and Activate Conda Environment

1. **Create and activate the environment:**

   > [!NOTE]
   > For now we only support Python 3.11.

    ```bash
    conda create -n grx-env python=3.11
    conda activate grx-env
    ```

   For more details, see the [Conda user guide](https://docs.conda.io/projects/conda/en/latest/user-guide/getting-started.html).

### Step 3: Clone the Repository

1. **Clone the official repo:**
    ```bash
    git clone https://gitee.com/FourierIntelligence/wiki-grx-deploy.git
    ```

### Step 4: Set Up Firewall

If you are using `ufw`, follow these steps to enable firewall access for the `grx` server to be able to automatically detect clients:

1. **Enable firewall access:**
    ```bash
    sudo ufw allow 7446/udp
    ```

2. **Check the firewall status:**
    ```bash
    sudo ufw status
    ```

### Step 5: Install `fourier-grx` Library

1. **Install the library:**
    ```bash
    python -m pip install fourier-grx
    ```

2. **Verify installation:**
    ```bash
    grx --help
    ```

## 🛠️ Calibration

> [!CAUTION]
> Ensure the `sensor_offset.json` file contains the correct absolute encoder values before running any code. Proper calibration is crucial for the robot’s operation and prevents potential damage. The grx run command reads the sensor_offset.json file
> from the directory where the server is started. Make sure this file is in the same directory when starting the server.

### Calibrate Your Humanoid Robot's Absolute Encoder

1. Physical calibration could be down with the instructions shown in [Physical_Calibration](Calibration_Procedure.md)

2. **Run the `grx` server:**
    ```bash
    grx run ./config/config_GR1_T1.yaml --urdf-path ./urdf
    ```

3. **Open a second terminal, activate the environment, and run:**
    ```bash
    conda activate grx-env
    grx calibrate
    ```

> **Notice: Ensure that all calibration tools have been removed before proceeding with other operations.**

This saves sensor offsets to `sensor_offset.json`.

## 🎛️ Usage

### Start the `grx` Server

1. **Run with the sample config file:**
    ```bash
    grx run ./config/config_GR1_T1.yaml --urdf-path ./urdf
    ```

### Run the Robot Client

1. **Open a second terminal, activate the environment, and run:**
    ```bash
    conda activate grx-env
    python demo_robot_client.py
    ```

### Robot Client Options

- **Enable:** Enable the motor.
- **Disable:** Disable the motor.
- **Set_Home:** Calibrate all absolute encoders.
- **Set_Gains:** Set PD parameters.
- **Reboot:** Reboot all motors.
- **Print_States:** Print motor status.
- **Move_to_Default:** Move to default positions.
- **Record:** Save joint movements.
- **Play:** Replay recorded tasks.
- **Abort:** Stop current movements.
- **List_Frames:** List all URDF links.
- **Get_Transform:** Get transformation matrices.
- **Exit:** Exit the client panel.

## 🤖 Reinforcement Learning (RL) Demo

> [!WARNING]
> Ensure a safe position with ample space. Be ready to push emergency stop if needed.

### Run RL Demos

1. **Start the server:**
    ```bash
    grx run ./config/config_GR1_TX.yaml --urdf-path ./urdf
    ```

2. **Run the standing demo:**
    ```bash
    python demo_nohla_stand.py --act
    ```
   Demo result:

   ![RL_Stand_result](pictures/GIF/RL_stand.gif)


3. **Run the walking demo:**

   First, you need to run `demo_nohla_stand.py` to get similar results as shown above. Then, place the robot on the ground and run the following code. Do not forget to ensure the robot is balanced before starting to walk.

    ```bash
    python demo_nohla_rl_walk.py --model-dir ./data/nohla_rl_walk --act
    ```
   Demo result:

   ![RL_Stand_result](pictures/GIF/RL_walk.gif)

Now your humanoid robot should be up and walking! 🦾🚶‍♂️

Enjoy exploring the fascinating world of humanoid robotics with `fourier-grx`! 🌍🤖✨


