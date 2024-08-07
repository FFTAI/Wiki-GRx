# Process to test and add new algorithm

## Develop new algorithm based on zenoh interface (good for demos)

It is suggested to read the `demo_robot_client.py` to understand how to get state of the robot and set the control command to the robot.

The main pipeline to develop the demo based on zenoh interface (client) is as following:

```python
#################################################
# In command line
# run the grx server as previous guide
#################################################

# 1. call RobotClient to connect to the robot
client = RobotClient(FREQUENCY)

# 2. set enable to True to enable the robot
client.set_enable(True)

# 3. get the state of the robot
joint_measured_position_urdf_deg = client.states["joint"]["position"].copy()
joint_measured_velocity_urdf_deg = client.states["joint"]["velocity"].copy()


# 4. write and run your algorithm
class Algorithm:
    def __init__(self):
        self.algorithm_input = None
        self.algorithm_output = None

    def run(algorithm_input=None):
        self.algorithm_input = algorithm_input
        # algorithm calculation...
        return self.algorithm_output


algorithm = Algorithm()
ALGORITHM_OUTPUT = algorithm.run(algorithm_input=ALGORITHM_INPUT)

# 5. set the control command to the robot
client.move_joints(group=ControlGroup.ALL, positions=joint_target_position_deg)
#################################################
```

> **Notice**:
> It is suggested to write all algorithms with **class** definition,
> and provide only `def run()` interface for the exchange of algorithm input and output.
> This will make the transfer of algorithm from demo to feature more convenient.