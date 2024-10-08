import time
from fourier_grx.sdk.end_effectors import InspireDexHand

# Ensure that the server is running on the robot before executing this script.

# Instantiate the hand object
# For left hand use IP: 192.168.137.39
# For right hand use IP: 192.168.137.19
HAND_IP = '192.168.137.39'  # Change to the appropriate IP address
hand = InspireDexHand(HAND_IP)
time.sleep(1.0)  # Wait for the device to initialize

# Finger control sequence:
# [pinky, ring, middle, index, thumbending, thumbrotation]
# Maximum position: 1000
# Minimum position: 0
positions = [
    [700, 1000, 1000, 1000, 1000, 1000],
    [1000, 700, 1000, 1000, 1000, 1000],
    [1000, 1000, 700, 1000, 1000, 1000],
    [1000, 1000, 1000, 700, 1000, 1000],
    [1000, 1000, 1000, 1000, 700, 1000],
    [1000, 1000, 1000, 1000, 1000, 700]
]

# Execute the finger control sequence
for pos in positions:
    hand.set_positions(pos)
    time.sleep(2.0)  # Wait for 2 seconds before moving to the next position
