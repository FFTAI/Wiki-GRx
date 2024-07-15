from pathlib import Path
import time

import numpy as np
import typer
from fourier_grx.sdk import ControlGroup, ControlMode, RobotClient
from fourier_grx.sdk.algorithm_rl import FourierGR1NohlaRLWalkControl
from ischedule import run_loop, schedule


class DemoNohlaRLWalk:
    """
    Reinforcement Learning Walker
    """

    def __init__(self, comm_freq: int = 400, step_freq: int = 100, model_dir: Path | str | None = None, act: bool = False):
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

        # default position
        # fmt: off
        self.default_position = np.array(
            [
                0.0, 0.0, -0.5236, 1.0472, -0.5236, 0.0,  # left leg (6)
                0.0, 0.0, -0.5236, 1.0472, -0.5236, 0.0,  # right leg (6)
                0.0, 0.0, 0.0,  # waist (3)
                0.0, 0.0, 0.0,  # head (3)
                0.0, 0.3, 0.0, -0.3, 0.0, 0.0, 0.0,  # left arm (7)
                0.0, -0.3, 0.0, -0.3, 0.0, 0.0, 0.0,  # right arm (7)
            ]
        )  # unit : rad
        # fmt: on

        # algorithm
        algorithm_control_period = 1.0 / step_freq
        if model_dir is not None:
            self.model = FourierGR1NohlaRLWalkControl(
                dt=algorithm_control_period,
                decimation=int((1 / 100) / algorithm_control_period),
                warmup_period=1.0,
                actor_model_file_path=model_dir + "/actor.pt",
                encoder_model_file_path=model_dir + "/encoder.pt",
            )
        else:
            self.model = FourierGR1NohlaRLWalkControl(
                dt=algorithm_control_period, decimation=int((1 / 100) / algorithm_control_period), warmup_period=1.0
            )

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

    def step(self, commands: np.ndarray | None = None):
        """
        Step function for the RL Walker

        Input:
        - act: whether to actuate the robot or not
        """

        # get states
        imu_quat = self.client.states["imu"]["quat"].copy()
        imu_angular_velocity_deg = self.client.states["imu"]["angular_velocity"].copy()  # unit : deg/s
        joint_measured_position_urdf_deg = self.client.states["joint"]["position"].copy()  # unit : deg
        joint_measured_velocity_urdf_deg = self.client.states["joint"]["velocity"].copy()  # unit : deg/s

        # prepare input
        if commands is None:
            commands = np.zeros(3)
        base_measured_quat_to_world = imu_quat
        base_measured_rpy_vel_to_self = np.deg2rad(imu_angular_velocity_deg)

        # extract model constants
        controlled_joints = self.model.index_of_joints_real_robot
        init_output = self.model.joint_default_position
        self.model.gait_phase_ratio = self.model.gait_phase_ratio_walk

        joint_measured_position_nohla_urdf = np.zeros(len(controlled_joints))
        joint_measured_velocity_nohla_urdf = np.zeros(len(controlled_joints))

        # joint: real robot urdf -> algorithm urdf
        joint_measured_position_nohla_urdf = np.deg2rad(joint_measured_position_urdf_deg)[controlled_joints]
        joint_measured_velocity_nohla_urdf = np.deg2rad(joint_measured_velocity_urdf_deg)[controlled_joints]

        # run algorithm
        joint_target_position_nohla_urdf_rad = self.model.run(
            init_output=init_output,
            commands=commands,
            base_measured_quat_to_world=base_measured_quat_to_world,
            base_measured_rpy_vel_to_self=base_measured_rpy_vel_to_self,
            joint_measured_position_urdf=joint_measured_position_nohla_urdf,
            joint_measured_velocity_urdf=joint_measured_velocity_nohla_urdf,
        )  # unit : rad

        joint_target_position_nohla_urdf_deg = np.rad2deg(joint_target_position_nohla_urdf_rad)  # unit : deg
        joint_target_position_urdf_deg = np.rad2deg(self.default_position.copy())  # unit : deg
        joint_target_position_urdf_deg[controlled_joints] = joint_target_position_nohla_urdf_deg

        if self.act:
            self.client.move_joints(ControlGroup.ALL, joint_target_position_urdf_deg, 0.0)


def main(comm_freq: int = 400, step_freq: int = 100, act: bool = False, model_dir: str  = ""):
    walker = DemoNohlaRLWalk(comm_freq=comm_freq, step_freq=step_freq, act=act, model_dir=model_dir)

    # start the scheduler
    schedule(walker.step, interval=1 / step_freq)

    # run the scheduler
    run_loop()


if __name__ == "__main__":
    typer.run(main)
