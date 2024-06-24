import threading
import time

import msgpack_numpy as m
import numpy as np
import zenoh
from rich.console import Console
from rich.pretty import pprint
from rich.prompt import Confirm, Prompt
from rich.table import Table
from robot_rcs_gr.sdk import ControlGroup, RobotClient

m.patch() # Patch msgpack_numpy to handle numpy arrays

zenoh.init_logger()# Initialize zenoh logger

# Initialize console for rich logging and printing
console = Console()
log = console.log
print = console.print

# Set control frequency
FREQ = 150


def task_enable(client: RobotClient):
    client.set_enable(True)


def task_disable(client: RobotClient):
    client.set_enable(False)


def task_set_home(client: RobotClient):
    client.set_home()


def task_reboot(client: RobotClient):
    client.reboot()


def task_move_left_arm_to_default(client: RobotClient):
    client.set_enable(True)
    time.sleep(0.5)

    # Move LEFT_ARM joint to default position that predefined for each robot
    # while blocking = False: means user could not use any function before the movement done
    client.move_joints(
        ControlGroup.LEFT_ARM,
        client.default_group_positions[ControlGroup.LEFT_ARM],
        2.0,
        blocking=False,
    )


def task_move_to_default(client: RobotClient):
    client.set_enable(True)
    time.sleep(0.5)

    # Move all joints to default position that defined for each robot
    # while blocking = False: means user could not use any function before the movement done
    client.move_joints(
        ControlGroup.UPPER,
        client.default_group_positions[ControlGroup.UPPER],
        2.0,
        blocking=False,
    )


def task_abort(client: RobotClient):
    client.abort()


# Check and print out motor status and informations
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


def record(client: RobotClient):
    '''
    How to use the record function:
    1. Move to the start position and press enter to set the start position.
    2. Press enter to start recording; robot arms can move freely.
    3. Move to the final position and press enter again to finish recording.
    4. The trajectory will be stored as a npy file; use play to replay it.
    '''

    traj = []
    client.set_enable(False) # Disable the force applied to the motor so the robot can move freely
    
    time.sleep(1)

    # Prompt user to move to start position
    reply = Prompt.ask("Move to start position and press enter")
    if reply == "":
        client.update_pos() # Update position before enabling the motor
        time.sleep(0.1)
        client.set_enable(True) # Enable force applied into motor, and motor could not move freely 
        time.sleep(1)

        # Confirm if the user wants to start recording
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

    '''
    Two threads aiming to:
    1. Keep adding the joint positions to the traj list.
    2. Prompt the user to stop recording.
    '''

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


def task_record(client: RobotClient):
    traj = record(client)
    print(traj)


def play(recorded_traj: list[np.ndarray], client: RobotClient):
    '''
    Move_joint function:
    Three argument: joint position, time duration for movement, and blocking
    Notice: Could access other funciton while blcoking = True
    time duration will change the robot moving speed, it means the time that robot take to finish the task
    '''

    client.set_enable(True)
    time.sleep(1)

    # Move to the first position
    first = recorded_traj[0]
    
    client.move_joints(ControlGroup.ALL, first, 2.0, blocking=True)

    # Move along the trajectory stored in the list
    for pos in recorded_traj[1:]:
        client.move_to(pos)
        time.sleep(1 / FREQ)
    time.sleep(1)
    client.set_enable(False)


def task_play(client: RobotClient):
    # Load npy file and repaly the trajectory recorded from record function
    rec = np.load("record.npy", allow_pickle=True)
    play(rec, client)


def task_set_gains(client: RobotClient):
    kp = np.array([0.1] * 32)
    kd = np.array([0.01] * 32)

    # Set PD parameters
    new_gains = client.set_gains(kp, kd)
    print(new_gains)


def task_exit(client: RobotClient):
    import sys

    client.close()
    sys.exit(0)


if __name__ == "__main__":
    client = RobotClient(FREQ)
    time.sleep(0.5)
    while True:
        task = Prompt.ask(
            "What do you want the :robot: to do?",
            choices=[
                "enable", # Enable the force applied into motor
                "disable", # Disable the force applied into motor 
                "set_home", # Get sensor offsets and save to `sensor_offset.json`, it could be used to calibrating all the absolute encoder
                "set_gains", # Get PD parameter of the motor
                "reboot", # Reboot all the motor and go back to zero position
                "print_states", # Print out the motor status and information
                "move_to_default", # Move joint to default position
                "record", # Recording the movement of the robot joint as a npy file
                "play", # Replay the task recorded in the record.npy
                "abort", # Stop any movement that robot is doing right now
                "exit", # Exit the robot client control
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

        time.sleep(0.5)

    # client.spin()
    # time.sleep(1)
    # client.set_enable(False)

