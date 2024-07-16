import time

import numpy as np

from fourier_grx.sdk import RobotClient

if __name__ == "__main__":
    # Initialize robotclient
    r = RobotClient(60)
    
    # start setting home
    r.set_home()