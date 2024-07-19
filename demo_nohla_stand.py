import time

import numpy as np
import typer
from fourier_grx.sdk.algorithm import FourierGR1NohlaStandControlModel
from fourier_grx.sdk import ControlGroup, ControlMode, RobotClient
from ischedule import run_loop, schedule


class DemoNohlaStand:
    """
    Reinforcement Learning Walker
    """

    def __init__(self, comm_freq=400, step_freq=100, act=False):
        """
        Initialize the RL Walker

        Input:
        - comm_freq: communication frequency, in Hz
        - step_freq: step frequency, in Hz
        """

        # setup RobotClient
        self.client = RobotClient(comm_freq)
        self.act = act
        time.sleep(1.0)

        self.set_gains()
        self.client.set_enable(True)

        # algorithm
        algorithm_control_period = 1.0 / step_freq
        self.algorithm_nohla_stand_control_model = FourierGR1NohlaStandControlModel(dt=algorithm_control_period)

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
        """
        Step function for the RL Walker

        Input:
        - act: whether to actuate the robot or not
        """

        # get states
        joint_measured_position_urdf_deg = self.client.states["joint"]["position"].copy()
        joint_measured_velocity_urdf_deg = self.client.states["joint"]["velocity"].copy()

        controlled_joints = self.algorithm_nohla_stand_control_model.index_of_joints_real_robot

        # prepare input
        joint_measured_position_nohla_urdf = np.zeros(len(controlled_joints))
        joint_measured_velocity_nohla_urdf = np.zeros(len(controlled_joints))

        joint_measured_position_nohla_urdf = np.deg2rad(joint_measured_position_urdf_deg)[controlled_joints]
        joint_measured_velocity_nohla_urdf = np.deg2rad(joint_measured_velocity_urdf_deg)[controlled_joints]

        # run algorithm
        _, _, joint_target_position_nohla_urdf = self.algorithm_nohla_stand_control_model.run(
            joint_measured_position_urdf=joint_measured_position_nohla_urdf,
            joint_measured_velocity_urdf=joint_measured_velocity_nohla_urdf,
        )  # [rad]

        joint_target_position_nohla_urdf_deg = np.rad2deg(joint_target_position_nohla_urdf)
        joint_target_position_deg = np.zeros_like(joint_measured_position_urdf_deg)
        joint_target_position_deg[controlled_joints] = joint_target_position_nohla_urdf_deg

        if self.act:
            self.client.move_joints(ControlGroup.ALL, joint_target_position_deg, 0.0)

        return joint_target_position_deg


def main(comm_freq: int = 400, step_freq: int = 100, act: bool = False):
    walker = DemoNohlaStand(comm_freq=comm_freq, step_freq=step_freq, act=act)

    # start the scheduler
    schedule(walker.step, interval=1 / step_freq)

    # run the scheduler
    run_loop()


if __name__ == "__main__":
    typer.run(main)
