import time
from enum import Enum

import numpy as np
import typer
from fourier_grx.sdk import ControlGroup, ControlMode, RobotClient
from fourier_grx.sdk.gamepad_controller import GamePad
from fourier_grx.sdk.sonnie_control import SonnieControl
from ischedule import run_loop, schedule

RobotStates = Enum(
    "RobotStates",
    ["UNINITIALIZED", "ZEROED", "STAND", "PRE_WALK", "WALKING", "STOPPED"],
)


class Demo:
    def __init__(self):
        self.gamepad = GamePad()
        self.gamepad.start()

        # self.client = RobotClient(400)
        self.sonnie = SonnieControl("127.0.0.1")

        print("RobotClient initialized.")
        time.sleep(1.0)

        self.sonnie.zero()

        time.sleep(1.0)

        # self.set_gains()
        # self.client.set_enable(True)

        self.robot_state: RobotStates = RobotStates.UNINITIALIZED

        self.last_btn = None

    def set_gains(self):
        """
        Set gains for the robot
        """

        # fmt: off
        control_mode = [
            ControlMode.PD, ControlMode.PD, ControlMode.PD, ControlMode.PD, ControlMode.PD, ControlMode.PD,  # left leg
            ControlMode.PD, ControlMode.PD, ControlMode.PD, ControlMode.PD, ControlMode.PD, ControlMode.PD,  # right leg
            ControlMode.PD, ControlMode.PD, ControlMode.PD,  # waist
            ControlMode.NONE, ControlMode.NONE, ControlMode.NONE,  # head
            ControlMode.PD, ControlMode.PD, ControlMode.PD, ControlMode.PD, ControlMode.NONE, ControlMode.NONE, ControlMode.NONE,  # left arm
            ControlMode.PD, ControlMode.PD, ControlMode.PD, ControlMode.PD, ControlMode.NONE, ControlMode.NONE, ControlMode.NONE,  # right arm
        ]
        kp = np.array([
            251.625, 362.52, 200, 200, 10.98, 10.98,  # left leg
            251.625, 362.52, 200, 200, 10.98, 10.98,  # right leg
            251.625, 251.625, 251.625,  # waist
            112.06, 112.06, 112.06,  # head
            92.85, 92.85, 112.06, 112.06, 112.06, 10, 10,  # left arm
            92.85, 92.85, 112.06, 112.06, 112.06, 10, 10,  # right arm
        ])
        kd = np.array([
            14.72, 10.0833, 11, 11, 0.6, 0.6,  # left leg
            14.72, 10.0833, 11, 11, 0.6, 0.6,  # right leg
            14.72, 14.72, 14.72,  # waist
            3.1, 3.1, 3.1,  # head
            2.575, 2.575, 3.1, 3.1, 3.1, 1.0, 1.0,  # left arm
            2.575, 2.575, 3.1, 3.1, 3.1, 1.0, 1.0,  # right arm
        ])
        # fmt: on

        self.client.set_gains(kp, kd, control_mode=control_mode)

    def step(self):
        gamepad_input = self.gamepad.read()
        # print(gamepad_input)

        # print(gamepad_input["button_east"], self.last_btn)

        if (
            gamepad_input["button_east"]
            and self.last_btn != gamepad_input["button_east"]
        ):
            print(f"State: {self.robot_state}")
            match self.robot_state:
                case RobotStates.UNINITIALIZED:
                    self.sonnie.zero()
                    print("Zeroing robot")
                    self.robot_state = RobotStates.ZEROED
                case RobotStates.ZEROED:
                    self.sonnie.stand()
                    print("Standing...Please wait till the robot is stable")
                    self.robot_state = RobotStates.STAND
                case RobotStates.STAND:
                    self.sonnie.walk(0.0, 0.0, 0.0)
                    print("Walking in place...")
                    self.robot_state = RobotStates.PRE_WALK
                case RobotStates.PRE_WALK:
                    self.robot_state = RobotStates.WALKING
                case RobotStates.WALKING:
                    self.sonnie.stand()
                    self.robot_state = RobotStates.STAND
                case RobotStates.STOPPED:
                    self.robot_state = RobotStates.STAND

            print(f"New state: {self.robot_state}")

        self.last_btn = gamepad_input["button_east"]
        if gamepad_input["button_mode"]:
            self.sonnie.stop()
            self.robot_state = RobotStates.STOPPED

        if self.robot_state != RobotStates.WALKING:
            return

        max_vx = 0.5
        max_vr = 0.3

        vx = -gamepad_input["left_stick_y"] * max_vx
        vr = -gamepad_input["left_stick_x"] * max_vr

        self.sonnie.walk(vx, 0, vr)
        print(vx, vr)


def main():
    demo = Demo()

    # start the scheduler
    schedule(demo.step, interval=1 / 100)

    # run the scheduler
    run_loop()


if __name__ == "__main__":
    typer.run(main)
