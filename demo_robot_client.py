import threading
import time

import numpy as np
from rich.console import Console
from rich.pretty import pprint
from rich.prompt import Confirm, Prompt
from rich.table import Table

from fourier_grx.sdk import ControlGroup, RobotClient


# Initialize console for rich logging and printing
console = Console()
log = console.log
print = console.print


FREQUENCY = 150  # Set control frequency, could set any number below 400Hz


# The enable function results in the motor being operable.
def task_enable(client: RobotClient):
    client.set_enable(True)


# The disable function results in the motor being inoperable.
def task_disable(client: RobotClient):
    client.set_enable(False)


# Set sensor offsets and save to `sensor_offset.json`
def task_set_home(client: RobotClient):
    client.set_home()


# Get PD parameter of the motor
def task_set_gains(client: RobotClient):
    kp = np.array([0.1] * 32)
    kd = np.array([0.01] * 32)

    # Set PD parameters
    new_gains = client.set_gains(kp, kd)
    print(new_gains)


# Reboot all the motor and go back to zero position
def task_reboot(client: RobotClient):
    client.reboot()


# Print out the motor status and information
def task_print_states(client: RobotClient):
    table = Table("Type", "Data", title="Current :robot: state")
    for sensor_type, sensor_data in client.states.items():
        for sensor_name, sensor_reading in sensor_data.items():
            print(sensor_type + "/" + sensor_name, sensor_reading.tolist())
            table.add_row(
                sensor_type + "/" + sensor_name,
                str(np.round(sensor_reading, 3)),
            )
    print(table)


"""
Move_joint function:
Three argument: joint position, time duration for movement, and blocking
Notice: Could access other funciton while blcoking = True
time duration will change the robot moving speed, it means the time that robot take to finish the task
"""


# Move joint to default position
def task_move_to_default(client: RobotClient):
    client.set_enable(True)
    time.sleep(0.5)
    # Move joint in the UPPER group
    client.move_joints(
        ControlGroup.UPPER,
        client.default_group_positions[ControlGroup.UPPER],
        2.0,
        blocking=False,
    )


# Similar to move_to_default, move left arm to default position
def task_move_left_arm_to_default(client: RobotClient):
    client.set_enable(True)
    time.sleep(0.5)
    # Move joint in the LEFT_ARM group
    client.move_joints(
        ControlGroup.LEFT_ARM,
        client.default_group_positions[ControlGroup.LEFT_ARM],
        2.0,
        blocking=False,
    )


# Recording the movement of the robot joint as a npy file
def record(client: RobotClient):
    """
    How to use the record function:
    1. Move to the start position and press enter to set the start position.
    2. Press enter to start recording; robot arms can move freely.
    3. Move to the final position and press enter again to finish recording.
    4. The trajectory will be stored as a npy file; use play to replay it.
    """
    traj = []
    client.set_enable(False)

    time.sleep(1)

    # Prompt user to move to start position
    reply = Prompt.ask("Move to start position and press enter")
    if reply == "":
        # Update position before enabling the motor in order to avoid the damage
        client.update_pos()
        time.sleep(0.1)
        client.set_enable(True)
        time.sleep(1)
        for sensor_type, sensor_data in client.states.items():
            for sensor_name, sensor_reading in sensor_data.items():
                if sensor_type == "joint":
                    print(sensor_type + "/" + sensor_name, sensor_reading.tolist())
    else:
        return

    # Confirm if the user wants to start recording
    time.sleep(0.5)
    reply = Confirm.ask("Start recording?")

    if not reply:
        return

    # client.update_pos()
    client.set_enable(False)
    time.sleep(1)
    event = threading.Event()
    """
    Two threads aiming to:
    1. Keep adding the joint positions to the traj list.
    2. Prompt the user to stop recording.
    """

    # inner_task used for keep recording the trjactory
    def inner_task():
        while not event.is_set():
            client.loop_manager.start()
            traj.append(client.joint_positions.copy())
            client.loop_manager.end()
            client.loop_manager.sleep()

    thread = threading.Thread(target=inner_task)
    thread.daemon = True
    thread.start()

    # Prompt user to stop recording
    reply = Prompt.ask("Press enter to stop recording")
    if reply == "":
        event.set()
        thread.join()

        # Ensure to update joint position before enbale function
        client.update_pos()
        time.sleep(0.1)
        client.set_enable(True)

        # Save recorded trajectory
        np.save("record.npy", traj)
        return traj


