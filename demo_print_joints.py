import time

import numpy as np

from fourier_grx.sdk import RobotClient

if __name__ == "__main__":
    r = RobotClient()
    time.sleep(1.0)
    while True:
        print(np.round(r.joint_positions, 1))
        # print(r.states["joint"]["velocity"])
        time.sleep(0.1)