# Call record function
def task_record(client: RobotClient):
    traj = record(client)
    pprint(traj)


# Replay the task recorded in the record function
def play(recorded_traj: list[np.ndarray], client: RobotClient):
    """
    Move_joint function:
    Three argument: joint position, time duration for movement, and blocking
    Notice: Could access other funciton while blcoking = True
    time duration will change the robot moving speed, it means the time that robot take to finish the task
    """

    client.set_enable(True)
    time.sleep(1)

    # Move to the first position
    first = recorded_traj[0]
    client.move_joints(ControlGroup.ALL, first, 2.0, blocking=True)

    # Move along the trajectory stored in the list
    for pos in recorded_traj[1:]:
        client.move_joints(ControlGroup.ALL, pos, duration=0.0)
        time.sleep(1 / FREQUENCY)
    time.sleep(1)
    client.set_enable(False)


# Call play function
def task_play(client: RobotClient):
    # Load npy file repaly the trajectory recorded from record function
    rec = np.load("record.npy", allow_pickle=True)
    play(rec, client)


# Stop any movement that robot is doing right now
def task_abort(client: RobotClient):
    client.abort()


# List all the links from robot URDF
def task_list_frames(client: RobotClient):
    frames = client.list_frames()
    print(frames)


# Get Transformation matix from one link to another one
def task_get_transform(client: RobotClient):
    # The parameters that could be fiiled in this function is name listed out by function list_frames
    # You could put any two links to get their transformation matrix
    transform = client.get_transform("base", "l_wrist_roll")
    print(f"Transform from base to l_wrist_roll: {transform}")


# Exit the client
def task_exit(client: RobotClient):
    import sys

    client.close()
    sys.exit(0)


if __name__ == "__main__":
    client = RobotClient()
    time.sleep(0.5)
    while True:
        task = Prompt.ask(
            "What do you want the :robot: to do?",
            choices=[
                "enable",  # The enable function results in the motor being operable.
                "disable",  # The disable function results in the motor being inoperable.
                "set_home",  # Get sensor offsets and save to `sensor_offset.json`, it could be used to calibrating all the absolute encoder
                "set_gains",  # Get PD parameter of the motor
                "reboot",  # Reboot all the motor and go back to zero position
                "print_states",  # Print out the motor status and information
                "move_to_default",  # Move joint to default position
                "record",  # Recording the movement of the robot joint as a npy file
                "play",  # Replay the task recorded in the record.npy
                "abort",  # Stop any movement that robot is doing right now
                "list_frames",  # List all the links and joint from robot URDF
                "get_transform",  # Get Transformation from one link to another one
                "exit",  # Exit the client
            ],
        )
        if task == "enable":
            task_enable(client)
        elif task == "disable":
            task_disable(client)
        elif task == "set_home":
            task_set_home(client)
        elif task == "set_gains":
            task_set_gains(client)
        elif task == "reboot":
            task_reboot(client)
        elif task == "move_to_default":
            task_move_to_default(client)
        elif task == "abort":
            task_abort(client)
        elif task == "print_states":
            task_print_states(client)
        elif task == "record":
            task_record(client)
        elif task == "play":
            task_play(client)
        elif task == "exit":
            task_exit(client)
        elif task == "list_frames":
            task_list_frames(client)
        elif task == "get_transform":
            task_get_transform(client)

        time.sleep(0.5)

    # client.spin()
    # time.sleep(1)
    # client.set_enable(False)
